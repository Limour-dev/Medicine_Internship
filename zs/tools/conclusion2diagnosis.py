import re, httpx, json
_timeout = httpx.Timeout(120.0, connect=10.0)

try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

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

url = os.environ['QUICKER_AI_URL']
headers = {
    'Authorization': os.environ["QUICKER_AI_KEY"]
}

system = '''
根据用户输入的心脏磁共振结论中尽力推断最可能的诊断，以方便后续的绘图
+ 一行一个相对应
+ 规范为ICD诊断
+ 使用缩写
+ 只给出一个诊断
+ 无法明确，则给出 Others
+ HCM不区分梗阻型，都写HCM
+ 缺血性心肌病不区分陈旧性心梗，都写ICM
'''.strip()

cc = get_clipboard_text()
assert cc.count('\n') == 50
cc = '\n'.join(f'{i:02}.{line}' for i,line in enumerate(cc.splitlines()))


tp_u = '''
00.（梗阻型）肥厚型心肌病，肥厚心肌内散在水肿及多发纤维灶形成；左心房增大，轻度二尖瓣、主动脉瓣反流；少量心包积液。
01.ICIs相关性心肌炎治疗后病例：左室心肌水肿大部分吸收，室间隔水肿少许残留可能，室间隔壁基底段微小纤维灶形成，较前25-02-07相仿，建议3月后CMR随访；轻度二尖瓣返流，轻度主动脉瓣返流。
02.心脏MRI检查未见明显异常。
03.LAD供血区陈旧性心肌梗死并缺血性心肌病改变机会大，请结合临床并随访；轻度二尖瓣返流，心包少量积液。
04.左房室扩大伴左室整体收缩活动减弱，左室壁增厚伴少许纤维化，心肌少许水肿，建议基因检测除外特殊类型心肌病；二尖瓣、三尖瓣轻度返流，心包少许积液。
05.左室多壁段初始T1mapping值升高，心肌水肿待排，少量心包积液，建议1月后CMR复查。
06.左室壁肥厚（室间隔为著），左室多壁段初始T1值明显升高及延迟强化，可符合淀粉样变累及心脏，建议核医学检查。心包及两侧胸腔少量积液。
'''.strip()

tp_a = '''
00.HCM
01.ICIs-M
02.Normal
03.ICM
04.DCM
05.Others
06.CA
'''.strip()

data = {
    'model': "gpt-4.1",
    'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': tp_u},
        {'role': 'assistant', 'content': tp_a},
        {'role': 'user', 'content': cc}
    ],
    'stream': True
}

tmp = ''
with httpx.stream("POST", url, headers=headers, json=data, timeout=_timeout) as r:
    for line in r.iter_lines():
        if line.endswith('[DONE]'):
            continue
        if line.startswith("data:"):
            # print(True, line)
            data = json.loads(line[5:])['choices']
            if data:

                data = data[0]
                if 'delta' in data:
                    data = data['delta']
                    if data:
                        tmp += data['content']
                        print(data['content'], end='')
        else:
            pass


set_clipboard_text('\n'.join(line.strip()[3:] for line in tmp.strip().splitlines()))