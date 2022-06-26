import requests
from bs4 import BeautifulSoup

url = 'https://kemono.party/fantia/user/6561/post/784019'
host = 'https://kemono.party'


def DownloadPicOrgin(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    data = soup.select('.post__thumbnail a')

    for trumbpic in data:
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
        with open('D:/a.jpg','wb') as f:
            f.write(data.content)

        

DownloadPicOrgin(url)