if True:
    import pyperclip
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    if True:
        import httpx
        from bs4 import BeautifulSoup

    _t = httpx.Timeout(120)

if True:
    input('任意键粘贴数据...')
    eid = pyperclip.paste().strip()
    eids = eid.splitlines()[1:]

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
    # 获得一份记录
    cn = 'zs-his|' + f[0].split('|')[-2]
    res.append(cn)
pyperclip.copy('\n'.join(res))

if True:
    input('任意键粘贴数据...')
    zsh = pyperclip.paste().strip()
    zshs = zsh.splitlines()[1:]

# 获得检查记录
res = []
for i in range(len(res),len(zshs)):
    eid = eids[i]
    print(i)
    b_l = eid.split('\t')
    zsh = zshs[i]
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
        hc_lba = c_s.select_one('#listBoxAdmissions > option').get_attribute_list('value')
        data3 = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": hc_vs[0],
            "__VIEWSTATEGENERATOR": hc_vr[0],
            "listBoxAdmissions": hc_lba[0],
            "inputCardNo": b_l[1],
            "inputEMPIID": b_l[0],
            "inputDomainIDCureNo": "",
            "inputOP": "",
            "__CALLBACKID": "__Page",
            "__CALLBACKPARAM": "mztechreport" + zsh,
            "__EVENTVALIDATION": hc_ev[0]
        }
    d = httpx.post(url2, params=data2, data=data3, timeout=_t)
    if d.text.count('@') > 0:
        if 'MRI报告单' in d.text:
            an = [l for l in d.text.split('|@|') if l.find('MRI报告单') >= 0]
            an = [x.split('|')[-1] for x in an]
            an = '|@|'.join(an)
        else:
            an = '(null)'
    else:
        assert len(d.text) > 0
        an = '(none)'
    res.append(an)
pyperclip.copy('\n'.join(res))

if True:
    input('任意键粘贴数据...')
    zsan = pyperclip.paste().strip()
    zsans = zsan.splitlines()[1:]


# 获得检查结论
if True:
    url4 = r'http://v-emrservice01.zshis.com.sh/EmrPortal_new/Admission/TechReport.aspx'
    import re
    re_html = re.compile(r'<[^>]+>')
    def clear_value(_v):
        _v = _v.replace('\t', ' ').replace('\n', '  ').replace('\r', '  ')
        _v = re_html.sub('', _v)
        return _v

res = []
for i in range(len(res),len(zsans)):
    print(i)
    zsan = zsans[i].split('\t')
    cn = zsan[0]
    an = zsan[1].split('|@|')[0].split('@')
    data4 = {
        "cureno": cn,
        "applyno": an[0],
        "reporttype": an[-1],
    }
    g = httpx.get(url4, params=data4)
    g_s = BeautifulSoup(g, "html.parser")
    zsid = g_s.select_one('#label7').getText()
    res.append(zsid)

pyperclip.copy('\n'.join(res))


