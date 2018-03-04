from flask import Flask, Blueprint, render_template, request
from flask.views import MethodView
from flask_mail import Mail, Message
import os


import flask

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
    def post(self):
        print('nejra1235')
        if os.environ.get('BUG_SEND_TO_EMAIL', None) is None:
            bug_send_to_email = 'pptxbuilder@gmail.com'
        else:
            bug_send_to_email = os.environ.get('BUG_SEND_TO_EMAIL')
        bug_email = os.environ.get('BUG_EMAIL')
        contact_name = request.form.get('contactName')
        contact_email = request.form.get('contactEmail')
        contact_message = request.form.get('contactMsg')
        mail = Mail(flask.current_app)
        msg = Message('Hello', sender = bug_email, recipients = [bug_send_to_email])
        msg.body = "From:"+contact_email+"\nName:"+contact_name+"\n"+contact_message
        mail.send(msg)
        #send email
        return render_template('bugreport/index.jinja2')

        # mail = Mail(flask.current_app)
        # msg = Message("Hello",
        #           sender="from@example.com",
        #           recipients=["sibrahimpa1@gmail.com"])
        # msg.body = "nejra"
        # mail.send(msg)
        # sender = 'from@fromdomain.com'
        # receivers = ['sibrahimpa1@gmail.com']
        #
        # message = """From: From Person <from@fromdomain.com>
        # To: To Person <to@todomain.com>
        # Subject: SMTP e-mail test
        #
        # This is a test e-mail message.
        # """
        #
        # # try:
        # server = smtplib.SMTP('smtp.gmail.com', 25)
        # server.connect("smtp.gmail.com",465)
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        #
        # text = msg.as_string()
        # server.sendmail("npasic00@gmail.com", receivers[0], "text")
        # server.quit()
        # print("Successfully sent email")
        # except SMTPException:
        #    print("Error: unable to send email")


home_bp.add_url_rule('/', view_func=HomeIndex.as_view('index'))
home_bp.add_url_rule('/about', view_func=About.as_view('about'))
home_bp.add_url_rule('/bug-report', view_func=BugReport.as_view('bugReport'))
