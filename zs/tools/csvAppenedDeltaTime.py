from datetime import datetime

a = r'C:\Users\limou\OneDrive\Documents\IMH_raw\data\time.txt'
alls = {}
with open(a, 'r', encoding='utf-8') as rf:
    for line in rf:
        rows = line.split('\t')
        id = rows[0].strip()
        if not id:
            continue
        zsid = rows[1].strip()
        time = datetime.strptime(rows[-1].strip(), "%Y/%m/%d %H:%M")

        alls[zsid] = (id, time)

b = r'C:\Users\limou\OneDrive\Documents\IMH_raw\STEMI\检验结果.csv'

with (open(b, 'r', encoding='GB18030') as rf,
      open('检验结果_deltaT.csv', 'w', encoding='GB18030') as wf):
    tmp = rf.readline()
    tmp = '距PCI天数,' + tmp
    wf.write(tmp)
    for line in rf:
        tmp = line.split(',', maxsplit=2)
        zsid = tmp[0].strip()
        time = tmp[1].strip()
        time = datetime.strptime(time, r'%Y-%m-%d %H:%M:%S')
        delta = time - alls[zsid][1]
        delta = round(delta.total_seconds() / 3600 / 24, 1)
        if 0.1 > delta > -0.1:
            delta = 0
        wf.write(f'{delta},' + line)

