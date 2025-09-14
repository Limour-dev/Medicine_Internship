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

def ff_ptime(tstr):
    ffs = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%Y年%m月%d日'
    ]
    for fs in ffs:
        try:
            return datetime.strptime(tstr, fs)
        except ValueError:
            continue
    raise ValueError('ffs')

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
    i_t = re_find(h, '时间')
    
    for line in nfs[1:]:
        line = line.strip()
        tmp = line.split('\t')
        case = Case()

        case.ID = tmp[i_id]
        case.t = ff_ptime(tmp[i_t])

        cases.append(case)

    print(len(cases),  cases[0].ID,  cases[-1].ID)


def extract(key, new_name):
    res = []
    for aaa,_case in enumerate(cases):
        if _case.ID not in labs:
            res.append('NA')
            continue
        c_labs = labs[_case.ID]
        # print(_case.ID)
        _line = []
        for _lab in c_labs:
            if key(_lab, _case):
                # print(_lab.k, _lab.v)
                # _lab.k = new_name
                _lab.v = _lab.v.strip(' 复')
                delta = _lab.t - _case.t
                _lab.dt = delta
                _line.append(_lab)
        _line.sort(key=lambda x:abs(x.dt))
        if not _line:
            res.append('NA')
        else:
            res.append(_line[0].v)
            if aaa % 20 == 0:
                print(_line[0].k, _line[0].v, _line[0].r, _line[0].u)
    return res


pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙肝病毒表面抗原'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙肝病毒表面抗体'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙肝病毒e抗原'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙肝病毒e抗体'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙肝病毒核心抗体'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'乙型肝炎病毒核酸'}, '')))

pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'总蛋白'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'甲胎蛋白'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'糖类抗原19-9'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'癌胚抗原'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'红细胞', '红细胞计数'} and _lab.u in {"X10^12/L"}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'血红蛋白'} and _lab.r in {'130 -- 175', "115 -- 150"}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'红细胞压积'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'平均红细胞体积'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'平均血红蛋白量'}, '')))

pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'平均血红蛋白浓度'}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case: _lab.k in {'血小板计数'} and _lab.u in {"X10^9/L"}, '')))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'白细胞计数'} and _lab.r == '3.5 -- 9.5', "WBC")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'中性粒细胞百分比'} and _lab.r in {'40.0 -- 75.0', '40 -- 75'}, "N%")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'淋巴细胞百分比'} and _lab.r in {'20.0 -- 50.0', '20 -- 50'}, "L%")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'单核细胞百分比'}and _lab.r in {'3.0 -- 10.0', '3.0 -- 10'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'嗜酸性粒细胞百分比'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'嗜碱性粒细胞百分比'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'中性粒细胞数'} and _lab.r in {'1.8 -- 6.3'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'淋巴细胞数'} and _lab.r in {'1.1 -- 3.2'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'单核细胞数'} and _lab.r in {'0.1 -- 0.6'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'嗜酸性粒细胞数'} and _lab.r in {'0.02 -- 0.52'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'嗜碱性粒细胞数'} and _lab.u in {"X10^9/L"}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'红细胞体积分布宽度CV'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'红细胞体积分布宽度SD'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'平均血小板体积'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'血小板压积'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'大血小板比率'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'血小板体积分布宽度'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'直接胆红素'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'总胆红素'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'丙氨酸氨基转移酶'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'γ-谷氨酰转移酶'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'碱性磷酸酶'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'尿酸'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'肌酐'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'葡萄糖'} and _lab.u in {"mmol/L"}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'总胆固醇'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'甘油三酯'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'低密度脂蛋白胆固醇'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'非高密度脂蛋白胆固醇'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'高密度脂蛋白胆固醇'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'脂肪酶'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'淀粉酶', '淀粉酶（急）'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'高敏感C反应蛋白'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'凝血酶原时间'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'国际标准化比值'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'7种微小核糖核酸'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'循环肿瘤细胞'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'甲胎蛋白异质体'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'异常凝血酶原'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'糖类抗原50'}, "")))

pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'透明质酸'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'层粘连蛋白'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'III型前胶原'}, "")))
pyperclip.copy('\n'.join(extract(lambda _lab,_case:  _lab.k in {'IV型胶原'}, "")))

