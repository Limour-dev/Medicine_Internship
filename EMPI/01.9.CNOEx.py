import pyperclip
import os
import re


def re_find(_l, _r):
    if type(_r) is str:
        r = re.compile(_r)
    else:
        r = _r
    for i, _i in enumerate(_l):
        if r.search(_i):
            return i
    return 0


pt1 = input('输入ZSIDCNO路径:')
res = {}

reg_zsid = re.compile(r'ZS\d{5,}', re.IGNORECASE)

for one in os.listdir(pt1):
    header = ''
    body = []
    with open(os.path.join(pt1, one), 'r', encoding='GB18030') as rf:
        header = next(rf).strip()
        print(one, header)
        body.extend(rf.readlines())
    header = header.split('\t')

    body = [x.split('\t') for x in body]

    i_zsid = re_find(header, '医技号')
    i_exid = re_find(header, '检查序号')
    assert i_zsid < i_exid
    i_cno_1 = re_find(header, '卡号')
    i_cno_2 = re_find(header, '住院号')

    for line in body:
        i_fuck = re_find(line, reg_zsid) - i_zsid
        zsid = line[i_zsid + i_fuck]
        con_1 = line[i_cno_1 + i_fuck]
        con_2 = line[i_cno_2 + i_fuck]
        if line[i_zsid] in res:
            res[line[i_zsid]].add(con_1)
            res[line[i_zsid]].add(con_2)
        else:
            res[zsid] = {con_1, con_2}

res_l = []
for k, v in res.items():
    v = [x for x in v if len(x) > 3]
    if not v:
        continue
    res_l.append(f'{k}\t{v[0]}')

pyperclip.copy('\n'.join(res_l))