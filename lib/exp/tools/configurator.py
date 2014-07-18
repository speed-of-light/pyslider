class Configurator(object):
    def __init__(self):
        self.set_default_vars()

    def set_var(self, var="bbft", val=0.9, log=False):
        self.__dict__[var] = val
        if log:
            self._log_cfg()

    def set_dict_vars(self, vd, log=True):
        for dk, dv in vd.iteritems():
            self.set_var(dk, dv)
        self._log_cfg()

    def _log_cfg(self):
        st = "Current Configs:\n  "
        lc = list(self._configs().iteritems())
        lc.sort()
        for k, v in lc:
            st += "{}:{}, ".format(k, v)
        print st
        self.elog.info(st)

    def set_default_vars(self):
        self.elog.info("Setting default vars")
        self.set_dict_vars(self._conf, log=0)
