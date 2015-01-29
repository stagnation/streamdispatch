#!/usr/bin/python3
from __future__ import division
from subprocess import Popen, PIPE
import pyperclip as pc
import sys
sys.path.append("/home/spill/arbete/streampy/")
from redirect_parse import *

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
        elif arg[0] == 'v':
            verbose=True

    if not url:
        url = read_url_from_clipboard()

    try:
        print(url)
        url = final_url(url)
        print(url)
        play_url(url, verbose)
    except Exception as e:
        print(e)
        pass

def play_url(url, verbose=False):
    livestreamer_args = ['best']
    youtubeviewer_args = ['best', '--no-interactive']

    #if isinstance(url, unicode):
    #    url = url.encode('UTF-8','ignore')
    if isinstance(url, bytes):
        url = url.decode('UTF-8')

    print(url)
    if 'twitch.tv' in url:
        conditional_print('twitch stream', verbose)

        args = ['livestreamer', url] + livestreamer_args
        if verbose:
            print(args, len(args))
        Popen(args)

    elif 'youtube.com' not in url:
        conditional_print('not youtube url - possibly shortened', verbose)
        url = final_url(url)

    if 'youtube.com' in url:
        conditional_print('youtube url', verbose)
        args = ['livestreamer', url] + livestreamer_args
        if verbose:
            print(args, len(args))

        p = Popen(args, stdout=PIPE, stderr=PIPE)
        outmsg, errmsg = p.communicate()

        if verbose:
            print("process output\n", outmsg)
            print("error?", errmsg)
            print("msg type", type(outmsg))

        outmsg_string = outmsg.decode(encoding='UTF-8')
        if 'youtube-dl' in outmsg_string:
            if verbose:
                print("process output\n", outmsg)
                print("TRYING youtube-viewer")

            #args[0] = 'youtube-viewer'
            #args.append('--no-interactive')
            args = ['youtube-viewer', url] + youtubeviewer_args
            conditional_print("args:\n", args, verbose)
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            outmsg = p.communicate()

    elif "twitch.tv" not in url:
        #hope livestreamer works, output to stdout
        args = ['livestreamer', url] + livestreamer_args
        conditional_print(args, len(args), verbose)
        Popen(args)
        p.communicate()



if __name__ == '__main__':
    main()
    """
    url = 'http://www.twitch.tv/forgg'
    url = 'https://www.youtube.com/watch?v=QcqC4jtrR9Y'#regular
    url = 'https://www.youtube.com/watch?v=NJ3aiM8K6D0'#protected
    """
