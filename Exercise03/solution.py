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
import pandas as pd
import urllib


class UrlHandler:
    def __init__(self, file_name):
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


def process_website(url, regex_list):
    f = None
    try:
        f = urllib.request.urlopen(url)
    except:
        print("url cannot be opened")
    finally:
        if f:
            myfile = f.read()
            print(myfile)
    return


if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')
    # I assume the arguments are the files containing urls and regex
    regex_list = []
    url_handler = None
    flag_main_loop = False
    if arguments['--url'] and arguments['--regex']:
        url_file = arguments['--url']
        regex_file = arguments['--regex']

        # I use pandas for reading urls to handle huge amount of urls in the big data file
        url_handler = UrlHandler(url_file)
        # I read the whole regex file as it is not expected to have huge amount of data entries
        regex_list = FileHandler.fetch_lines(regex_file)
        flag_main_loop = True

    while flag_main_loop:
        url_link = url_handler.fetch_first()
        process_website(url_link, regex_list)

        if not url_handler.has_data():
            flag_main_loop = False
