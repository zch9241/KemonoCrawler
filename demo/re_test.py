import re

#string = 'https://data8.kemono.party/data/ad/26/ad26917457da07a22f8b2c0adf15b733e3af93d839deaa38a7241797f014397e.png?f=bac77975-f3b2-4388-95db-10ce2787686f.png&%3Aauthority=kemono.party&%3Amethod=GET&%3Ascheme=https&%3Apath=%2Fdata%2Fad%2F26%2Fad26917457da07a22f8b2c0adf15b733e3af93d839deaa38a7241797f014397e.png%3Ff%3Dbac77975-f3b2-4388-95db-10ce2787686f.png&accept=image%2Favif%2Cimage%2Fwebp%2Cimage%2Fapng%2Cimage%2Fsvg%2Bxml%2Cimage%2F%2A%2C%2A%2F%2A%3Bq%3D0.8&accept-encoding=gzip%2C+deflate%2C+br&accept-language=zh-CN%2Czh%3Bq%3D0.9%2Cja%3Bq%3D0.8%2Cen%3Bq%3D0.7%2Cen-US%3Bq%3D0.6&dnt=1&cookie=__ddg1_%3Dhiv3SY00KuBX0ApYjacE%3B+_pk_id.1.5bc1%3D91fc9c392a521176.1655783181.&referer=https%3A%2F%2Fkemono.party%2Ffantia%2Fuser%2F6561%2Fpost%2F784019&sec-ch-ua=%22+Not+A%3BBrand%22%3Bv%3D%2299%22%2C+%22Chromium%22%3Bv%3D%22102%22%2C+%22Google+Chrome%22%3Bv%3D%22102%22&sec-ch-ua-mobile=%3F0&sec-ch-ua-platform=%22Windows%22&sec-fetch-dest=image&sec-fetch-mode=no-cors&sec-fetch-site=same-origin&user-agent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F102.0.0.0+Safari%2F537.36'

#pattern = re.compile(r'.*?(.*?)\?f=')
#picfile_extensions = re.findall(pattern,string)
#picfile_extensions = '.' + str(picfile_extensions[0]).split('.')[-1]
#print(picfile_extensions)


string = ['/',':','*','?','<','>','|','\\','"']

    

