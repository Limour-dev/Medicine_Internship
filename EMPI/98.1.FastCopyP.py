if True:
    import pyperclip
    import os
    from datetime import datetime
    pts = input('输入源文件夹路径:')
    pto = input('输入目标文件夹路径:')
    ldt = input('输入过滤的最早的时间：')
    try:
        ldt = datetime.strptime(ldt,'%Y-%m-%d')
    except:
        ldt = datetime.strptime('2000-1-1','%Y-%m-%d')
    print(ldt)

def getmt(fp):
    mtime = os.path.getmtime(fp)
    return datetime.fromtimestamp(mtime)

res = set()

for one in os.listdir(pts):
    for two in os.listdir(os.path.join(pts, one)):
        if getmt(os.path.join(pts, one, two)) >= ldt:
            if os.path.exists(os.path.join(pto, one, two)):
                print('skip exists', two)
            else:
                res.add(os.path.join(pts, one) + '\\')

pyperclip.copy('\r\n'.join(res))
