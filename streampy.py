#!/usr/bin/python3
from __future__ import division
from subprocess import Popen, PIPE
import pyperclip as pc
import sys
import urllib.parse
import urllib.request
import re

#html redirect following taken from torskbot
#https://github.com/sebth/torskbot

class FinalURLHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):

    def __init__(self, *args, **kwargs):
        self.final_url = None
        super().__init__(*args, **kwargs)

    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        self.final_url = newurl
        return super().redirect_request(req, fp, code, msg, hdrs, newurl)

def quote_nonascii_path(path):
    return re.sub(
            b'[\x80-\xff]',
            lambda match: '%{:x}'.format(ord(match.group())).encode('ascii'),
            path.encode()).decode('ascii')

def urlquote(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
            (parts[0], parts[1].encode('idna').decode('ascii'),
                quote_nonascii_path(parts[2])) + parts[3:])

def final_url(url):
    if "www" not in url:
        if "http://" in url:
            url = url.replace("http://","http://www.")
        else:
            return url
    if "http" not in url:
        if "www." in url:
            url = url.replace("www.", "http://www.")
    url = quote_nonascii_path(url)
    rh = FinalURLHTTPRedirectHandler()
    opener = urllib.request.build_opener(rh)
    opener.open(url)
    final_url = rh.final_url
    return rh.final_url if rh.final_url else url

#end html redirect
#

def read_url_from_clipboard():
    clipboard = pc.paste()
    if isinstance(clipboard, bytes):
        clipboard = clipboard.encode('UTF-8','ignore')
    return clipboard

def is_url(text):
    #rudimentary check, replace with proper regexp.

    return '.' in text

def conditional_print(arguments, verbose=False):
    if verbose:
        print(arguments)

def main():
    arguments = sys.argv
    url = None
    verbose = False
    for arg in sys.argv[1:]:
        if is_url(arg):
            url = arg
        elif arg == '--verbose' or arg == '-v':
            verbose=True
    conditional_print('verbose output on', verbose)

    if not url:
        url = read_url_from_clipboard()

    try:
        url = final_url(url)
        play_url(url, verbose)
    except Exception as e:
        print(e)
        pass


def play(url, youtube_args,  verbose):
    conditional_print('youtube url', verbose)
    args = youtube_args.format(url).split(' ')
    if verbose:
        print(args)

    p = Popen(args, stdout=PIPE, stderr=PIPE)
    outmsg, errmsg = p.communicate()

    if verbose:
        print("process output\n", outmsg)
        if errmsg:
            print("error?", errmsg)

    return outmsg, errmsg

def play_url(url, verbose=False):

    CLI_args = 'mpv {}'

    if isinstance(url, bytes):
        url = url.decode('UTF-8')

    if 'twitch.tv' or 'youtube.com' in url:
        play(url, CLI_args, verbose)

    else:
        #fallback: hope livestreamer works, output to stdout
        args = CLI_args.format(url).split(' ')
        if verbose:
           print(args)
        p = Popen(args)
        p.communicate()


if __name__ == '__main__':
    main()
    #a couple of example links to test whether it works
    """
    url = 'http://www.twitch.tv/forgg'
    url = 'https://www.youtube.com/watch?v=QcqC4jtrR9Y'     #regular
    url = 'https://www.youtube.com/watch?v=NJ3aiM8K6D0'     #protected
    url = 'http://tinyurl.com/comeonnn'                     #tinyurl
    """
