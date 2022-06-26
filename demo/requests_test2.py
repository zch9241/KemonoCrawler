import requests
from bs4 import BeautifulSoup


html = requests.get('https://kemono.party/fanbox/user/14496985/post/3968336').content.decode('utf-8')
soup = BeautifulSoup(html, 'lxml')
data = soup.select('.post__content')[0].contents[0]

print(data)

with open(file = 'a.txt', mode = 'x',encoding = 'utf-8') as f:
    f.write(data)
    f.close()