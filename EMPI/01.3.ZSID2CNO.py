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
    
    input('任意键粘贴ZSID...')
    zs = pyperclip.paste().strip().splitlines()[1:]
    print(len(zs), zs[0], zs[-1], sep='\n')
    
    url = 'http://10.16.90.35:8000/api/record/v1/admission_record_list'

    ast = input('输入access_token...').strip()

    headers = { "access_token": ast }

res = []
for i in range(len(res), len(zs)):
    zsid = zs[i]
    data = {"currentPage":1,"pageSize":1,"filter":{"medTechNo": zsid}}
    a = httpx.post(url, headers=headers,json=data).json()
    a = a.get('result')
    if not a:
        res.append('')
        continue
    a = a.get('records')
    if not a:
        res.append('')
        continue
    a = a[0]
    if not a:
        res.append('')
        continue
    res.append(a['cardNo'])
    print(i, zsid, a)
pyperclip.copy('\n'.join(res))
