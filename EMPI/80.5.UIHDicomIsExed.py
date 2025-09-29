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
    input('任意键粘贴登记号...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]
    print(sl[0], '\n', sl[-1])
    a = control.EditControl(AutomationId = 'study-accessNumber')
    b = control.GroupControl(ClassName = 'ant-table-body')
    auto.SetGlobalSearchTimeout(20)

if True:
    res = []
    for i in range(0,len(sl)):
        sl_i = sl[i]
        print(i, sl_i)
        a.GetValuePattern().SetValue(sl_i)
        c = get_control_depth(b, 4)
        if len(c) < 9:
            res.append('NA')
        else:
            res.append('1')

    pyperclip.copy('\n'.join(res))
        
