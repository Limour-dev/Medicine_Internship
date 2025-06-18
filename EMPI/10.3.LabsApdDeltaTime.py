if True:
    import pyperclip
    from datetime import datetime

if True:
    input('任意键粘贴ZSID和时间...')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(nfs[0], nfs[-1], sep='\n')
    alls = {}
    i_id = 0
    i_mri_t = -1
    for line in nfs:
        line = line.strip()
        tmp = line.split('\t')

        zsid = tmp[i_id]
        time = datetime.strptime(tmp[i_mri_t],'%Y/%m/%d %H:%M')
        alls[zsid] = time


if True:
    input('任意键粘贴Labs...')
    nfs = pyperclip.paste().strip().splitlines()
    print(nfs[0], nfs[1], nfs[-1], sep='\n')
    labs = {}
    nfs[0] = '经历天数\t' + nfs[0]
    i = 1
    for i in range(i,len(nfs)):
        tmp = nfs[i].split('\t', maxsplit=2)
        zsid = tmp[0].strip()
        time = tmp[1].strip()
        time = datetime.strptime(time, r'%Y/%m/%d %H:%M')
        delta = time - alls[zsid]
        delta = delta.total_seconds() / 3600 / 24
        if 0.05 > delta > -0.05:
            delta = 0
        else:
            delta = round(delta, 1)
        nfs[i] = f'{delta}\t' + nfs[i]

pyperclip.copy('\n'.join(nfs))
