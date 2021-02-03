import re
import math
import time
import html
import imghdr
import random
import atexit
import requests
import zipfile
from threading import Thread
from collections import deque

from rdstr import randstr
from headers import HEADER


ses = requests.session()
ses.headers.update(HEADER)


HOST = 'https://cn.bing.com'


search = '动漫壁纸'
count = 1000

url = 'https://cn.bing.com/images/async?q=%(topic)s&first=%(page)d&count=%(count)d&relp=35&scenario=ImageBasicHover&datsrc=N_I&layout=R'

tag_a = re.compile('<a class="iusc" .*?>')
murl = re.compile('"murl":"(.*?)"')

page = 200
#page = 1

startn = 200 * 35

All = deque()

def main():
    thrs = deque()
    for p in range(page):
        p = startn + p * 35
        iurl = url % dict(topic = search, page = p, count = 35)
        print(iurl)
    
        #try:
        #    get(iurl)
        #except Exception as e:
        #    print(e)
        
        thrs.append(Thread(None, get, iurl, (iurl, thrs, len(thrs))))

    for t in thrs:
        t.setDaemon(1)
    for t in thrs:
        t.start()
    for t in thrs.copy():
        t.join()
        print(t,'end')

def last_write():
    print('zipping')
    if not All:
        return
    with zipfile.ZipFile('all.zip', 'a') as zf:
        for f in All:
            try:
                zf.write(f)
            except FileNotFoundError:
                pass

atexit.register(last_write)

def get(ur, thrs, _i):
    this = thrs[_i]

    r = ses.get(ur)
    as_ = tag_a.findall(r.text)
    print(len(as_))

    n = 0
    for a in as_:
        text = html.unescape(a)
        try:
            s = murl.search(text).group(1)
        except Exception:
            #print('no murl')
            continue
        fn = randstr(s)
        if fn is None:
            #print('exists')
            continue

        try:
            b_img = ses.get(s).content
        except Exception:
            #print('pass', s)
            continue
        n += 1

        ext = imghdr.what(None, b_img)
        if ext is None:
            ext = 'jpeg'
        fn = "%s.%s" % (fn, ext)

        with open(fn, 'wb') as f:
            f.write(b_img)

        print('get', fn, 'at', s)
        All.append(fn)

    if n:print('get', n ,'pics')
    thrs.remove(this)
    print(this, 'finish tasks', 'rest', len(thrs), 'works')


if __name__ == '__main__':
    main()
