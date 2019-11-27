import sys
import os
from datetime import datetime
import signal


def ret_error(str1, str2):
    from difflib import SequenceMatcher

    s = SequenceMatcher(None, str1, str2)
    return 1 - s.ratio()


def is_match(_worker_id, _text, _re):
    import re

    out = {}

    out['worker_id'] = _worker_id
    time_start = datetime.now()
    out['time'] = time_start.ctime()
    out['RE'] = _re
    p = re.compile(_re)

    x = p.search(_text)
    if x:
        out['error'] = 0
        out['matched-string'] = 'something'#x.group(0)
    else:
        out['error'] = ret_error(_text, _re)
        out['matched-string'] = ''

    out['deltatime'] = (datetime.now() - time_start).total_seconds()
    return out


def fetch_text_from_url(_url):
    import urllib

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


def exit_no_error():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def get_time_date_format():
    datetime.now().ctime()


def os_kill_process():
    os.kill(os.getpid(), signal.CTRL_BREAK_EVENT)
