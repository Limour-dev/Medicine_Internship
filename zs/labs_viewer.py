import os
import tkinter as tk
import tkinter.filedialog as tkf
from tkinter import ttk
from datetime import datetime
import json, re

sort_key_re = re.compile(r'(-?[0-9]+.?[0-9]*)')


def _float(s):
    try:
        return float(s)
    except ValueError:
        return s


def sort_key(_s):
    s = _s[0]
    # 将字符串中的数字部分转换为整数，然后进行排序
    return [_float(x) for x in sort_key_re.split(s)]


class Treeview(ttk.Treeview):

    def tv_clear(self):
        x = self.get_children()
        for item in x:
            self.delete(item)

    def heading(self, col, text):
        super().heading(col, text=text, command=lambda _col=col: self._tv_sort_column(_col, True))

    def _tv_sort_column(self, col, reverse):  # Treeview、列名、排列方式
        l = [(self.set(k, col), k) for k in self.get_children('')]
        # print(self.get_children(''))
        l.sort(reverse=reverse, key=sort_key)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            self.move(k, '', index)
            # print(k)
        # 重写标题，使之成为再点倒序的标题
        super().heading(col, command=lambda: self._tv_sort_column(col, (not reverse)))


def re_find(_l, _r):
    r = re.compile(_r)
    for i, _i in enumerate(_l):
        if r.search(_i):
            return i
    return 0


def try_get(_l, _i):
    for _ in range(_i):
        try:
            return _l[_i]
        except IndexError:
            _i -= 1
    return 'NA'


def sp_fix(_l, _n):
    res = []
    cache = []
    cache_str = []
    for item in _l:
        item = item.split('\t')
        if len(item) >= _n:
            res.append(item)
        else:
            if len(cache) + len(item) >= _n:
                cache_str.append(item[0])
                item[0] = ';'.join(cache_str)
                cache.extend(item)

                res.append(cache)
                cache = []
                cache_str = []
            else:
                cache_str.append(item.pop())
                cache.extend(item)

    return res


