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

    pts = input('请输入病史记录路径：')
    pto = input('请输入记录另存路径：')

    res = []

    reg_d = re.compile(r'\n^(\d\d\d\d-\d\d-\d\d)\t(.+?)$', re.MULTILINE+re.IGNORECASE)
    reg_sp = re.compile(r'\n^\d\d\d\d-\d\d-\d\d\t.+?$', re.MULTILINE+re.IGNORECASE)

if True:
    zsid2pt = {}
    pth3s = os.listdir(pts)
    for pth3 in pth3s:
        pth4 = pth3.split('_')[-1][:-4]
        # print(pth4)
        zsid2pt[pth4] = (os.path.join(pts, pth3), os.path.join(pto, pth3))

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

system = '''
输出日期格式：%Y/%m/%d
ici指免疫检查点抑制剂；ecg_pre_ici指使用ICI之前的心电图；myositis仅指骨骼肌炎，不包括心肌炎
目标：从用户输入的病史中抽取信息，并按示例的顺序和格式输出，无法获得的数据用`#`号代替(同时在括号里标注推测的最可能状态)
示例：
primary_cancer：anal_canal_cancer
cancer_diagnosis_date：2024/6/1
ecg_pre_ici：Normal
ici_start_date：2024/9/27
ici_name：替雷利珠单抗
ici_mechanism：PD-1
dyspnea：0
chest_symptoms：0
myositis：1
ici_stop_date：2024/10/19
ecg_post_ici：occasional_PACs
steroid_start_date：2024/10/28
ecg_post_steroid：occasional_PACs
'''.strip()

if True:
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

        with open(pth1[0], 'r', encoding='utf-8') as rf:
            content = clear_value(rf.read()).replace('\xa0','')

        data = {
            'model': "claude",
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': content}
            ],
            'stream': True
        }

        one = AI(data)

        with open(pth1[1], 'w', encoding='utf-8') as wf:
            wf.write(one)
        res.append(one)

def extract(_reg):
    reg_a = re.compile(_reg, re.MULTILINE+re.IGNORECASE)
    rres = []
    for zid in zs:
        if not zid in zsid2pt:
            print('skip', zid)
            rres.append('NA\tNA')
            continue
        pth1 = zsid2pt[zid]
        print(pth1)

        with open(pth1[1], 'r', encoding='utf-8') as rf:
            content = rf.read()

        tmp = reg_a.findall(content)

        if tmp:
            rres.append(tmp[0].strip())
        else:
            rres.append('#')

        pyperclip.copy('\n'.join(rres))


extract(r'^primary_cancer[：:](.+)$')
extract(r'^cancer_diagnosis_date[：:](.+)$')
extract(r'^ici_start_date[：:](.+)$')
extract(r'^ici_stop_date[：:](.+)$')
extract(r'^steroid_start_date[：:](.+)$')
extract(r'^ecg_pre_ici[：:](.+)$')
extract(r'^ici_name[：:](.+)$')
extract(r'^ici_mechanism[：:](.+)$')
extract(r'^dyspnea[：:](.+)$')
extract(r'^chest_symptoms[：:](.+)$')
extract(r'^myositis[：:](.+)$')
extract(r'^ecg_post_ici[：:](.+)$')
extract(r'^ecg_post_steroid[：:](.+)$')
