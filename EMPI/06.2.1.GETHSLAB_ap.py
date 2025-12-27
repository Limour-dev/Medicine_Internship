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

    def rm_rep(x):
        return x[2]
    zs2lb = {}

for i in range(len(lrs1)):
    lres = []
    for lr in lrs1[i].split('|@|'):
        if not lr:
            continue
        flr = lr.split('||')
        if not flr[0].startswith('检验:'):
            continue
        lr = flr[-1].split('@')
        flr = flr[0].split('  ', maxsplit=1)
        ffc = flr[0][3:].split('.')
        ffc = f'20{ffc[0]}-{ffc[1]}-{ffc[2]} 00:00'
        fff = lr[-1].split('-')
        fff = [x.lstrip('0') for x in fff]
        lres.append((ffc, flr[1], (lr[-2], lr[-3], '-'.join(fff))))

    lres.sort(key=rm_rep)
    lres = [next(g) for k,g in groupby(lres, key=rm_rep)]
    lres.sort(key=lambda x:x[0])
    zs2lb[zs[i]] = lres

if not os.path.exists('GETHSLAB'):
    os.mkdir('GETHSLAB')

i=0
for i in range(i,len(lrs1)):
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

        try:
            tr = div.select('tr')
        except AttributeError:
            continue
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
    
