if True:
    import pyperclip, re
    rv = input('任意键后输入表格(r反向)...').lower().strip().startswith('r')
    a = pyperclip.paste().strip()
    a = a.splitlines()[1:]
    if a[-1].count('\t') <= 0:
        a[-1] += '\t'
    print(rv, '\n', a[0], a[-1])

reg_zs = re.compile(r'ZS\d{5,}', re.IGNORECASE)
res = {}
for b in a:
    b = reg_zs.findall(b)
    if len(b) != 2:
        continue
    res[b[1].upper()] = b[0].upper()

pyperclip.copy('\n'.join(f'{v}\t{k}' for k,v in res.items()))
