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

def play_twitch(url, twitch_args, verbose):
    conditional_print('twitch stream', verbose)

    args = twitch_args.format(url).split(' ')
    if verbose:
        print(args)
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    outmsg, errmsg = p.communicate()
    return outmsg, errmsg

def play_youtube(url, youtube_args, protected_args, verbose):
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

    outmsg_string = outmsg.decode(encoding='UTF-8')
    if 'youtube-dl' in outmsg_string:
        #livestreamer suggests to use youtube-dl for protected videos
        if verbose:
            print("process output\n", outmsg)
            print("TRYING youtube-viewer")

        args = protected_args.format(url).split(' ')
        if verbose:
            print("args:\n", args, verbose)
        p = Popen(args, stdout=PIPE, stderr=PIPE)
        outmsg, errmsg = p.communicate()
    return outmsg, errmsg

def play_url(url, verbose=False):

    twitch_args = 'livestreamer {} best'
    youtube_args = 'livestreamer {} best'
    protected_args = 'youtube-viewer {} best --no-interactive'
    fallback_args = twitch_args

    if isinstance(url, bytes):
        url = url.decode('UTF-8')
    if 'youtube.com' not in url and 'twitch.tv' not in url:
        conditional_print('neither youtube nor twitch - possibly shortened', verbose)
        url = final_url(url)
        conditional_print('final url %s' % (url), verbose)

    if 'twitch.tv' in url:
        play_twitch(url, twitch_args, verbose)

    elif 'youtube.com' in url:
        play_youtube(url, youtube_args, protected_args, verbose)

    else:
        #fallback: hope livestreamer works, output to stdout
        args = fallback_args.format(url).split(' ')
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
    """
