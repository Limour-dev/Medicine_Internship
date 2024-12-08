# Medicine_Internship
![1733654310086](https://github.com/user-attachments/assets/76fdadfd-e218-48d4-98ce-7ded999e4adc)

文件传递：https://hexo.limour.top/internal-network-uses-p4wnp1-to-transfer-file
## 打包成 exe
+ 下载最新的upx：https://upx.github.io/
```powershell
conda create -n pyinstaller conda-forge::pyinstaller
conda activate pyinstaller 
pyinstaller --upx-dir "D:\D\upx" labs_viewer.pyw --clean
```
