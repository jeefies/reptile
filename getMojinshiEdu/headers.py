HEADER = {
        "User-Agent": "Mozilla/5.0 (X11; Linux aarch64; rv:78.0) Gecko/20100101 Firefox/78.0" ,
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip",
        "Connection": 'keey-alive',
}

QRCODE = dict(**HEADER)
#QRCODE['']
MOJINSHI = dict(**HEADER)
MOJINSHI.update({
        "Referer": "https://py.mojinshi.online/v1/",
        "Origin": "https://py.mojinshi.online",
        })


