class Ranker(object):
    def __init__(this):
        pass

    def movieItemKey(this, item):
        candidates = item[1]
        ratings = map(lambda x: x[1], candidates)
        ratings = [i for i in ratings if i != 'Not Found']

        if len(ratings):
            return float(ratings[0])
        else:
            return 0
        print ratings
        return 1

    def rank(this, data):
        if not data:
            return
        data.sort(key = this.movieItemKey, reverse = True)
        return data
