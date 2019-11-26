"""Solution CLI
Usage:
    hello.py --url=<address_to_url_files> --regex=<address_to_regex_file>
    hello.py -h|--help
    hello.py -v|--version
Options:
    --url=<address_to_url_file>  address to the file containing urls.
    --regex=<address_to_regex_file>  address to the file containing urls.
    -h --help  Show this screen.
    -v --version  Show version.
"""

from docopt import docopt
import urllib
import re
from difflib import SequenceMatcher
from datetime import datetime
from multiprocessing import Process, Queue
from threading import Lock
import sys, os

class UrlDataFrameHandler:
    def __init__(self, file_name):
        import pandas as pd
        self.file_name = file_name
        self.url_df_handle = pd.read_csv(url_file, header=None, encoding='utf-8', delimiter='\n')
        self.index_on_df = 0

    def fetch_first(self):
        out = ""
        if self.url_df_handle.count()[0] > self.index_on_df:
            out = self.url_df_handle.iloc[self.index_on_df][0]
            self.index_on_df += 1
        return out

    def has_data(self):
        return self.url_df_handle.count()[0] > self.index_on_df


class FileHandler:
    @staticmethod
    def fetch_lines(filename):
        with open(filename) as f:
            out = f.read().splitlines()
        return out


def ret_error(str1, str2):
    s = SequenceMatcher(None, str1, str2)
    return 1 - s.ratio()


def is_match(worker_id, Text, RE):
    out = {}

    out['worker_id'] = worker_id
    time_start = datetime.now()
    out['time'] = time_start.ctime()
    out['RE'] = RE
    p = re.compile(RE)

    x = p.search(Text)
    if x:
        out['error'] = 0
        out['matched-string'] = x.group(0)
    else:
        out['error'] = ret_error(Text, RE)
        out['matched-string'] = ''

    out['deltatime'] = (datetime.now() - time_start).total_seconds()
    return out


def fetch_text_from_url(_url):
    f = None
    _text = ""
    _url_exist = False
    try:
        f = urllib.request.urlopen(_url)
    except:
        _text = ""
        _url_exist = False
    finally:
        if f:
            _text = f.read().decode('utf-8')
            _url_exist = True
    return _text, _url_exist

# this function gets the text and process regex_value value on it
def process_text(_worker_id, _output_queue, _url, _url_exist, _text, _regex_value):
    lock = Lock()
    lock.acquire()
    log = {}
    try:
        if not _url_exist:
            log['worker_id'] = _worker_id
            log['time'] = datetime.now().ctime()
            log['RE'] = ''
            log['error'] = 1
            log['matched-string'] = ''
            log['deltatime'] = 0
            log['Interrupted'] = 0
            log['url'] = _url
            log['url-code'] = 404 # url not found
        else:
            log = is_match(_worker_id, _text, _regex_value)
            log['url'] = _url
            log['url-code'] = 0 # url ok
    except:
        log['worker_id'] = _worker_id
        log['time'] = datetime.now().ctime()
        log['RE'] = ''
        log['error'] = 1
        log['matched-string'] = ''
        log['deltatime'] = 0
        log['Interrupted'] = 0
        log['url'] = _url
        log['url-code'] = -1
        log['Interrupted'] = 1
        _output_queue.put(log)
        lock.release()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        log['Interrupted'] = 0
        _output_queue.put(log)
        lock.release()
    return


if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')
    # I assume the arguments are the files containing urls and regex
    lock = Lock()
    lock.acquire()
    jobs = []
    log_queue = Queue()
    try:
        regex_list = []
        url_handler = None
        flag_main_loop = False
        if arguments['--url'] and arguments['--regex']:
            url_file = arguments['--url']
            regex_file = arguments['--regex']

            # I use pandas for reading urls to handle huge amount of urls in the big data file
            url_handler = UrlDataFrameHandler(url_file)
            # I read the whole regex file as it is not expected to have huge amount of data entries
            regex_list = FileHandler.fetch_lines(regex_file)
            flag_main_loop = True

        results = []

        max_num_workers = 5

        index_on_regex_list = 0
        url_link = ""
        text = ""
        url_exist = False

        while flag_main_loop:

            # assign workers to the jobs
            for worker_id in range(max_num_workers):
                if index_on_regex_list == 0:
                    if not url_handler.has_data():
                        break
                    url_link = url_handler.fetch_first()
                    text, url_exist = fetch_text_from_url(url_link)

                p = Process(target=process_text,
                            args=(worker_id, log_queue, url_link, url_exist, text, regex_list[index_on_regex_list]))
                p.daemon = True
                jobs.append(p)
                p.start()

                if url_exist:
                    index_on_regex_list += 1
                else:
                    index_on_regex_list = 0
                if index_on_regex_list >= len(regex_list):
                    index_on_regex_list = 0

            for p in jobs:
                p.join()
                print(log_queue.get(p))
            jobs.clear()
            if not url_handler.has_data():
                flag_main_loop = False
    except KeyboardInterrupt:
        #for p in jobs:
        #    p.join()
        #    #print(log_queue.get(p))

        print('Interrupted')
        lock.release()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        lock.release()
