import uiautomation as auto
import time
import pyperclip
import re

if True:
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
    return _v.replace('\t', ' ').replace('\n', '  ')

if True:
    a = get_control_depth(control, 10)
    b = get_control_depth(a[1], 1)

    h = get_control_depth(control, 7)
    j = get_control_depth(h[1], 6)

    c = get_control_depth(b[0], 1)
    o = get_control_name(c, '垂直滚动条')
    o = get_control_name(o.GetChildren(), '向下翻页')

res = []
# ========== loop start ==========
for line in c[len(res)+2:]:
    name = line.Name
    print(name)
    items = []
    for x in line.GetChildren():
        v = get_value(x)
        v = clear_value(v)
        items.append((x.Name, v))
        # print(items[-1])
    while line.IsOffscreen:
        o.Click()
    if name != '首行':
        line.Click()
        k = get_control_depth(j[0], 2)
        l = get_control_name(k, '心超')
        if l:
            m = get_control_depth(l, 1)
            m = [x for x in m if x.Name.startswith('常规超声心动图')]
            if m:
                m = m[-1]
                print(name, m.Name)
                v = m.Name
                items.append(('心超', clear_value(v)))
                m.GetExpandCollapsePattern().Collapse()
                m.DoubleClick()
                q = get_control_depth(h[1], 4)
                r = get_control_name(q[2].GetChildren(), m.Name)
                r.Click()
                q = get_control_depth(h[1], 4)
                r = get_control_name(q[2].GetChildren(), m.Name)
                r = get_control_depth(r, 7)[0]
                v = r.Name
                if v.startswith('影像学诊断'):
                    v = v[6:]
                items.append(('心超', clear_value(v)))
            else:
                print(name, '1 没有该项目, 跳过')
        else:
            print(name, '0 没有该项目, 跳过')
    res.append('\t'.join(x[1] for x in items))
# ========== loop end ==========
pyperclip.copy('\n'.join(res))
