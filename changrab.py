import os
from os import path
import sys
import json
import re
import time as t
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse


def parse_4ch_url(url):
    pat = re.compile(r'(https://|http://)?boards.4chan.org/(\w+)/thread/(\d+)')
    ret = pat.match(url).groups()
    return ret

def get_thread_image_paths(url):
    _, board, thread_id = parse_4ch_url(url)
    path = r'http://a.4cdn.org/%s/thread/%s.json' % (board, thread_id)
    json_response = json.loads( urlopen(path).readall().decode() )
    posts = json_response['posts']
    image_paths = []
    for (fname, fext) in [ (p['tim'], p['ext']) for p in posts if 'filename' in p]:
        filepath = r'http://i.4cdn.org/%s/%s%s' % (board, fname, fext)
        image_paths.append(filepath)
    return board, thread_id, image_paths

def main():
    inp_urls = sys.argv[1:]
    for inp_url in inp_urls:
        board, thread_id, image_paths = get_thread_image_paths(inp_url)
        filecount = 0

        before_t = t.clock()
        for imgpath in image_paths:
            localfname = path.basename(urlparse(imgpath)[2])
            localpath = path.join(os.path.curdir, board, thread_id, localfname)
            os.makedirs(path.dirname(localpath), exist_ok=True)
            sys.stdout.write(imgpath + '\t\t')
            urlretrieve(imgpath, localpath)
            sys.stdout.write('successful\n')
            filecount += 1
        after_t = t.clock()

        tdelta = (after_t - before_t)
        print("Scraped %d image(s) in %f seconds" % (filecount, tdelta))
        sys.stdout.flush()

if __name__ == '__main__':
    sys.exit(main())