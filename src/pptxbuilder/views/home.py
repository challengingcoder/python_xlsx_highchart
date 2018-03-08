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

class BugReport(MethodView):
    def get(self):
        return render_template('bugreport/index.jinja2', mailSent=False)
    def post(self):

        if os.environ.get('BUG_SEND_TO_EMAIL', None) is None:
            bug_send_to_email = 'pptxbuilder@gmail.com'
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
