import atexit
import requests
from collections import deque
from threading import Thread



MAX_THREAD_NUM = 6
url = 'https://haoa.haozuida.com/20181117/xLDdVyCg/800kb/hls/X2CA303%(nums)s.ts'

numlist = deque(range(4000, 5000)) # All page numbers
numlist.extend(range(41000, 42000))
allfn = numlist.copy()
errorlist = deque() # for storing error pages

def T_get(nl, el, i):
    ses = requests.session() # intialize for a session
    pop = nl.popleft if i // 2 else nl.pop
    ur = url
    while nl:
        pn = pop()
        u = ur % dict(nums = pn)
        try:
            r = ses.get(u)
            if r.status_code != 200:
                raise TypeError
            c = r.content
        except Exception:
            el.append(pn)
            print("Error at", u, 'code:', r.status_code)
            continue
        with open(f"tss/{pn}.ts", 'wb') as f:
            f.write(c)
        print(f'get page {pn}; remained {len(nl)}\n', end='')
    print("Get All finish!")

def cc():
    with open("Movie.ts", 'wb') as wf:
        for n in allfn:
            fn = f"tss/{n}.ts"
            with open(fn, 'rb') as rf:
                wf.write(rf.read())
            print('write', fn)
atexit.register(cc)

def main():
    thrs = [Thread(None, T_get, f'Movie{i}', (numlist, errorlist, i)) for i in range(MAX_THREAD_NUM)]

    for t in thrs:
        t.setDaemon(True)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()
    print(errorlist)

if __name__ == '__main__':
    #T_get(numlist, errorlist, True)
    main()
