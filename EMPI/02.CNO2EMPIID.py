if True:
    import pyperclip
    def h2f(h,n):
        with open(n+'.txt', 'w', encoding='utf-8') as wf:
            wf.write(h.text)
    import httpx
    from bs4 import BeautifulSoup
    import re
    from urllib.parse import urlencode
    re_b = re.compile(r"EMPIID=([^']+?)&CardNO=([^']+)")
    input('任意键粘贴CNO...')
    kh = pyperclip.paste().strip()
    khs = kh.splitlines()[1:]
    print(khs[0], '\n', khs[-1])
    headers = {
        "Cookie": input('输入Cookie: ')
    }
    print(headers)

# 获取检索令牌
if True:
    url1 = r'http://v-emrservice01.zshis.com.sh/EmrPortal_new/OrientPatient.aspx'
    a = httpx.get(url1, headers=headers)
    a_s = BeautifulSoup(a, "html.parser")
    h_vs = a_s.select_one('#__VIEWSTATE').get_attribute_list('value')
    h_vsr = a_s.select_one('#__VIEWSTATEGENERATOR').get_attribute_list('value')
    h_ed = a_s.select_one('#__EVENTVALIDATION').get_attribute_list('value')

res = []
try:
    for i in range(len(res),len(khs)):
        kh = khs[i]
        print(i)
        data1 = {
            "__VIEWSTATE": h_vs[0],
            "__VIEWSTATEGENERATOR": h_vsr[0],
            "__EVENTVALIDATION": h_ed[0],
            "wardDropDownList": "-1",
            "txbKeyWord": kh.strip(),
            "searchButton.x": "57",
            "searchButton.y": "14"
        }
        a = httpx.post(url1, data=data1, headers=headers)
        a_s = BeautifulSoup(a, "html.parser")
        b = a_s.select_one('body > form script').getText()
        b_l = re_b.findall(b)[0]
        if True:
            h_vs = a_s.select_one('#__VIEWSTATE').get_attribute_list('value')
            h_vsr = a_s.select_one('#__VIEWSTATEGENERATOR').get_attribute_list('value')
            h_ed = a_s.select_one('#__EVENTVALIDATION').get_attribute_list('value')
            res.append('\t'.join(b_l))
finally:
    print(kh)
pyperclip.copy('\n'.join(res))
