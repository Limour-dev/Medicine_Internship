if True:
    import pyperclip
    import os, json, re
    from datetime import datetime
    pt1 = input('输入CVI_TSV路径:')

    reg_zid = re.compile(r'ZS\d+', re.IGNORECASE)
    reg_sdt = re.compile(r'^[\t ]*Study Date\t(\d+/\d+/\d+)', re.MULTILINE)

    cvi = {}
    for two in os.listdir(pt1):
        two = os.path.join(pt1, two)
        for one in os.listdir(two):
            zid = reg_zid.findall(one)[0].upper()
            with open(os.path.join(two, one), 'r', encoding='GB18030') as rf:
                data = rf.read()
            dtn = reg_sdt.findall(data)[0]
            dtn = datetime.strptime(dtn,'%m/%d/%Y')
            if zid in cvi:
                cvi[zid].append((dtn, data))
                cvi[zid].sort(key=lambda x:x[0])
            else:
                cvi[zid] = [(dtn, data)]

    re_v = re.compile(r'\r?\n\t*((?:Segment\s)?\d\d?)\t([^\t]+)\t*', re.MULTILINE + re.IGNORECASE)
    re_v2 = re.compile(r'^[\t ]*([^\t]+)\t+([^\t]+)\t*', re.MULTILINE)
    

if True:
    input('任意键粘贴ZSID及时间...')
    sl = pyperclip.paste().rstrip()
    sl = sl.splitlines()[1:]
    print(sl[0], sl[-1])

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

def get_zsid_dtn(_line, _dtnf='%Y/%m/%d'):
    zid = _line.split('\t')
    dtn = zid[-1]
    zid = zid[0]
    zid = zid.strip().upper()
    dtn = datetime.strptime(dtn, _dtnf)
    return zid, dtn

day10 = abs(datetime.strptime('11','%d') - datetime.strptime('1','%d'))

def get_skip(_data, _sst, _dtni=0):
    _tmp = [(abs(_sst - x[_dtni]), i) for i,x in enumerate(_data)]
    _tmp.sort(key = lambda x:x[0])
    if _tmp[0][0] < day10:
        return _tmp[0][1]
    else:
        return -1

raise(BaseException("手动模式"))

# height	weight	HR
if True:
    re_hwh = re.compile(r'^[\t ]*(1\d\d\.?\d*)\t(\d\d\d?\.?\d*)\t\t?(\d\d\d?)\t*$', re.MULTILINE)
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_hwh.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1[0])))
    pyperclip.copy('\n'.join(res))

# LV
# EF	EDVi	ESVi	SVi	CI
if True:
    re_lv = re.compile(r'^[\t ]*(?:(?:LV)|(?:Clinical Results LV)).*(?:\r?\n.*){5}(\r?\nEDV.*(?:\r?\n.*){20})', re.MULTILINE)
    oh = ['EF', 'EDV/BSA', 'ESV/BSA', 'SV/BSA', 'CI']
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_lv.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v2.findall(nt1[0].split('\nClinical')[0])
        ov = {k.strip():v for k,v in ov}
        res.append('\t'.join([dtn] + list(ov.get(x, 'NA') for x in oh)))

    pyperclip.copy('\n'.join(res))

# RV
# EF	EDVi	ESVi	SVi	CI
if True:
    re_rv = re.compile(r'^[\t ]*(?:(?:RV)|(?:Clinical Results RV)).*(?:\r?\n.*){4}(\r?\nEDV.*(?:\r?\n.*){14})', re.MULTILINE)
    oh = ['EF', 'EDV/BSA', 'ESV/BSA', 'SV/BSA', 'CI']
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_rv.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v2.findall(nt1[0].split('\nClinical')[0])
        ov = {k.strip():v for k,v in ov}
        res.append('\t'.join([dtn] + list(ov.get(x, 'NA') for x in oh)))

    pyperclip.copy('\n'.join(res))

