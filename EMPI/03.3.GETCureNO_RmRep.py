if True:
    import pyperclip
    input('任意键粘贴记录...')
    eid = pyperclip.paste().strip()
    eids = eid.splitlines()[1:]
    print(eids[0], '\n', eids[-1])

if True:
    print('=====开始=====')
    fuck = set()
    for i in range(len(eids)):
        eid = set(eids[i].strip().split('|@|'))
        for x in eid:
            if x in fuck:
                print(x)
            else:
                fuck.add(x)
    
    

