import uiautomation as auto
import time
import pyperclip

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

def get_value(_c):
    _t = _c.GetPattern(auto.PatternId.ValuePattern)
    if _t:
        return _t.Value
    else:
        return ''

def clear_value(_v):
    return _v.replace('\t', ' ').replace('\n', '  ')

a = get_control_depth(control, 10)
b = get_control_depth(a[1], 1)
c = get_control_depth(b[0], 1)

res = []
for line in c[2:]:
    name = line.Name
    print(name)
    items = []
    for x in line.GetChildren():
        v = get_value(x)
        v = clear_value(v)
        items.append((x.Name, v))
        print(items[-1])
    res.append('\t'.join(x[1] for x in items))

pyperclip.copy('\n'.join(res))
