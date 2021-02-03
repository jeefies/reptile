import atexit
import string
import random
from collections import deque

_exists = deque()
_getted = deque()

try:
    with open("exists.txt") as f:
        _exists.extend(f.read().strip().split(','))
except FileNotFoundError:
    open('exists.txt', 'x').close()
try:
    with open("getted.txt") as f:
        _getted.extend(f.read().strip().split())
except FileNotFoundError:
    open('getted.txt', 'x').close()

print(len(_exists), len(_getted))

def randstr(url):
    if url in _getted:
        return None
    rs = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    if rs in _exists:
        return randstr()
    _exists.append(rs)
    _getted.append(url)
    return rs

def writein():
    print('writing')
    with open("exists.txt", 'w') as f:
        if _exists:
            f.write(','.join(_exists))
    with open("getted.txt", 'w') as f:
        if _getted:
            f.write('\n'.join(_getted))

atexit.register(writein)
