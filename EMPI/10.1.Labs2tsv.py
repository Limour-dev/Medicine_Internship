if True:
    import pyperclip
    import os, json, re
    from datetime import datetime
    pt1 = input('输入GETHSLAB路径:')
    ag_rg = re.compile(r"\('(.+?)', '(.+?)', \('.+?', '.+?', '\d+-\d+-\d+'\)\)")
    def re_find(_l, _r):
        r = re.compile(_r)
        for i, _i in enumerate(_l):
            if r.search(_i):
                return i
        return 0

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
        data = data[1].split('\n')
        res = []
        for _item in data:
            _item = _item.strip().split('\t')
            name = try_get(_item, i_name)
            value = try_get(_item, i_value)
            ref = try_get(_item, i_ref)
            unit = try_get(_item, i_unit)
            values = (name, value, ref, unit)
            res.append(values)
        return res

oTsv = ['ID\t时间\t来源\t项目\t结果\t参考值\t单位']

for case in os.listdir(pt1):
    path2 = os.path.join(pt1, case)
    if not os.path.isdir(path2):
        continue
    print(path2)

    path2s = os.listdir(path2)

    for path3 in path2s:
        path3 = os.path.join(path2, path3)
        with open(path3, 'r', encoding='utf-8') as rf:
            ag = ag_rg.findall(rf.readline())[0]
            i_time = datetime.strptime(ag[0], '%Y-%m-%d %H:%M')
            k = ag[1].split('-', maxsplit=1)[0].strip()
            v = rf.read().strip()
            for values in p_v(v):
                if all(x==values[0] for x in values):
                    continue
                line = f'{case}\t{i_time}\t{k}\t'
                line += '\t'.join(x for x in values)
                oTsv.append(line)
if True:
    pyperclip.copy('\n'.join(oTsv).replace(' ', ' '))


