if True
    import os, re, shutil
    pth = input('请输入文件夹路径:')
    new_pth = input('请输入另存的文件夹路径:')
    reg_zs = re.compile(r'ZS\d{5,}', re.IGNORECASE)

    def fast_copy_move(src, dst, is_move=True, verbose=True):
        # 如果源是文件
        if os.path.isfile(src):
            # 确保目标目录存在
            dst_dir = os.path.dirname(dst)
            if dst_dir and not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
                
            # 如果目标文件存在，先删除
            if os.path.exists(dst):
                os.remove(dst)
                
            # 执行移动或复制
            if is_move:
                shutil.move(src, dst)
                if verbose:
                    print(f"已移动: {src} -> {dst}")
            else:
                shutil.copy2(src, dst)  # copy2保留文件元数据
                if verbose:
                    print(f"已复制: {src} -> {dst}")
            return
        
        # 如果源是目录
        if not os.path.exists(dst):
            os.makedirs(dst)
        
        # 递归处理所有文件和子目录
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            fast_copy_move(src_item, dst_item, is_move, verbose)
        
        # 如果是移动操作且当前源目录已空，则删除源目录
        if is_move and not os.listdir(src):
            os.rmdir(src)
            if verbose:
                print(f"已删除空目录: {src}")

for pth1 in os.listdir(pth):
    pth2 = os.path.join(pth, pth1)
    for pth3 in os.listdir(pth2):
        tmp = pth3.split('=', maxsplit=1)
        name = tmp[0]
        tmp = tmp[-1].split('_')
        zsid = tmp[-2]
        zsid = reg_zs.findall(zsid)[0]
        fuck = tmp[-1]
        # print(name, zsid, pth1)
        npth1 = os.path.join(new_pth, f'{name}_{zsid}')
        if not os.path.exists(npth1):
            os.mkdir(npth1)
        # print(f'{name}_{zsid}', tmp)
        pth3 = os.path.join(pth2, pth3)
        ntph3 = os.path.join(npth1, f'{pth1}_{fuck}')
        
        try:
            os.rename(pth3, ntph3)
        except:
            print(pth3, '-->', ntph3)
            fast_copy_move(pth3, ntph3, verbose=False)
            

