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
    o_zs = zs[i].strip()
    print(i+1, o_zs)
    o_data = {"currentPage":1,"pageSize":10,"filter":{"medTechNo": o_zs }}

    a = httpx.post(
            url, headers=headers,
            json = o_data,
            timeout = _t
        )
    r = a.json()
    if len(r['result']['records']) < 1:
        res.append('skip')
        continue
    cos = []
    for o_r in r['result']['records']:
        co = o_r['cureNo']
        cos.append(f'zs-his|{co}')
    cos = '|@|'.join(cos)
    cn = o_r['admitNo']
    can = o_r['cardNo']
    name = o_r['name'].strip()
    sex = o_r['sex']
    birthday = o_r['birthday'].split(' ', maxsplit=1)[0]
    res.append(f'{i+1}\t{o_zs}\t{sex}\t{birthday}\t{cn}\t{can}\t{cos}')
pyperclip.copy('\n'.join(res))
