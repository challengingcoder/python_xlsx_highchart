import os
import tempfile
from base64 import b64decode
from gettext import gettext as _

from flask import Blueprint, request, abort, session, redirect, url_for, render_template
from flask import jsonify
from flask.views import MethodView

from pptxbuilder.constants import *
from pptxbuilder.excel_parser import parse, UnsupportedFileException
from pptxbuilder.helper import str_chart_type
from pptxbuilder.util import random_alphanum

builder_bp = Blueprint('builder', __name__)

builder_bp.add_app_template_global(CHART_TYPE_BAR, name='CHART_TYPE_BAR')
builder_bp.add_app_template_global(CHART_TYPE_COLUMN, name='CHART_TYPE_COLUMN')
builder_bp.add_app_template_global(CHART_TYPE_LINE, name='CHART_TYPE_LINE')
builder_bp.add_app_template_global(CHART_TYPE_PIE, name='CHART_TYPE_PIE')
builder_bp.add_app_template_global(str_chart_type)


class Create(MethodView):
    def post(self):
        xls_str = request.form.get('file')

        try:
            xls_str = xls_str.split('base64,')[1]
            xls_data = b64decode(xls_str)
        except IndexError:
            abort(406, 'Invalid form data')

        save_path = os.path.join(tempfile.gettempdir(), random_alphanum(10))
        with open(save_path, 'wb') as f:
            f.write(xls_data)
            f.close()

        try:
            bundle = parse(save_path)
        except UnsupportedFileException:
            abort(406, 'Unsupported file format')
        finally:
            os.remove(save_path)

        tables = bundle.to_dict()['tables'][:]
        for table in tables:
            table['view_settings'] = {
                'cross_break': 0,
                'chart_type': CHART_TYPE_BAR
            }

        session['tables'] = tables
        session['builder_flag'] = 1

        return redirect(url_for('builder.index'))


class Index(MethodView):
    def get(self):
        if 'builder_flag' not in session:
            return redirect(url_for('home.index'))

        return redirect(url_for('builder.table', table_index=0))


class TableAtIndex(MethodView):
    def get(self, table_index):
        if 'builder_flag' not in session:
            return redirect(url_for('home.index'))

        tables = session['tables']

        try:
            table = session['tables'][table_index]
        except IndexError:
            abort(404)

        if request.args.get('json'):
            return jsonify(table)

        return render_template('builder/table.jinja2',
                               tables=tables,
                               table=table,
                               index=table_index)

    def post(self, table_index):
        cross_break = request.form.get('cross-break', type=int)
        chart_type = request.form.get('chart-type', type=int)

        if chart_type not in [CHART_TYPE_BAR, CHART_TYPE_COLUMN, CHART_TYPE_LINE, CHART_TYPE_PIE]:
            abort(400, _('Invalid chart type'))

        try:
            session['tables'][table_index]['sections'][cross_break]
        except IndexError:
            abort(400, _('Invalid crossbreak'))

        try:
            table = session['tables'][table_index]
        except IndexError:
            abort(404)

        table['view_settings']['cross_break'] = cross_break
        table['view_settings']['chart_type'] = chart_type

        return redirect(url_for('builder.table', table_index=table_index))


builder_bp.add_url_rule('/builder/create', view_func=Create.as_view('create'))
builder_bp.add_url_rule('/builder', view_func=Index.as_view('index'))
builder_bp.add_url_rule('/builder/<int:table_index>', view_func=TableAtIndex.as_view('table'))
