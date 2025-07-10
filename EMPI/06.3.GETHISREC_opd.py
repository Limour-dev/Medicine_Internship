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
    
    input('任意键粘贴ZSID和卡号...')
    zs = pyperclip.paste().strip().splitlines()[1:]
    print(len(zs), zs[0], zs[-1], sep='\n')

    input('任意键粘贴门诊记录...')
    lrs1 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')
    url = 'http://v-emrservice01.zshis.com.sh/EmrPortal_new/RegInfo/RegDetailInfo.aspx'

if not os.path.exists('GETHSREC'):
    os.mkdir('GETHSREC')

for i,o_zs in enumerate(zs):
    o_zs = o_zs.split('\t')
    o_cn = o_zs[-1].strip()
    o_zs = o_zs[0].strip()
    
    pt = os.path.join('GETHSREC', o_zs)
    if not os.path.exists(pt):
        os.mkdir(pt)
    pt = os.path.join(pt, 'opd')
    if not os.path.exists(pt):
        os.mkdir(pt)
    for cun in set(lrs1[i].split('|@|')):
        cun = cun.strip()
        if not cun:
            continue
        pto = os.path.join(pt, cun.split('|')[-1] + '.html')
        print(pto)
        if os.path.exists(pto):
            print('skip')
            continue
        d = httpx.get(url, params={
            "CureNO": cun,
            "CardNO": o_cn
            })
        with open(pto, 'w', encoding='utf-8') as wf:
            wf.write(d.text)
