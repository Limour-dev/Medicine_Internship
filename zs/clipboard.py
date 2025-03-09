import ctypes
from ctypes import wintypes

# 定义一些常量
CF_TEXT = 1
GMEM_MOVEABLE = 0x0002

# 加载必要的DLL
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 定义函数原型
user32.OpenClipboard.restype = wintypes.BOOL
user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.CloseClipboard.restype = wintypes.BOOL
user32.EmptyClipboard.restype = wintypes.BOOL
user32.SetClipboardData.restype = wintypes.HANDLE
user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]

kernel32.GlobalAlloc.restype = wintypes.HGLOBAL
kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalLock.restype = wintypes.LPVOID
kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL
kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]


# 打开剪贴板
def open_clipboard():
    if not user32.OpenClipboard(None):
        raise ctypes.WinError(ctypes.get_last_error())


# 关闭剪贴板
def close_clipboard():
    if not user32.CloseClipboard():
        raise ctypes.WinError(ctypes.get_last_error())


# 将文本放入剪贴板
def set_clipboard_text(text):
    # 打开剪贴板
    open_clipboard()
    try:
        # 清空剪贴板
        user32.EmptyClipboard()

        # 将文本转换为字节
        text_bytes = text.encode('utf-8') + b'\0'  # 以 null 字节结束

        # 分配内存
        h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(text_bytes))
        if not h_global:
            raise ctypes.WinError(ctypes.get_last_error())

        # 锁定内存以获取指针
        ptr = kernel32.GlobalLock(h_global)
        if not ptr:
            kernel32.GlobalFree(h_global)
            raise ctypes.WinError(ctypes.get_last_error())

        # 将文本复制到分配的内存中
        ctypes.memmove(ptr, text_bytes, len(text_bytes))

        # 解锁内存
        kernel32.GlobalUnlock(h_global)

        # 将剪贴板内容设置为我们的文本
        if not user32.SetClipboardData(CF_TEXT, h_global):
            kernel32.GlobalFree(h_global)
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        # 关闭剪贴板
        close_clipboard()


# 示例用法
if __name__ == "__main__":
    try:
        set_clipboard_text("Hello, World!")
        print("Text has been copied to clipboard.")
    except Exception as e:
        print(f"Error: {e}")
