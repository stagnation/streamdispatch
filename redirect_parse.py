import urllib.parse
import urllib.request
import re

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
    url = quote_nonascii_path(url)
    rh = FinalURLHTTPRedirectHandler()
    opener = urllib.request.build_opener(rh)
    opener.open(url)
    final_url = rh.final_url
    return rh.final_url if rh.final_url else url

if __name__ == '__main__':
    url = "http://youtu.be/uxCGgcX3wfA"
    print(final_url(url))
    None
