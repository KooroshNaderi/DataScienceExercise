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

def FetchLines(filename):
    with open(filename) as f:
        out = f.read().splitlines()
    return out

if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')
    # I assume the arguments are the files containing urls and regex
    regex_list = []
    url_list = []
    flag_main_loop = False
    if arguments['--url'] and arguments['--regex']:
        url_file = arguments['--url']
        regex_file = arguments['--regex']
        # I am reading the files and keeping a list of [urls,regex] to process, however if url_file is a big data
        # using pandas is a better solution, not fetching all the info into memory
        url_list = df = pd.read_csv(url_file, header=None, encoding='utf-8', delimiter='\n')
        regex_list = FetchLines(regex_file)
        flag_main_loop = True

    while flag_main_loop:
        t = 0
