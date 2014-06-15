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
        wi = self.df[self.df.fid < fid].iloc[-1].name + 1
        pa = self.df[:wi]
        pa = pa.append([(fid, sid, ftype, -99)], columns=pa.columns)
        pa = pa.append(self.df[wi:])
        return pa

    def insert(self, fid, sid, ftype):
        """
        Insert a row to dataframe
        Input should never be `none`
        """
        valid = self.__check_input(fid, sid, ftype)
        if valid:
            return self.__insert_data(fid, sid, ftype)
