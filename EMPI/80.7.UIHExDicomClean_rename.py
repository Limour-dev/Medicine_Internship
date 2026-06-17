if True:
    from pathlib import Path
    from datetime import datetime
    import pyperclip
    import re

    def ff_ptime(tstr):
        ffs = [
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d %H:%M',
            '%Y/%m/%d',
            '%Y年%m月%d日'
        ]
        tstr = tstr.split(' 星期', maxsplit=1)[0]
        for fs in ffs:
            try:
                return datetime.strptime(tstr, fs)
            except ValueError:
                continue
        raise ValueError('ffs')

if True:
    h = (input('任意键粘贴ID、ZSID和时间...').strip().upper() == 'H')
    sl = pyperclip.paste()
    sl = sl.splitlines()[int(h):]
    print(sl[0], sl[-1])

op = Path(input('请输入目录路径：'))

for one in sl:
    one = one.strip().split('\t')
    if len(one) != 3 or not one[1]:
        continue
    one[-1] = ff_ptime(one[-1])
    print(one)

    sp = list(op.glob(f'*_{one[1]}'))
    if not sp:
        continue
    sp = sp[0]
    new_sp = op / f'{one[0]}_{one[1]}'

    print(sp, '-->', new_sp)
    sp.rename(new_sp)
    
