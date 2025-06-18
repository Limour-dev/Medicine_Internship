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

    input('任意键粘贴LRS1...')
    lrs1 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')
    url = 'http://v-emrservice01.zshis.com.sh/EmrPortal_new/MedicalEvent/LabCheckDetail.aspx'

if True:
    input('任意键粘贴LRS2...')
    lrs2 = pyperclip.paste().strip().splitlines()[1:]
    print(len(lrs2), lrs2[0], lrs2[-1], sep='\n')

    m_l = max(len(lrs1), len(lrs2))
    if len(lrs1) < m_l:
        lrs1 += ['']*(m_l - len(lrs1))
    if len(lrs2) < m_l:
        lrs2 += ['']*(m_l - len(lrs2))
    zs2lb = {}

    def rm_rep(x):
        return x[2]

for i in range(m_l):
    lres = []
    for lr in lrs1[i].split('|@|'):
        if not lr:
            continue
        lr = lr.split('|')
        lres.append((lr[0], lr[1], (lr[2], lr[3], lr[4])))
    for lr in lrs2[i].split('|@|'):
        if not lr:
            continue
        lr = lr.split('|')
        lres.append((lr[0], lr[1], (lr[2], lr[3], lr[4])))
    lres.sort(key=rm_rep)
    lres = [next(g) for k,g in groupby(lres, key=rm_rep)]
    lres.sort(key=lambda x:x[0])
    zs2lb[zs[i]] = lres

if not os.path.exists('GETHSLAB'):
    os.mkdir('GETHSLAB')

for i in range(0,m_l):
    print('i', i)
    k = zs[i]
    v = zs2lb[zs[i]]
    pt = os.path.join('GETHSLAB', k)
    if not os.path.exists(pt):
        os.mkdir(pt)
    for o in v:
        pto = os.path.join(pt, '_'.join(o[2])).replace(' ','-')
        print(pto)
        if os.path.exists(pto) or int(o[2][2][:4]) < 2010:
            print('skip')
            continue
        d = httpx.get(url, params={
                "sampleNo": o[2][1],
                "instrid": o[2][0],
                "sampleDate": o[2][2]
            })
        d_s = BeautifulSoup(d, "html.parser")
        div = d_s.select_one("#gridViewLabCheck")
        
        tr = div.select('tr')
        tb = ['\t'.join(x.getText() for x in tr[0].select('th'))]
        for tro in tr[1:]:
            td = '\t'.join(clear_value(x.getText()) for x in tro.select('td'))
            tb.append(td)
        with open(pto, 'w', encoding='utf-8') as wf:
            wf.write(repr(o))
            wf.write('\n')
            for td in tb:
                wf.write(td)
                wf.write('\n')
    
