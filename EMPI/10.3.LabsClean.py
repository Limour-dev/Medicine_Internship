if True:
    import pyperclip
    import os, json, re
    from datetime import datetime

    def re_find(_l, _r):
        r = re.compile(_r, re.IGNORECASE)
        for i, _i in enumerate(_l):
            if r.search(_i):
                return i
        return 0

if True:
    class Lab:
        ID:str
        t: datetime
        r: str
        k: str
        v: str
        u: str

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
    i_u = re_find(h, '单位')
    for line in nfs[1:]:
        line = line.strip()
        tmp = line.split('\t')
        lab = Lab()
        lab.ID = tmp[i_id]
        lab.t = datetime.strptime(tmp[i_t], '%Y/%m/%d %H:%M')
        lab.r = tmp[i_r].strip()
        lab.k = tmp[i_k]
        lab.v = tmp[i_v]
        try:
            lab.u = tmp[i_u].strip()
        except:
            lab.u = '#'
        # print(lab.k, lab.v)
        if lab.ID in labs:
            labs[lab.ID].append(lab)
        else:
            labs[lab.ID] = [lab]

if True:
    class Case:
        ID:str
        t: datetime

    cases = []
    
    input('任意键粘贴cases...')
    nfs = pyperclip.paste().strip().splitlines()
    print(nfs[0], nfs[-1], sep='\n')
    
    h = nfs[0].split('\t')
    
    i_id = re_find(h, 'ID')
    i_t = re_find(h, '_date')
    
    for line in nfs[1:]:
        line = line.strip()
        tmp = line.split('\t')
        case = Case()

        case.ID = tmp[i_id]
        case.t = datetime.strptime(tmp[i_t],'%Y-%m-%d')

        cases.append(case)

    print(len(cases),  cases[0].ID,  cases[-1].ID)


def extract(key, new_name):
    res = []
    for _case in cases:
        if _case.ID not in labs:
            continue
        c_labs = labs[_case.ID]
        # print(_case.ID)
        _line = []
        for _lab in c_labs:
            if key(_lab, _case):
                # print(_lab.k, _lab.v)
                _lab.k = new_name
                _lab.v = _lab.v.strip(' 复')
                # print(_lab.k, _lab.v)
                delta = _lab.t - _case.t
                delta = delta.total_seconds() / 3600 / 24
                _lab.dt = delta
                _line.append(_lab)
        _line.sort(key=lambda x:x.t)
        res.extend(_line)
    return res

if True:
    aa = []
    aa.extend(extract(lambda _lab,_case: _lab.k in {'心肌肌钙蛋白T'}, 'cTnT'))
    aa.extend(extract(lambda _lab,_case: _lab.k in {'肌酸激酶', '肌酸激酶（急）'}, 'CK'))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'肌酸激酶MB亚型'}, "CK-MB_U"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'肌酸激酶MM亚型'}, "CK-MM"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'肌酸激酶MB质量'}, "CK-MB_ng"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'肌红蛋白'}, "Myo"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'氨基末端利钠肽前体'}, "pro-BNP"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'cTnI定量测定'}, "cTnI"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白细胞计数'} and _lab.r == '3.5 -- 9.5', "WBC"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'中性粒细胞百分比'} and _lab.r == '40.0 -- 75.0', "N%"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'淋巴细胞百分比'} and _lab.r == '20.0 -- 50.0', "L%"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'单核细胞百分比'} and _lab.r == '3.0 -- 10.0', "M%"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'嗜酸性粒细胞百分比'} and _lab.r == '0.4 -- 8.0', "E%"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'嗜碱性粒细胞百分比'} and _lab.r == '0.0 -- 1.0', "B%"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'中性粒细胞数'} and _lab.r == '1.8 -- 6.3', "N"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'淋巴细胞数'} and _lab.r == '1.1 -- 3.2', "L"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'单核细胞数'} and _lab.r == '0.1 -- 0.6', "M"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'嗜酸性粒细胞数'} and _lab.r == '0.02 -- 0.52', "E"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'嗜碱性粒细胞数'} and _lab.r == '0.00 -- 0.06', "B"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'凝血酶原时间'}, "PT"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'国际标准化比值'}, "INR"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'D-二聚体'}, "DD"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'高敏感C反应蛋白'}, "hsCRP"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'降钙素原'}, "PCT"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'B淋巴细胞 CD19'}, "CD19+B"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'T淋巴细胞 CD3'}, "CD3+T"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'Th淋巴细胞 CD4'}, "CD4+Th"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'Ts淋巴细胞 CD8'}, "CD8+Ts"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'CD4/CD8'}, "CD4/CD8"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'自然杀伤细胞(CD56+16)'}, "CD56+16+NK"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'淋巴细胞数'} and _lab.r == '' and _lab.u == 'cells/uL', "L_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'B淋巴细胞绝对计数'} and _lab.r == '92 - 498', "B_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'T淋巴细胞绝对计数'} and _lab.r == '834 - 2217', "T_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'Th淋巴细胞绝对计数'} and _lab.r == '395 - 1264', "Th_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'Ts淋巴细胞绝对计数'} and _lab.r == '269 - 1059', "Ts_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'自然杀伤细胞绝对计数'} and _lab.r == '136 - 880', "NK_cells"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'总胆固醇'} and _lab.r == r'3\0n增高 5.20--6.20\1n很高 >6.20\2n适宜 <5.20', "TC"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'甘油三酯'} and _lab.r == r'3\0n增高 1.70--2.30\1n很高 >2.30\2n适宜 <1.70', "TG"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'低密度脂蛋白胆固醇'}, "LDL"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'高密度脂蛋白胆固醇'}, "HDL"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'载脂蛋白A-I'}, "APO-A-I"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'载脂蛋白B'}, "APO-B"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'载脂蛋白E'}, "APO-E"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'脂蛋白(a)'} and _lab.r == '0 -- 75', "Lp-a"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'肿瘤坏死因子'}, "TNF"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白介素1β'}, "IL-1β"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白介素2受体'}, "IL-2R"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白介素6'}, "IL-6"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白介素8'}, "IL-8"))
    aa.extend(extract(lambda _lab,_case:  _lab.k in {'白介素10'}, "IL-10"))
    pyperclip.copy('\n'.join(f'{_lab.ID}\t{_lab.t}\t{_lab.k}\t{_lab.v}\t{_lab.u}\t{_lab.dt}' for _lab in aa))