class Wd:

    def __init__(self):
        self.rt = tk.Tk()
        self._path(1)
        self._time(2)
        self._tree_k(3)
        self._tree_v(3)
        self._tip(4)
        self.data = []

    # ===== 选择文件 =====
    def _path(self, r):
        et = self.path_et = tk.Entry(self.rt, textvariable=tk.StringVar(value='请选择文件...'), state=tk.DISABLED)
        et.grid(row=r, column=1, columnspan=8, padx=10, ipadx=300)
        self.path = './labs/'

        def _bt():
            _dir, _file = os.path.split(self.path)
            _askd_path = tkf.askopenfilename(
                title='选择 json 文件路径',
                initialdir=_dir,
                initialfile=_file,
                filetypes=(('JSON文件', '.json'),)
            )
            if not _askd_path:
                return
            self.path = _askd_path
            self.path_et.config(textvariable=tk.StringVar(value=_askd_path))
            self._load()
            self.update_k()

        bt = self.path_bt = tk.Button(self.rt, text='选择文件', command=_bt)
        bt.grid(row=r, column=9, columnspan=1)

    # 读取数据
    def _load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)[::-1]

    # ===== 设定起始时间 =====
    def _time(self, r):
        lb = self.time_lb = tk.Label(self.rt, text='设置 PCI 时间：', anchor=tk.E)
        lb.grid(row=r, column=7)
        self.now = datetime.now()
        self.time = tk.StringVar(value=self.now.strftime("%Y/%m/%d %H:%M"))
        time = self.time_et = tk.Entry(self.rt, textvariable=self.time)
        time.grid(row=r, column=8, pady=10)

        def _bt():
            time_str = self.time.get().strip()
            try:
                self.now = datetime.strptime(time_str, "%Y/%m/%d %H:%M")
            except ValueError:
                try:
                    self.now = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")
                except ValueError:
                    self.time.set(self.now.strftime("%Y/%m/%d %H:%M"))
            self.update_k()

        bt = self.time_bt = tk.Button(self.rt, text='设置时间', command=_bt)
        bt.grid(row=r, column=9, columnspan=1)

    # ===== 创建表格k =====
    def _tree_k(self, r):
        tv = self.k_tv = Treeview(self.rt, columns=("time", "name"), show="headings", height=25)
        tv.grid(row=r, column=1, columnspan=3, padx=10)
        # 设置列标题
        tv.heading("time", text="时间")
        tv.heading("name", text="项目")
        # 设置列宽
        tv.column("time", width=50)
        tv.column("name", width=200)

        def tv_click(event):  # 单击
            for iid in tv.selection():
                self.update_v(iid)

        tv.bind('<ButtonRelease-1>', tv_click)  # 绑定单击离开事件

    # ===== 创建表格v =====
    def _tree_v(self, r):
        tv = self.v_tv = Treeview(self.rt, columns=("name", "value", 'ref', "unit"), show="headings", height=25)
        tv.grid(row=r, column=4, columnspan=6, padx=10)
        # 设置列标题
        tv.heading("name", text="项目")
        tv.heading("value", text="值")
        tv.heading("ref", text="参考值")
        tv.heading("unit", text="单位")
        # 设置列宽
        tv.column("name", width=200)
        tv.column("value", width=100)
        tv.column("ref", width=150)
        tv.column("unit", width=100)

        def tv_click(event):  # 单击
            st = []
            for iid in tv.selection():
                item_text = tv.item(iid, "values")
                # print(item_text)
                st.append(item_text[1])
            st = ' '.join(st)
            if st:
                self.rt.clipboard_clear()
                self.rt.clipboard_append(st)
                self.tip(f'已复制到剪贴板：{st}')

        tv.bind('<ButtonRelease-1>', tv_click)  # 绑定单击离开事件

    # ===== 读取表格k =====
    def update_k(self):
        if not self.data:
            return
        self.k_tv.tv_clear()
        for iid, item in enumerate(self.data):
            key: str = item['key']
            tb = key.split('\t')
            time = datetime.strptime(tb[0], '%Y-%m-%d %H:%M')
            time_difference = time - self.now
            days_difference = time_difference.total_seconds() / (24 * 3600)
            if 0 > days_difference > -0.1:
                days_difference = 0
            days_difference = f'{days_difference:.1f}天'
            self.k_tv.insert("", "end", iid=iid, values=(days_difference, tb[1]))

    # ===== 读取表格v =====
    def update_v(self, iid):
        if not self.data:
            return
        self.v_tv.tv_clear()
        data = self.data[int(iid)]
        data = data['value'].split('\n', maxsplit=1)
        header = data[0].split('\t')
        # print(header)
        i_name = re_find(header, r'项目')
        i_value = re_find(header, r'结果')
        i_ref = re_find(header, r'参考值')
        i_unit = re_find(header, r'单位')
        data = sp_fix(data[1].split('\n'), len(header))
        for item in data:
            # print(item)
            name = try_get(item, i_name)
            value = try_get(item, i_value)
            ref = try_get(item, i_ref)
            unit = try_get(item, i_unit)
            values = (name, value, ref, unit)
            self.v_tv.insert("", "end", values=values)

    def _tip(self, r):
        self.tip_v = tk.StringVar(value='By Limour')
        et = self.tip_et = tk.Entry(self.rt, textvariable=self.tip_v, background='#DDDDDD')
        et.grid(row=r, column=1, columnspan=9, ipadx=340, padx=10, pady=10)

    def tip(self, text):
        self.tip_v.set(text)


# ===== 初始化窗口 =====
Wd = Wd()
Wd.rt.title("labs_viewer v0.1 ")
Wd.rt.geometry('850x640+10+10')

Wd.rt.mainloop()
