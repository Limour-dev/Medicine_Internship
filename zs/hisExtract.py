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

try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

import httpx, json
_timeout = httpx.Timeout(120.0, connect=10.0)

url = os.environ['QUICKER_AI_URL']
headers = {
    'Authorization': os.environ["QUICKER_AI_KEY"]
}

system = '''
输出日期格式：%Y/%m/%d
从用户输入的病史中抽取以下信息，并按同样的顺序和格式输出，无法获得的数据用`#`号代替：
---
原发肿瘤：结肠恶性肿瘤
确诊肿瘤时间：2024/6/1
肿瘤分期（TNM）： T1aN1M0，IIIb期
高血脂：1
既往冠脉相关病史（CAD，MI等）：2024-10-09冠脉CT：左前降支及左旋支近中段散在斑块伴管腔轻中度狭窄
心衰：0
房颤：0
桥本甲状腺炎：0
## ICIs（免疫检查点抑制剂）治疗前
ECG：Normal
## ICIs治疗后
ICI用药时间：2024/9/15 - 2024/12/7
ICI药类：替雷利珠单抗
机制：PD-1
剂量：200mg
频率：2次/疗程
呼吸困难：0
心慌/胸闷/胸痛：偶有心悸
肌炎：上睑下垂
ECG： I度房室传导阻滞
首次怀疑心肌炎CTnT升高日期：2024/10/27
## 激素治疗后
激素种类：甲泼尼龙
ICI药是否停用：1
激素剂量：500mg qd冲击；60mg口服，逐步减量
激素停用时间：至今
是否联合丙球：是
丙球剂量：20g qd
丙球时间：2024/11/12 - 2024/11/17
联合免疫治疗药物（TOF、马替麦考酚酯等）：TOF
联合剂量：11mg qd
联合时间：2024/10/0 - 至今
心慌/胸闷/胸痛缓解：0
肌炎缓解：1
ECG：频发房性早搏
'''.strip()

data = {
    'model': "claude",
    'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': get_clipboard_text()}
    ],
    'stream': True
}

res = ''
with httpx.stream("POST", url, headers=headers, json=data, timeout=_timeout) as r:
    for line in r.iter_lines():
        if line.endswith('[DONE]'):
            continue
        if line.startswith("data:"):
            print(True, line)
            data = json.loads(line[5:])['choices']
            if data:
                data = data[0]['delta']
                if data:
                    res += data['content']
        else:
            print(False, line)
set_clipboard_text(res)