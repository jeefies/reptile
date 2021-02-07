import json # to resolve the data
# regist the function to call when program exit
import atexit
import random # to generate virtual datas
import zipfile # archive all files into a zip file
import requests # main method to reptile the datas
from threading import Thread
from collections import deque # use thread safe sequence

from headers import HEADER # user-agent
from rdstr import randstr # generate random file names


ses = requests.session()
ses.headers.update(HEADER)

url = ('https://image.baidu.com/search/acjson'
        '?tn=resultjson_com&ipn=rj&ct=201326592'
        '&is=&fp=result&queryWord=%(word)s&cl=2&lm=-1'
        '&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd='
        '&latest=&copyright=&word=%(word)s&s='
        '&se=&tab=&width=&height=&face=&istype=&qc=&nc=1'
        '&fr=&expermode=&force=&cg=wallpaper&pn=%(start)s'
        '&rn=%(rn)s&gsm=%(hex)s&%(page)s=')

topic = "动漫壁纸"
num = 10
repeat = 10
rn = 50

def get(u, de):
    """main  of getting the page data"""
    g = 0
    sess = requests.session()
    sess.headers.update(HEADER)
    text = json.loads(sess.get(u).text)
    data = text['data']
    for i in data:
        if not i:
            continue
        # get the extension of the file
        ext = i.get('type', 'jpg')
        ext = ext if ext else 'jpg'

        # get the replaceUrl list with some dict in
        ur = i.get('replaceUrl', None)
        if ur is None:
            print("No replace url")
            continue
        # check the url is right of not
        if not 'gimg' in str(ur):
            continue

        repur = ur[1]['ObjURL']
        ctt = sess.get(repur).content
        if len(ctt) < 500:
            # check if the data is validate to use
            continue

        fn = randstr(repur)
        if not fn:
            # the picture has getted
            continue
        fn = f'imgs/{fn}.{ext}'
        de.append(fn)

        with open(fn, 'wb') as f:
            f.write(ctt)

        print('get', fn, 'at', repur)
        g += 1

    print('got', g, 'images')

de = deque()
def main():
    thrs = []
    for n in range(num):
        s = n * rn
        page = random.randint(100, 1000000000000)
        u = url % dict(word = topic, page = page, start = s, hex = hex(s)[2:], rn = rn)
        print(u)
        thr = Thread(None, get, u, (u, de))
        thrs.append(thr)

    for t in thrs:
        # use daemon threads
        t.setDaemon(True)
    for t in thrs:
        t.start()
    for t in thrs:
        # run until every complete
        t.join()

def zipall(d):
    with zipfile.ZipFile('all.zip', 'a') as zf:
        for f in d:
            zf.write(f)

    print('zipped...')
atexit.register(zipall, de)

if __name__ == '__main__':
    for i in range(repeat):
        main()
