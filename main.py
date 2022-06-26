# Author: zch9241 <github.com/zch9241><zch2426936965@gmail.com>
# 
# 版权声明：该软件（KemonoCrawler）为「zch」所有，转载请附上本声明。保留所有权利。
# License: Apache 2.0
# 
# version: 1.3.1
# 
# 版本更新说明:
# v1.0: 程序首个版本
# v1.1: 增加多线程下载功能；增加下载进度显示
# v1.2: 修正下载进度显示；增加文件下载功能
# v1.3: 增加下载投稿时将文本(content)，图片，文件(files)打包成一个文件夹的可选下载功能(default)
# v1.3.1: 更改更友好的下载进度条显示，重构下载方法及Url分配方式，修复已知错误
# 
# 

import os
import re
import threading

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
#from progress.bar import ChargingBar


def GetPageAmount(html):
    """
    # 获取概览页总数
    - html: 第一概览页
    - return: 概览页总数
    """
    soup_ = BeautifulSoup(html, 'lxml')
    data = soup_.select('#paginator-top menu li a')
    if data == []:
        print('[main(info)]: 共 1 张概览页')  #只有一页
        return 1

    else:
        lastpage = str(data[-2])     #寻找最后一页的元素
        #print(lastpage)
        pattern = re.compile(r'(\d+)\n+')   #寻找元素中的数字文本['(\d+)‘表示提取数字，'\n+'表示换行符]
        pageamount_list = re.findall(pattern = pattern, string = lastpage)
        pageamount = int(pageamount_list[0])
        print('[main(info)]: 共 {} 张概览页'.format(pageamount))
        return pageamount

def FormatPageLinks(amount):
    """
    # 将页面数格式化为链接
    - amount: 页面数
    - return: 格式化后的链接
    """
    global request_url
    o_list = []
    links_list = []
    for o in range(1, amount + 1):
        o_ = 25 * (o - 1)
        o_list.append(o_)
    for item in o_list:
        link = request_url + '?o=' + str(item)
        links_list.append(link)
    return links_list

def GetEachPage(html_):
    """
    # 获取单页的内容链接
    - html: 每一概览页
    """
    links = []
    soup = BeautifulSoup(html_, 'lxml')
    data = soup.select('.fancy-link[rel="noopener noreferrer"]')
    
    for link in data:
        link_orgi = host + link['href']
        links.append(link_orgi)
    links.pop()
    return links

def GetAllpages(links_list):
    """
    # 获取所有概览页的内容链接
    """
    all_links = []
    for link in links_list:
        html = requests.get(link).content.decode('utf-8')
        detail_links = GetEachPage(html_ = html)
        all_links = all_links + detail_links

    print('[main(info)]: 所有详情页链接获取成功。长度 {}'.format(len(all_links)))
    #print(all_links)

    return all_links

def Downloader(url):
    """
    下载
    """
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    data = soup.select('.post__thumbnail a')    #pic
    data_file_url = soup.select('.post__attachment-link')    #flie_url
    title = soup.select('.post__title span')    #[<span>雫ちゃん！</span>, <span>(Fantia)</span>]
    

    #filedownloader
    if len(data_file_url) == 1:
        file_url = host + data_file_url[0]['href']
        file_name = soup.select('.post__attachment-link')[0].contents[0].replace('\n', '').replace(' ','')

        file_bytes = requests.get(file_url)

        with open(file_path + file_name, 'wb') as f:
            f.write(file_bytes.content)
            f.close()
    elif len(data_file_url) == 0:
        pass
    else:
        file_name_list = []
        file_url_list = []
        for file_name_ in data_file_url:
            file_name = file_name_.contents[0].replace('\n', '').replace(' ','')
            file_name_list.append(file_name)

        for file_url_ in data_file_url:
            file_url = host + file_url_['href']
            file_url_list.append(file_url)
            
        for i in range(len(file_name_list)):
            with open(file_path + file_name_list[i], 'wb') as f:
                f.write(requests.get(file_url_list[i]).content)
                f.close()


    #picdownloader
    if len(title) == 1:
            picname_ = re.findall(re.compile(r'\<span>+(.*?)\</span>+'),title[0])[0]
    else:
        picname_ = ''
        for subtitle in title:
            subtitle = str(subtitle)
            picname = re.findall(re.compile(r'\<span>+(.*?)\</span>+'),subtitle)
            picname_ = picname_ + picname[0]
  
    if len(data) == 1:
        trumbpic = data[0]
        link = trumbpic['href']
        headers = {
            ':authority': 'kemono.party',
            ':method': 'GET',
            ':scheme': 'https',
            ':path': link,
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'cookie': '__ddg1_=hiv3SY00KuBX0ApYjacE; _pk_id.1.5bc1=91fc9c392a521176.1655783181.',
            'referer': url,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        data__ = requests.get(host + link, headers)

        picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data__.url)
        picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
        pic = picname_ + picfile_extensions
        for item in string:
            pic = pic.replace(item, '')
        #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

        with open(pic_path + pic, 'wb') as f:
            f.write(data__.content)
            f.close()
            #print('...完成')
    elif len(data) == 0:    #返回空列表，即没有图片
            pass
    else:
        i = 0
        for trumbpic in data:
            i = i + 1
            link = trumbpic['href']
            headers = {
                ':authority': 'kemono.party',
                ':method': 'GET',
                ':scheme': 'https',
                ':path': link,
                'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-US;q=0.6',
                'dnt': '1',
                'cookie': '__ddg1_=hiv3SY00KuBX0ApYjacE; _pk_id.1.5bc1=91fc9c392a521176.1655783181.',
                'referer': url,
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'image',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
            data__ = requests.get(host + link, headers)

            picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data__.url)
            picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
            pic = picname_ + '_' + str(i) + picfile_extensions
            for item in string:
                pic = pic.replace(item, '')
            #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

            with open(pic_path + pic, 'wb') as f:
                f.write(data__.content)
                f.close()
            #print('...完成')
    if len(data_file_url) == 0 and len(data) == 0:
        print('\n----[main(info)]: 当前链接无可用加载资源，跳过... {}'.format(url))