# Myocardial Thickness
# AHA-1	AHA-2	AHA-3	AHA-4	AHA-5	AHA-6	AHA-7	AHA-8	AHA-9	AHA-10	AHA-11	AHA-12	AHA-13	AHA-14	AHA-15	AHA-16
if True:
    re_mt = re.compile(r'^[\t ]*SAX 3D LV.+AHA.*(?:\r?\n.*){10}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_mt.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# Global Measurements Report
# Basal	Mid	Apical	Global	Basal	Mid	Apical	Global	Basal	Mid	Apical	Global
if True:
    re_gmr = re.compile(r'^[\t ]*Global Measurements Report.*(?:\r?\n.*){6}((?:\r?\n.*){8,}?)\s*?Left Ventricle', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_gmr.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = nt1[0].strip().splitlines()
        ovs = ov[0:4]
        ovl = ov[-4:]
        tmp = []
        # GRS
        for line in ovs:
            line = line.strip().split('\t')
            tmp.append(line[2])
        # GCS
        for line in ovs:
            line = line.strip().split('\t')
            tmp.append(line[3])
        # GLS
        for line in ovl:
            line = line.strip().split('\t')
            tmp.append(line[4])
        res.append('\t'.join([dtn] + tmp))

    pyperclip.copy('\n'.join(res))

# nT1
# AHA-1	AHA-2	AHA-3	AHA-4	AHA-5	AHA-6	AHA-7	AHA-8	AHA-9	AHA-10	AHA-11	AHA-12	AHA-13	AHA-14	AHA-15	AHA-16
if True:
    re_nt1 = re.compile(r'^[\t ]*Regional\sNative\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_nt1.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# Global-mean	Global-SD nT1
if True:
    re_gnt1 = re.compile(r'^[\t ]*Native T1.*(?:\r?\n.*){10}\s*Global Myo T1 Across Slices\s*([^\t ]+)\s*±\s*([^\t ]+)', re.MULTILINE)
    res = []
    for zid in sl:
        zid,dtn = get_zsid_dtn(zid)
        data = cvi[zid]
        skip = get_skip(data, dtn)
        if skip < 0:
            res.append('NA')
            continue
        print(zid, skip)
        nt1 = re_gnt1.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1[0])))

    pyperclip.copy('\n'.join(res))

