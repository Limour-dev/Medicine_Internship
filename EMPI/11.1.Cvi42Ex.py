if True:
    import pyperclip
    import os, json, re
    from datetime import datetime
    pt1 = input('输入CVI_TSV路径:')

    reg_zid = re.compile(r'([Zz][Ss]\d+?)([（(].+?[）)])?\s*\.txt')
    reg_sdt = re.compile(r'^[\t ]*Study Date\t(\d+/\d+/\d+)', re.MULTILINE)

    cvi = {}
    for one in os.listdir(pt1):
        zid = reg_zid.findall(one)[0][0].upper()
        with open(os.path.join(pt1, one), 'r', encoding='GB18030') as rf:
            data = rf.read()
        if zid in cvi:
            dtn = reg_sdt.findall(data)[0]
            dtl = reg_sdt.findall(cvi[zid])[0]
            dtn = datetime.strptime(dtn,'%m/%d/%Y')
            dtl = datetime.strptime(dtl,'%m/%d/%Y')
            if dtn > dtl:
                cvi[zid] = cvi[zid] + '\n' + data
            else:
                cvi[zid] = data + '\n' + cvi[zid]
        else:
            cvi[zid] = data

    re_v = re.compile(r'\r?\n\t*((?:Segment\s)?\d\d?)\t([^\t]+)\t*', re.MULTILINE + re.IGNORECASE)
    re_v2 = re.compile(r'^[\t ]*([^\t]+)\t+([^\t]+)\t*', re.MULTILINE)


if True:
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste()
    sl = sl.splitlines()

def mergebp(bps):
    res = []
    li = -2
    for i,v in bps:
        if int(i) - li != 1:
            res.append([float(v)])
        else:
            res[-1].append(float(v))
        li = int(i)
    for i in range(len(res)):
        tmp = sum(res[i]) / len(res[i])
        res[i] = f'{tmp:.3f}'
    return res

raise(BaseException("手动模式"))

# nT1
if True:
    re_nt1 = re.compile(r'^[\t ]*Regional\sNative\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_nt1.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# pT1
if True:
    re_pt1 = re.compile(r'^[\t ]*Regional\sCA\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_pt1.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# height weight HR
if True:
    re_hwh = re.compile(r'^[\t ]*(1\d\d\.?\d*)\t(\d\d\d?\.?\d*)\t\t?(\d\d\d?)\t*$', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_hwh.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append('\t'.join(nt1[skip]))

    pyperclip.copy('\n'.join(res))

# LV
if True:
    re_lv = re.compile(r'^[\t ]*(?:(?:LV)|(?:Clinical Results LV)).*(?:\r?\n.*){5}(\r?\nEDV.*(?:\r?\n.*){20})', re.MULTILINE)
    oh = ['EF', 'EDV/H', 'ESV/H', 'SV/H', 'CI']
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_lv.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v2.findall(nt1[skip])
        ov = {k.strip():v for k,v in ov}
        res.append('\t'.join(ov[x] for x in oh))

    pyperclip.copy('\n'.join(res))

# RV
if True:
    re_rv = re.compile(r'^[\t ]*(?:(?:RV)|(?:Clinical Results RV)).*(?:\r?\n.*){4}(\r?\nEDV.*(?:\r?\n.*){14})', re.MULTILINE)
    oh = ['EF', 'EDV/H', 'ESV/H', 'SV/H', 'CI']
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_rv.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v2.findall(nt1[skip])
        ov = {k.strip():v for k,v in ov}
        res.append('\t'.join(ov[x] for x in oh))

    pyperclip.copy('\n'.join(res))


# Myocardial Thickness
if True:
    re_mt = re.compile(r'^[\t ]*SAX 3D LV.+AHA.*(?:\r?\n.*){10}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_mt.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# Global-mean	Global-SD nT1
if True:
    re_gnt1 = re.compile(r'^[\t ]*Native T1.*(?:\r?\n.*){10}\s*Global Myo T1 Across Slices\s*([^\t ]+)\s*±\s*([^\t ]+)', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_gnt1.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append('\t'.join(nt1[skip]))

    pyperclip.copy('\n'.join(res))

# Global-mean	Global-SD pT1
if True:
    re_gpt1 = re.compile(r'^[\t ]*CA T1.*(?:\r?\n.*){10}\s*Global Myo T1 Across Slices\s*([^\t ]+)\s*±\s*([^\t ]+)', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_gpt1.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append('\t'.join(nt1[skip]))

    pyperclip.copy('\n'.join(res))

# nT1 Blood Pool
if True:
    re_nt1bp = re.compile(r'^[\t ]*Regional Native T1 Slice (\d\d?).*(?:\r?\n.*){102}\s*Blood Pool\s+([^\s]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = mergebp(re_nt1bp.findall(cvi[zid]))
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append(nt1[skip])

    pyperclip.copy('\n'.join(res))

# pT1 Blood Pool
if True:
    re_pt1bp = re.compile(r'^[\t ]*Regional CA T1 Slice (\d\d?).*(?:\r?\n.*){102}\s*Blood Pool\s+([^\s]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = mergebp(re_pt1bp.findall(cvi[zid]))
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append(nt1[skip])

    pyperclip.copy('\n'.join(res))

# nT2
if True:
    re_nt2 = re.compile(r'^[\t ]*Regional\sT2\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_nt2.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# Rest (MBF, ml/g/min)
if True:
    re_qprm = re.compile(r'^[\t ]*\"Rest \(MBF, ml/g/min\)\"\s*(?:\r?\n.*){3}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_qprm.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# Rest (MBF, ml/g/min) Territory
if True:
    re_qprmt = re.compile(r'^[\t ]*\"Rest \(MBF, ml/g/min\)\"\s*(?:\r?\n)LAD.+?([\d.]+)\s*(?:\r?\n)RCA.+?([\d.]+)\s*(?:\r?\n)LCx.+?([\d.]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_qprmt.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append('\t'.join(nt1[skip]))

    pyperclip.copy('\n'.join(res))

# Rest rMBF 
if True:
    re_qprrm = re.compile(r'^[\t ]*Rest \(rMBF\)\s*(?:\r?\n.*){3}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_qprrm.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        ov = re_v.findall(nt1[skip])
        res.append('\t'.join(x[1] for x in ov))

    pyperclip.copy('\n'.join(res))

# Rest rMBF Territory
if True:
    re_qprrmt = re.compile(r'^[\t ]*Rest \(rMBF\)\s*(?:\r?\n)LAD.+?([\d.]+)\s*(?:\r?\n)RCA.+?([\d.]+)\s*(?:\r?\n)LCx.+?([\d.]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            nt1 = re_qprrmt.findall(cvi[zid])
        else:
            skip += 1
        print(zid, skip, len(nt1))
        if skip >= len(nt1):
            res.append('')
            continue
        res.append('\t'.join(nt1[skip]))

    pyperclip.copy('\n'.join(res))
