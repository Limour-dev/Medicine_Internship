if True:
    import pyperclip
    import os, json, re
    from datetime import datetime

    def re_find(_l, _r):
        r = re.compile(_r)
        for i, _i in enumerate(_l):
            if r.search(_i):
                return i
        return 0

    class Case:
        ID:str
        mri_t: datetime

    class Lab:
        ID:str
        t: datetime
        r: str
        k: str
        v: str

if True:
    input('任意键粘贴Labs...')
    nfs = pyperclip.paste().strip().splitlines()
    print(nfs[0], nfs[-1], sep='\n')
    labs = {}
    h = nfs[0].split('\t')
    i_id = re_find(h, 'ID')
    i_t = re_find(h, '时间')
    i_r = re_find(h, '参考值')
    i_k = re_find(h, '项目')
    i_v = re_find(h, '结果')
    for line in nfs[1:]:
        line = line.strip()
        tmp = line.split('\t')
        lab = Lab()
        lab.ID = tmp[i_id]
        lab.t = datetime.strptime(tmp[i_t], '%Y/%m/%d %H:%M')
        lab.r = tmp[i_r]
        lab.k = tmp[i_k]
        lab.v = tmp[i_v]
        if lab.ID in labs:
            labs[lab.ID].append(lab)
        else:
            labs[lab.ID] = [lab]

if True:
    input('任意键粘贴ZSID和时间...')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(nfs[0], nfs[-1], sep='\n')
    cases = []
    i_id = 0
    i_mri_t = -1
    for line in nfs:
        line = line.strip()
        tmp = line.split('\t')
        case = Case()
        case.ID = tmp[i_id]
        case.mri_t = datetime.strptime(tmp[i_mri_t],'%Y/%m/%d')
        cases.append(case)

for k,v in labs.items():
    labs[k] = sorted(v, key=lambda x:x.t)

res = []

for _case in cases:
    if _case.ID not in labs:
        res.append('#\t#')
        continue
    c_labs = labs[_case.ID]
    print(_case.ID)
    _line = []
    for _lab in c_labs:
        if _lab.k in {'红细胞压积'}:
            _delta_t = abs((_case.mri_t - _lab.t).days)
            _line.append((_delta_t, _lab.t, _lab.v.strip(' 复')))
    _line = sorted(_line, key=lambda x: x[0])
    if _line:
        res.append(f'{_line[0][1]}\t{_line[0][-1]}')
    else:
        res.append('#\t#')
pyperclip.copy('\n'.join(res))
