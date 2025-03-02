import os, json, re
from datetime import datetime

re_em_t = re.compile(r'^检验:(\d\d\.\d\d\.\d\d)\s(.*)')

def re_find(_l, _r):
    r = re.compile(_r)
    for i, _i in enumerate(_l):
        if r.search(_i):
            return i
    return 0

def sp_fix(_l, _n):
    res = []
    cache = []
    cache_str = []
    for item in _l:
        item = item.split('\t')
        if len(item) >= _n:
            res.append(item)
        else:
            if len(cache) + len(item) >= _n:
                cache_str.append(item[0])
                item[0] = ';'.join(cache_str)
                cache.extend(item)

                res.append(cache)
                cache = []
                cache_str = []
            else:
                cache_str.append(item.pop())
                cache.extend(item)
    return res

def try_get(_l, _i):
    for _ in range(-1, _i):
        try:
            return _l[_i]
        except IndexError:
            _i -= 1
    return 'NA'

def p_v(_v):
    data = _v.split('\n', maxsplit=1)
    header = data[0].split('\t')
    i_name = re_find(header, r'(项目|细菌名称)')
    i_value = re_find(header, r'(结果|测值)')
    i_ref = re_find(header, r'参考值')
    i_unit = re_find(header, r'(单位|菌落计数)')
    data = sp_fix(data[1].split('\n'), len(header))
    res = []
    for _item in data:
        # print(item)
        name = try_get(_item, i_name)
        value = try_get(_item, i_value)
        ref = try_get(_item, i_ref)
        unit = try_get(_item, i_unit)
        values = (name, value, ref, unit)
        res.append(values)
    return res

path1 = r'E:\Cases\pericardial-mesothelioma'
oCsv = 'ID,时间,来源,项目,结果,参考值,单位\n'
for case in os.listdir(path1):
    path2 = os.path.join(path1, case)
    if not os.path.isdir(path2):
        continue

    with open(os.path.join(path2, '急诊检验报告.json'), 'r', encoding='utf-8') as rf:
        rd = json.load(rf)
    for item in rd:
        k = item['key']
        tb = re_em_t.findall(k)[0]
        i_time = datetime.strptime(tb[0], "%y.%m.%d")
        v = item['value']
        k:str = tb[1].replace(',', '，')
        k = k.split('-', maxsplit=1)[0].strip()

        for values in p_v(v):
            line = f'{case},{i_time},{k},'
            line += ','.join(x.replace(',', '，') for x in values)
            oCsv += line + '\n'

    with open(os.path.join(path2, '住院检验报告.json'), 'r', encoding='utf-8') as rf:
        rd = json.load(rf)
    for item in rd:
        k = item['key']
        tb = k.split('\t')
        i_time = datetime.strptime(tb[0], '%Y-%m-%d %H:%M')
        v = item['value']
        k = tb[1].replace(',', '，')
        k = k.split('-', maxsplit=1)[0].strip()
        for values in p_v(v):
            line = f'{case},{i_time},{k},'
            line += ','.join(x.replace(',', '，') for x in values)
            oCsv += line + '\n'

oCsv = oCsv.replace(' ', ' ')
with open(os.path.join(path1, '检验结果.csv'), 'w', encoding='gbk') as wf:
    wf.write(oCsv)