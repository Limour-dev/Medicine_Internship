if True:
    import os,re,json
    re_id = re.compile(r'[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}', re.IGNORECASE)
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
    
    input('任意键粘贴PIS...')
    lrs1 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')
    url = 'http://v-risservice01.zshis.com.sh:8066'

if not os.path.exists('GETHSREC'):
    os.mkdir('GETHSREC')

re_pisn = re.compile(r'number=(\d+)', re.IGNORECASE)

for i in range(min(len(zs),len(lrs1))):
    o_zs = zs[i].strip()
    pt = os.path.join('GETHSREC', o_zs)
    if not os.path.exists(pt):
        os.mkdir(pt)
    pt = os.path.join(pt, 'pis')
    if not os.path.exists(pt):
        os.mkdir(pt)
    pisn = re_pisn.findall(lrs1[i])
    if pisn:
        try:
            
            pisn = pisn[0]
            pisn = httpx.get(f'http://136.100.100.185/api/outer/clinical/lists?apply_number={pisn}')
            pisn = pisn.json()
            pisn = pisn['data']
            for piso in pisn:
                piso = piso.get('id')
                if not piso:
                    continue
                pto = os.path.join(pt, f'{piso}.json')
                print(pto)
                if os.path.exists(pto):
                    print('skip')
                    continue
                piso = httpx.get(f'http://136.100.100.185/api/outer/clinical/pathology/{piso}')
                piso = piso.json()
                with open(pto, 'w', encoding='utf-8') as wf:
                    json.dump(piso, wf, ensure_ascii=False)
            continue
        except:
            print(pisn)
    for cun in set(lrs1[i].split('|@|')):
        cun = cun.strip()
        if not cun:
            continue
        cun = cun.split('|')
        try:
            pto = os.path.join(pt, f'{cun[0]}_{cun[1]}_{re_id.findall(cun[2])[0].upper()}.html')
        except IndexError:
            print(cun)
            continue
        print(pto)
        if os.path.exists(pto):
            print('skip')
            continue
        if cun[2].startswith('http'):
            a = httpx.get(cun[2])
        else:
            a = httpx.get(url + cun[2])
        with open(pto, 'w', encoding='utf-8') as wf:
            wf.write(a.text)
