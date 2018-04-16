from flask import Flask, Blueprint, render_template, request
from flask.views import MethodView
import sendgrid
import os
from sendgrid.helpers.mail import *


import flask

home_bp = Blueprint('home', __name__)

class HomeIndex(MethodView):
    def get(self):
        return render_template('home/index.jinja2')
class About(MethodView):
    def get(self):
        return render_template('about/index.jinja2')
class Blog(MethodView):
    def get(self):
        return render_template('blog/index.jinja2')

class BugReport(MethodView):
    def get(self):
        return render_template('bugreport/index.jinja2', mailSent=False)
    def post(self):

        if os.environ.get('BUG_SEND_TO_EMAIL', None) is None:
            bug_send_to_email = 'info@pptxbuilder.com'
        else:
            bug_send_to_email = os.environ.get('BUG_SEND_TO_EMAIL')
        contact_name = request.form.get('contactName')
        contact_email = request.form.get('contactEmail')
        contact_message = request.form.get('contactMsg')

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(contact_email)
        subject = "Bug report"
        to_email = Email(bug_send_to_email)
        content = Content("text/html", "Name: " + contact_name + "<br>" + contact_message)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

        #send email
        return render_template('bugreport/index.jinja2', mailSent=True)


home_bp.add_url_rule('/', view_func=HomeIndex.as_view('index'))
home_bp.add_url_rule('/about', view_func=About.as_view('about'))
home_bp.add_url_rule('/blog', view_func=Blog.as_view('blog'))
home_bp.add_url_rule('/get-in-touch', view_func=BugReport.as_view('bugReport'))
