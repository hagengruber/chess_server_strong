"""
    Sends the activation Code
"""
from smtplib import SMTPRecipientsRefused
from smtplib import SMTP_SSL as SMTP
from socket import gaierror
from email.mime.text import MIMEText
from json import load
from os import urandom


class Mail:
    """Sends activation code via mail"""

    def __init__(self):

        with open('./certs/smtp.json', encoding="UTF-8") as open_file:
            json_dumb = load(open_file)

        self.smtp_server = json_dumb['server']
        self.sender = json_dumb['sender']
        self.username = json_dumb['username']
        self.password = json_dumb['password']

    @staticmethod
    def create_code():
        """Creates 10 Byte Code for login"""
        return int.from_bytes(urandom(10), byteorder="big")

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
        except gaierror:
            return "Failed to send email. Make sure that you are " \
                   "connected to the Internet and your " \
                   "Firewall allows smtp connections"

        try:
            conn.sendmail(self.sender, destination, msg.as_string())
        except SMTPRecipientsRefused:
            return "Failed to send email. Make sure that you are " \
                   "connected to the Internet and your " \
                   "Firewall allows smtp connections"
        finally:
            conn.quit()
        return None
