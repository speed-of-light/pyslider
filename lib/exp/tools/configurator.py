class Configurator(object):
    def __init__(self):
        self.set_default_vars()

    def set_var(self, var="bbft", val=0.9, log=False):
        self.__dict__[var] = val
        if log:
            self._log_cfg()

    def set_vars(self, vals):
        # len(vals) should be the same with self._vars
        map(self.set_var, self._vars, vals)

    def set_dict_vars(self, vd):
        for dk, dv in vd.iteritems():
            self.set_var(dk, dv)
        self._log_cfg()

    def _log_cfg(self):
        st = "Current Configs:"
        for vi, va in enumerate(self._vars):
            if vi % 5 == 0:
                st += "\n"
            st += " {}: {},".format(va, self.__dict__[va])
        print st
        self.elog.info(st)

    def set_default_vars(self):
        self.set_vars(self._vals)
        self.elog.info("Setting default vars")
        self._log_cfg()
