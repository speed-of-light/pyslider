class _Conf(object):
    def preset(self, kp, des):
        self._kp_des_core(kp, des)

    def _kp_des_core(self, kp, des):
        self.set_algorithm(engine="kp_core", method=kp)
        self.set_algorithm(engine="des_core", method=des)
