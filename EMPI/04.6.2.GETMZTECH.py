if True:
    import pyperclip
    import pathlib
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup

    _t = httpx.Timeout(120)
    
    input('任意键粘贴RIS...')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(nfs[0], nfs[-1], sep='\n')

    url = 'http://v-emrservice01.zshis.com.sh/EmrPortal_new/Admission/TechReport.aspx'

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        return _v

if True:
    ft = input('任意键粘贴zs-his(f表示仅最新)...').lower().strip().startswith('f')
    zshis = pyperclip.paste().strip().splitlines()[1:]
    print(zshis[0], zshis[-1], sep='\n')


res = []
empip = pathlib.Path(input('保存路径：'))

for i in range(len(res),len(zshis)):
    zshisi = zshis[i].strip().split('|@|')[0]
    print(i)
    
    b_l = nfs[i].strip().split('|@|')

    tp = empip / str(i)
    tp.mkdir(parents=True, exist_ok=True)

    for bl_j in b_l:
        b_j = bl_j.split('||')
        b_k = b_j[-1].split('@')
        data2 = {
            "cureno": zshisi,
            "applyno": b_k[0],
            "reporttype": b_k[1]
        }

        d = httpx.get(url, params=data2, timeout=_t)
        (tp / (b_j[0].replace(' ', '_') + f'_{b_k[0]}.html')).write_text(d.text, encoding='utf-8')

    res.append(zshisi)
