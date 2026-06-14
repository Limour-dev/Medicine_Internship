if True:
    import pyperclip
    import pathlib
    from datetime import datetime
    import re

    from bs4 import BeautifulSoup

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        return _v



empip = pathlib.Path(input('EMPI路径：'))

dirs = [p for p in empip.iterdir() if p.is_dir()]
dirs.sort(key=lambda x:int(x.name))

res = [''] * len(dirs)

reg_exam_id = re.compile(r'ris_exam_id=(ZS\d+)')

def idirs_sort_key(x):
    s = x.name.split('_')[0]
    s = '20' + s
    return datetime.strptime(s, r'%Y.%m.%d')

for i,zsi in enumerate(dirs):
    print(i, zsi)
    idirs = [p for p in zsi.rglob('*MRI*')]
    idirs.sort(key=idirs_sort_key, reverse=True)
    
    for mri in idirs:
        mri = mri.read_text(encoding='utf-8')
        d_exam_id = reg_exam_id.findall(mri)[0]
        d_s = BeautifulSoup(mri)
        d_jcmc = clear_value(d_s.select_one("#label22").text)
        if "MRCP" not in d_jcmc:
            if d_jcmc not in {"肝脏平扫+DWI+增强(普美显)"}:
                continue
        d_jl = clear_value(d_s.select_one("#label11").text)
        if '术后' in d_jl:
            continue
        if '术区' in d_jl:
            continue
        if '治疗后' in d_jl:
            continue
        if '根治性' in d_jl:
            continue
        d_xm = d_s.select_one("#label1").text
        d_zs = d_s.select_one("#label7").text
        d_rq = d_s.select_one("#label8").text

        res[i] = f"{d_rq}\t{d_xm}\t{d_zs}\t{d_exam_id}\t{d_jl}"
        break

for i,tmp in enumerate(res):
    if tmp:
        continue
    zsi = dirs[i]
    print(i, zsi)
    
    idirs = [p for p in zsi.rglob('*MRI*')]
    idirs.sort(key=idirs_sort_key)

    if not idirs:
        res[i] = 'NA'
        continue

    for mri in idirs:
        mri = mri.read_text(encoding='utf-8')
        d_exam_id = reg_exam_id.findall(mri)[0]
        d_s = BeautifulSoup(mri)
        d_jcmc = clear_value(d_s.select_one("#label22").text)
        if "MRCP" not in d_jcmc:
            if d_jcmc not in {"肝脏平扫+DWI+增强(普美显)"}:
                continue
        d_jl = clear_value(d_s.select_one("#label11").text)
        d_xm = d_s.select_one("#label1").text
        d_zs = d_s.select_one("#label7").text
        d_rq = d_s.select_one("#label8").text

        res[i] = f"{d_rq}\t{d_xm}\t{d_zs}\t{d_exam_id}\t{d_jl}"
        break
    
pyperclip.copy('\n'.join(res))
