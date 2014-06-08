from tools import ToolHelper as TH


class Explog(object):
    def _init_logger(self):
        cn = TH.underscore(self.__class__.__name__)
        fmt = logging. \
            Formatter(fmt="%(asctime)s,%(levelname)s,\
                      %(name)s,%(funcName)s,%(lineno)d, %(message)s",
                      datefmt='%m/%d/%Y %H:%M:%S')
        logger = logging.getLogger("{}.{}.{}.{}".
                                   format(__name__, cn, self.root, self.name))
        logger.setLevel(logging.INFO)
        logger.propagate = 0
        # FileHandler
        fn = self.make_path('log', 'log', True, False)
        fnh = fn + "_fh"
        cnh = fn + "_ch"
        if fnh not in [lh.name for lh in logger.handlers]:
            fh = logging.handlers. \
                RotatingFileHandler(fn, maxBytes=10485760, backupCount=5)
            fh.name = fnh
            fh.setFormatter(fmt)
            logger.addHandler(fh)
        # StreamHandler
        if 0 and cnh not in [lh.name for lh in logger.handlers]:
            ch = logging.StreamHandler()
            ch.name = cnh
            ch.setFormatter(fmt)
            logger.addHandler(ch)
        logger.info(">>============== {} inited ================= <<".
                    format(cn))
        self.log = logger

