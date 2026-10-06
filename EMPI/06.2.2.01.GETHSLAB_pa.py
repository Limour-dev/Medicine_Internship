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
    
    input('任意键粘贴住院记录...')
    zs = pyperclip.paste().strip().splitlines()[1:]
    print(len(zs), zs[0], zs[-1], sep='\n')

    url = 'http://10.16.90.239:30008/api/visit/getVisitInfo'

    def rm_rep(x):
        return x[2]
    zs2lb = {}

usr = input('账号信息：')

headers = {
    "Cookie": input('输入Cookie: ')
}

res = []
for i in range(len(res), len(zs)):
    ks = zs[i].split('|@|')
    for k in ks:
        if k.startswith('zs'):
            print(i+1, k)
            break
    else:
        print(i+1, k, 'skip')
        continue
    k = k[7:]

    o_data = {"vid":k,"vidType":"02","appId":"EMR","user": usr}
    
    a = httpx.post(
            url, headers=headers,
            json = o_data,
            timeout = _t
        )

    r = a.json()
    
    pid = r['data']['pid']

    name = r['data']['name'].strip()

    res.append(f'{pid}\t{name}')

pyperclip.copy('\n'.join(res))
