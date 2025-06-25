if True:
    import pyperclip
    import os, json, re
    pt1 = input('输入文件夹路径:')
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]

    alls = os.listdir(pt1)
    sl = list(enumerate(sl))

for o in alls:
    op = o[:-4]
    for i,x in sl:
        if op.endswith(x):
            os.rename(os.path.join(pt1,o), os.path.join(pt1, f'{i:03}_{x}.txt'))
            break
    else:
        print(o)
