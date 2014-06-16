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

    def __save_key(self, fpath, key):
        kf = self.load('keys')
        if key not in kf.key.values:
            kf = kf.append(pd.DataFrame([key], columns=['key']))
            kf = kf.reset_index(drop=True)
            kf.to_hdf(fpath, 'keys', mode='a', data_columns=True,
                      format='t', complib='blosc', complevel=self.comp)

    def store(self):
        sp = self.common_path()
        return pd.HDFStore(sp, format='t', data_columns=True,
                           complib='blosc', complevel=self.comp)

    def delete_file(self, tar=[('stores', 'h5', False)]):
        for res, ext, root in tar:
            ph = self.common_path(resource=res, ext=ext, asure=False,
                                  root=root)
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
        sp = self.common_path(resource='stores', ext='h5', asure=True,
                              root=False)
        data.to_hdf(sp, key, mode='a', data_columns=True, format='t',
                    complib='blosc', complevel=self.comp)
        self.elog.info('Key [{}] saved to path: {}'.format(key, sp))
        self.__save_key(sp, key)

    def __make_keyfile(self, key):
        kf = pd.DataFrame([key], columns=['key'])
        sp = self.common_path(resource='stores', ext='h5',
                              asure=True, root=False)
        kf.to_hdf(sp, key, mode='a', data_columns=True, format='t',
                  complib='blosc', complevel=self.comp)
        return kf

    def load(self, key):
        sp = self.common_path(asure=False)
        try:
            df = pd.read_hdf(sp, key, format='t')
        except KeyError, e:
            print e
            self.elog.error('load key [{}] from path: {}'.format(key, sp))
            if "No object named" in str(e) and key is "keys":
                print "auto create one"
                return self.__make_keyfile(key)
            return None
        return df
