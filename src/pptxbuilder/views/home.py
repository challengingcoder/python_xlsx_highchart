from flask import Blueprint, render_template
from flask.views import MethodView

home_bp = Blueprint('home', __name__)

class HomeIndex(MethodView):
    def get(self):
        return render_template('home/index.jinja2')
class About(MethodView):
    def get(self):
        return render_template('about/index.jinja2')

class BugReport(MethodView):
    def get(self):
        return render_template('bugreport/index.jinja2')

home_bp.add_url_rule('/', view_func=HomeIndex.as_view('index'))
home_bp.add_url_rule('/about', view_func=About.as_view('about'))
home_bp.add_url_rule('/bug-report', view_func=BugReport.as_view('bugReport'))
