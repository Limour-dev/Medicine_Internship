if True:
    import pyperclip
    import os, re
    from datetime import datetime
    pts = input('输入源文件夹路径:')

    zid = {}

    for a in os.listdir(pts):
        pth1 = os.path.join(pts,a)
        b = a.split('_')
        z = b[-1].strip().upper()
        for c in os.listdir(pth1):
            t = c.split('_')[0]
            t = datetime.strptime(t, '%Y%m%d')
            pth2 = os.path.join(pth1, c)
            if z in zid:
                print(b)
                zid[z].append([t,pth2])
            else:
                zid[z] = [[t,pth2]]

if True:
    h = (input('任意键粘贴ZSID和时间...').strip().upper() == 'H')
    sl = pyperclip.paste()
    sl = sl.splitlines()[int(h):]
    print(sl[0], sl[-1])
    slt = []
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        tmp = tmp[-1].split(' ', maxsplit=1)[0]
        sst = datetime.strptime(tmp, '%Y-%m-%d')
        slt.append((zsid, sst))

if True:
    out = input('输入out文件夹路径:')
    icis = set(x[0] for x in slt)
    if '' in icis:
        icis.remove('')

for z, pths in zid.items():
    if z in icis:
        continue
    for t,pth in pths:
        pth2, pth1 = os.path.split(pth)
        pth2 = os.path.split(pth2)[-1]
        # print(pth1, pth2)
        pth2 = os.path.join(out, pth2)
        if not os.path.exists(pth2):
            os.mkdir(pth2)
        pth1 = os.path.join(pth2, pth1)
        print(pth, pth1)
        os.rename(pth, pth1)

if False:
    input('cnm')
    caonima = pyperclip.paste()
    for cnm in caonima.splitlines()[2:]:
        cnm = cnm.split(' E:')
        # print('E:' + cnm[1], cnm[0])
        os.rename('E:' + cnm[1], cnm[0])

for pth in os.listdir(pts):
    pth = os.path.join(pts, pth)
    if os.path.exists(pth) and not os.listdir(pth):
        print(pth)
        os.rmdir(pth)

for pth in os.listdir(out):
    pth = os.path.join(out, pth)
    if os.path.exists(pth) and not os.listdir(pth):
        print(pth)
        os.rmdir(pth)

if True:
    res = []
    for zsid,sst in slt:
        if zsid:
            if zsid in zid:
                data = zid[zsid]
            else:
                res.append('NA\tNA')
                continue
        else:
            if res[-1].startswith('NA'):
                res.append('NA\tNA')
                continue
        tmp = [(abs(sst - x[0]), x[0], x[1]) for x in data]
        tmp.sort(key = lambda x:x[0])
        tmp = tmp[0]
        if tmp[0].total_seconds() > 3600*24*5:
            res.append(datetime.strftime(tmp[1],'%Y/%m/%d') + '\tNA')
            continue
        res.append(datetime.strftime(tmp[1],'%Y/%m/%d') + '\t1')
    pyperclip.copy('\n'.join(res))
