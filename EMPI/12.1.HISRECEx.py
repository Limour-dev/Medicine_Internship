if True:
    import os, json, re
    from bs4 import BeautifulSoup
    import pyperclip

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        return _v
    
    input('任意键粘贴ZSID...')
    zs = pyperclip.paste().strip().splitlines()
    print(len(zs), zs[0], zs[-1], sep='\n')

    res = []

if True:
    if len(res):
        res = res[:-1]
    reg_hbp_dm = re.compile(r'(?:(?:【既往史】\s*(?:疾病史：)?)|(?:疾病史：))\s*(.+?)\s*(?:(?:手术史外伤史：)|(?:传染病史：)|(?:【个人史】))', re.DOTALL)
    for zidi in range(len(res), len(zs)):
        zid = zs[zidi]
        pth = os.path.join('GETHSREC', zid, 'ipd')
        if not os.path.exists(pth):
            res.append('NA\tNA')
            continue
        pths = os.listdir(pth)
        rons = []
        for pth1 in pths:
            pth1 = os.path.join(pth, pth1)
            print(pth1)
            with open(pth1, 'r', encoding='utf-8') as rf:
                data = json.load(rf)
            data = data['result']
            if not data:
                continue
            for one in data:
                if one['sectionName'].strip().startswith('入院记录') or one['sectionName'] in {
                        '24小时入出院记录', '入观记录'
                    }:
                    data = one
                    break
                print(one['sectionName'])
            else:
                raise BaseException('无入院记录')
            d_s = BeautifulSoup(data['form'], "html.parser")
            one = reg_hbp_dm.findall(d_s.getText())
            if not one or not one[-1].strip():
                if data['sectionName'] == '24小时入出院记录':
                    continue
                print((d_s.getText()))
                raise BaseException('无疾病史')
            one =  data['create_date'].split(' ')[0] + '|' + clear_value(one[-1])
            rons.append(one)
        res.append('|@|'.join(rons))
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
            {'role': 'user', 'content': "2024-11-01|高血压病史：血压最高达150/90mmHg，平日不规律服用药物降压，血压控制欠佳。否认糖尿病史。"},
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
        
