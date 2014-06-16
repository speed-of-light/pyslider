__all__ = ["slider", "video", "ToolHelper", "logger", "path_maker"]

import re
import time


class ToolHelper(object):
    """
    Helper methods for expriments
    """
    def __init__(self):
        # precompile regex to speed up underscore matching
        self.fc = re.compile("(.)([A-Z][a-z]+)")
        self.ac = re.compile("([a-z0-9])([A-Z])")

    def timing(f):
        """
        A simple method wrapper to get runtime
        example:
            @timing
        """
        def wrap(*args):
            time1 = time.time()
            ret = f(*args)
            time2 = time.time()
            print "{} function took {:0.3f} ms".\
                format(f.func_name, (time2-time1)*1000.0)
            return ret
        return wrap

    @staticmethod
    def underscore(string=""):
        """
        Use instance method to speed up if needed.
        """
        first_cap_re = re.compile("(.)([A-Z][a-z]+)")
        all_cap_re = re.compile("([a-z0-9])([A-Z])")
        s1 = first_cap_re.sub(r"\1_\2", string)
        return all_cap_re.sub(r"\1_\2", s1).lower()

    def fast_underscore(self, string=""):
        s1 = self.fc.sub(r"\1_\2", string)
        return self.ac.sub(r"\1_\2", s1).lower()
