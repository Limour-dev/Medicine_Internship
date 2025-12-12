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
        b = a.split('_')[-2].strip().upper()
        if b in zid:
            print(b)
            zid[b].append(os.path.join(pts,a))
        else:
            zid[b] = [os.path.join(pts,a)]

    for b in zid.keys():
        c = []
        for a in zid[b]:
            c += [os.path.join(a, x) for x in os.listdir(a)]
        zid[b] = c

    for b in zid.keys():
        for i,a in enumerate(zid[b]):
            sst = datetime.strptime(a.split('_')[-2], '%Y%m%d')
            zid[b][i] = [sst, a]
        zid[b].sort(key=lambda x:x[0])

if True:
    input('任意键粘贴ZSID和时间...')
    sl = pyperclip.paste()
    sl = sl.splitlines()
    print(sl[0], sl[-1])

# DTI
if True:
    res = []
    re_dti = re.compile(r'(ep2d_diff_m2_DTI_Zoomed_\d+_MR)|(dti_10dir_zoomit_b300_\d+_MR)|(ep2d_diff_inline_CCF_C2Pshare_rFOV_\d+_MR)', re.IGNORECASE)
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
        ss = os.listdir(tmp[2])
        ss = [x for x in ss if re_dti.match(x)]
        if not ss:
            res.append(datetime.strftime(tmp[1],'%Y/%m/%d') + '\tNA')
            continue
        for i,d in enumerate(ss):
            c = os.path.join(tmp[2], d)
            n = len(os.listdir(c))
            if d.startswith('ep2d_diff'):
                m = 121
            else:
                m = 210
            ss[i] = [n, n%m == 0, c]
            # print(ss[i])
        ss = [x for x in ss if x[1]]
        if ss:
            res.append(datetime.strftime(tmp[1],'%Y/%m/%d') + f'\t{ss[0][0]}')
        else:
            res.append(datetime.strftime(tmp[1],'%Y/%m/%d') + '\tNULL')
    pyperclip.copy('\n'.join(res))

# all copy
if input('all fastcopy').strip().upper() == 'Y':
    res = []
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        sst = datetime.strptime(tmp[-1], '%Y/%m/%d')
        if zsid:
            if zsid in zid:
                data = zid[zsid]
            else:
                res.append('NA')
                continue
        else:
            if res[-1].startswith('NA'):
                res.append('NA')
                continue
        tmp = [(abs(sst - x[0]), x[0], x[1]) for x in data]
        tmp.sort(key = lambda x:x[0])
        tmp = tmp[0]
        res.append(os.path.split(tmp[2])[0])
    pyperclip.copy('\r\n'.join(x for x in res if x != 'NA'))



# DTI copy
ndtip = input('输入新dti文件夹路径:')
if input('dti fastcopy').strip().upper() == 'Y':
    res = []
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        sst = datetime.strptime(tmp[-1], '%Y/%m/%d')
        if zsid:
            if zsid in zid:
                data = zid[zsid]
            else:
                res.append('NA')
                continue
        else:
            if res[-1].startswith('NA'):
                res.append('NA')
                continue
        tmp = [(abs(sst - x[0]), x[0], x[1]) for x in data]
        tmp.sort(key = lambda x:x[0])
        tmp = tmp[0]
        ss = os.listdir(tmp[2])
        ss = [x for x in ss if re_dti.match(x)]
        if not ss:
            res.append('NA')
            continue
        for i,d in enumerate(ss):
            c = os.path.join(tmp[2], d)
            n = len(os.listdir(c))
            if d.startswith('ep2d_diff'):
                m = 121
            else:
                m = 210
            ss[i] = [n, n%m == 0, os.path.split(tmp[2])[0], zsid, c, tmp[1]]
            # print(ss[i])
        ss = [x for x in ss if x[1]]
        if ss:
            print(ss[0])
            tmp = os.path.split(ss[0][2])[1]
            tmp = tmp.split(ss[0][3], maxsplit=1)[0]
            tmp = tmp.replace(',', '')
            npn = datetime.strftime(ss[0][5],'%Y%m%d') + '_' + tmp + ss[0][3]
            npn = os.path.join(ndtip, npn)
            print(ss[0][4], '-->', npn)
            os.rename(ss[0][4], npn)
        else:
            res.append('NA')
    pyperclip.copy('\r\n'.join(x for x in res if x != 'NA'))
    
