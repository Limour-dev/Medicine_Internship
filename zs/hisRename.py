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

path1 = r'C:\Users\limou\Downloads\icis\ICIs_Hematocrit.TSV'
cases = []
with open(path1, 'r', encoding='gbk') as rf:
    h = next(rf).split('\t')
    i_id = re_find(h, 'ZSID')
    i_mri_t = re_find(h, 'Study date')
    for line in rf:
        line = line.strip()
        tmp = line.split('\t')
        case = Case()
        case.ID = tmp[i_id]
        case.mri_t = datetime.strptime(tmp[i_mri_t],'%Y/%m/%d')
        cases.append(case)

for _i, _case in enumerate(cases):
    path2 = r'C:\Users\limou\Downloads\icis\ICI-history' + os.path.sep
    os.rename(path2 + _case.ID + '.txt', path2 + f'{_i + 1}_{_case.ID}.txt')