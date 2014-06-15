import pandas as pd


class DfExt(object):
    def __init__(self, df):
        """
        Helper class to extend pandas dataframe usage
        """
        self.df = df

    def __check_input(self, fid, sid, ftype):
        if fid is None or sid is None or ftype is None:
            print "Failed to add new record"
            return False
        else:
            return True

    def __insert_data(self, fid, sid, ftype):
        # find last frame id
        pa = self.df[self.df.fid < fid]
        pb = self.df[self.df.fid >= fid]
        apdf = pd.DataFrame([[fid, sid, ftype, -99]], columns=pa.columns)
        pa = pa.append(apdf)
        pa = pa.append(pb)
        pa = pa.reset_index(drop=True)
        return pa

    def __overwrite_data(self, fid, sid, ftype):
        wi = self.df[self.df.fid == fid].index[0]
        self.df.ix[wi, "sid"] = sid
        self.df.ix[wi, "ftype"] = ftype
        return self.df

    def insert(self, fid, sid, ftype, ow=False):
        """
        Insert a row to dataframe, if the index was existed, then overwrite it.
        Input should never be `none`
        """
        valid = self.__check_input(fid, sid, ftype)
        if valid:
            if len(self.df[self.df.fid == fid]) == 0:
                return self.__insert_data(fid, sid, ftype)
            else:  # overwrite original data
                if ow is False:
                    print "use ow=True to overwrite existed fid"
                else:
                    return self.__overwrite_data(fid, sid, ftype)
