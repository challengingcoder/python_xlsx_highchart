from flask import Blueprint, render_template
from flask.views import MethodView

home_bp = Blueprint('home', __name__)


class HomeIndex(MethodView):
    def get(self):
        return render_template('home/index.jinja2')


home_bp.add_url_rule('/', view_func=HomeIndex.as_view('index'))
