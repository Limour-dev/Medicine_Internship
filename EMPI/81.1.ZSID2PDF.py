if True:
    import uiautomation as auto
    import time, os
    import pyperclip
    from pynput import mouse, keyboard
    msc = mouse.Controller()
    kbc = keyboard.Controller()
    import re

    import platform
    isWin7 = (platform.release() == '7')
    
    re_html = re.compile(r'<[^>]+>')
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
        if isWin7:
            _t = _c.GetLegacyIAccessiblePattern()
        else:
            _t = _c.GetPattern(auto.PatternId.ValuePattern)
        if _t:
            return _t.Value
        else:
            return ''

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        _v = re_html.sub('', _v)
        return _v

if True:
    a = get_control_depth(control, 4)
    yjh = get_control_depth(a[5], 1)[0]
    cx = get_control_name(a[12].GetChildren(), '查询')

if True:
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]
    print(sl[0], '\n', sl[-1])
    a = get_control_depth(control, 3)
    auto.SetGlobalSearchTimeout(120)


pdf_p = input('请输入pdf路径:')
pdf_o = input('请输入pdf保存路径:')

for i in range(0,11):
    sl_i = sl[i]
    print(i, sl_i)
    yjh.GetValuePattern().SetValue(sl_i)
    cx.Click(simulateMove=False)
    if True:
        try:
            b = get_control_depth(a[1], 1)
        except:
            time.sleep(2)
            b = get_control_depth(a[1], 1)
        c = get_control_depth(b[1], 2)
        c_st = 2
        if len(c) < 3:
            continue
        if c[2].Name == '首行':
            c_st += 1
        for line in c[c_st:]:
            name = line.Name
            print(name)
            if not get_value(line.GetChildren()[8]).startswith('心脏'):
                continue
            x = line.GetChildren()[2]
            v = get_value(line.GetChildren()[1]) + '_' + get_value(x)
            print(v)
            if os.path.exists(os.path.join(pdf_o, f'{v}_{0}.pdf')):
                continue
            if True:
                x.Click(simulateMove=False)
                x.RightClick(simulateMove=False)
                time.sleep(1)
                # print(msc.position)
                msc.move(96, 134)
                time.sleep(0.5)
                msc.click(mouse.Button.left, 1)
                time.sleep(5)
                kbc.press(keyboard.Key.alt)
                kbc.press(keyboard.Key.f4)
                time.sleep(0.5)
                kbc.release(keyboard.Key.f4)
                kbc.release(keyboard.Key.alt)
                # print(msc.position)
                all_pdfs = os.listdir(pdf_p)
                print(all_pdfs)
                for num, opdf in enumerate(all_pdfs):
                    os.rename(os.path.join(pdf_p, opdf), os.path.join(pdf_o, f'{v}_{num}.pdf'))
    
