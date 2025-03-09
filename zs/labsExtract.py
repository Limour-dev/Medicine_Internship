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
    ici_s: datetime
    ici_e: datetime
    hor_s: datetime

path1 = r'C:\Users\limou\Downloads\icis\ICIs.CSV'
cases = []
with open(path1, 'r', encoding='gbk') as rf:
    h = next(rf).split(',')
    i_id = re_find(h, 'ID')
    i_ici_s = re_find(h, 'ICI用药开始')
    i_ici_e = re_find(h, 'ICI用药结束')
    i_hor_s = re_find(h, '激素治疗开始')
    for line in rf:
        line = line.strip()
        tmp = line.split(',')
        case = Case()
        case.ID = tmp[i_id]
        if tmp[i_ici_s] == '#':
            case.ici_s = datetime.now()
            case.ici_e = datetime.now()
        else:
            case.ici_s = datetime.strptime(tmp[i_ici_s],'%Y/%m/%d')
            case.ici_e = datetime.strptime(tmp[i_ici_e], '%Y/%m/%d')
        if tmp[i_hor_s] == '#':
            case.hor_s = datetime.now()
        else:
            case.hor_s = datetime.strptime(tmp[i_hor_s], '%Y/%m/%d')
        cases.append(case)

class Lab:
    ID:str
    t: datetime
    r: str
    k: str
    v: str

path1 = r'C:\Users\limou\Downloads\icis\cases\检验结果.csv'
labs = {}
with open(path1, 'r', encoding='gbk') as rf:
    h = next(rf).split(',')
    i_id = re_find(h, 'ID')
    i_t = re_find(h, '时间')
    i_r = re_find(h, '参考值')
    i_k = re_find(h, '项目')
    i_v = re_find(h, '结果')
    for line in rf:
        line = line.strip()
        tmp = line.split(',')
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

for k,v in labs.items():
    labs[k] = sorted(v, key=lambda x:x.t)

from clipboard import set_clipboard_text

def extract(key):
    res = []
    for _case in cases:
        c_labs = labs[_case.ID]
        _line = []
        for _lab in c_labs:
            if key(_lab, _case):
                _line.append(_lab.v.strip(' 复'))
        res.append(','.join(_line))
    set_clipboard_text('\n'.join(res))

del lab, case, line

if False:
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'心肌肌钙蛋白T'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肌酸激酶', '肌酸激酶（急）'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肌酸激酶MB亚型'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肌酸激酶MM亚型'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肌酸激酶MB质量'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肌红蛋白'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'氨基末端利钠肽前体'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'cTnI定量测定'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白细胞计数'} and _lab.r == '3.50 -- 9.50')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'中性粒细胞百分比'} and _lab.r == '40.0 -- 75.0')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'淋巴细胞百分比'} and _lab.r == '20.0 -- 50.0')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'单核细胞百分比'} and _lab.r == '3.0 -- 10.0')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'嗜酸性粒细胞百分比'} and _lab.r == '0.4 -- 8.0')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'嗜碱性粒细胞百分比'} and _lab.r == '0.0 -- 1.0')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'中性粒细胞数'} and _lab.r == '1.8 -- 6.3')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'淋巴细胞数'} and _lab.r == '1.1 -- 3.2')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'单核细胞数'} and _lab.r == '0.1 -- 0.6')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'嗜酸性粒细胞数'} and _lab.r == '0.02 -- 0.52')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'嗜碱性粒细胞数'} and _lab.r == '0.00 -- 0.06')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'凝血酶原时间'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'国际标准化比值'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'D-二聚体'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'高敏感C反应蛋白'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'降钙素原'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'B淋巴细胞 CD19'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'T淋巴细胞 CD3'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'Th淋巴细胞 CD4'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'Ts淋巴细胞 CD8'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'CD4/CD8'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'自然杀伤细胞(CD56+16)'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'淋巴细胞数'} and _lab.r == '')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'B淋巴细胞绝对计数'} and _lab.r == '92 - 498')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'T淋巴细胞绝对计数'} and _lab.r == '834 - 2217')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'Th淋巴细胞绝对计数'} and _lab.r == '395 - 1264')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'Ts淋巴细胞绝对计数'} and _lab.r == '269 - 1059')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'自然杀伤细胞绝对计数'} and _lab.r == '136 - 880')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'总胆固醇'} and _lab.r == '适宜 <5.20;增高 5.20--6.20;很高 >6.20')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'甘油三酯'} and _lab.r == '适宜 <1.70;增高 1.70--2.30;很高 >2.30')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'低密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'高密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'载脂蛋白A-I'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'载脂蛋白B'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'载脂蛋白E'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'脂蛋白(a)'} and _lab.r == '0 -- 75')
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'肿瘤坏死因子'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白介素1β'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白介素2受体'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白介素6'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白介素8'})
    extract(lambda _lab,_case: _lab.t < _case.ici_s and _lab.k in {'白介素10'})

