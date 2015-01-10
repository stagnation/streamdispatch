from __future__ import division
from subprocess import Popen, PIPE
import pyperclip as pc
import sys

def read_url_from_clipboard():
    clipboard = pc.paste()
    print( type(clipboard))
    clip_string = clipboard.encode('UTF-8','ignore')
    print(clip_string)
    return clip_string

def main():
    arguments = sys.argv
    if len(arguments) > 1:
        url = arguments[1]
    else:
        url = read_url_from_clipboard()

    try play_url(url)

def play_url(url):
    read_url_from_clipboard()
    url = 'http://www.twitch.tv/forgg'
    url = 'https://www.youtube.com/watch?v=QcqC4jtrR9Y'#regular
    url = 'https://www.youtube.com/watch?v=NJ3aiM8K6D0'#protected
    livestreamerargs = ['best']
    if 'twitch.tv' in url:
        print('twitch stream')
        args = ['livestreamer', url] + livestreamerargs
        print(args, len(args))
        Popen(args)
    elif 'youtube.com' not in url:

        print('not youtube url - possibly shortened')

    if 'youtube.com' in url:
        print('youtube url')
        args = ['livestreamer', url] + livestreamerargs
        print(args, len(args))
        p = Popen(args, stdout=PIPE, stderr=PIPE)
        outmsg, errmsg = p.communicate()

        print("process output\n", outmsg)
        print("error?", errmsg)
        print("msg type", type(outmsg))
        outmsg_string = outmsg.decode(encoding='UTF-8')
        if 'youtube-dl' in outmsg_string:
            print("process output\n", outmsg)
            print("TRYING youtube-viewer")
            args[0] = 'youtube-viewer'
            args.append('--no-interactive')
            p = Popen(args, stdout=PIPE, stderr=PIPE)
            m = p.stdout
            outmsg = p.communicate()

            """
            outmsg_string = outmsg.decode(encoding='UTF-8')
            print(outmsg_string)
            if 'Select' in outmsg_string:
                #don't want to select anothe video to watch, kill process
                None
                p.term()
            """
if __name__ == '__main__':
