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

    re_nt1 = re.compile(r'^[\t ]*Regional\sNative\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)
    re_v = re.compile(r'\r?\n\t*(\d\d?)\t([^\t]+)\t*', re.MULTILINE)
    re_pt1 = re.compile(r'^[\t ]*Regional\sCA\sT1\s\(AHA\sSegmentation\)\s*(?:\r?\n.*){2}((?:\r?\n.*){16})', re.MULTILINE)


if True:
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste()
    sl = sl.splitlines()

if True:
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

if True:
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
