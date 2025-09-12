import os, pyperclip

pts = input('输入源文件夹路径:')

if True:
    hasHd = (input('任意键粘贴ZSID...').strip().upper() == 'H')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[hasHd:]
    print(sl[0], sl[-1])

if True:
    res = []

    alf = set(os.listdir(pts))

    for zsid in sl:
        if zsid in alf:
            res.append('1')
        else:
            res.append('0')

    pyperclip.copy('\n'.join(res))
