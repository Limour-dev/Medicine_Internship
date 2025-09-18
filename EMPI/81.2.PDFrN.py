import pyperclip, os

if True:
    input('任意键粘贴ZSID...')
    sl = pyperclip.paste().strip()
    sl = sl.splitlines()[1:]
    print(sl[0], '\n', sl[-1])

pdf_p = input('请输入pdf路径:')
pdf_o = input('请输入pdf保存路径:')

all_pdfs = os.listdir(pdf_p)

for sli in sl:
    sli = sli.split('\t')
    print(sli)
    for one in all_pdfs:
        if one.startswith(sli[-1]):
            two = f'(id-{sli[0]})' + one[len(sli[-1]):]
            p1 = os.path.join(pdf_p, one)
            p2 = os.path.join(pdf_o, two)
            print(p1, '->', p2)
            if os.path.exists(p1):
                os.rename(p1, p2)
