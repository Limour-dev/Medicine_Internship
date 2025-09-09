import os, lmdb, json

pto = input('请输入lmdb路径：')
pts = input('请输入文件夹路径：')

pts = os.path.join(pts, os.path.split(pto)[-1])

env = lmdb.open(pto, map_size=1024*1024*1024*10)

txn = env.begin(write=False)

def v2f(rv, _pt, _k):
    if not os.path.exists(_pt):
        os.makedirs(_pt)
    for diro in rv[0]:
        pt1 = os.path.join(_pt, diro)
        k = f'{_k}{diro}'
        v = json.loads(txn.get(k.encode('utf8')).decode('utf8'))
        v2f(v, pt1, k)
    print(_pt, _k)
    for fo in rv[1]:
        pt1 = os.path.join(_pt, fo)
        k = f'{_k}{fo}'.encode('utf8')
        with open(pt1, 'wb') as wf:
            wf.write(txn.get(k))

v2f(json.loads(txn.get(b'\x00').decode('utf8')), pts, '')  
env.close()
