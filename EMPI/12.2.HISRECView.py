if True:
    import os, json, re
    from bs4 import BeautifulSoup
    import pyperclip
    from datetime import datetime

    reg_sp = re.compile(r'[\n\r]\s*')
    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('','')
        _v = reg_sp.sub('\n', _v)
        return _v.strip()
    
    input('任意键粘贴ZSID...')
    zs = pyperclip.paste().strip().splitlines()
    print(len(zs), zs[0], zs[-1], sep='\n')

    pts = input('请输入GETHSREC路径：')
    pto = input('请输入保存路径：')
    if not os.path.exists(pto):
        os.mkdir(pto)
if True
    class HisRec:
        def __init__(self, _t, _n, _r):
            self.time = _t
            self.name = _n
            self.rec = _r
        def getText(self):
            _t = self.time.strftime('%Y-%m-%d')
            return f'{_t}\t{clear_value(self.name)}\n{clear_value(self.rec)}\n\n'

    reg_ipd_skip = re.compile(r'(须知)|(同意)|(自评)|(告知)|(清单)')
    reg_ipd_labs = re.compile(r'【主要化验结果】[^【]+')
    
for num,zid in enumerate(zs):
    pth1 = os.path.join(pts, zid)
    print(pth1)
    if not os.path.exists(pth1):
        print('skip')
        continue
    res = []

    pth2 = os.path.join(pth1, 'ris')
    pth3s = os.listdir(pth2)
    for pth3 in pth3s:
        pth3 = os.path.join(pth2, pth3)
        print(pth3)
        with open(pth3, 'r', encoding='utf-8') as rf:
            d_s = BeautifulSoup(rf.read())
        onet = d_s.select_one('#table8 > tr:nth-child(2) > td:nth-child(2)').getText().strip()
        onet = datetime.strptime(onet, r'%Y-%m-%d %H:%M')
        onen = d_s.select_one("#table8 > tr:nth-child(5) > td:nth-child(2)").getText().strip()
        onen += '-' + d_s.select_one("#table8 > tr:nth-child(5) > td:nth-child(4)").getText().strip()
        oner = d_s.select_one("#table8 > tr:nth-child(7) > td").getText().strip()
        res.append(HisRec(onet, onen, oner))
    
    pth2 = os.path.join(pth1, 'ipd')
    pth3s = os.listdir(pth2)
    for pth3 in pth3s:
        pth3 = os.path.join(pth2, pth3)
        print(pth3)
        with open(pth3, 'r', encoding='utf-8') as rf:
            data = json.load(rf)
        data = data['result']
        if not data:
            continue
        for one in data:
            onen = one['sectionName']
            if reg_ipd_skip.search(onen):
                continue
            print(onen)
            onet = datetime.strptime(one['create_date'], r'%Y-%m-%d %H:%M:%S')
            d_s = BeautifulSoup(one['form'], "html.parser")
            oner = d_s.getText()
            if onen.find('出院') >= 0:
                oner = reg_ipd_labs.sub('', clear_value(oner))
            res.append(HisRec(onet, onen, oner))

    pth2 = os.path.join(pth1, 'opd')
    pth3s = os.listdir(pth2)
    for pth3 in pth3s:
        pth3 = os.path.join(pth2, pth3)
        print(pth3)
        with open(pth3, 'r', encoding='utf-8') as rf:
            d_s = BeautifulSoup(rf.read())
        data = d_s.select_one('#labelOutPatEmrDocAndOrder')
        if not data or not data.getText().strip():
            continue
        div = data.select('body > div')
        div = [x for x in div if x.attrs.get('align') != 'right']
        i = 0
        while i < len(div):
            ndiv = div[i]
            i += 1
            if not ndiv.attrs.get('onclick'):
                continue
            rdiv = div[i]
            if not rdiv.attrs.get('id', '').startswith('title'):
                continue
            i += 1
            onet = ndiv.select_one('table > tr > td:nth-child(1) > span > strong').getText()
            onet = datetime.strptime(onet, r'+%Y-%m-%d %H:%M')
            onen = ndiv.select_one('table > tr > td:nth-child(2) > span > strong').getText()
            oner = rdiv.getText()
            res.append(HisRec(onet, onen, oner))
    
    res.sort(key=lambda x:x.time)
    pth1 = os.path.join(pto, f'{num:03}_{zid}.txt')
    print(pth1)
    with open(pth1, 'w', encoding='utf-8') as wf:
        for r in res:
            wf.write(r.getText())
    
