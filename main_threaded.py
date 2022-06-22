# Author: zch9241 <github.com/zch9241><zch2426936965@gmail.com>
# 
# 版权声明：该软件（KemonoCrawler）为「zch」所有，转载请附上本声明。保留所有权利。
# License: Apache 2.0
# 
# version: 1.1
# 版本更新说明:
# v1.0: 程序首个版本
# v1.1: 增加多线程下载功能；增加下载进度显示
# 
# 


import os
import re
import threading

import requests
from bs4 import BeautifulSoup
from progress.bar import ChargingBar


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
    links.pop(-1)
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
    return all_links

def DownloadPicOrgin():
    """
    # 下载原图
    """
    global all_links
    global task_done
    while len(all_links) > 0:
        url = all_links.pop()
        html = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        data = soup.select('.post__thumbnail a')
        title = soup.select('.post__title span')    #[<span>雫ちゃん！</span>, <span>(Fantia)</span>]
            
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
            data = requests.get(host + link, headers)

            picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data.url)
            picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
            pic = picname_ + picfile_extensions
            for item in string:
                pic = pic.replace(item, '')
            #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

            with open(pic_path + pic, 'wb') as f:
                f.write(data.content)
                task_done = task_done + 1
                f.close()
            #print('...完成')
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
                data = requests.get(host + link, headers)

                picfile_extensions = re.findall(re.compile(r'.*?(.*?)\?f='), data.url)
                picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
                pic = picname_ + '_' + str(i) + picfile_extensions
                for item in string:
                    pic = pic.replace(item, '')
                #print('[main(info)]: 准备下载 {}'.format(pic), end = '')

                with open(pic_path + pic, 'wb') as f:
                    f.write(data.content)
                    task_done = task_done + 1
                    f.close()
                #print('...完成')
        

def bar_(max):
    task_done_ = 0
    with ChargingBar('下载进度 (共{}个链接): '.format(max), max = max) as bar:
        while True:
            if task_done - task_done_ > 0:
                for _ in range(task_done - task_done_):
                    bar.next()
                task_done_ = task_done
            elif task_done_ == max:
                break
                



if __name__ == '__main__':
    project_path = os.getcwd()
    pic_path = project_path + '.\\pics\\'

    task_done = 0
    string = ['/',':','*','?','<','>','|','\\','"']
    host = 'https://kemono.party'

    #request_url = 'https://kemono.party/fantia/user/6561'
    request_url = str(input('[main(input)]: 请输入完整链接: '))

    html = requests.get(request_url)
    status = html.status_code

    #检查网络连接
    if status == 200:
        print('[main(info)]: 连接成功！')
        html = html.content.decode('utf-8')
    else:
        print('[main(warning)]: 请检查网络连接，状态码:{}'.format(status))
    
    pageamount = GetPageAmount(html = html)
    links_list = FormatPageLinks(amount = pageamount)
    all_links = GetAllpages(links_list = links_list)


    thread_1 = threading.Thread(target = DownloadPicOrgin)
    thread_2 = threading.Thread(target = DownloadPicOrgin)
    thread_3 = threading.Thread(target = DownloadPicOrgin)
    thread_4 = threading.Thread(target = bar_, args = (len(all_links),))
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()

    print('[main(info)]: 所有插画下载完成！')
