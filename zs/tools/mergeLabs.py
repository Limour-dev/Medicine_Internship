a = r'C:\Users\limou\OneDrive\Documents\IMH_raw\data\time.txt'
alls = []
with open(a, 'r', encoding='utf-8') as rf:
    for line in rf:
        rows = line.split('\t')
        id = rows[0].strip()
        if not id:
            continue
        zsid = rows[1].strip()
        alls.append((id, zsid))

import os

b = r'C:\Users\limou\OneDrive\Documents\IMH_raw\STEMI'

c = r'C:\Users\limou\OneDrive\Documents\IMH_raw\labs'

for one in alls:
    if not os.path.exists(f'{c}\\{one[0]}.json'):
        continue
    if not os.path.exists(f'{b}\\{one[1]}'):
        os.mkdir(f'{b}\\{one[1]}')
    with (open(f'{c}\\{one[0]}.json', 'r', encoding='utf-8') as rf,
          open(f'{b}\\{one[1]}\\住院检验报告_0.json', 'w', encoding='utf-8') as wf):
        wf.write(rf.read())