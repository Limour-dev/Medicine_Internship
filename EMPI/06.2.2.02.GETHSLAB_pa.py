if True:
    import os
    from itertools import groupby

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        return _v

    import pyperclip
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup

    _t = httpx.Timeout(120)
    
    input('任意键粘贴pid...')
    zs = pyperclip.paste().strip().splitlines()[1:]
    print(len(zs), zs[0], zs[-1], sep='\n')

    url = 'http://10.16.90.239:30008/api/visit/getFullEventList'

    def rm_rep(x):
        return x[2]

    headers = {
        "Cookie": input('输入Cookie: ')
    }

res = []
for i in range(len(res), len(zs)):
    pid = zs[i].strip()

    print(i+1, pid)
    
    if pid == 'skip':
        res.append('')
        continue

    o_data = {"pid": pid,"classCode":"A01"}
    
    a = httpx.post(
            url, headers=headers,
            json = o_data,
            timeout = _t
        )

    r = a.json()
    
    o_data = r['data']

    rres = []
    for r in o_data:
        did = r['did'].split('_')
        t = r['eventDatetime'][:16]
        n = r['eventName']
        st = did[2]
        st = f'{st[:4]}-{st[4:6]}-{st[6:]}'
        rres.append(f'{t}|{n}|{did[-1]}|{did[1]}|{st}')

    res.append('|@|'.join(rres))

pyperclip.copy('\n'.join(res))
