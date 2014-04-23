import smtplib, email, logging
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# see also: https://pypi.python.org/pypi/mailer/ ##

class Emailer():
  def __init__(self, host='smtp.gmail.com', port=587,
      config=dict(uname='abc', upass='123')):
    # The below code never changes, though obviously those variables need values.
    """
    Usage:
      with Emailer('smtp.gmail.com', 587, dict(uname='xxx', upass='yyy')) as mailer:
        mailer.send("test", 'wowo', 'dearest@hot.mail')
    """
    self._init_logger()
    session = smtplib.SMTP(host, port)
    session.ehlo()
    session.starttls()
    session.login(config['uname'], config['upass'])
    self.config = config
    self.session = session

  def __enter__(self):
    self.log.info("Start session for {}".format(self.config['uname']))
    return self

  def __exit__(self, type, value, traceback):
    self.session.quit()
    self.log.info("close session for {}".format(self.config['uname']))

  def send(self, subject="[Emailer Default Subject]",
      text="No content", recipients=[]):
    self.log.info("{} composing email".format(self.config['uname']))
    cfg = self.config
    msg = MIMEMultipart()
    msg['From']    = cfg['uname']
    msg['To']      = email.Utils.COMMASPACE.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText("\nSent via Emailer\n{}".format(text), 'plain'))
    # body_of_email can be plaintext or html!
    self.session.sendmail( cfg['uname'], recipients, msg.as_string())
    self.log.info("{} email sent".format(self.config['uname']))

  def attach_files(msg):
    filename = raw_input('File name: ')
    try:
      f = open(filename,'rb')
    except IOError:
      print 'Attachment not found'
      return msg
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
      ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
      part = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
      part = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
      part = MIMEAudio(f.read(), _subtype=subtype)
    else:
      part = MIMEBase(maintype, subtype)
      msg.set_payload(f.read())
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
    msg.attach(part)
    f.close()
    return msg

  def _init_logger(self):
    cn = 'emailer'
    fmt = logging.Formatter(fmt= '%(asctime)s,%(levelname)s,'+
        '%(name)s,%(funcName)s,%(lineno)d, %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger("{}.{}".format(__name__, cn))
    logger.setLevel(logging.INFO)
    logger.propagate = 0
    # FileHandler
    fn = "log/emailer.log"
    fnh = "emailer_fh"
    if fnh not in [lh.name for lh in logger.handlers]:
      fh = logging.handlers.RotatingFileHandler(fn, maxBytes=10485760, backupCount=2)
      fh.name = fnh
      fh.setFormatter(fmt)
      logger.addHandler(fh)
    logger.info(">>============== Emailer logger inited ================= <<".format(cn))
    self.log = logger
