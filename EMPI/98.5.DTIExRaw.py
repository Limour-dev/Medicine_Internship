# -*- coding: utf-8 -*-

if True:
    import pyperclip
    import os, re
    from datetime import datetime
    import pydicom 
    import numpy as np
    pts = input('输入源文件夹路径:')


    def getmt(fp):
        mtime = os.path.getmtime(fp)
        return datetime.fromtimestamp(mtime)

    zid = {}

    for a in os.listdir(pts):
        b = a.split('_')[-2].strip().upper()
        if b in zid:
            print(b)
            zid[b].append(os.path.join(pts,a))
        else:
            zid[b] = [os.path.join(pts,a)]

    for b in zid.keys():
        c = []
        for a in zid[b]:
            c += [os.path.join(a, x) for x in os.listdir(a)]
        zid[b] = c

    for b in zid.keys():
        for i,a in enumerate(zid[b]):
            sst = datetime.strptime(a.split('_')[-2], '%Y%m%d')
            zid[b][i] = [sst, a]
        zid[b].sort(key=lambda x:x[0])

if True:
    import os
    import shutil
    from pathlib import Path
    
    
    def copy_all_files(src_dir: str, dst_dir: str) -> None:
        """
        复制源文件夹下（含子文件夹）的所有内容到目标文件夹。
        - src_dir: 源文件夹路径
        - dst_dir: 目标文件夹路径（不存在会自动创建）
        """
        src = Path(src_dir)
        dst = Path(dst_dir)
    
        if not src.is_dir():
            raise NotADirectoryError(f"源路径不是文件夹或不存在: {src}")
    
        dst.mkdir(parents=True, exist_ok=True)
    
        # 递归复制：保持目录结构
        for root, dirs, files in os.walk(src):
            root_path = Path(root)
            rel = root_path.relative_to(src)
            target_root = dst / rel
            target_root.mkdir(parents=True, exist_ok=True)
    
            for fname in files:
                s = root_path / fname
                d = target_root / fname
                shutil.copy2(s, d)  # copy2 会尽量保留时间戳等元数据


if True:

    def get_b_value(ds):
        """
        从 DICOM 文件中提取 b 值
        不同厂商存储 b 值的方式不同
        """
        b_value = None
        
        # ---- 方法1: 标准 DICOM 标签 (0018,9087) ----
        if hasattr(ds, 'DiffusionBValue'):
            b_value = float(ds.DiffusionBValue)
            return b_value
        
        # ---- 方法2: 通过 tag 直接读取 ----
        try:
            b_value = float(ds[0x0018, 0x9087].value)
            return b_value
        except (KeyError, AttributeError):
            pass
        
        # ---- 方法3: Siemens 私有标签 ----
        try:
            # Siemens CSA Header
            csa_header = ds[0x0019, 0x100c].value  # B_value in Siemens
            b_value = float(csa_header)
            return b_value
        except (KeyError, AttributeError):
            pass
        
        try:
            b_value = float(ds[0x0019, 0x100a].value)  # 另一个 Siemens 标签
            return b_value
        except (KeyError, AttributeError):
            pass
        
        # ---- 方法4: GE 私有标签 ----
        try:
            b_value = float(ds[0x0043, 0x1039].value[0])
            return b_value
        except (KeyError, AttributeError, IndexError):
            pass
        
        # ---- 方法5: Philips 私有标签 ----
        try:
            b_value = float(ds[0x2001, 0x1003].value)
            return b_value
        except (KeyError, AttributeError):
            pass
        
        # ---- 方法6: 从序列描述中解析 ----
        series_desc = getattr(ds, 'SeriesDescription', '')
        if 'b' in series_desc.lower():
            import re
            match = re.search(r'b(\d+)', series_desc, re.IGNORECASE)
            if match:
                b_value = float(match.group(1))
                return b_value
        
        return b_value
    
    def print_b_value_info(ds):
        """打印所有可能的 b 值相关标签"""
        print("\n--- b 值相关信息 ---")
        
        # 检查标准标签
        tags_to_check = {
            (0x0018, 0x9087): "DiffusionBValue (标准)",
            (0x0019, 0x100c): "Siemens B_value",
            (0x0019, 0x100a): "Siemens NumberOfImagesInMosaic",
            (0x0043, 0x1039): "GE B_value",
            (0x2001, 0x1003): "Philips B_value",
        }
        
        for tag, desc in tags_to_check.items():
            try:
                value = ds[tag].value
                print(f"  {desc} {tag}: {value}")
            except KeyError:
                pass
        
        b_value = get_b_value(ds)
        print(f"  >>> 解析到的 b 值: {b_value}")
        
    def get_b_values_enhanced(ds):
        """
        Enhanced DICOM 的 b 值存储在
        PerFrameFunctionalGroupsSequence 中，每帧独立
        """
        b_values = []
        
        per_frame_seq = ds.PerFrameFunctionalGroupsSequence
        
        for frame_idx, frame in enumerate(per_frame_seq):
            b_val = None
            
            # ---- 标准路径 ----
            try:
                b_val = float(
                    frame
                    .MRDiffusionSequence[0]
                    .DiffusionBValue
                )
            except AttributeError:
                pass
            
            # ---- 备用路径 ----
            if b_val is None:
                try:
                    b_val = float(
                        frame[0x0018, 0x9117][0]  # MRDiffusionSequence
                        [0x0018, 0x9087].value     # DiffusionBValue
                    )
                except (KeyError, IndexError):
                    pass
            
            b_values.append({
                'frame_index': frame_idx,
                'b_value': b_val
            })
        return b_values


