import os, lmdb, json

pto = input('请输入lmdb路径：')

env = lmdb.open(pto, readonly=True, map_size=1024*1024*1024*10)

info = env.info()
stat = env.stat()

map_size = info["map_size"]     # 配置的最大容量（字节）
last_pgno = info["last_pgno"]   # 已经分配到的最后一个页号
psize = stat["psize"]           # 每个页的大小（字节）

used_bytes = (last_pgno + 1) * psize
remaining_bytes = map_size - used_bytes

print(f"map_size: {map_size / (1024*1024)} MB")
print(f"used:     {used_bytes / (1024*1024)} MB")
print(f"free:     {remaining_bytes / (1024*1024)} MB")

env.close()
