import os, re

try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

path1 = r'C:\Users\limou\Downloads\icis\ICI-history' + os.path.sep

reg_a = re.compile(r'^ICI药是否停用[：:](.+)$', re.MULTILINE)
res = []
for filename in sorted(os.listdir(path1), key=lambda x:int(x.split('_')[0])):
    print(filename)
    path2 = path1 + filename
    try:
        with open(path2, 'r', encoding='utf-8') as rf:
            content = rf.read()
    except UnicodeDecodeError:
        with open(path2, 'r', encoding='gbk') as rf:
            content = rf.read()
    tmp = reg_a.findall(content)
    if tmp:
        res.append(tmp[0].strip())
    else:
        res.append('#')
set_clipboard_text('\n'.join(res))