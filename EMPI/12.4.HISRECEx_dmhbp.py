if True:
    import os, json, re
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

    pts = input('请输入病史原始记录路径：')

    res = []

    reg_d = re.compile(r'\n^(\d\d\d\d-\d\d-\d\d)\t(.+?)$', re.MULTILINE+re.IGNORECASE)
    reg_sp = re.compile(r'\n^\d\d\d\d-\d\d-\d\d\t.+?$', re.MULTILINE+re.IGNORECASE)
    
if True:
    zsid2pt = {}
    pth3s = os.listdir(pts)
    for pth3 in pth3s:
        pth4 = pth3.split('_')[-1][:-4]
        # print(pth4)
        zsid2pt[pth4] = os.path.join(pts, pth3)
        
    
if True:
    re_dh = re.compile(r'^.*(?:糖尿病|高血压).*$', re.MULTILINE+re.IGNORECASE)
    if len(res):
        res = res[:-1]
    for zsi_i in range(len(res), len(zs)):
        zid = zs[zsi_i]
        if not zid in zsid2pt:
            print('skip', zid)
            res.append('NA\tNA')
            continue
        pth1 = zsid2pt[zid]
        print(pth1)

        with open(pth1, 'r', encoding='utf-8') as rf:
            data = rf.read()
        
        th = reg_d.findall(data)
        if (not th) and (not data.strip()):
            print('skip', zid)
            res.append('NA\tNA')
            continue
        
        td = reg_sp.split(data)
        tt = td[0].split('\n', maxsplit=1)
        td[0] = tt[-1]
        th = [tt[0].split('\t', maxsplit=1)] + th
        
        assert len(th) == len(td)

        rons = []

        for i, cel in enumerate(td):
            cel = cel.replace('\xa0','')
            cel = re_dh.findall(cel)
            if cel:
                rons.append(th[i][0] + ':'+ ';'.join(cel))
        print(rons)

        if rons:
            res.append(clear_value('|@|'.join(rons)))
        else:
            res.append('NA\tNA')
    pyperclip.copy('\n'.join(res))

if True:
    import os
    def dotenv():
        with open('.env', 'r', encoding='utf-8') as env:
            for line in env:
                tmp = line.strip().split('=', maxsplit=1)
                if len(tmp) <= 1:
                    continue
                k, v = tmp[0].strip(), tmp[1].strip()
                if (not k) or (not v):
                    continue
                os.environ[k] = v
    dotenv()
    
    import httpx
    _timeout = httpx.Timeout(120.0, connect=10.0)

    url = os.environ['QUICKER_AI_URL']
    headers = {
        'Authorization': os.environ["QUICKER_AI_KEY"]
    }

    def AI(data):
        res = ''
        with httpx.stream("POST", url, headers=headers, json=data, timeout=_timeout) as r:
            for line in r.iter_lines():
                # print(True, line)
                if line.endswith('[DONE]'):
                    continue
                if line.startswith("data:"):
                    data = json.loads(line[5:])['choices']
                    if data:
                        data = data[0]
                        if 'delta' not in data:
                            continue
                        data = data['delta']
                        if data:
                            res += data['content']
                            print(data['content'], end='')
                else:
                    pass
        return res


rres = []
if True:
    data = {
        'model': "claude",
        'messages': [
            {'role': 'system', 'content': "判断目前是否有高血压和糖尿病，按示例格式输出，不做解释"},
            {'role': 'user', 'content': "2024-11-01:高血压病史：血压最高达150/90mmHg，平日不规律服用药物降压，血压控制欠佳。否认糖尿病史。"},
            {'role': 'assistant', 'content': "HBP 1\nDM 0"},
            {'role': 'user', 'content': ""}
        ],
        'stream': True
    }
    reg_hbp_dm = re.compile(r'HBP\s+([01])\s+DM\s+([01])', re.IGNORECASE)
    for i in range(len(rres), len(res)):
        one = res[i]
        print(one)
        if (not one.strip()) or (one == 'NA\tNA'):
            rres.append('')
            continue
        data['messages'][-1]['content'] = one
        print(data)
        one = AI(data)
        print(one)
        one = reg_hbp_dm.findall(one)
        rres.append('\t'.join(one[-1]))
    pyperclip.copy('\n'.join(rres))
