class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PrettyPrint(object):
    def __init__(this):
        pass

    def _should_be_printed(this, item):
        if not item: return False
        ratings = map(lambda x: x[1], item)
        ratings = list(set(ratings))

        if len(ratings) == 0: return False
        if len(ratings) == 1 and ratings[0] == 'Not Found': return False
        return True

    def pp(this, data):
        if not data:
            return

        for movieItem in data:
            movieName = movieItem[0]
            movieData = movieItem[1]
            if this._should_be_printed(movieData):
                print bcolors.OKGREEN + movieName + bcolors.ENDC
                for dataItem in movieData:
                    if dataItem[1] != 'Not Found':
                        print "\t", dataItem[0], '-', bcolors.OKBLUE + str(dataItem[1]) + bcolors.ENDC
        return

