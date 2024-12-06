# Medicine_Internship
文件传递：https://hexo.limour.top/internal-network-uses-p4wnp1-to-transfer-file
## 打包成 exe
+ 下载最新的upx：https://upx.github.io/
```powershell
conda create -n pyinstaller conda-forge::pyinstaller
conda activate pyinstaller 
pyinstaller --upx-dir "D:\D\upx" labs_viewer.pyw --clean
```
