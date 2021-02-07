import re
import os.path
import codecs
import requests
from chardet import detect
from collections import deque
from threading import Thread
from getNovel import Novel
from headers import HEADER

ses = requests.session()

ses.headers.update(HEADER)

page = ses.get('http://www.xbiquge.la/9/9419/index.html')
detection = detect(page.content)
encoding = detection['encoding']
text = codecs.decode(page.content, encoding)

host = 'http://www.xbiquge.la'

textlist = re.findall(b'<div id="list">([\s\S]*?)</div>'.decode(encoding), text)
hrefcon = textlist[0]

hrefs = re.findall(b"<a href='(.*?)' >".decode(encoding), hrefcon)
names = re.findall(b"<a .*? >(.*?)</a>".decode(encoding), hrefcon)
assert len(hrefs) == len(names), (len(hrefs), len(names))


def get(url, ni, sess):
    name, index = ni
    try:
        codecs.open("{}.txt".format(index + 1), 'x')
    except:
        return
    r = sess.get(url)
    text = r.content
    encoding = detect(text)['encoding']
    text = codecs.decode(text, encoding).replace('\r', '\n')
    con = re.search('<div id="content">[\s\S]*?</div>', text).group()
    con = con.replace("&nbsp;", ' ').replace("<br />", '')[18:]
    con = con.split("<p>", 1)[0]
    con = con.split("--", 1)[0]
    con.strip(';').strip()
    con = "章节%d %s\n" % (index + 1, name) + con
    with codecs.open("{}.txt".format(index + 1), 'w') as f:
        print(con, file=f)
        print('Wrote', name)

de = deque(enumerate(zip(names, hrefs)))
length = len(de)

def thr(de):
    sess = requests.session()
    sess.headers.update(HEADER)
    while de:
        i, (n, h) = de.popleft()
        url = host + h
        try:
            get(url, (n, i), sess)
        except requests.ConnectionError:
            sess = requests.session()
            sess.headers.update(HEADER)
            get(url, (n, i), sess)
    print("get OK")

novel = Novel('/', length)
novel.plain = [f"{i + 1}.txt" for i in range(length)]

def check():
    print('checking')
    sess = requests.session()
    sess.headers.update(HEADER)
    names = [f"{i + 1}.txt" for i in range(length)]
    for i, n in enumerate(names):
        if not os.path.exists(n):
            print('missing', n)
            n, h = names[i], hrefs[i]
            url = host + h
            try:
                get(url, (n, i), sess)
            except requests.ConnectionError:
                check()
    print('check ok..')

thrs = [Thread(None, thr, "getNovel %d" % i, (de,))  for i in range(5)]
for t in thrs:
    t.setDaemon(True)
for t in thrs:
    t.start()
try:
    for t in thrs:
        t.join()
    check()
except KeyboardInterrupt:
    print('\rInterrupt')
novel.concat()
novel.zipall()
