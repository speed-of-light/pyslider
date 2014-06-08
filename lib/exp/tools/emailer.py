import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# see also: https://pypi.python.org/pypi/mailer/ ##


class Emailer(object):
    def __init__(self, uname='', upass=''):
        """
        Usage:
          with Emailer(uname='xxx', upass='yyy') as mailer:
            mailer.send("test", 'wowo', 'dearest@hot.mail')
        """
        self.set_host()
        self.set_user(uname, upass)
        self.create_session()

    def create_session(self):
        session = smtplib.SMTP(self.host, self.port)
        session.ehlo()
        session.starttls()
        session.login(self.uname, self.upass)
        self.session = session

    def set_host(self, host="smtp.gmail.com", port=587):
        self.host = host
        self.port = port

    def set_user(self, uname, upass):
        self.uname = uname
        self.upass = upass

    def __enter__(self):
        self.log.info("Start session for {}".format(self.config['uname']))
        return self

    def __exit__(self, type, value, traceback):
        self.session.quit()
        self.log.info("close session for {}".format(self.config['uname']))

    def send(self, subj="Subject", text="--Content--", rcpts=[]):
        msg = MIMEMultipart()
        msg['From'] = self.uname
        msg['To'] = email.Utils.COMMASPACE.join(rcpts)
        msg['Subject'] = subj
        contents = "\nEmailer Notifications\n{}".format(text)
        mts = MIMEText(contents, 'plain')
        msg.attach(mts)
        # body_of_email can be plaintext or html!
        self.session.sendmail(self.uname, rcpts, msg.as_string())
