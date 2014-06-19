import os
import shutil
import pandas as pd
from tools.path_maker import PathMaker
from tools.logger import Explog


class ExpCommon(Explog, PathMaker):
    def __init__(self, root, name):
        """
        Common methods for experiments
        `root`: file root
        `name`: project name
        """
        PathMaker.__init__(self, root, name)
        Explog.__init__(self)
        self.comp = 6
        self.silent = False

    def store(self):
        sp = self.stores_path()
        return pd.HDFStore(sp, format='t', data_columns=True,
                           complib='blosc', complevel=self.comp)

    def __stores_path(self):
        kv = self.__klass_var()
        sp = self.common_path("stores", kvar=kv, ext="h5", asure=False)
        return sp

    def __save_key(self, fpath, key):
        kf = self.load("keys", force=True)
        if key not in kf.key.values:
            kf = kf.append(pd.DataFrame([key], columns=['key']))
            kf = kf.reset_index(drop=True)
            kf.to_hdf(fpath, "keys", mode='a', data_columns=True,
                      format='t', complib='blosc', complevel=self.comp)

    def __make_key(self, fp, key):
        kf = pd.DataFrame([key], columns=['key'])
        kf.to_hdf(fp, key, mode='a', data_columns=True, format='t',
                  complib='blosc', complevel=self.comp)
        return kf

    def __klass_var(self):
        if hasattr(self, "klass_var"):
            return self.klass_var
        else:
            return ""

    def delete_store(self):
        sp = self.__stores_path()
        self.rm_file_path(sp)

    def load(self, key, force=False):
        """
        use `force` to create a new store if not exist.
        """
        sp = self.__stores_path()
        try:
            df = pd.read_hdf(sp, key, format='t')
        except KeyError, e:
            if not self.silent:
                print e, self.silent
            self.elog.error('load key [{}] from path: {}'.format(key, sp))
            if force and "No object named" in str(e):
                print "Forced to create {}-{}".format(sp, key)
                return self.__make_key(sp, key)
            return None
        return df

    def delete(self, tar=[('stores', 'h5', False)]):
        """
        TODO: Check path validity
        """
        for res, ext, root in tar:
            ph = self.common_path(resource=res, ext=ext, asure=False)
            print ph
            if ext is None or root:  # for whole directory
                shutil.rmtree(ph)
            else:  # for a single file
                if os.path.isfile(ph):
                    os.remove(ph)

    def save(self, key, data):
        """
        Save key to hstore, and create a key to `keys`
        """
        sp = self.__stores_path()
        data.to_hdf(sp, key, mode='a', data_columns=True, format='t',
                    complib='blosc', complevel=self.comp)
        # self.elog.info('Key [{}] saved to path: {}'.format(key, sp))
        self.__save_key(sp, key)

    def list_stores(self):
        """
        List available stores
        """
        sp = self.common_path("stores", ext="", asure=True)
        files = [f for f in os.listdir(sp) if os.path.isfile(f)]
        print "{} files included".format(len(files))
        for f in files:
            print "  -", f

    def save_rtlog(self, cols, data):
        """
        Save and load runtime log
        """
        df = self.load("rtlog")
        if df is None:
            df = pd.DataFrame([data], columns=cols)
        else:
            ldf = pd.DataFrame([data], columns=cols)
            df = df.append(ldf)
        self.save("rtlog", df)

    def _reload(self, key):
        self.__dict__[key] = self.load(key)

    def _preload(self, key):
        if hasattr(self, key):
            self.__reload(key)
