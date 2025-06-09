if True:
    import uiautomation as auto
    import time
    import pyperclip
    import re
    re_html = re.compile(r'<[^>]+>')
    
    time.sleep(3)
    control = auto.GetFocusedControl()

    controlList = []
    while control:
        controlList.insert(0, control)
        control = control.GetParentControl()
    if len(controlList) == 1:
        control = controlList[0]
    else:
        control = controlList[1]
    print(control.Name)

    def get_control_depth(_c, _depth):
        _t = [_c]
        for i in range(_depth):
            _t = _t[0].GetChildren()
            print(i, [(x.Name, x.AutomationId) for x in _t])
        return _t

    def get_control_name(_cs, _n):
        for _c in _cs:
            if _c.Name == _n:
                print(_c.Name, _c.AutomationId)
                return _c

    def get_value(_c):
        _t = _c.GetPattern(auto.PatternId.ValuePattern)
        if _t:
            return _t.Value
        else:
            return ''

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        _v = re_html.sub('', _v)
        return _v

    def get_lgvalue(_c):
        return _c.GetLegacyIAccessiblePattern().Value


if True:
    a = get_control_depth(control, 10)
    z = get_control_depth(a[2], 1)
    z = get_control_name(z, '医技号：')

if True:
    input('任意键粘贴数据...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]
    

res = []
for i in range(len(res),len(sl)):
    sl_i = sl[i]
    print(i)
    z.GetValuePattern().SetValue(sl_i)
    z.SendKey(13)
    b = get_control_depth(a[1], 1)
    c = get_control_depth(b[0], 1)
    c_st = 2
    if len(c) < 3:
        res.append([])
        continue
    if c[2].Name == '首行':
        c_st += 1
    res_i = []
    for line in c[c_st:]:
        name = line.Name
        print(name)
        items = []
        for x in line.GetChildren():
            v = get_value(x)
            v = clear_value(v)
            items.append((x.Name, v))
            print(items[-1])
        tmp = '\t'.join(x[1] for x in items)
        res_i.append(tmp)
    res.append(res_i)

pyperclip.copy('\n'.join(res))
