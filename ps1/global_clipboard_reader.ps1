Add-Type -AssemblyName System.Windows.Forms

Add-Type -ReferencedAssemblies System.Windows.Forms,System.Drawing @"
using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class HotkeyForm : Form
{
    [DllImport("user32.dll")]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

    [DllImport("user32.dll")]
    public static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    public const int WM_HOTKEY = 0x0312;
    public const uint MOD_CONTROL = 0x0002;

    public event EventHandler HotkeyPressed;

    private int hotkeyId;

    public HotkeyForm(int id)
    {
        hotkeyId = id;
        ShowInTaskbar = false;
        WindowState = FormWindowState.Minimized;
        FormBorderStyle = FormBorderStyle.FixedToolWindow;
    }

    protected override void SetVisibleCore(bool value)
    {
        base.SetVisibleCore(false);
    }

    public bool RegisterCtrlB()
    {
        return RegisterHotKey(this.Handle, hotkeyId, MOD_CONTROL, (uint)Keys.B);
    }

    protected override void WndProc(ref Message m)
    {
        if (m.Msg == WM_HOTKEY && (int)m.WParam == hotkeyId)
        {
            if (HotkeyPressed != null)
                HotkeyPressed(this, EventArgs.Empty);
        }
        base.WndProc(ref m);
    }

    protected override void OnFormClosed(FormClosedEventArgs e)
    {
        UnregisterHotKey(this.Handle, hotkeyId);
        base.OnFormClosed(e);
    }
}
"@

$filePath = Read-Host "请输入文本文件路径"

if (-not (Test-Path $filePath)) {
    Write-Host "文件不存在：$filePath"
    exit
}

$lines = Get-Content -Path $filePath -Encoding utf8
$script:index = 0

function Get-NextNonEmptyLine {
    param(
        [string[]]$Lines,
        [ref]$Index
    )

    while ($Index.Value -lt $Lines.Count) {
        $text = $Lines[$Index.Value].Trim()
        $Index.Value++

        if ($text -ne "") {
            return $text
        }
    }

    return $null
}

$form = New-Object HotkeyForm(1001)

$registered = $form.RegisterCtrlB()
if (-not $registered) {
    Write-Host "注册全局热键 Ctrl+B 失败，可能已被其他程序占用"
    exit
}

Write-Host "已启动后台全局监听 Ctrl+B"
Write-Host "每按一次 Ctrl+B，将复制文件中的下一条非空行到剪贴板"
Write-Host "文本文件按 UTF-8 编码读取"
Write-Host "文件读完后程序自动退出"

$form.add_HotkeyPressed({
    $text = Get-NextNonEmptyLine -Lines $lines -Index ([ref]$script:index)

    if ($null -ne $text) {
        [System.Windows.Forms.Clipboard]::SetText($text)
        Write-Host "已复制：$text"
    }
    else {
        Write-Host "文本文件已全部读取完毕，程序退出"
        $form.Close()
        [System.Windows.Forms.Application]::ExitThread()
    }
})

[System.Windows.Forms.Application]::Run($form)
