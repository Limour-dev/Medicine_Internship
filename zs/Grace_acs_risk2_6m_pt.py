try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

def get_tb_from_cb():
    header, body = get_clipboard_text().split('\n', maxsplit=1)
    header = {i:n.strip().lower() for i,n in enumerate(header.split('\t'))}
    res = {n:[] for n in header.values()}
    for line in body.splitlines():
        for i,v in enumerate(line.split('\t')):
            v = v.strip()
            try:
                v = float(v)
            except ValueError:
                pass
            res[header[i]].append(v)
    return res

data = get_tb_from_cb()

def p_age(age):
    age = int(age)
    if age <= 35:
        return 0
    if age >= 90:
        return 100
    tmp = {
        "36": "1.8",
        "37": "3.6",
        "38": "5.4",
        "39": "7.2",
        "40": "9",
        "41": "10.8",
        "42": "12.6",
        "43": "14.4",
        "44": "16.2",
        "45": "18",
        "46": "19.8",
        "47": "21.6",
        "48": "23.4",
        "49": "25.2",
        "50": "27",
        "51": "28.8",
        "52": "30.6",
        "53": "32.4",
        "54": "34.2",
        "55": "36",
        "56": "37.8",
        "57": "39.6",
        "58": "41.4",
        "59": "43.2",
        "60": "45",
        "61": "46.8",
        "62": "48.6",
        "63": "50.4",
        "64": "52.2",
        "65": "54",
        "66": "55.9",
        "67": "57.8",
        "68": "59.7",
        "69": "61.6",
        "70": "63.5",
        "71": "65.4",
        "72": "67.3",
        "73": "69.2",
        "74": "71.1",
        "75": "73",
        "76": "74.8",
        "77": "76.6",
        "78": "78.4",
        "79": "80.2",
        "80": "82",
        "81": "83.8",
        "82": "85.6",
        "83": "87.4",
        "84": "89.2",
        "85": "91",
        "86": "92.8",
        "87": "94.6",
        "88": "96.4",
        "89": "98.2"
    }
    return float(tmp[str(age)])

def p_HR(hr):
    hr = int(hr)
    if hr < 70:
        return 0
    elif hr < 80:
        return 1.35
    elif hr < 90:
        return 3.9
    elif hr < 100:
        return 6.35
    elif hr < 110:
        return 8.9
    elif hr < 130:
        return 12.85
    elif hr < 150:
        return 18.85
    elif hr < 200:
        return 34.37
    else:
        return 34.0

def p_SBP(sbp):
    sbp = int(sbp)
    if sbp < 80:
        return 40
    elif sbp < 100:
        return 37.15
    elif sbp < 110:
        return 32.65
    elif sbp < 120:
        return 29.2
    elif sbp < 130:
        return 25.65
    elif sbp < 140:
        return 22.65
    elif sbp < 160:
        return 16.2
    elif sbp < 180:
        return 11.15
    else:
        return 8.0

def p_CR(cr):
    if cr < 35.4:
        return 0.975
    elif cr < 71:
        return 3.975
    elif cr < 106:
        return 6.975
    elif cr < 141:
        return 9.95
    elif cr < 177:
        return 12.95
    elif cr < 354:
        return 20.965
    else:
        return 28

def p_Di(arg):
    if arg > 0:
        return 20
    else:
        return 0

def p_st(arg):
    if arg > 0:
        return 17
    else:
        return 0

def p_enzymes(arg):
    if arg > 0:
        return 13
    else:
        return 0

def p_cardiac(arg):
    if arg > 0:
        return 30
    else:
        return 0

res = []
for i in range(167):
    pt = p_age(data['age'][i]) + \
         p_HR(data['hr'][i]) + \
         p_SBP(data['sbp'][i]) + \
         p_Di(data['diuretic'][i]) + \
         p_CR(data['cr'][i]) + \
         p_st(data['stemi'][i]) + \
         p_enzymes(data['enzymes'][i]) + \
         p_cardiac(data['cardiac'][i])
    res.append(str(pt))
set_clipboard_text('\n'.join(res))