import json
from datetime import datetime
import pyperclip

with open('res.json', 'r', encoding='utf-8') as rf:
    res = json.load(rf)

if True:
    input('任意键粘贴数据...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]



def get_bd_p(line, sl_i):
    ls = line.split('\t')
    zsid = ls[1]
    bd_p = ls[7]
    et = ls[19]
    et_t = datetime.strptime(et, r"%Y-%m-%d %H:%M")
    ot, zid = sl_i.strip().split('\t')
    try:
        ot_t = datetime.strptime(ot, r"%Y/%m/%d %H:%M")
    except:
        ot_t = datetime.strptime(ot, r"%Y/%m/%d")
    delta = ot_t - et_t
    delta = round(delta.total_seconds() / 3600 / 24, 1)
    if zsid != zid or bd_p != '腹部':
        return -999, '(null)\t(null)\t(null)\t(null)\t(null)'
    return delta,f'{ls[1]}\t{ls[2]}\t{ls[7]}\t{ls[19]}\t{ls[23]}'
    

rres = []
for i in range(len(rres), len(res)):
    l = res[i]
    if len(l) <=0 :
        rres.append('(null)\t(null)\t(null)\t(null)\t(null)')
        continue
    if len(l) ==1:
        ls = l[0].split('\t')
        if ls[1] == sl[i].split('\t')[-1] and ls[7] == '腹部':
            rres.append(f'{ls[1]}\t{ls[2]}\t{ls[7]}\t{ls[19]}\t{ls[23]}')
        else:
            rres.append('(null)\t(null)\t(null)\t(null)\t(null)')
        continue
    l = [get_bd_p(ll, sl[i]) for ll in l]
    l = [ll for ll in l if ll[0] > 0]
    l.sort(key=lambda x:x[0])
    if len(l) > 0:
        rres.append(l[0][-1])
    else:
        rres.append('(null)\t(null)\t(null)\t(null)\t(null)')

pyperclip.copy('\n'.join(rres))
