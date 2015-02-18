streamdispatch
==============

Overview
--------
A simple wrapper script that takes an url and does some domain name matching and dispatches it to a media player or another script. The link can be given as a comandline argument or parsed from the system clipboard.

For instance a twitch link will be opened in vlc via livestreamer with some arguments and a youtube url will be opened in vlc via livestreamer with some arguments, but if that fails the script tries to open the link in vlc via youtube-viewer instead.

The distinction of different domains is done via simple heuristic if-statements and what commands are called in each case is hard coded but easily exchangeable in the program source.

simple html-redirects is handled in case a given url is shortened or so. taken from https://github.com/sebth/torskbot/

Usage
-----
``python setup.py install``
``$ streamdispatch <url>``

dispatches the link to livestreamer or youtube-viewer to be opened in VLC.

``$ streamdispacth``

since no url is specified the content of the system clipboard is read (via pyperclip dependency)

``$ streamdpy -v <url>``

verbose mode of the above with <url> given or left out.

Dependencies
------------

Due to the split of urllib in python3 the code will only run out of the box with python3, this should easily be rektified by looking up the correct use of urllib in python2.

streamdispatch requires pyperclip to read from system clipboard, which can be installed by ``pip3 install pyperclip``

also uses python libraries, subprocess, sys and re which ought to be present in default python.

Installation
------------

this is a simple self-contained script. download it and link it to a directory in your path
for instance

``$ ln -s ~/Downloads/streamdispatch/strempy.py ~/bin/streampy``


if ~/bin is in your path.

Note, Caution
-------------

This is a very ugly ad hoc script developed with minimal effort for my personal needs, however due to the simplicity it should be evident which hard coded strings should be changed to include your prefered media players and their arguments.

Integration
-----------

URXVT integration
if you use urxvt and the url-select script to open or copy links from your terminal it is easy to add a key that takes the link and opens it in streampy.

Change the url-select script for urxvt like below (here key s has been used for Stream, and d because it is next to s).

``~/.urxvt/ext$ diff url-select urxvt-perls/url-select``

``137,140c137``
``<     } elsif ($char eq 's' || $char eq 'd') {``
``<         $self->exec_async( "streampy", ${$self->{found}[$self->{n}]}[4], "&" );``
``<         deactivate($self) unless $char eq 's';``
``<     } elsif ($char eq 'y') {``
``---``
``> 	} elsif ($char eq 'y') {``

i3 integration

if the link in question is music (my primary use) I donät want a media player window popping so I tried several commandline arguments to pass to vlc and mpv with various degrees of success (see commit history), however i3 allows for simple rules governing where to open windows for application which trivializes the problem

The follwing rule will assign all vlc windows to workspace 9, out of sight, and by default the urgency flag is raised to you can easily see that it worked.
add the following lines to your i3 config

``assign [class="Vlc"] 9``

This means that even videos I do want to see are moved, but you can easily go there manually.

if you want to bind a hotkey in i3 to run the script, if you have a link on clipboard for instance you can add the line

``bindsym $mod+i exec /home/spill/bin/streampy``

to your config.

Contributions
-------------
are very welcome.

License
-------

I don't know, for me do whatever. the html redirect code was taken from https://github.com/sebth/torskbot under the GNU general public license.

Remarks on mpv
--------------

I have been informed that mpv have added support for protected youtube videos as well so with that the distinction between protected and unprotected youtube videos in the code can be omitted, if that is your player of choice a lot of code can be scrapped.
