try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

def get_tb_from_cb():
    header, body = get_clipboard_text().split('\n', maxsplit=1)
    header = {i:n.strip().lower() for i,n in enumerate(header.split('\t'))}
    res = {n:[] for n in header.values()}
    for line in body.splitlines():
        for i,v in enumerate(line.split('\t')):
            v = v.strip()
            try:
                v = float(v)
            except ValueError:
                pass
            res[header[i]].append(v)
    return res

data = get_tb_from_cb()

def s1(vp):
    if vp < 1:
        return 0
    elif vp < 26:
        return 1
    elif vp < 51:
        return 2
    elif vp < 76:
        return 4
    elif vp < 91:
        return 8
    elif vp < 100:
        return 16
    else:
        return 32

res = []
for i in range(167):
    pt = 5 * s1(data['lm'][i])
    pt += (2.5 * s1(data['ladp'][i]))
    pt += (1.5 * s1(data['ladm'][i]))
    pt += (1 * s1(data['lada'][i]))
    pt += (1 * s1(data['d1'][i]))
    pt += (1 * s1(data['rcap'][i]))
    pt += (1 * s1(data['rcam'][i]))
    pt += (1 * s1(data['rcad'][i]))
    if data['dominance'] == 'L':
        pt += (3.5 * s1(data['lcxp'][i]))
        pt += (2 * s1(data['lcxm'][i]))
        pt += (2 * s1(data['lcxd'][i]))
    else:
        pt += (2.5 * s1(data['lcxp'][i]))
        pt += (1 * s1(data['lcxm'][i]))
        pt += (1 * s1(data['lcxd'][i]))
    res.append(str(pt))
set_clipboard_text('\n'.join(res))