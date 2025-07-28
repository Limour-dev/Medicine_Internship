import os
import pandas as pd
import h5py
import numpy as np
pth = r'D:\DTI\results\ICIs'
for pth1 in os.listdir(pth):
    pth1 = os.path.join(pth, pth1, 'Python_post_processing')
    pth_rm_pre = os.path.join(pth1, 'session', 'image_manual_removal_pre.zip')
    rm_pre = pd.read_pickle(pth_rm_pre)
    pth_rm_pre = os.path.join(pth1, 'results', 'numpy results', 'image_manual_removal_pre.csv')
    pth_h5 = os.path.join(pth1, 'results', 'data', 'DTI_maps.h5')
    with h5py.File(pth_h5, 'r') as rf:
        # print(list(rf.keys()))
        all_snr = (x for x in rf.keys() if x.startswith('snr_'))
        res = {'b0': {}, 'b1': {}}
        for snr in all_snr:
            data = rf[snr]
            valid_data = data[~np.isnan(data)]
            tmp = snr.split('_')
            sli = tmp[1]
            bx = tmp[2]
            if int(bx) > 200:
                bx = 'b1'
            else:
                bx = 'b0'
            if sli in res[bx]:
                res[bx][sli].append(valid_data)
            else:
                res[bx][sli] = [valid_data]
            # print(snr, bx, sli)
        all_snr = list(res['b1'].keys())
        all_snr.sort(key=int)
        sli_n = len(res['b0'].keys())
        if sli_n:
            bs = sli_n // 3
            ap = bs
            bs = all_snr[:bs]
            mid = all_snr[ap:sli_n-ap]
            ap = all_snr[sli_n-ap:]
            print(bs, mid, ap, all_snr)
            snr = []
            
            tmp = []
            for k in bs:
                tmp.extend(res['b0'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
            
            tmp = []
            for k in mid:
                tmp.extend(res['b0'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
            
            tmp = []
            for k in ap:
                tmp.extend(res['b0'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
            
            tmp = []
            for k in bs:
                tmp.extend(res['b1'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
            
            tmp = []
            for k in mid:
                tmp.extend(res['b1'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
            
            tmp = []
            for k in ap:
                tmp.extend(res['b1'][k])
            tmp = np.concatenate(tmp)
            snr.append(np.mean(tmp))
        else:
            print(pth1, 'no SNR')
            snr = ['#', '#', '#', '#', '#', '#']
        print(snr)
    snr.append(sum(rm_pre['to_be_removed']))
    with open(pth_rm_pre, 'w') as wf:
        wf.write('\t'.join(str(x) for x in snr))