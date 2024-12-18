import os
from datetime import datetime

rp = os.getenv('LABS_VIEWER', '.') + '/'


def read(_r, _p, _ex, _f, _skip_h=False):
    with open(rp + _r + _p + _ex, 'r', encoding='utf-8') as f:
        if _skip_h:
            next(f)
        x: str
        return [_f(x.rstrip('\r\n')) for x in f]


g_others = set()
g = {
    'anti_platelet_txa2i': {
        '阿司匹林', '吲哚布芬',
    },
    'anti_platelet_p2y12i': {
        '氯吡格雷', '普拉格雷', '替格瑞洛',
    },
    'anti_platelet_tirofiban': {
        '替罗非班',
    },
    'anti_platelet_camp': {
        '西洛他唑', '双嘧达莫',
    },
    'anti_coagulant': {
        '肝素', '磺达肝癸钠',
        '华法林',
        '利伐沙班', '艾多沙班', '比伐芦定',
    },
    'beta_blocker1': {
        '美托洛尔', '比索洛尔', '阿替洛尔',
    },
    'beta_blocker': {
        '阿罗洛尔', '卡维地洛',
    },
    'ivabradine': {
        '伊伐布雷定',
    },
    'acei': {
        '贝那普利', '培哚普利', '雷米普利', '卡托普利',
    },
    'arb1': {
        '缬沙坦', '氯沙坦', '坎地沙坦',
    },
    'arb2': {
        '厄贝沙坦', '奥美沙坦', '替米沙坦',
    },
    'ccb': {
        '氨氯地平', '硝苯地平', '非洛地平',
    },
    'diuretic1': {
        '托拉塞米', '呋塞米', '布美他尼',
    },
    'diuretic_hctz': {
        '氢氯噻嗪',
    },
    'diuretic_spironolactone': {
        '螺内酯',
    },
    'diuretic_tolvaptan': {
        '托伐普坦',
    },
    'anti_lip_st': {
        '瑞舒伐他汀', '阿托伐他汀', '血脂康胶囊',
    },
    'fenofibrate': {
        '非诺贝特',
    },
    'ezetimibe': {
        '依折麦布',
    },
    'anti_lip_pcsk9i': {
        '依洛尤单抗', '阿利西尤单抗',
    },
    'anti_arrhythmia': {
        '胺碘酮', '心脏电除颤', '利多卡因', '艾司洛尔',
    },
    'nourish': {
        '曲美他嗪', '辅酶Q10'
    },
    'stimulant': {
        '地高辛', '多巴胺', '毛花苷', '多巴酚丁胺',
    },
    'nitrate': {
        '硝酸甘油', '单硝酸异山梨酯', '尼可地尔',
        '硝酸异山梨酯', '硝普钠',
    },
    'stomach_protecting': {
        '泮托拉唑', '奥美拉唑', '雷贝拉唑', '兰索拉唑', '艾普拉唑', '瑞巴派特',
    },
    'anti_diabetic_metformin': {
        '二甲双胍',
    },
    'anti_diabetic_insulin': {
        '胰岛素',
    },
    'anti_diabetic_su': {
        '格列喹酮', '格列齐特', '格列美脲', '格列吡嗪',
    },
    'anti_diabetic_tzd': {
        '吡格列酮'
    },
    'anti_diabetic_sglt2i': {
        '达格列净'
    },
    'anti_diabetic_agi': {
        '伏格列波糖', '阿卡波糖',
    },
    'anti_diabetic_dpp4i': {
        '艾托格列净', '沙格列汀',
    },
    'anti_diabetic_glp1ra': {
        '度拉糖肽', '司美格鲁肽', '聚乙二醇洛塞那肽',
    },
    'anti_allergic': {
        '西替利嗪', '甲泼尼龙',
    },
    'sleeping_pill': {
        '咪达唑仑', '艾司唑仑', '阿普唑仑', '地西泮', '唑吡坦', '氯硝西泮',
    },
    'analgesia': {
        '洛索洛芬', '塞来昔布', '非布司他', '布洛芬', '吗啡', '度洛西汀', '芬太尼',
    },
}

g_all = {
    '护理', '输液', '心电图', '氧气吸入', '甲状腺素', '病毒', '尿糖', '血糖',
    '胆固醇', '脂蛋白', '糖化', '氯化钠注射液', '葡萄糖注射液', '结核', '_尿',
    '留置针', '传感器', '三通', '心电监', '抗原', '抗体', '受体', '真菌', '细菌',
    '葡萄糖测定', '加压', '降温', '血压', '注射器', '采血器', '换药', '雾化器',
    '分类', '观察', '计数', '培养', '血气', '生化', '冲洗', '胶原', '通气',
    '电泳', '探头', '监测', '敷料', '试验', '导尿', '延长管',
}

for k,v in g.items():
    g_all = g_all | v

all_p = read('data/', 'time', '.txt', lambda x: x.split('\t')[0])
all_t = read('data/', 'time', '.txt',
             lambda x: datetime.strptime(x.split('\t')[-1].strip(), "%Y/%m/%d %H:%M"))


def any_in(_l, _s):
    return any((x in _s) for x in _l)


headers = list(g.keys())
res = ['\t'.join(['id'] + headers)]
for p, t in zip(all_p, all_t):
    try:
        one_p_ = read('orders/', p, '.txt', lambda x: x.split(',')[5], True)
        one_t = read('orders/', p, '.txt',
                     lambda x: datetime.strptime(x.split(',')[3].strip(), "%Y-%m-%d"), True)
        one_tp = read('orders/', p, '.txt', lambda x: x.split(',')[2], True)
        one_p = []
        for _p, _t, tp in zip(one_p_, one_t, one_tp):
            delta = (_t - t).total_seconds() / (24 * 3600)
            if -1 <= delta <= 4:
                # if tp == '长期':
                one_p.append(_p)
    except FileNotFoundError:
        res.append('\t'.join([p] + ['/'] * len(headers)))
        continue

    r_res = ['0'] * len(headers)
    for item in one_p:
        for i, h in enumerate(headers):
            if any_in(g[h], item):
                r_res[i] = '1'
        if any_in(g_all, item):
            continue
        if len(item) > 2 and item[-2] == '急':
            continue
        if any_in(g_others, item):
            continue
        print(item)
        g_others.add(item)

    res.append('\t'.join([p] + r_res))

res = '\n'.join(res)
print(g_others)
