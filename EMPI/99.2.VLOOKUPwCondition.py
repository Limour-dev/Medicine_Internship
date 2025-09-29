if True:
    from datetime import datetime
    import pyperclip
    rv = input('任意键后输入表格(r反向)...').lower().strip().startswith('r')
    a = pyperclip.paste().strip()
    a = a.splitlines()[1:]
    if a[-1].count('\t') <= 0:
        a[-1] += '\t'
    print(rv, '\n', a[0], a[-1])


if True:
    ap = input('任意键后输入待查找值(p补充)...').lower().strip().startswith('p')
    b  = pyperclip.paste().strip()
    b = b.splitlines()[1:]
    if ap and b[-1].count('\t') <= 0:
        b[-1] += '\t'
    print(ap,'\n', b[0], b[-1])


def ff_ptime(tstr):
    ffs = [
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%Y/%m/%d',
        '%Y年%m月%d日'
    ]
    for fs in ffs:
        try:
            return datetime.strptime(tstr, fs)
        except ValueError:
            continue
    raise ValueError('ffs')

zsid = {}
for l in a:
    l = l.strip().split('\t')
    if len(l) < 4:
        continue
    l[-2] = ff_ptime(l[-2])
    if l[0] in zsid:
        zsid[l[0]].append((l[-2],l[-1]))
    else:
        zsid[l[0]] = [(l[-2],l[-1])]

if True:
    res = []
    for l in b:
        l = l.strip().split('\t')
        l[-1] = ff_ptime(l[-1])
        if l[0] not in zsid:
            res.append('')
            continue
        tmp = [(abs(x[0] - l[-1]), x[0], x[1]) for x in zsid[l[0]]]
        tmp.sort(key = lambda x:x[0])
        # print(tmp)
        res.append(tmp[0][2])

    pyperclip.copy('\n'.join(res))
    