def Downloader_(url, ignore_texts):
    """
    下载(以每一个POST作为文件夹)
    """

    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    data = soup.select('.post__thumbnail a')    #pic
    data_file_url = soup.select('.post__attachment-link')    #flie_url
    title = soup.select('.post__title span')    #[<span>雫ちゃん！</span>, <span>(Fantia)</span>]


    if len(title) == 1:
            foldertitle = re.findall(re.compile(r'\<span>+(.*?)\</span>+'),title[0])[0]
    else:
        foldertitle = ''
        for subtitle in title:
            subtitle = str(subtitle)
            title_ = re.findall(re.compile(r'\<span>+(.*?)\</span>+'),subtitle)
            foldertitle = foldertitle + title_[0]

        for item in string:
            foldertitle = foldertitle.replace(item, '')
        
    #整合绝对路径
    Absolute_path = file_path + username + '\\' + foldertitle + '\\'
    try:
        os.mkdir(Absolute_path)
    except FileExistsError:
        pass

    #textdownloader
    if ignore_texts == False:
        #data_contents = soup.select('.post__content')[0].contents[0]
        _data = soup.select('.post__content')
        if _data == []:
            pass
        else:
            data_contents = _data[0].text
        
            with open(file = Absolute_path + 'content.txt', mode = 'w', encoding = 'utf-8') as f:
                f.write(data_contents)
                f.close()

    #filedownloader
    if len(data_file_url) == 1:
        file_url = host + data_file_url[0]['href']
        file_name = soup.select('.post__attachment-link')[0].contents[0].replace('\n', '').replace(' ','')

        file_bytes = requests.get(file_url)

        with open(Absolute_path + file_name, 'wb') as f:
            f.write(file_bytes.content)
            f.close()
    elif len(data_file_url) == 0:
        pass
    else:
        file_name_list = []
        file_url_list = []
        for file_name_ in data_file_url:
            file_name = file_name_.contents[0].replace('\n', '').replace(' ','')
            file_name_list.append(file_name)

        for file_url_ in data_file_url:
            file_url = host + file_url_['href']
            file_url_list.append(file_url)
            
        for i in range(len(file_name_list)):
            with open(Absolute_path + file_name_list[i], 'wb') as f:
                f.write(requests.get(file_url_list[i]).content)
                f.close()


    #picdownloader
    if len(data) == 1:
        trumbpic = data[0]
        link = trumbpic['href']
        headers = {
            ':authority': 'kemono.party',
            ':method': 'GET',
            ':scheme': 'https',
            ':path': link,
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-US;q=0.6',
            'dnt': '1',
            'cookie': '__ddg1_=hiv3SY00KuBX0ApYjacE; _pk_id.1.5bc1=91fc9c392a521176.1655783181.',
            'referer': url,
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        data__ = requests.get(host + link, headers)

        picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data__.url)
        picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
        pic = '0' + picfile_extensions
        for item in string:
            pic = pic.replace(item, '')
        #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

        with open(Absolute_path + pic, 'wb') as f:
            f.write(data__.content)
            f.close()
        #print('...完成')
    elif len(data) == 0:    #返回空列表，即没有图片
        pass
    else:
        i = 0
        for trumbpic in data:
            i = i + 1
            link = trumbpic['href']
            headers = {
                ':authority': 'kemono.party',
                ':method': 'GET',
                ':scheme': 'https',
                ':path': link,
                'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-US;q=0.6',
                'dnt': '1',
                'cookie': '__ddg1_=hiv3SY00KuBX0ApYjacE; _pk_id.1.5bc1=91fc9c392a521176.1655783181.',
                'referer': url,
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'image',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
            }
            data__ = requests.get(host + link, headers)

            picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data__.url)
            picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
            pic = str(i) + picfile_extensions
            for item in string:
                pic = pic.replace(item, '')
            #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

            with open(Absolute_path + pic, 'wb') as f:
                f.write(data__.content)
                f.close()
            #print('...完成')


