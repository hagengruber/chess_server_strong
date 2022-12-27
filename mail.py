"""
    Sends the activation Code
"""

from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
import random
import json


class Mail:
    """Sends activation code via mail"""

    def __init__(self):

        with open('./certs/smtp.json') as f:
            json_dumb = json.load(f)

        self.smtp_server = json_dumb['server']
        self.sender = json_dumb['sender']
        self.username = json_dumb['username']
        self.password = json_dumb['password']

    @staticmethod
    def create_code():
        """Creates Code for login"""
        return random.randint(1000000000, 9999999999)

    def send_mail(self, destination, code):
        """Sends mail"""

        destination = [destination]
        text_subtype = 'plain'
        subject = "Activation Code"

        content = ' Thanks for your registration! Your activation Code is: ' + \
                  str(code)

        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = self.sender

        try:
            conn = SMTP(self.smtp_server)
            conn.set_debuglevel(False)
            conn.login(self.username, self.password)
        except TimeoutError:
            return "Failed to send email. Make sure that you are " \
                   "connected to the Internet and your " \
                   "Firewall allows smtp connections"

        try:
            conn.sendmail(self.sender, destination, msg.as_string())
        finally:
            conn.quit()
        # ToDo: Testen ob return statement in finally muss
        return None
