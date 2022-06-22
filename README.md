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
>pip install progress
```

**三、运行程序**
- 输入完整的网址，Enjoy it!
- 若想在有带宽闲置时提升下载速度，请尝试在此段代码后增加线程：
```
<ln 277>

for i in range(5):    #将5改为更大的数字
    thread = threading.Thread(target = DownloadPicOrgin)
    threads__.append(thread)
```

