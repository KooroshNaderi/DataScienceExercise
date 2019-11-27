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
from multiprocessing import Process, Queue
from docopt import docopt

from file_utils import UrlDataFrameHandler, FileHandler
from function_utils import exit_no_error, is_match, fetch_text_from_url, get_time_date_format, os_kill_process

verbose = 1


def handle_error(_log_queue):
    if not (_log_queue is None):
        _log_queue.cancel_join_thread()
        _log_queue.close()

    exit_no_error()


# this function gets the text and process regex_value value on it
def process_text(_worker_id, _output_queue, _url, _url_exist, _text, _regex_value):
    try:
        log = {}
        if not _url_exist:
            log['worker_id'] = _worker_id          # the id of worker
            log['time'] = get_time_date_format()   # starting time of the process
            log['RE'] = ''                         # the regular expression under process
            log['error'] = 1                       # error between re and url text
            log['matched-string'] = ''             # the first matched string in the text
            log['deltatime'] = 0                   # the time in seconds taken for the process
            log['url'] = _url                      # the under process url
            log['url-code'] = 404                  # url code determining whether it exists (0) or not (404)
        else:
            log = is_match(_text, _regex_value, _worker_id)
            log['url'] = _url
            log['url-code'] = 0
        _output_queue.put(log)
    except:
        os_kill_process()
        exit_no_error()

    return


def multi_process_urls(_url_file, _regex_file, _max_num_workers):
    regex_list = []           # a list contains of regex strings
    url_handler = None        # a handler to data-frame containing urls
    flag_main_loop = False
    if not (_url_file is None) and not (_regex_file is None):
        # I use pandas for reading urls to handle huge amount of urls in the big data file
        url_handler = UrlDataFrameHandler(_url_file)
        # I read the whole regex file as it is not expected to have huge amount of data entries
        regex_list = FileHandler.fetch_lines(_regex_file)
        flag_main_loop = True

    jobs = []
    log_queue = Queue()      # a queue for logging the worker's outputs

    index_on_regex_list = 0  # index moving on regex list for different urls
    url_link = ""            # the current url under processing
    text = ""                # the text loaded from url
    url_exist = False        # a boolean for determining the url is valid or not
    if verbose:
        print(".... started processing the urls .....")

    while flag_main_loop:
        # assign workers to the jobs
        for worker_id in range(_max_num_workers):
            if index_on_regex_list == 0:
                if not url_handler.has_data():
                    break                 # do not assign any more worker as we are done with the url database
                url_link = url_handler.fetch_first()
                print("processing url: ", url_link)
                text, url_exist = fetch_text_from_url(url_link)

            p = Process(
                target=process_text,
                args=(worker_id, log_queue, url_link, url_exist, text, regex_list[index_on_regex_list]),
            )

            jobs.append(p)
            p.start()

            if url_exist:
                index_on_regex_list += 1  # walk on regex list to assign worker for matching it with text from url
            else:
                index_on_regex_list = 0   # load another url as this one does not exist and a worker is assigned to log
            if index_on_regex_list >= len(regex_list):
                index_on_regex_list = 0

        for i in range(0, len(jobs)):
            jobs[i].join(timeout=1.0)
        try:
            for p in jobs:
                if not p.is_alive() and not log_queue.empty():
                    print(log_queue.get_nowait())
                    pass
        except Exception as e:
            # print(e)
            pass

        jobs.clear()
        if not url_handler.has_data():
            flag_main_loop = False


if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')

    # I assume the arguments are the files containing urls and regex
    url_file = None
    regex_file = None
    if arguments['--url'] and arguments['--regex']:
        url_file = arguments['--url']
        regex_file = arguments['--regex']
    max_num_workers = 5  # maximum number of workers for assigning jobs

    try:
        multi_process_urls(url_file, regex_file, max_num_workers)
    except KeyboardInterrupt and SystemExit:
        if verbose:
            print('Keyboard Interrupt')
        handle_error(None)
    except Exception as e:
        if verbose:
            print('Error happened')
        handle_error(None)
    finally:
        if verbose:
            print('Done')
        handle_error(None)
