import os
import shutil
import pandas as pd
from tools.path_maker import PathMaker
from tools.logger import Explog
from tools.emailer import Emailer


class ExpCommon(PathMaker, Explog):
    def __init__(self, root, name):
        """
        `root`: file root
        `name`: project name
        """
        PathMaker.__init__(self, root, name)
        Explog.__init__(self, root, name)
        self.root = root
        self.name = name
        self.comp = 6

    def __save_key(self, fpath, key):
        kf = self.load('keys')
        if kf is None:
            kf = pd.DataFrame([key], columns=['key'])
        else:
            kf = kf.append(pd.DataFrame([key], columns=['key']))
            kf = kf.reset_index()
            for rc in ['index', 'level']:
                if rc in kf.columns:
                    del kf[rc]
        kf.to_hdf(fpath, 'keys', mode='a', data_columns=True,
                  format='t', complib='blosc', complevel=self.comp)

    def _ustr_dict(self, di):
        """
        Make dict keys underscore for saving to hdfs
        """
        s = ""
        ks = di.keys()
        ks.sort()
        for k in ks:
            s += "/{}_{}".format(k, di[k])
        return s

    def store(self):
        sp = self.make()
        return pd.HDFStore(sp, format='t', data_columns=True,
                           complib='blosc', complevel=self.comp)

    def delete_file(self, tar=[('store', 'h5', False)]):
        for res, ext, root in tar:
            ph = self.make(res, ext, False, root)
            print ph
            if ext is None or root:  # for whole directory
                shutil.rmtree(ph)
            else:  # for a single file
                if os.path.isfile(ph):
                    os.remove(ph)

    def save(self, key, data):
        """
        Save key to hstore
        """
        sp = self.make('stores', 'h5', asure=True, root=False)
        data.to_hdf(sp, key, mode='a', data_columns=True, format='t',
                    complib='blosc', complevel=self.comp)
        self.elog.info('Key [{}] saved to path: {}'.format(key, sp))
        self.__save_key(sp, key)

    def load(self, key):
        sp = self.make(asure=False)
        try:
            df = pd.read_hdf(sp, key, format='t')
        except KeyError, e:
            print e
            self.elog.error('load key [{}] from path: {}'.format(key, sp))
            self.elog.error('  >> Error: {}'.format(e))
            return None
        return df

    def notify(self, summary):
        if self.upass is None:
            return
        ps = self.upass
        cn = self._underscore(self.__class__.__name__)
        title = "Pyslider Job: {} <{}-{}> Finished". \
            format(cn, self.root, self.name)
        me = "speed.of.lightt@gmail.com"
        with Emailer(config=dict(uname=me, upass=ps)) as mailer:
            mailer.send(title, summary, ['speed.of.lightt@gmail.com'])
