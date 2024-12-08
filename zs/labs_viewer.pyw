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

    def heading(self, col, text, key=sort_key, reverse=True):
        super().heading(col, text=text,
                        command=lambda _col=col, _key=key:
                        self._tv_sort_column(_col, _key, reverse))

    def _tv_sort_column(self, col, key, reverse):  # Treeview、列名、排列方式
        l = [(self.set(k, col), k) for k in self.get_children('')]
        # print(self.get_children(''))
        l.sort(reverse=reverse, key=key)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            self.move(k, '', index)
            # print(k)
        # 重写标题，使之成为再点倒序的标题
        super().heading(col, command=lambda: self._tv_sort_column(col, key, (not reverse)))


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
        self._search(2)
        self.data = []
        self.search = None
        self._load_time()
        self._detach(2)

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
        _dir, _file = os.path.split(self.path)
        self.now = self.default_time.get(_file, self.now)
        self.time.set(self.now.strftime("%Y/%m/%d %H:%M"))
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)[::-1]
        self.search = None
        self.tip(f'载入文件：{self.path}')

    def _load_time(self):
        self.default_time = {}
        try:
            with open('./data/time.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    item = line.split('\t')
                    try:
                        time = datetime.strptime(item[-1].strip(), "%Y/%m/%d %H:%M")
                        self.default_time[item[0].strip() + '.json'] = time
                    except ValueError:
                        print('载入默认时间配置未成功', line)
        except FileNotFoundError:
            self.tip(f'载入默认时间配置未成功！')

    # ===== 隐藏负值 =====
    def _detach(self, r):
        self.detach_set = set()

        def _bt():
            for iid in self.k_tv.get_children():
                value: str = self.k_tv.item(iid, 'value')[0]
                if value.startswith('-'):
                    self.k_tv.delete(iid)
                    self.detach_set.add(int(iid))

        bt = self.detach_bt = tk.Button(self.rt, text='隐藏负值', command=_bt)
        bt.grid(row=r, column=5, columnspan=1)

    # ===== 搜索功能 =====
    def _search(self, r):
        self.search_v = tk.StringVar(value='')
        et = self.search_et = tk.Entry(self.rt, textvariable=self.search_v)
        et.grid(row=r, column=1, columnspan=3, ipadx=55)

        last_search = ''

        def _search(search):
            for i in range(self.search, len(self.data)):
                item = self.data[i]
                if search in item['value']:
                    if i in self.detach_set:
                        continue
                    self.search = i + 1
                    if self.search >= len(self.data):
                        self.search = 0
                    self.k_tv.selection_set(i)
                    # self.update_v(i)
                    break
            else:
                self.search = 0
                self.tip(f'未找到项目：{search}')

        def _bt(event=None):
            nonlocal last_search
            search = self.search_v.get()

            if not search:
                self.tip('搜索项目不能为空！')
                return
            elif self.search is not None and last_search == search:
                self.tip(f'继续搜索项目：{search}')
                _search(search)
            else:
                self.tip(f'正在搜索项目：{search}')
                last_search = search
                self.search = 0
                _search(search)

        et.bind("<Return>", _bt)
        bt = self.search_bt = tk.Button(self.rt, text='搜索项目', command=_bt)
        bt.grid(row=r, column=4, columnspan=1)

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
                    self.tip('时间格式错误！')
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

        def name_key(_s):
            s = _s[0]
            if ' - ' in s:
                return ' - '.join(s.split(' - ')[::-1])
            return s

        tv.heading("name", text="项目", key=name_key)
        # 设置列宽
        tv.column("time", width=50)
        tv.column("name", width=200)

        def tv_select(event):
            for iid in tv.selection():
                self.update_v(iid)

        tv.bind('<<TreeviewSelect>>', tv_select)  # 绑定新选择项目事件

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
            st = '\t'.join(st)
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
        self.detach_set.clear()
        if len(self.data) > 1:
            self.k_tv.selection_set(0)

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
        self.tip_v = tk.StringVar(value='Blog: https://hexo.limour.top/')
        et = self.tip_et = tk.Entry(self.rt, textvariable=self.tip_v, background='#DDDDDD')
        et.grid(row=r, column=1, columnspan=9, ipadx=340, padx=10, pady=10)

    def tip(self, text):
        self.tip_v.set(text)


# ===== 初始化窗口 =====
Wd = Wd()
Wd.rt.title("labs_viewer v0.2 by limour")
Wd.rt.geometry('850x640+10+10')

Wd.rt.mainloop()