def jutils(mode):
    global file_path
    project_path = os.getcwd()
    try:
        #print('[main(info)]: 尝试创建 Downloads 文件夹...')
        os.mkdir(project_path + '\\Downloads\\')
    except FileExistsError:
        pass
    
    if mode == 0:
        global pic_path

        pic_path = project_path + '\\Downloads\\pics\\'
        file_path = project_path + '\\Downloads\\file\\'
    
        try:
            os.mkdir(pic_path)
        except FileExistsError:
            pass
        try:
            os.mkdir(file_path)
        except FileExistsError:
            pass

    else:   #mode == 1
        file_path = project_path + '\\Downloads\\'
        try:
            os.mkdir(file_path)
        except:
            pass

def dumper(list, n):
    """
    ```
    e.g.
    lst = [1,2,3,4,5,6,7,8,9]
    n = 5
    result = [[1,2],[3,4],[5,6],[7,8],[9]]
    ```
    """
    intercept = len(list) // n
    def foo(lst, intercept):
        sp_lst = []
        if len(lst) - intercept * n < intercept:
            for _ in range(n):
                sublist = lst[0:intercept]
                sp_lst.append(sublist)
                for item in sublist:
                    lst.remove(item)
            if lst != []:
                sp_lst.append(lst)
        else:
            intercept = intercept + 1
            sp_lst = foo(lst, intercept)
        return sp_lst
    sp_lst = foo(list, intercept)
    if len(sp_lst) > n:
        m = sp_lst[-1]
        for n in range(len(m)):
            sp_lst[-1 - (n + 1)].append(m[0])
            m.remove(m[0])
    for p in sp_lst:
        if p == []:
            sp_lst.remove(p)
    return sp_lst

def switcher(urls, mode = None,ignore_texts = None):
    """
    - mode = 0: 将图片和文件分开下载
    - mode = 1: 将图片和文件打包下载，同时下载文本
    """
    ThreadName = threading.current_thread().name
    urlbar = tqdm(urls, colour = 'blue',leave = False)
    for url in urlbar:
        url_short = url.split('/')[-1]
        if mode == 0:
            urlbar.set_description('{} 正在下载: {}'.format(ThreadName, url_short))
            Downloader(url)
        elif mode == 1:
            if ignore_texts != None:
                if ignore_texts == False:
                    urlbar.set_description('{} 正在下载: {}'.format(ThreadName, url_short))
                    Downloader_(url, False)
                elif ignore_texts == True:
                    urlbar.set_description('{} 正在下载: {}'.format(ThreadName, url_short))
                    Downloader_(url, True)
                else:
                    print('[main(wran)]: 模式错误 ignore_texts = {}'.format(ignore_texts))
        elif mode == None:
            urlbar.set_description('{} 正在下载: {}'.format(ThreadName, url_short))
            Downloader(url)
        else:
            print('[main(warn)]: 模式错误 mode = {}'.format(mode))

if __name__ == '__main__':
    #----config----
    # mode = 0: 将图片和文件分开下载
    # mode = 1: 将图片和文件打包下载
    mode = 1
    # ignore_texts: 是否下载文本（仅在 mode = 1 时可用）
    ignore_texts = False
    # n: 下载线程数量
    n = 5
    #----config_end----

    pic_path = ''
    file_path = ''

    string = ['/',':','*','?','<','>','|','\\','"']
    host = 'https://kemono.party'


    print('[main(info)]: config: mode = {} \n                      ignore_texts = {} \n                      n = {}'.format(mode, ignore_texts, n))

    #request_url = 'https://kemono.party/fantia/user/6561'
    request_url = str(input('[main(input)]: 请输入完整链接: '))
    l = request_url.split('/',3)[-1]
    source_from = l.split('/')[0]
    headers = {
        #':authority': 'kemono.party',
        #':method': 'GET',
        #':path': l,
        #':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': '__ddg1_=hiv3SY00KuBX0ApYjacE; _pk_id.1.5bc1=91fc9c392a521176.1655783181.',
        'dnt': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    html = requests.get(request_url, headers = headers)
    status = html.status_code
    
    #检查网络连接
    if status == 200:
        print('[main(info)]: 连接成功！')
        html = html.content.decode('utf-8')
    else:
        print('[main(warning)]: 请检查网络连接，状态码:{}'.format(status))
        print('\n[main(info)]: 即将退出主程序...', end = '')
        os.system('pause')

    pageamount = GetPageAmount(html = html)
    links_list = FormatPageLinks(amount = pageamount)
    all_links = GetAllpages(links_list = links_list)


    #获取用户名
    html = requests.get(all_links[0]).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    username = re.findall(re.compile(r'\n+(.*?)\n+'), soup.select('.post__user-name')[0].contents[0])[0].replace(' ', '')

    username = username + '(' + source_from + ')'

    jutils(mode = mode)
    try:
        os.mkdir(file_path + username + '\\')
    except FileExistsError:
        pass



    splited_links = dumper(list = all_links, n = n)
    threads__ = []
    for i in range(n):
        thread = threading.Thread(target = switcher, args = (splited_links[i], mode, ignore_texts))
        threads__.append(thread)

    for a in threads__:
        a.start()

    for b in threads__:
        b.join()

    print('\n[main(info)]: 所有插画下载完成！',end = '')
    os.system('pause')
