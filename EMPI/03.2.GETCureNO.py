if True:
    import pyperclip
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup

    _t = httpx.Timeout(120)
    
    input('任意键粘贴EMPIID...')
    eid = pyperclip.paste().strip()
    eids = eid.splitlines()[1:]
    print(eids[0], '\n', eids[-1])

res = []
for i in range(len(res),len(eids)):
    eid = eids[i]
    print(i)
    b_l = eid.split('\t')
    data2 = {
        "EMPIID": b_l[0],
        "CardNO": b_l[1]
    }
    if True:
        url2 = 'http://v-emrservice01.zshis.com.sh/EmrPortal_new/NavigateFunc.aspx'
        c = httpx.get(url2, params=data2, timeout=_t)
        c_s = BeautifulSoup(c, "html.parser")
        hc_vs = c_s.select_one('#__VIEWSTATE').get_attribute_list('value')
        hc_vr = c_s.select_one('#__VIEWSTATEGENERATOR').get_attribute_list('value')
        hc_ev = c_s.select_one('#__EVENTVALIDATION').get_attribute_list('value')
        hc_lba = c_s.select('#listBoxAdmissions > option')
        hc_lba = [x.get_attribute_list('value')[0] for x in hc_lba]
        hc_lba = '|@|'.join(hc_lba)
        nf = f'{hc_vr[0]}|@|{hc_ev[0]}|@|{hc_vs[0]}'
    res.append(f'{hc_lba}\t{nf}')
pyperclip.copy('\n'.join(res))
