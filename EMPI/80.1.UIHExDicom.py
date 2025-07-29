if True:
    import uiautomation as auto
    import time
    import pyperclip
    import re
    import platform
    isWin7 = (platform.release() == '7')
    print('Win7', isWin7)
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
        if (type(_c) is list):
            _t = _c
        else:
            _t = [_c]
            
        for i in range(_depth):
            _t = _t[0].GetChildren()
            print(i, [(x.Name, x.AutomationId) for x in _t])
        return _t

    def get_control_name(_cs, _n, offset=0):
        if not (type(_cs) is list):
            _cs = _cs.GetChildren()
        for i,_c in enumerate(_cs):
            if _c.Name == _n:
                _c = _cs[i+offset]
                print(_c.Name, _c.AutomationId)
                return _c

    def get_control_id(_cs, _id, offset=0):
        if not (type(_cs) is list):
            _cs = _cs.GetChildren()
        for i,_c in enumerate(_cs):
            if _c.AutomationId == _id:
                _c = _cs[i+offset]
                print(_c.Name, _c.AutomationId)
                return _c

    def get_value(_c):
        if isWin7:
            _t = _c.GetLegacyIAccessiblePattern()
        else:
            _t = _c.GetPattern(auto.PatternId.ValuePattern)
        if _t:
            return _t.Value
        else:
            return ''

if True:
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()
    print(sl[0], '\n', sl[-1])
    auto.SetGlobalSearchTimeout(120)

# e.GetValuePattern().SetValue('limour')
# f.Click(simulateMove=False)
# m.Click(simulateMove=False)



if True:
    import keyboard
    a = get_control_depth(control, 2)
    b = get_control_name(a, 'DICOM节点导入')
    b = get_control_id(b, 'PACSExplorerWindow')
    c = get_control_depth(b, 2)
    d = get_control_depth(c[3], 1)
    e = get_control_name(d, '登记号', 1)
    f = get_control_name(c, '查询', 0)
    g = get_control_id(c, 'studyList_ListView', 0)
    m = get_control_name(c, '导入检查')

i = 0
for i in range(i, len(sl)):
    zid = sl[i]
    print(i, zid)
    e.GetValuePattern().SetValue(zid)
    # print(get_value(e))
    while f.IsEnabled == 0:
        f.Click(simulateMove=False)
        keyboard.press_and_release('esc')
        time.sleep(1)
        e.GetValuePattern().SetValue(zid)
    f.Click(simulateMove=False)
    h = get_control_name(g, 'UIH.Mcsf.Archiving.StudyViewModel')
    if h:
        n = get_control_depth(h, 1)[2]
        nn = get_value(n)
        print(nn)
        if not nn: break
        n.Click(simulateMove=False)
        m.Click(simulateMove=False)
        
