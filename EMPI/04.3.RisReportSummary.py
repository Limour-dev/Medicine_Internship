if True:
    import pyperclip, re
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup
        from urllib.parse import unquote

    _t = httpx.Timeout(120)

    url = r'http://v-risservice01.zshis.com.sh:8066/Home/RisReportSummary/'

    
    ft = input('任意键粘贴住院记录(f表示仅最新)...').lower().strip().startswith('f')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(ft, nfs[0], nfs[-1], sep='\n')

    re_op = re.compile(r'(\d{4}-\d{2}-\d{2})\s*([^\s]+)')

res = []
try:
    for i in range(len(res),len(nfs)):
        print(i)
        nf = nfs[i].strip()
        if not nf:
            res.append('')
            continue
        res_i = set()
        for co in nf.split('|@|'):
            print(co)
            lb = httpx.get(url + co[7:], timeout=_t)
            lb_s = BeautifulSoup(lb, "html.parser")
            lbs = lb_s.select("#tblRisContent > tbody > tr")
            for opc in lbs:
                op = opc.getText().strip()
                try:
                    op = re_op.findall(op)[0]
                except:
                    continue
                opu = opc.select_one('td:nth-child(3) > a')
                opu = opu.get_attribute_list('href')[0]
                op = '|'.join(op) + '|' + unquote(opu)
                assert op.count('\t') == 0
                res_i.add(op)
            if ft:
                break
        res.append('|@|'.join(res_i))
finally:
    pyperclip.copy('\n'.join(res))

