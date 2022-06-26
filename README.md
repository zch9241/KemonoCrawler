# KemonoCrawler
对相关网站的内容（图片、文件）进行爬取并下载

- 本程序使用'Python@3.10'编写
- 本程序（KemonoCrawler）仅供学习交流，最初目的达成后请自行删除，请勿用于商业用途
- 使用后任何不可知事件都与原作者无关，原作者不承担任何后果

## 使用
**一、运行环境**
  - Python 3
  - （建议）Visual Studio Code
  - （建议）Windows 11

**二、第三方库**
```
cmd:
>pip install requests
>pip install bs4
>pip install lxml
>pip install tqdm
```

**三、运行程序**
- 输入完整的网址，Enjoy it!
- 可选下载设置
```
<ln:445>
#----config----
# mode = 0: 将图片和文件分开下载
# mode = 1: 将图片和文件打包下载
mode = 1
# ignore_texts: 是否下载文本（仅在 mode = 1 时可用）
ignore_texts = False
# n: 下载线程数量
n = 5
#----config_end----
```
