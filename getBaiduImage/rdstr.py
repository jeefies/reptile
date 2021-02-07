import atexit
import string
import random
from collections import deque

# use thread safe sequence
_exists = deque()
_getted = deque()


# init for the names
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

ol = len(_exists)
print(ol, len(_getted))

# the main method the generate the name
def randstr(url):
    if url in _getted:
        return None
    rs = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    if rs in _exists:
        # check if is exist
        return randstr()
    _exists.append(rs)
    _getted.append(url)
    return rs

# write in the files for next use
def writein():
    print('writing')
    with open("exists.txt", 'w') as f:
        if _exists:
            f.write(','.join(_exists))
    with open("getted.txt", 'w') as f:
        if _getted:
            f.write('\n'.join(_getted))
    nl = len(_exists)
    print('new', nl - ol[0])
    print(nl, len(_getted))

atexit.register(writein)
