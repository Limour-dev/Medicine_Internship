import os, lmdb, json

pto = input('请输入文件夹路径：')
pts = input('请输入lmdb路径：')

pts = os.path.join(pts, os.path.split(pto)[-1])

env = lmdb.open(pts, map_size=1024*1024*1024*10)

txn = env.begin(write=True)

pto_l = len(pto) + 1
for root, dirs, files in os.walk(pto):
    v = json.dumps([dirs, files], ensure_ascii=False).encode('utf8')
    if len(root) < pto_l:
        k = ''
        txn.put(b'\x00', v)
    else:
        k = root[pto_l:]
        txn.put(k.encode('utf8'), v)
    print(root)
    for file in files:
        pt1 = os.path.join(root, file)
        with open(pt1, 'rb') as rf:
            v = rf.read()
        txn.put(f'{k}{file}'.encode('utf8'), v, overwrite=False)
txn.commit()
env.close()
