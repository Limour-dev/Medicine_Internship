try:
    from clipboard import set_clipboard_text, get_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text, get_clipboard_text

a = get_clipboard_text()
a = a.strip()

input('任意键继续输入下一份数据')

b = get_clipboard_text()
b = b.strip()

zs2id = {k.lower().strip():v for v,k in (x.split('\t', maxsplit=1) for x in a.split('\n'))}
res = [zs2id.get(k.lower().strip(), 'NA') for k in b.split('\n')]

set_clipboard_text('\n'.join(res))