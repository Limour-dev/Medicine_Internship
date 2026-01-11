if True:
    import os, json, re
    import pyperclip
    from datetime import datetime

    reg_sp = re.compile(r'[\n\r]\s*')
    reg_nn = re.compile(r'\n\n+')
    reg_html = re.compile('<.+?>')
    def clear_value(_v, rmHt=False):
        if rmHt:
            _v = reg_html.sub('', _v)
        _v = _v.replace('\t', ' ').replace('','')
        _v = reg_sp.sub('\n', _v)
        _v = reg_nn.sub('\n', _v)
        return _v.strip()

    input('任意键粘贴ZSID...')
    zs = pyperclip.paste().strip().splitlines()
    print(len(zs), zs[0], zs[-1], sep='\n')

    pts = input('请输入病史记录路径：')
    pto = input('请输入记录另存路径：')

    res = []

    reg_d = re.compile(r'\n^(\d\d\d\d-\d\d-\d\d)\t(.+?)$', re.MULTILINE+re.IGNORECASE)
    reg_sp = re.compile(r'\n^\d\d\d\d-\d\d-\d\d\t.+?$', re.MULTILINE+re.IGNORECASE)

if True:
    zsid2pt = {}
    pth3s = os.listdir(pts)
    for pth3 in pth3s:
        pth4 = pth3.split('_')[-1][:-4]
        # print(pth4)
        zsid2pt[pth4] = (os.path.join(pts, pth3), os.path.join(pto, pth3))


if True:
    if len(res):
        res = res[:-1]
    reg_cd = re.compile(r'心电图', re.MULTILINE+re.IGNORECASE)
    for zsi_i in range(len(res), len(zs)):
        zid = zs[zsi_i]
        if not zid in zsid2pt:
            print('skip', zid)
            res.append('NA\tNA')
            continue
        pth1 = zsid2pt[zid]
        print(pth1)

        with open(pth1[0], 'r', encoding='utf-8') as rf:
            data = rf.read()

        th = reg_d.findall(data)
        if (not th) and (not data.strip()):
            print('skip', zid)
            res.append('NA\tNA')
            continue

        td = reg_sp.split(data)
        tt = td[0].split('\n', maxsplit=1)
        td[0] = tt[-1]
        th = [tt[0].split('\t', maxsplit=1)] + th

        assert len(th) == len(td)

        with open(pth1[1], 'w', encoding='utf-8') as wf:
            for i,h in enumerate(th):
                if reg_cd.match(h[-1]):
                    wf.write(h[0])
                    wf.write('\t')
                    wf.write(h[-1])
                    wf.write(td[i])
                    wf.write('\n')