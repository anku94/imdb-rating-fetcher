import os, imdb, re
import sys
import pdb
from multiprocessing import Pool
import pickle
import time
from progressbar import ProgressBar, SimpleProgress, Bar, Percentage

delimiters = "(){}[].-"
delimiters = list(delimiters)
regexPattern = '|'.join(map(re.escape, delimiters))

VALID_MOVIE_FORMATS = ['mp4', 'mkv', 'avi', 'wmv', 'mov', 'flv', '3gp', 'webm', 'mpg', 'mpeg']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_publish_year(name):
    res = re.findall(r'(20\d\d|19\d\d)', name)
    return res

def remove_redundant_chars(name):
    res = re.findall(r'(^.*20\d\d|^.*19\d\d)', name)
    return res[0] if len(res) else name

def sanitize_movie_name(name):
    name = re.sub(regexPattern, " ", name);
    return re.sub("\s+", " ", name)

def is_movie_filename(name):
    if 'sample' in name.lower():
        return False
    ptn = '|'.join(map(lambda x: x + '$', map(re.escape, VALID_MOVIE_FORMATS)))
    return True if re.search(ptn, name, flags = re.IGNORECASE) else False

def remove_format(name):
    ptn = '|'.join(map(lambda x: "(.*)" + x + '$', map(re.escape, map(lambda x: '.' + x, VALID_MOVIE_FORMATS))))
    valid_match = filter(lambda x: len(x) > 0, re.findall(ptn, name)[0])
    return valid_match[0] if len(valid_match) > 0 else None

def get_all_unique_movie_strings(path):
    all_movienames = []

    for root, subFolders, files in os.walk(path):
        movie_names = filter(is_movie_filename, files)
        all_movienames += movie_names

    all_movienames = map(remove_format, all_movienames)
    all_movienames = map(sanitize_movie_name, all_movienames)
    all_movienames = map(remove_redundant_chars, all_movienames)

    return all_movienames

def retrieve_candidate_ratings(movieName):
    ia = imdb.IMDb()
    result = ia.search_movie(movieName)
    result = result[:min(len(result), 3)]
    info = []
    for res in result:
        ia.update(res)
        name = res['long imdb canonical title']
        rating = res.get('rating', 'Not Found')
        info.append((name, rating))
    return (movieName, info)

def mock_map():
    f = open('data', 'rb').read()
    obj = pickle.loads(f)
    return obj 

def pretty_print(res):
    for movieItem in res:
        movieName = movieItem[0]
        movieData = movieItem[1]
        if len(movieData) > 0:
            print bcolors.OKGREEN + movieName + bcolors.ENDC
            for dataItem in movieData:
                if dataItem[1] != 'Not Found':
                    print "\t", dataItem[0], '-', bcolors.OKBLUE + str(dataItem[1]) + bcolors.ENDC
    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "\n\t", "Usage: python", sys.argv[0], "/path/to/movie/folder", "\n"
        sys.exit(-1)

    filenames = get_all_unique_movie_strings(sys.argv[1])
    p = Pool(20)
    results = []
    res = p.map_async(retrieve_candidate_ratings, filenames, callback=results.append)

    TOTALJOBS = res._number_left
    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage()], maxval=TOTALJOBS).start()
    while True:
        if(res.ready()):
            break
        DONE = TOTALJOBS - res._number_left
        pbar.update(DONE);
        time.sleep(1)
    pbar.finish()
    pretty_print(results[0])
    p.close()
