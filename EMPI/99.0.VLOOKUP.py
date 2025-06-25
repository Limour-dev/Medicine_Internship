if True:
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
if True:
    if rv:
        zs2id = {y[0].strip():y[-1].strip() for y in (x.split('\t') for x in a)}
    else:
        zs2id = {y[-1].strip():y[0].strip() for y in (x.split('\t') for x in a)}
    if ap:
        res = []
        for l in b:
            ls = l.split('\t')
            if ls[-1].strip():
                res.append(l)
            else:
                ls[-1] = zs2id.get(ls[0].strip(), '')
                res.append('\t'.join(ls))
    else:
        res = [zs2id.get(k.strip(), '') for k in b]
    pyperclip.copy('\n'.join(res))
