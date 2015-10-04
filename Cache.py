import pickle
import os, sys

class Cache(object):

    data = None
    DATAFILE = ".movie-manager-data"

    _loglevel = 0;

    def __init__(this):
        if this._file_exists(this.DATAFILE):
            this.data = pickle.loads(open(this.DATAFILE, 'rb').read())
        else:
            this.data = {}

    def has_key(this, key):
        return key in this.data

    def update_key(this, key, val):
        this.data[key] = val

    def get_key(this, key):
        if not key in this.data:
            return None
        return this.data[key]

    def del_key(this, key):
        del this.data[key]

    def close(this, ):
        f = open(this.DATAFILE, 'wb+')
        f.write(pickle.dumps(this.data))
        f.close()

    def _file_exists(this, filename):
        if this.log_warning():
            this.print_log("Checking if", filename, "exists = ", os.path.isfile(filename));
        return os.path.isfile(filename)
        pass

    def log_warning(this):
        return this._loglevel >= 1

    def print_log(this, *args):
        msg = ' '.join(map(lambda x: str(x), args))
        print >> sys.stderr, " [[CACHE]] " + msg

