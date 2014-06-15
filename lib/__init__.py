__doc__ = """
    Pyslider library
    `exp`: core part
    `auto`: some auto scripts
    `plotter`: plotting library
    `ext`: some helpers provided by others
"""
__all__ = ["exp"]

from tools.emailer import Emailer


class Dataset(object):
    def __init__(self, root, name):
        self.root = root
        self.name = name

    def notify(self, summary):
        if self.upass is None:
            return
        ps = self.upass
        cn = self.underscore(self.__class__.__name__)
        title = "Pyslider Job: {} <{}-{}> Finished". \
            format(cn, self.root, self.name)
        me = "speed.of.lightt@gmail.com"
        with Emailer(config=dict(uname=me, upass=ps)) as mailer:
            mailer.send(title, summary, ['speed.of.lightt@gmail.com'])
