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
            # print(i, [(x.Name, x.AutomationId) for x in _t])
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
        return _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')

    def get_lgvalue(_c):
        return _c.GetLegacyIAccessiblePattern().Value

if True:
    a = get_control_depth(control, 2)
    b = get_control_depth(a[1], 1)
    c = get_control_depth(b[1], 2)
    res = []
    for z,d in enumerate(c[2:]):
        if z % 10 == 0:
            print(z)
        e = get_control_depth(d, 1)
        l = []
        for f in e[1:]:
            v = clear_value(get_lgvalue(f))
            l.append(v)
        res.append('\t'.join(l))
    pyperclip.copy('\n'.join(res))
    
    

