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

# subset
if True:
    res = set()
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        sst = datetime.strptime(tmp[-1], '%Y/%m/%d')

        if zsid:
            if zsid in zid:
                data = zid[zsid]
            else:
                print(tmp, 'skip')
                continue
        else:
            print(tmp, 'skip')
            continue
        tmp = [(abs(sst - x[0]), x[0], x[1]) for x in data]
        tmp.sort(key = lambda x:x[0])
        tmp = tmp[0]
        if tmp[0].total_seconds() > 3600*24*5:
            print(tmp, 'skip')
            continue
        res.add(tmp[2] + '\\')

    pyperclip.copy('\r\n'.join(res))



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


# re_draw
pth_rep = input('输入重画文件夹路径:')
for pths in zid.values():
    for t,pth in pths:
        pth2 = os.path.join(pth_rep, os.path.split(pth)[-1])
        if not os.path.exists(pth):
            continue
        pth1 = os.path.join(pth, 'Python_post_processing', 'results')
        pth2 = os.path.join(pth2, 'Python_post_processing', 'session')
        # print(pth1, pth2)
        tmp = os.listdir(pth1)
        tmp = [f'manual_lv_segmentation_slice_0{x[23:-4]}.npz' for x in tmp if x.startswith('results_montage__slice')]
        for x in tmp:
            pth3 = os.path.join(pth2, x)
            if os.path.exists(pth3):
                print(pth3)
                os.unlink(pth3)

# DTI Ex median
if True:
    def dti_ex_o(pth1):
        with open(pth1, 'r', encoding='utf-8') as rf:
            csv = rf.read()
        csv = csv.splitlines()
        csv = csv[3:10]
        line = []
        for o in csv:
            o = o.strip().split(',')
            if o[0] in {'FA', 'MD'}:
                line.append(o[1])
            else:
                line.append(o[3])
                if o[0] in {'HA'}:
                    line.append(str(float(o[5])-float(o[4])))
        return line
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
        gline = [datetime.strftime(tmp[1],'%Y/%m/%d')]
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_anterior.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_inferior.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_lateral.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_septal.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'results_table.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        res.append('\t'.join(gline))
    pyperclip.copy('\n'.join(res))

# DTI Ex mean
if True:
    def dti_ex_o(pth1):
        with open(pth1, 'r', encoding='utf-8') as rf:
            csv = rf.read()
        csv = csv.splitlines()
        csv = csv[3:10]
        line = []
        for o in csv:
            o = o.strip().split(',')
            line.append(o[1])
            if o[0] in {'HA'}:
                line.append(str(float(o[5])-float(o[4])))
        return line
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
        gline = [datetime.strftime(tmp[1],'%Y/%m/%d')]
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_anterior.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_inferior.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_lateral.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'sectors_tables', 'results_table_sector_septal.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'results_table.csv')
        print(pth)
        gline.extend(dti_ex_o(pth))
        res.append('\t'.join(gline))
    pyperclip.copy('\n'.join(res))

# DTI n_images
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
        gline = [datetime.strftime(tmp[1],'%Y/%m/%d')]
        pth = os.path.join(tmp[-1], 'Python_post_processing', 'results', 'numpy results', 'image_manual_removal_pre.csv')
        with open(pth, 'r', encoding='utf-8') as rf:
            gline.extend(rf.read().strip().split('\t'))
        res.append('\t'.join(gline))
    pyperclip.copy('\n'.join(res))
