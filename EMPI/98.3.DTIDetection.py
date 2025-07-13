if True:
    import pyperclip
    import os, re
    from datetime import datetime
    pts = input('输入源文件夹路径:')

    def getmt(fp):
        mtime = os.path.getmtime(fp)
        return datetime.fromtimestamp(mtime)

    zid = {}

    for a in os.listdir(pts):
        pth1 = os.path.join(pts,a)
        b = a.split('_')
        z = b[-1].strip().upper()
        t = b[0]
        if len(t) == 6:
            t = '20' + t
            pth2 = os.path.join(pts, '20' + a)
            os.rename(pth1, pth2)
            pth1 = pth2
        t = datetime.strptime(t, '%Y%m%d')
        if z in zid:
            print(b)
            zid[z].append([t,pth1])
        else:
            zid[z] = [[t,pth1]]


    for b in zid.keys():
        zid[b].sort(key=lambda x:x[0])

if True:
    input('任意键粘贴ZSID和时间...')
    sl = pyperclip.paste()
    sl = sl.splitlines()
    print(sl[0], sl[-1])

if True:
    out = input('输入out文件夹路径:')
    icis = set(x.split('\t')[0].strip().upper() for x in sl)
    icis.remove('')

for z, pths in zid.items():
    if z in icis:
        continue
    for t,pth in pths:
        pth1 = os.path.split(pth)[-1]
        pth1 = os.path.join(out, pth1)
        print(pth, pth1)
        os.rename(pth, pth1)

# DTI
if True:
    res = []
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        sst = datetime.strptime(tmp[-1], '%Y/%m/%d')
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

# re_removal
for pths in zid.values():
    for t,pth in pths:
        pth = os.path.join(pth, 'Python_post_processing', 'session', 'image_manual_removal_post.zip')
        print(pth)
        if os.path.exists(pth):
            print('unlink')
            os.unlink(pth)