if True:
    input('任意键粘贴ZSID和时间...')
    sl = pyperclip.paste()
    sl = sl.splitlines()
    print(sl[0], sl[-1])


# DTI copy
ndtip = input('输入新dti文件夹路径:')
if input('dti fastcopy').strip().upper() == 'Y':
    res = []
    re_dti = re.compile(r'(ep2d_diff_m2_DTI_Zoomed_\d+_MR)|(dti_10dir_zoomit_b300_\d+_MR)|(ep2d_diff_inline_CCF_C2Pshare_rFOV_\d+_MR)', re.IGNORECASE)
    for zsid in sl:
        tmp = zsid.split('\t')
        zsid = tmp[0].strip().upper()
        sst = datetime.strptime(tmp[-1], '%Y/%m/%d')
        if zsid:
            if zsid in zid:
                data = zid[zsid]
            else:
                res.append('NA')
                continue
        else:
            if res[-1].startswith('NA'):
                res.append('NA')
                continue
        tmp = [(abs(sst - x[0]), x[0], x[1]) for x in data]
        tmp.sort(key = lambda x:x[0])
        tmp = tmp[0]
        ss = os.listdir(tmp[2])
        ss = [x for x in ss if re_dti.match(x)]
        if not ss:
            res.append('NA')
            continue
        for i,d in enumerate(ss):
            c = os.path.join(tmp[2], d)
            n = len(os.listdir(c))
            if d.startswith('ep2d_diff'):
                m = 121
            else:
                m = 210
            ss[i] = [n, n%m == 0, os.path.split(tmp[2])[0], zsid, c, tmp[1]]
            # print(ss[i])
        ss = [x for x in ss if x[1]]
        if ss:
            print(ss[0])
            tmp = os.path.split(ss[0][2])[1]
            tmp = tmp.split(ss[0][3], maxsplit=1)[0]
            tmp = tmp.replace(',', '')
            npn = datetime.strftime(ss[0][5],'%Y%m%d') + '_' + tmp + ss[0][3]
            npn = os.path.join(ndtip, npn)
            print(ss[0][4], '-->', npn)
            copy_all_files(ss[0][4], npn)
        else:
            res.append('NA')
    pyperclip.copy('\r\n'.join(x for x in res if x != 'NA'))



cdtip = Path(input('输入新dti文件夹路径:'))
for acase in os.listdir(ndtip):
    acase_s = os.path.join(ndtip, acase)
    acase_d = cdtip / acase
    print(acase_s, '-->', str(acase_d))
    acase_d.mkdir(parents=True, exist_ok=True)
    for dsp in os.listdir(acase_s):
        dsp_s = os.path.join(acase_s, dsp)
        dsp_d = acase_d / dsp
        # print(dsp_s, '-->', dsp_d)
        ds = pydicom.dcmread(dsp_s)
        bvalue = get_b_value(ds)
        if bvalue == 50:
            # ds.save_as(str(dsp_d))
            pass
        elif bvalue is None:
            if int(ds.NumberOfFrames) > 1:
                bvalue = get_b_values_enhanced(ds)
                if all(x['b_value'] == 50 for x in bvalue):
                    ds.save_as(str(dsp_d))
                else:
                    print(ds.pixel_array.shape)
                    print(bvalue)
            else:
                print_b_value_info(ds)

# for i in range(1,122):
#     ds = pydicom.dcmread(r'D:\Task\26\Cima.X_cases\HCM\20251218_Huang_Xiang_ZS24416786' + f'\\{i}.dcm')
#     print(all(x['b_value'] == 50 for x in get_b_values_enhanced(ds)))