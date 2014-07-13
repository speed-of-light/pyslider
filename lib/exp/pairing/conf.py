class _Conf(object):
    _vars = ["nn_dist", "ransac", "homo",
             "octaf", "save_matches"]

    _vals = [0.9, None, False,
             0, False]

    def __init__(self):
        pass

    def set_featx(self, preload=True, kp="SIFT", des="SIFT"):
        self.elog.info("Loading featx")
        self.preload("featx")
        self.featx.preset(kp, des)
        self.featx.preload_packs(preload)

    def set_matcher(self, fn="FlannBased"):
        """
        BruteForce BruteForce-L1
        BruteForce-Hamming BruteForce-Hamming(2)
        FlannBased
        """
        self.elog.info("Loading matcher")
        self.mcore = fn
        self._reload_mod("matcher")

    def set_var(self, var="nn_dist", val=0.9, log=False):
        """
        nn_dist=.9, ransac=False, homo=False
        """
        self.__dict__[var] = val
        if log:
            self._log_cfg()

    def set_default_vars(self):
        # nn_dist: distance
        # ransac: px torlerance
        # homo: homo negative weight
        # vals: consider only normal frame, 0 forall
        self.set_vars(self._vals)
        self.elog.info("Setting default vars")
        self._log_cfg()

    def set_vars(self, vals):
        # len(vals) should be the same with self._vars
        map(self.set_var, self._vars, vals)

    def _log_cfg(self):
        st = "Current Configs:"
        for vi, va in enumerate(self._vars):
            if vi % 5 == 0:
                st += "\n"
            st += " {}: {},".format(va, self.__dict__[va])
        print st
        self.elog.info(st)