# pT1
if True:
    re_pt1 = re.compile(r'^[\t ]*Regional\sCA\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_pt1.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# nT1 Blood Pool
if True:
    re_nt1bp = re.compile(r'^[\t ]*Regional Native T1 Slice (\d\d?).*(?:\r?\n.*){102}\s*Blood Pool\s+([^\s]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_nt1bp.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        nt1 = mergebp(nt1)
        res.append('\t'.join([dtn, nt1[0]]))

    pyperclip.copy('\n'.join(res))

# pT1 Blood Pool
if True:
    re_pt1bp = re.compile(r'^[\t ]*Regional CA T1 Slice (\d\d?).*(?:\r?\n.*){102}\s*Blood Pool\s+([^\s]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_pt1bp.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        nt1 = mergebp(nt1)
        res.append('\t'.join([dtn, nt1[0]]))

    pyperclip.copy('\n'.join(res))

# ECV
if True:
    re_pt1 = re.compile(r'^[\t ]*Regional\sECV\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_pt1.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# nT2
if True:
    re_nt2 = re.compile(r'^[\t ]*Regional\sT2\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_nt2.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# Global-mean	Global-SD nT2
if True:
    re_gnt2 = re.compile(r'^[\t ]*Global\sMyocardial\sT2\sOffset.*?(?:\r?\n.*){1}((?:\r?\n.*)+?)\r?\n\t{5,}', re.MULTILINE + re.IGNORECASE)
    re_gnt2fix = re.compile(r'^[\t ]*Global\sMyocardial\sT2.*?(?:\r?\n.*){1}((?:\r?\n.*)+?)\r?\n\t{5,}', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_gnt2.findall(data[skip][1])
        if not nt1:
            nt1 = re_gnt2fix.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        ov = [float(x[1]) for x in ov if x[1].strip('-')]
        m = sum(ov) / len(ov)
        if len(ov) > 1:
            variance = sum((x - m) ** 2 for x in ov) / (len(ov) - 1)
            variance = variance ** 0.5
            res.append('\t'.join([dtn, f'{m:.3f}', f'{variance:.3f}']))
        else:
            res.append('\t'.join([dtn, f'{m:.3f}', 'NA']))

    pyperclip.copy('\n'.join(res))

# Rest (MBF, ml/g/min) Territory
if True:
    re_qprmt = re.compile(r'^[\t ]*\"Rest \(MBF, ml/g/min\)\"\s*(?:\r?\n)LAD.+?([\d.]+)\s*(?:\r?\n)RCA.+?([\d.]+)\s*(?:\r?\n)LCx.+?([\d.]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_qprmt.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1[0])))

    pyperclip.copy('\n'.join(res))

# Rest (MBF, ml/g/min)
if True:
    re_qprm = re.compile(r'^[\t ]*\"Rest \(MBF, ml/g/min\)\"\s*(?:\r?\n.*){3}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_qprm.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))

# Rest rMBF Territory
if True:
    re_qprrmt = re.compile(r'^[\t ]*Rest \(rMBF\)\s*(?:\r?\n)LAD.+?([\d.]+)\s*(?:\r?\n)RCA.+?([\d.]+)\s*(?:\r?\n)LCx.+?([\d.]+)', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_qprrmt.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1[0])))

    pyperclip.copy('\n'.join(res))

# Rest rMBF 
if True:
    re_qprrm = re.compile(r'^[\t ]*Rest \(rMBF\)\s*(?:\r?\n.*){3}((?:\r?\n.*){16})', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_qprrm.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + list(x[1] for x in ov)))

    pyperclip.copy('\n'.join(res))


# LGE
if True:
    re_lge = re.compile(r'^[\t ]*\"?((?:[1234] *,? *)+)\"?\t*(?:\r?\n\t{5,})*\r?\n\t?Myocardial Volume:.*?(?:\r?\n.*){6}\r?\n\t?([^\t]+?)g', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_lge.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1[0])))

    pyperclip.copy('\n'.join(res))

# LGE2
if True:
    re_lge = re.compile(r'Myocardial Volume:.*?(?:\r?\n.*){6}\r?\n\t?([^\t]+?)g', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_lge.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        res.append('\t'.join([dtn] + list(nt1)))

    pyperclip.copy('\n'.join(res))


# Global-mean	Global-SD nT2 fix
if True:
    re_gnt2 = re.compile(r'^[\t ]*Global\sMyocardial\sT2\sOffset.*?(?:\r?\n.*){1}((?:\r?\n.*)+?)\r?\n\t{5,}', re.MULTILINE + re.IGNORECASE)
    re_gnt2fix = re.compile(r'^[\t ]*Global\sMyocardial\sT2.*?(?:\r?\n.*){1}((?:\r?\n.*)+?)\r?\n\t{5,}', re.MULTILINE + re.IGNORECASE)
    res = []
    for zid in sl:
        zid = zid.strip().upper()
        if zid:
            skip = 0
            data = cvi[zid]
        else:
            skip += 1
        print(zid, skip)
        nt1 = re_gnt2.findall(data[skip][1])
        if not nt1:
            nt1 = re_gnt2fix.findall(data[skip][1])
        dtn = datetime.strftime(data[skip][0],'%Y/%m/%d')
        print(dtn, len(nt1))
        if not nt1:
            res.append(dtn)
            continue
        ov = re_v.findall(nt1[0])
        res.append('\t'.join([dtn] + [x[1] for x in ov]))

    pyperclip.copy('\n'.join(res))
