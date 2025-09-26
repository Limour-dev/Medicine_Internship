import pyperclip
def get_tb_from_cb():
    input('请粘贴数据：')
    header, body = pyperclip.paste().split('\n', maxsplit=1)
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

res = []
for i in range(167):
    st = 0
    t = data['ischemictime'][i]
    if t >= 1100:
        tp = 100
    else:
        tp = t / 1100 * 100
    st += tp

    t = data['ckmb'][i]
    if t >= 90:
        tp = 82.5
    else:
        tp = t / 90 * 82.5
    st += tp

    t = data['myo'][i]
    if t >= 600:
        tp = 40
    else:
        tp = t / 600 * 40
    st += tp

    t = data['rca'][i]
    if t >= 0.5:
        tp = 0
    else:
        tp = 20
    st += tp

    res.append(str(st))

pyperclip.copy('\n'.join(res))