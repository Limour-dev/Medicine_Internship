import re
rec_re = re.compile('^\d\d\d\d-\d\d-\d\d \d\d:\d\d.+\n\n\n', re.MULTILINE)

def clear_value(_v):
    return _v.replace('\t', ' ').replace('\n', '  ')

a = r'C:\Users\limou\OneDrive\Documents\IMH_raw\data\time.txt'
b = r'C:\Users\limou\OneDrive\Documents\IMH_raw\rec'

alls = []
with open(a, 'r', encoding='utf-8') as rf:
    for line in rf:
        row1 = line.split('\t', maxsplit=1)[0].strip()
        if row1:
            alls.append(row1)


def is_op_rec(s: str):
    return ((s.find('手术经过') > 0) or (s.find('冠状动脉造影描述') > 0)) and (s.find('手术名称') > 0)

err = []
res = []
for row1 in alls:
    with open(b + f'\\{row1}_rec.txt', 'r', encoding='utf-8') as rf:
        rec = rf.read()
    recs = rec_re.split(rec)
    for rec in recs:
        if is_op_rec(rec):
            res.append(clear_value(rec))
            break
    else:
        err.append(row1)

with open('tmp.txt', 'w', encoding='utf-8') as wf:
    wf.write('\n'.join(res))

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

with open('tmp.txt', 'r', encoding='utf-8') as rf:
    res = rf.readlines()

system = '''
从用户输入中结构化提取冠脉造影结果 // 不输出注释信息，未描述默认未狭窄，以介入前的结果为准
## 示例输入
TIG导管难以送至主动脉根部，可见升主动脉及主动脉弓严重扭曲，遂改穿刺右侧股动脉置入7F鞘，送入6F JL4造影导管行左冠状动脉造影见左主干狭窄30%；左前降支近中段长病变伴扭曲钙化，最狭窄80%，中远段心肌桥，收缩期受压20%，舒张期恢复，第一对角支狭窄30%；左回旋支迂曲，多处管壁不规则，中段弥漫性病变，狭窄80%。6F JR4造影导管行右冠状动脉造影见右冠近段起完全闭塞。向患者和家属详细交代病情，告知病情危重以及急诊介入治疗风险并商量后决定进一步行急诊右冠介入治疗。取6F SAL0.75指引导管送入右冠口，0.014”SION及Runthrough导丝通过病变送至右冠远端，送入ThrombusterII血栓抽吸导管于右冠近中段及远段反复抽吸，抽出出多块红色血栓，复查造影示右冠远段恢复前向血流，近段残余狭窄90%伴斑块破裂征象，近中段狭窄40%伴迂曲，远段后三叉处狭窄80%伴不稳定征象，左室后支粗大，近段狭窄70%，黄后降支相对细小，未见明显狭窄，另取Runthrough导丝保护后降支，冠脉内给予欣维宁10ml，Sprinter 2.5×20mm球囊于右冠远段及近段病变处8-10atm*10秒扩张后，植入Promus PREMIER 2.75*32mm依维莫司药物支架于右冠远段-左室后支近段，以12atm×10秒扩张释放，植入另一Promus PREMIER 3.5*24mm依维莫斯药物支架于右冠近段，以14atm*10秒扩张释放，复查造影示支架扩张满意，无残余狭窄，斑块轻度向后降支开口移位，TIMI血流均为3级。手术成功，拔鞘，以TR-Band桡动脉充气压迫器压迫止血（充气14ml），术中用肝素7500U、造影剂优维显150ml，术终血压130/70mmHg、心率70次/分，患者无不适主诉，术后注意局部渗血情况和生命体征监测，每1-2小时压迫器放气2ml，若无渗血，8-10小时后解除压迫，股动脉鞘管保留，局部加压包扎，至少6小时后拔鞘，右下肢制动24-30小时。术后静滴欣维宁4ml/h维持20小时，建议双联抗血小板治疗至少12月，阿司匹林100mg/日长期服用，9-12个月复查冠脉造影，择期（2-3个月后）行左冠介入治疗。 
## 示例输出
Dominance：R // 右冠优势型为R，左冠优势型为L，默认为R
LM: 30 // 左主干狭窄30%
LADp: 80 // 左前降支近段狭窄80%
LADm: 80 // 左前降支中段狭窄80%
LADa: 20 // 左前降支远段心肌桥，收缩期受压20%
D1: 30 // 第一对角支狭窄30%
LCXp: 0 // 左回旋支近段未狭窄
LCXm: 80 // 左回旋支中段狭窄80%
LCXd: 0 // 左回旋支远段未狭窄
RCAp: 100 // 右冠近段完全闭塞
RCAm: 40  // 右冠中段狭窄40%
RCAd: 80 // 右冠远段狭窄80%
'''.strip()

output = [''] * len(res)

for i in range(0, len(res)):
    data = {
        'model': "gpt-4.1",
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': res[i]}
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
    output[i] = tmp

with open('output.json', 'w', encoding='utf-8') as wf:
    json.dump(output, wf, ensure_ascii=False, indent=4)

arg = 'RCAd'
re_o = re.compile(f'^{arg}[:：]\s?(.+)', re.IGNORECASE)
cp = [''] * len(output)
for i in range(len(output)):
    for d in output[i].split('\n'):
        d = d.split('//')[0].strip()
        e = re_o.findall(d)
        if e:
            cp[i] = e[0]
            break
    else:
        print(output[i])

set_clipboard_text('\n'.join(cp))