# KemonoCrawler
一个针对该网站的下载爬虫（当前只支持下载图片功能，后续完善）

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

thread_1 = threading.Thread(target = DownloadPicOrgin)
thread_2 = threading.Thread(target = DownloadPicOrgin)
thread_3 = threading.Thread(target = DownloadPicOrgin)
thread_4 = threading.Thread(target = bar_, args = (len(all_links),))
[add]thread_n = threading.Thread(target = DownloadPicOrgin)
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
[add]thread_n.start()
thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()
[add]thread_n.join()
```

