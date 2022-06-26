import re
import requests
from bs4 import BeautifulSoup


html = requests.get('https://kemono.party/fantia/user/6561/post/791687').content.decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
print(re.findall(re.compile(r'\n+(.*?)\n+'), soup.select('.post__user-name')[0].contents[0])[0].replace(' ', ''))


username = re.findall(re.compile(r'\n+(.*?)\n+'), BeautifulSoup(requests.get('https://kemono.party/fantia/user/6561/post/791687').content.decode('utf-8'), 'lxml').select('.post__user-name')[0].contents[0])[0].replace(' ', '')
