if True:
    from pathlib import Path
    from datetime import datetime
    from collections import defaultdict
    import os
    import re
    import pyperclip

    ZS_RE = re.compile(r'_(ZS\d+)')

    def ff_ptime(tstr):
        ffs = [
            '%Y-%m-%d',
            '%Y%m%d',
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d %H:%M',
            '%Y/%m/%d',
            '%Y年%m月%d日',
        ]
        tstr = tstr.split(' 星期', maxsplit=1)[0]
        for fs in ffs:
            try:
                return datetime.strptime(tstr, fs)
            except ValueError:
                continue
        raise ValueError('ffs')

    def try_ptime(s):
        try:
            return ff_ptime(s)
        except ValueError:
            return None

    def ff_id(s):
        # 5 -> 005；非纯数字原样保留
        s = s.strip()
        return f'{int(s):03d}' if s.isdigit() else s

if True:
    h = (input('任意键粘贴ID、ZSID和时间...').strip().upper() == 'H')
    sl = pyperclip.paste()
    sl = sl.splitlines()[int(h):]
    print(sl[0], sl[-1])

# 解析输入：ZSID -> [(ID, 时间), ...]
zs_map = defaultdict(list)
for one in sl:
    one = one.strip().split('\t')
    if len(one) != 3 or not one[1]:
        continue
    one[-1] = ff_ptime(one[-1])
    zs_map[one[1]].append((one[0], one[-1]))

if True:
    # 找出同一 ZSID 出现多次（>1 条记录）的项
    dup = {k: v for k, v in zs_map.items() if len(v) > 1}
    print(f'重复 ZSID 数：{len(dup)} / 总 ZSID 数：{len(zs_map)}')
    for k, v in sorted(dup.items(), key=lambda kv: -len(kv[1])):
        print(f'{k}  x{len(v)}')
        for cid, t in sorted(v, key=lambda x: x[1]):
            print(f'    {ff_id(cid):>5}  {t:%Y-%m-%d}')


op = Path(input('请输入目录路径：'))

newop = Path(input('请输入另存目录路径：'))

# 确定日期目录列表：op 本身是日期目录，还是 rootpath
if try_ptime(op.name) is not None:
    date_dirs = [op]
else:
    date_dirs = []
    with os.scandir(op) as it:
        for e in it:
            if e.is_dir(follow_symlinks=False) and try_ptime(e.name) is not None:
                date_dirs.append(Path(e.path))

for dd in date_dirs:
    d = ff_ptime(dd.name)
    with os.scandir(dd) as it:
        for e in it:
            # 只处理直接子项，不递归；按需只要目录
            if not e.is_dir(follow_symlinks=False):
                continue
            m = ZS_RE.search(e.name)
            if not m:
                continue
            zsid = m.group(1)
            cands = zs_map.get(zsid)
            if not cands:
                continue

            # 时间最接近该日期目录的那条记录
            cid, _ = min(cands, key=lambda x: abs((x[1] - d).total_seconds()))
            new_name = f'{ff_id(cid)}_{zsid}'

            sp = Path(e.path)
            new_sp = newop / new_name

            print(sp, '-->', new_sp)
            sp.rename(new_sp)
