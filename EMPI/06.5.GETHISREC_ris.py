if True:
    import os,re
    re_id = re.compile(r'id=([^&]+)', re.IGNORECASE)
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
    
    input('任意键粘贴RIS...')
    lrs1 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')
    url = 'http://v-risservice01.zshis.com.sh:8066'

if not os.path.exists('GETHSREC'):
    os.mkdir('GETHSREC')

for i in range(min(len(zs),len(lrs1))):
    o_zs = zs[i].strip()
    pt = os.path.join('GETHSREC', o_zs)
    if not os.path.exists(pt):
        os.mkdir(pt)
    pt = os.path.join(pt, 'ris')
    if not os.path.exists(pt):
        os.mkdir(pt)
    for cun in set(lrs1[i].split('|@|')):
        cun = cun.strip()
        if not cun:
            continue
        cun = cun.split('|')
        pto = os.path.join(pt, f'{cun[0]}_{cun[1]}_{re_id.findall(cun[2])[0]}.html')
        print(pto)
        if os.path.exists(pto):
            print('skip')
            continue
        a = httpx.get(url + cun[2])
        with open(pto, 'w', encoding='utf-8') as wf:
            wf.write(a.text)