if False:
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'心肌肌钙蛋白T'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肌酸激酶', '肌酸激酶（急）'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肌酸激酶MB亚型'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肌酸激酶MM亚型'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肌酸激酶MB质量'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肌红蛋白'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'氨基末端利钠肽前体'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'cTnI定量测定'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白细胞计数'} and _lab.r == '3.50 -- 9.50')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'中性粒细胞百分比'} and _lab.r == '40.0 -- 75.0')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'淋巴细胞百分比'} and _lab.r == '20.0 -- 50.0')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'单核细胞百分比'} and _lab.r == '3.0 -- 10.0')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'嗜酸性粒细胞百分比'} and _lab.r == '0.4 -- 8.0')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'嗜碱性粒细胞百分比'} and _lab.r == '0.0 -- 1.0')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'中性粒细胞数'} and _lab.r == '1.8 -- 6.3')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'淋巴细胞数'} and _lab.r == '1.1 -- 3.2')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'单核细胞数'} and _lab.r == '0.1 -- 0.6')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'嗜酸性粒细胞数'} and _lab.r == '0.02 -- 0.52')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'嗜碱性粒细胞数'} and _lab.r == '0.00 -- 0.06')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'凝血酶原时间'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'国际标准化比值'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'D-二聚体'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'高敏感C反应蛋白'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'降钙素原'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'B淋巴细胞 CD19'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'T淋巴细胞 CD3'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'Th淋巴细胞 CD4'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'Ts淋巴细胞 CD8'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'CD4/CD8'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'自然杀伤细胞(CD56+16)'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'淋巴细胞数'} and _lab.r == '')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'B淋巴细胞绝对计数'} and _lab.r == '92 - 498')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'T淋巴细胞绝对计数'} and _lab.r == '834 - 2217')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'Th淋巴细胞绝对计数'} and _lab.r == '395 - 1264')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'Ts淋巴细胞绝对计数'} and _lab.r == '269 - 1059')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'自然杀伤细胞绝对计数'} and _lab.r == '136 - 880')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'总胆固醇'} and _lab.r == '适宜 <5.20;增高 5.20--6.20;很高 >6.20')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'甘油三酯'} and _lab.r == '适宜 <1.70;增高 1.70--2.30;很高 >2.30')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'低密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'高密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'载脂蛋白A-I'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'载脂蛋白B'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'载脂蛋白E'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'脂蛋白(a)'} and _lab.r == '0 -- 75')
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'肿瘤坏死因子'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白介素1β'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白介素2受体'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白介素6'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白介素8'})
    extract(lambda _lab,_case: _case.ici_s <= _lab.t <= _case.hor_s and _lab.k in {'白介素10'})

if False:
    extract(lambda _lab,_case: _case.hor_s < _lab.t  and _lab.k in {'心肌肌钙蛋白T'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肌酸激酶', '肌酸激酶（急）'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肌酸激酶MB亚型'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肌酸激酶MM亚型'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肌酸激酶MB质量'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肌红蛋白'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'氨基末端利钠肽前体'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'cTnI定量测定'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白细胞计数'} and _lab.r == '3.50 -- 9.50')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'中性粒细胞百分比'} and _lab.r == '40.0 -- 75.0')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'淋巴细胞百分比'} and _lab.r == '20.0 -- 50.0')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'单核细胞百分比'} and _lab.r == '3.0 -- 10.0')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'嗜酸性粒细胞百分比'} and _lab.r == '0.4 -- 8.0')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'嗜碱性粒细胞百分比'} and _lab.r == '0.0 -- 1.0')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'中性粒细胞数'} and _lab.r == '1.8 -- 6.3')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'淋巴细胞数'} and _lab.r == '1.1 -- 3.2')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'单核细胞数'} and _lab.r == '0.1 -- 0.6')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'嗜酸性粒细胞数'} and _lab.r == '0.02 -- 0.52')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'嗜碱性粒细胞数'} and _lab.r == '0.00 -- 0.06')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'凝血酶原时间'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'国际标准化比值'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'D-二聚体'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'高敏感C反应蛋白'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'降钙素原'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'B淋巴细胞 CD19'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'T淋巴细胞 CD3'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'Th淋巴细胞 CD4'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'Ts淋巴细胞 CD8'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'CD4/CD8'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'自然杀伤细胞(CD56+16)'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'淋巴细胞数'} and _lab.r == '')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'B淋巴细胞绝对计数'} and _lab.r == '92 - 498')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'T淋巴细胞绝对计数'} and _lab.r == '834 - 2217')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'Th淋巴细胞绝对计数'} and _lab.r == '395 - 1264')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'Ts淋巴细胞绝对计数'} and _lab.r == '269 - 1059')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'自然杀伤细胞绝对计数'} and _lab.r == '136 - 880')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'总胆固醇'} and _lab.r == '适宜 <5.20;增高 5.20--6.20;很高 >6.20')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'甘油三酯'} and _lab.r == '适宜 <1.70;增高 1.70--2.30;很高 >2.30')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'低密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'高密度脂蛋白胆固醇'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'载脂蛋白A-I'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'载脂蛋白B'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'载脂蛋白E'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'脂蛋白(a)'} and _lab.r == '0 -- 75')
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'肿瘤坏死因子'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白介素1β'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白介素2受体'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白介素6'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白介素8'})
    extract(lambda _lab,_case: _case.hor_s < _lab.t and _lab.k in {'白介素10'})