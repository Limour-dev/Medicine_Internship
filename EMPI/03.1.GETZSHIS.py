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
    url_mzjl = r'http://v-emrservice01.zshis.com.sh/EmrPortal_new/Patient/HypersasceptibilityInfo.aspx'

res = []
for i in range(len(res),len(eids)):
    eid = eids[i]
    print(i)
    b_l = eid.split('\t')
    
    data_mzjl = {
        "EMPIID": b_l[0],
        "CardNO": b_l[1]
    }

    # 获取检索令牌
    mzjl = httpx.get(url_mzjl, params=data_mzjl)
    if True:
        e_s = BeautifulSoup(mzjl, "html.parser")
        he_vs = e_s.select_one('#__VIEWSTATE').get_attribute_list('value')
        he_vr = e_s.select_one('#__VIEWSTATEGENERATOR').get_attribute_list('value')
        data4 = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": he_vs[0],
            "__VIEWSTATEGENERATOR": he_vr[0],
            "__CALLBACKID": "__Page",
            "__CALLBACKPARAM": f"labmed{b_l[1]}&empiid={b_l[0]}",
        }
    # 进行检索
    f = httpx.post(url_mzjl, params=data_mzjl, data=data4, timeout=_t)
    f = f.text.split('@')
    # 获得记录
    cn = ['zs-his|' + x.split('|')[-2] for x in f if x.find('zs-his')>=0]
    res.append('|@|'.join(cn))
pyperclip.copy('\n'.join(res))
