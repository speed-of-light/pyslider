class _Conf(object):
    def preset(self, kp, des):
        self._kp_des_core(kp, des)

    def _kp_des_core(self, kp, des):
        self.set_algorithm(engine="kp_core", method=kp)
        self.set_algorithm(engine="des_core", method=des)

    def set_algorithm(self, engine="kp_core", method="SIFT"):
        """
        Adaptive method for keypoints detection:
            `kp_adap`: '', 'Grid', 'Pyramid'
        Keypoints detection core:
            `kp_core`: "FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"
        Adaptive method for descriptor detection:
            `des_adap`: '', 'Opponent'
        Descriptor detection core:
            `des_core`: "SIFT", "SURF", "BRIEF", "BRISK", "ORB", "FREAK"
        """
        self.algo[engine] = method
        self._klass_var()
