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
    
    input('任意键粘贴住院记录...')
    lrs1 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')
    url = 'http://10.16.90.35:8000/api/record/v1/emr_view_doc_cureno'

    ast = input('输入access_token...').strip()

    headers = { "access_token": ast }

if not os.path.exists('GETHSREC'):
    os.mkdir('GETHSREC')

for i in range(min(len(zs),len(lrs1))):
    o_zs = zs[i].strip()
    pt = os.path.join('GETHSREC', o_zs)
    if not os.path.exists(pt):
        os.mkdir(pt)
    pt = os.path.join(pt, 'ipd')
    if not os.path.exists(pt):
        os.mkdir(pt)
    for cun in set(lrs1[i].split('|@|')):
        cun = cun.strip()
        if not cun:
            continue
        cun = cun.split('|')[-1]
        pto = os.path.join(pt,cun + '.json')
        print(pto)
        if os.path.exists(pto):
            print('skip')
            continue
        a = httpx.get(
                url, headers=headers,
                params={
                    "cureNo": cun,
                }
            )
        with open(pto, 'w', encoding='utf-8') as wf:
            wf.write(a.text)
