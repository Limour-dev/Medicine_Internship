if True:
    import pyperclip
    import re
    ag_rg = re.compile(r'InstrID=([^&]+)&SampleNo=([^&]+)&SampleTime=([^ ]+) ')
    input('任意键粘贴LabSummary...')
    nfs = pyperclip.paste().strip().splitlines()
    print(nfs[0], nfs[-1], sep='\n')

res = []
for nf in nfs:
    nf = nf.strip()
    if not nf:
        res.append(nf)
        continue
    res_i = set()
    for op in nf.split('|@|'):
        tm, tt, ag = op.split('|')
        ag = ag_rg.findall(ag)[0]
        sd = ag[2].replace('/', '-')
        res_i.add(f'{tm}|{tt}|{ag[0]}|{ag[1]}|{sd}')
    res_i = '|@|'.join(res_i)
    # assert len(res_i) < 30000
    res.append(res_i)
pyperclip.copy('\n'.join(res))
