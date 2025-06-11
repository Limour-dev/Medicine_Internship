if True:
    import pyperclip
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup

    _t = httpx.Timeout(120)

    url = r'http://v-risservice01.zshis.com.sh:8066/Home/LabReportSummary/'

    
    ft = input('任意键粘贴住院记录(f表示仅最新)...').lower().strip().startswith('f')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(ft, nfs[0], nfs[-1], sep='\n')

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
            lbs = lb_s.select_one('#tblLabContent').select('tr')
            lbs = lbs[1:-2]
            if len(lbs) == 1 and lbs[0].getText().find('暂无检验报告') >= 0:
                continue
            for opc in lbs:
                op = opc.getText().strip()
                op = op.split('\r\n')
                op = op[0].strip() + '|' + \
                     next(x for x in op if x.find(' - ') >= 0).strip()
                opu = opc.select_one('td:nth-child(2) > a')
                opu = opu.get_attribute_list('href')[0]
                op = op + '|' + opu
                assert op.count('\t') == 0
                res_i.add(op)
            if ft:
                break
        res.append('|@|'.join(res_i))
finally:
    pyperclip.copy('\n'.join(res))

