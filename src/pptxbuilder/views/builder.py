from flask import Blueprint, render_template, request, abort, session

from flask.views import MethodView
from io import BytesIO, StringIO
from xlrd import open_workbook
from base64 import b64decode, decodebytes

from pptxbuilder.excel_parser import parse
import tempfile
import os
from pptxbuilder.util import random_alphanum
from flask import jsonify

project_bp = Blueprint('project', __name__)

CHART_TYPE_BAR = 1


class Create(MethodView):
    def post(self):
        xls_str = request.form.get('file')

        try:
            xls_str = xls_str.split('base64,')[1]
            xls_data = b64decode(xls_str)
        except Exception:
            # Dosya oluşturulamadı
            abort(406)

        save_path = os.path.join(tempfile.gettempdir(), random_alphanum())
        with open(save_path, 'wb') as f:
            f.write(xls_data)
            f.close()

        bundle = parse(save_path)
        session['tables'] = bundle.to_dict()
        session['table_settings'] = [{'break': table.sections[0].name, 'type': CHART_TYPE_BAR} for table in
                                     bundle.tables]

        os.remove(save_path)
        return jsonify({'status': 1})


class Index(MethodView):
    def get(self, project_id):
        pass


project_bp.add_url_rule('/project/create', view_func=Create.as_view('create'))
