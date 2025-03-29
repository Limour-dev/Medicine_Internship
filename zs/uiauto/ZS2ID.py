a = '''
'''.strip()
b = '''
'''.strip()

zs2id = {k.lower().strip():v for v,k in (x.split('\t', maxsplit=1) for x in a.split('\n'))}
res = [zs2id.get(k.lower().strip(), 'NA') for k in b.split('\n')]
try:
    from clipboard import set_clipboard_text
except ModuleNotFoundError:
    from tmp.clipboard import set_clipboard_text

set_clipboard_text('\n'.join(res))