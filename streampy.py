#!/usr/bin/python3
from __future__ import division
from subprocess import Popen, PIPE
import pyperclip as pc
import sys

verbose=False

def read_url_from_clipboard():
    clipboard = pc.paste()
    clip_string = clipboard.encode('UTF-8','ignore')
    return clip_string

def conditional_print(arguments):
    if verbose:
        print(arguments)

def main():
    arguments = sys.argv
    if len(arguments) > 1:
        url = arguments[1]
    else:
        url = read_url_from_clipboard()

    try:
        play_url(url)
    except Exception as e:
        print(e)
        pass

def play_url(url):
    livestreamerargs = ['best']
    test = ['a', 'b']
    youtubeviewerargs = ['best', '--no-interactive']
    print(type(url))
    #if isinstance(url, unicode):
    #    url = url.encode('UTF-8','ignore')
    if isinstance(url, bytes):
        url = url.decode('UTF-8')
    if 'twitch.tv' in url:
        if verbose:
            print('twitch stream')

        args = ['livestreamer', url] + livestreamerargs
        if verbose:
            print(args, len(args))
        Popen(args)

    elif 'youtube.com' not in url:
        if verbose:
            print('not youtube url - possibly shortened')

    if 'youtube.com' in url:
        if verbose:
            print('youtube url')
        args = ['livestreamer', url] + livestreamerargs
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
            args = ['youtube-viewer', url] + youtubeviewerargs
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            outmsg = p.communicate()

if __name__ == '__main__':
    main()
    """
    url = 'http://www.twitch.tv/forgg'
    url = 'https://www.youtube.com/watch?v=QcqC4jtrR9Y'#regular
    url = 'https://www.youtube.com/watch?v=NJ3aiM8K6D0'#protected
    """
