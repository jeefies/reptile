import atexit
import requests
from collections import deque
from threading import Thread


MAX_THREAD_NUM = 6
url = "https://haoa.haozuida.com/20181117/xLDdVyCg/800kb/hls/X2CA303%s.ts"


filenumberlist = deque(range(4000, 5000), 2000)
filenumberlist.extend(range(41000, 42000))
allfn = filenumberlist.copy()

def T_get(fnl, i):
    ses = requests.session()

    pop = fnl.popleft if i % 2 else fnl.pop
    ur = url
    while fnl:
        fn = pop()
        u = ur % fn
        r = ses.get(u).content

        with open(f"ts/{fn}.ts", 'wb') as f:
            f.write(r)

        print(f'get {fn} ok', end='\t', flush = True)

    print("get all finish")

def conbineAll():
    with open('movie.ts', 'wb') as wf:
        for n in allfn:
            with open(f"ts/{n}.ts", 'rb') as rf:
                wf.write(rf.read())
    print('combined into one file')
atexit.register(conbineAll)

def main():
    thrs = [Thread(None, T_get, f"get Movie{i}", (filenumberlist, i)) for i in range(MAX_THREAD_NUM)]

    for t in thrs:
        t.setDaemon(True)
    for t in thrs:
        t.start()
    for t in thrs:
        t.join()

if __name__ == '__main__':
    main()
