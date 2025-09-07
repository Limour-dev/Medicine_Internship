if True:
    import pyperclip, re
    reg_id = re.compile(r'[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}', re.IGNORECASE)

if True:
    ish = (input('任意键粘贴RIS(h)...').strip().upper() == 'H')
    lrs1 = pyperclip.paste().rstrip().splitlines()[ish:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')

if True:
    input('任意键粘贴RIS2...')
    lrs2 = pyperclip.paste().rstrip().splitlines()
    print(len(lrs2), lrs2[0], lrs2[-1], sep='\n')
    m_l = max(len(lrs1), len(lrs2))
    if len(lrs1) < m_l:
        lrs1 += ['']*(m_l - len(lrs1))
    if len(lrs2) < m_l:
        lrs2 += ['']*(m_l - len(lrs2))
    for i in range(m_l):
        rs2 = lrs2[i].strip()
        if not rs2:
            continue
        rs1 = lrs1[i].strip()
        if rs1:
            lrs1[i] = f'{rs1}|@|{rs2}'
        else:
            lrs1[i] = rs2

if True:
    res = []
    for rs in lrs1:
        rs = rs.strip()
        if not rs:
            res.append('')
            continue
        rss = rs.split('|@|')
        fuck = set()
        res_i = []
        for rso in rss:
            rid = reg_id.findall(rso)
            assert len(rid) == 1
            rid = rid[0]
            if rid in fuck:
                continue
            fuck.add(rid)
            res_i.append(rso)
        res.append('|@|'.join(res_i))
    pyperclip.copy('\n'.join(res))

if True:
    ish = (input('任意键粘贴RIS(h)...').strip().upper() == 'H')
    lrs1 = pyperclip.paste().rstrip().splitlines()[ish:]
    print(len(lrs1), lrs1[0], lrs1[-1], sep='\n')

for i in range(min(len(res), len(lrs1))):
    rs1 = set(reg_id.findall(res[i]))
    rs2 = set(reg_id.findall(lrs1[i]))
    rs3 = rs1 - rs2
    if rs3:
        print(i, rs3, res[i], lrs1[i])
    
