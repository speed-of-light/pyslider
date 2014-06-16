import logging
import logging.handlers
from . import ToolHelper as TH
from path_maker import PathMaker


class Explog(PathMaker):
    """
    logger
    """
    def __init__(self):
        """
        usage:
            Explog(self.__class__.__name__)
        """
        self.enable_stream = False
        self.__add_logger()
        self.__add_handlers()
        self.__done()

    def __add_logger(self):
        lg = self.__get_logger()
        lg.setLevel(logging.INFO)
        lg.propagate = 0
        self.elog = lg

    def __add_handlers(self):
        """
        Should run after self.elog is inited
        """
        fmts = self.__format_str()
        fmt = logging.Formatter(**fmts)
        fn = self.common_path(resource='log', ext='log',
                              asure=True, root=False)
        self.__add_file_handler(fn, fmt)
        if self.enable_stream:
            self.__add_stream_handler(fn, fmt)

    def __add_stream_handler(self, fn, fmt):
        sh = self.__stream_handle(fn, fmt)
        if sh is not None:
            self.elog.addHandler(sh)

    def __add_file_handler(self, fn, fmt):
        fh = self.__file_handle(fn, fmt)
        if fh is not None:
            self.elog.addHandler(fh)

    def __done(self):
        cn = TH.underscore(self.__class__.__name__)
        raw = ">> ===== {} inited ===== <<".format(cn)
        self.elog.info(raw)

    def __format_str(self):
        items = ["%(asctime)s", "%(levelname)s", "%(name)s",
                 "%(funcName)s", "%(lineno)d", "%(message)s"]
        fmt = "{},{},{},{},{},{}".format(*items)
        dft = "%m/%d/%Y %H:%M:%S"
        return dict(fmt=fmt, datefmt=dft)

    def __get_logger(self):
        cn = TH.underscore(self.__class__.__name__)
        lgn = "{}.{}.{}".format(self.root, self.name, cn)
        logger = logging.getLogger(lgn)
        return logger

    def __file_handler_names(self):
        return [lh.name for lh in self.elog.handlers]

    def __create_file_handle(self, lfp, fmt, fh_name):
        fh = logging.handlers.\
            RotatingFileHandler(lfp,
                                maxBytes=10485760,
                                backupCount=5)
        fh.name = fh_name
        fh.setFormatter(fmt)
        return fh

    def __file_handle(self, lfp, fmt):
        fhn = lfp + "_fh"
        fhns = self.__file_handler_names()
        if fhn not in fhns:
            return self.__create_file_handle(lfp, fmt, fhn)
        return None

    def __create_stream_handle(self, lfp, fmt, sh_name):
        sh = logging.StreamHandler()
        sh.name = sh_name
        sh.setFormatter(fmt)
        return sh

    def __stream_handle(self, lfp, fmt):
        fhns = self.__file_handler_names()
        shn = lfp + "_sh"
        if shn not in fhns:
            return self.__create_stream_handle(lfp, fmt, shn)
        return None
