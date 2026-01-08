if True:
    import os, json, re
    from bs4 import BeautifulSoup
    import pyperclip
    from datetime import datetime

    reg_sp = re.compile(r'[\n\r]\s*')
    reg_nn = re.compile(r'\n\n+')
    reg_html = re.compile('<.+?>')
    def clear_value(_v, rmHt=False):
        if rmHt:
            _v = reg_html.sub('', _v)
        _v = _v.replace('\t', ' ').replace('','')
        _v = reg_sp.sub('\n', _v)
        _v = reg_nn.sub('\n', _v)
        return _v.strip()
    
    input('任意键粘贴ZSID...')
    zs = pyperclip.paste().strip().splitlines()
    print(len(zs), zs[0], zs[-1], sep='\n')

    pts = input('请输入GETHSREC路径：')

    def geto(_c):
        return clear_value(_c.get_text()) + '\t'

    res = []

if True:
    if len(res):
        res = res[:-1]
    for zsi_i in range(len(res), len(zs)):
        zid = zs[zsi_i]
        pth1 = os.path.join(pts, zid, 'ord')
        print(pth1)
        if not os.path.exists(pth1):
            print('skip')
            continue
        rres = []
        pth3s = os.listdir(pth1)

        for pth3 in pth3s:
            pth3 = os.path.join(pth1, pth3)
            print(pth3)
            with open(pth3, 'r', encoding='utf-8') as rf:
                d_s = BeautifulSoup(rf.read())
            tb = d_s.select_one('#gridViewWardChanged')
            trs = tb.find_all("tr")
            # cells = tr.find_all("th")
            for tr in trs[1:]:
                cells = tr.find_all("td")
                line = zid + '\t'
                line += geto(cells[3])
                line += geto(cells[4])
                line += geto(cells[0])
                line += geto(cells[13])
                line += geto(cells[5])
                line += geto(cells[6])
                line += geto(cells[7])
                line += geto(cells[8]).strip()
                rres.append(line)
        if rres:
            res.append('\n'.join(rres))

    outr = 'ZSID	开始日期	结束日期	类型	内部编码	名称	用法	规格	数量\n'
    outr += '\n'.join(res)
    pyperclip.copy(outr)
