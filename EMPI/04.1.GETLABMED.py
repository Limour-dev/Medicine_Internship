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
    print(eids[0], eids[-1], sep='\n')
    
    input('任意键粘贴NF...')
    nfs = pyperclip.paste().strip().splitlines()[1:]
    print(nfs[0], nfs[-1], sep='\n')

    url = 'http://v-emrservice01.zshis.com.sh/EmrPortal_new/NavigateFunc.aspx'

    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        return _v

res = []
for i in range(len(res),len(eids)):
    eid = eids[i]
    print(i)
    b_l = eid.split('\t')

    data2 = {
        "EMPIID": b_l[0],
        "CardNO": b_l[1]
    }

    hc_vr, hc_ev, hc_vs = nfs[i].strip().split('|@|')
    
    data3 = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": hc_vs,
        "__VIEWSTATEGENERATOR": hc_vr,
        "inputCardNo": b_l[1],
        "inputEMPIID": b_l[0],
        "inputDomainIDCureNo": "",
        "inputOP": "",
        "__CALLBACKID": "__Page",
        "__CALLBACKPARAM": "labmed" + b_l[0],
        "__EVENTVALIDATION": hc_ev
    }

    d = httpx.post(url, params=data2, data=data3, timeout=_t)
    ds = d.text.split('|@@|')
    ds = clear_value(ds[-2])
    if ds.endswith('|@|'):
        ds = ds[:-3]
    res.append(ds)
pyperclip.copy('\n'.join(res))
