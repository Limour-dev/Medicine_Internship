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
    pto = input('请输入保存路径：')
    if not os.path.exists(pto):
        os.mkdir(pto)
if True:
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


def htd2ttb(table):
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td","th"])
        row = [clear_value(cell.get_text(strip=True)) for cell in cells]
        rows.append(row)
    if not rows:
        return ''
    max_cols = max(len(row) for row in rows)
    for i, row in enumerate(rows):
        if len(row) < max_cols:
            # 补齐空字符串
            row.extend([""] * (max_cols - len(row)))
    # 计算每列最大宽度，方便排版
    col_widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = []
    for row in rows:
        formatted = "  ".join(word.ljust(col_widths[i]) for i, word in enumerate(row))
        lines.append(formatted)

    table_text = "\n".join(lines)
    return table_text

def hrmTb(bsoj):
    for table in bsoj.find_all("table"):
        table.decompose()
    return bsoj

skipiPd = False
skipoPd = True
skipPis = False

reg_risr = re.compile(r'(心超)|(心脏)|(冠状动脉)', re.IGNORECASE)
skiprisr = True

for num in range(210,len(zs)):
    zid = zs[num]
    pth1 = os.path.join(pts, zid)
    print(pth1)
    if not os.path.exists(pth1):
        print('skip')
        continue
    res = []

    pth2 = os.path.join(pth1, 'ris')
    pth3s = os.listdir(pth2)
    for pth3 in pth3s:
        nmbfuck = pth3.split('_')
        pth3 = os.path.join(pth2, pth3)
        print(pth3)
        with open(pth3, 'r', encoding='utf-8') as rf:
            d_s = BeautifulSoup(rf.read())
        try:
            onet = d_s.select_one('#table8 > tr:nth-child(2) > td:nth-child(2)').getText().strip()
            onet = datetime.strptime(onet, r'%Y-%m-%d %H:%M')
            onen = d_s.select_one("#table8 > tr:nth-child(5) > td:nth-child(2)").getText().strip()
            onen += '-' + d_s.select_one("#table8 > tr:nth-child(5) > td:nth-child(4)").getText().strip()
            if (not skiprisr) and reg_risr.search(onen):
                oner = d_s.select_one("#table8 > tr:nth-child(6) > td")
                oner = oner.getText().strip() + '\n'
            else:
                oner = ''
            oner += d_s.select_one("#table8 > tr:nth-child(7) > td").getText().strip()
            
        except AttributeError:
            oner = '\n'.join(htd2ttb(fuck) for fuck in d_s.select('table'))
            try:
                onet = nmbfuck[0]
                onet = datetime.strptime(onet, r'%Y-%m-%d')
                onen = nmbfuck[1]
            except:
                continue
        res.append(HisRec(onet, onen, oner))

    if not skipiPd:
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
    if not skipoPd:
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
    if not skipPis:
        pth2 = os.path.join(pth1, 'pis')
        if os.path.exists(pth2):
            pth3s = os.listdir(pth2)
        else:
            pth3s = []
        for pth3 in pth3s:
            pth3 = os.path.join(pth2, pth3)
            print(pth3)
            if pth3.endswith('.json'):
                with open(pth3, 'r', encoding='utf-8') as rf:
                    data = json.load(rf)
                data = data['data']
                try:
                    oner = '\n'.join(x['diagnostic_opinion'] for x in data['all_report'])
                except TypeError:
                    continue
                oner = clear_value(oner, rmHt=True)
                tmp = data.get('gigantic_inspection')
                if tmp:
                    oner = tmp + '\n' + oner
                onet = datetime.strptime(data['receive_at'], r'%Y-%m-%d %H:%M:%S')
                onen = '病理诊断报告单'
            else:
                with open(pth3, 'r', encoding='utf-8') as rf:
                    d_s = BeautifulSoup(rf.read())
                try:
                    onet = d_s.select_one("body > div > table:nth-child(4) > tr:nth-child(2) > td:nth-child(8)").getText(strip=True)
                    onet = datetime.strptime(onet, r'%Y-%m-%d')
                    onen = '病理诊断报告单-' + d_s.select_one("body > div > table:nth-child(4) > tr:nth-child(3) > td:nth-child(4)").getText(strip=True)
                    oner = d_s.select_one("body > div > table:nth-child(6) > tr:nth-child(2) > td")
                    oner = hrmTb(oner)
                    oner = oner.getText(strip=True)
                    oner = d_s.select_one("body > div > table:nth-child(6) > tr:nth-child(1) > td").getText(strip=True) + '\n' + oner
                except AttributeError:
                    try:
                        onet = d_s.select_one("body > table:nth-child(3) > tr:nth-child(5) > td:nth-child(2) > p > span").getText(strip=True)
                        onet = datetime.strptime(onet, r'%Y-%m-%d %H:%M')
                        onen = '病理诊断报告单-' + d_s.select_one("body > table:nth-child(3) > tr:nth-child(4) > td:nth-child(2) > p > span").getText(strip=True)
                        oner = d_s.select_one("body > table:nth-child(5) > tr:nth-child(4) > td:nth-child(2)").getText(strip=True)
                        oner = d_s.select_one("body > table:nth-child(5) > tr:nth-child(2) > td:nth-child(2)").getText(strip=True) + '\n' + oner
                    except AttributeError:
                        onen = '病理诊断报告单'
                        oner = d_s.getText(strip = True)
                        onet = os.path.split(pth3)[-1].split('_')[0]
                        onet = datetime.strptime(onet, r'%Y-%m-%d')
            res.append(HisRec(onet, onen, oner))
    
    res.sort(key=lambda x:x.time)
    pth1 = os.path.join(pto, f'{num:03}_{zid}.txt')
    print(pth1)
    with open(pth1, 'w', encoding='utf-8') as wf:
        for r in res:
            wf.write(r.getText())
    
