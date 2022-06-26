import re
import requests
from bs4 import BeautifulSoup

html = requests.get('https://kemono.party/fantia/user/17148/post/1244218').content.decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
#data = soup.select('.post__attachment-link')[0].contents[0].replace(' ','')
data = soup.select('.post__attachment-link')

for dat in data:
    x = dat.contents[0].replace('\n', '').replace(' ','')

#url = 'url'
#print('\n [main(info)]: 当前链接无可用加载资源，跳过... {}'.format(url))

#data = requests.get('https://kemono.party/data/31/8b/318b056fb4479c17dd0bdbf868aa63142ea01b19ec6d8b505212fc3924903065.zip?f=Aqua%28Tier2%29.zip')











