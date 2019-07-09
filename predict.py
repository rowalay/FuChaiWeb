
#code idea from 上海小胖

import requests
from bs4 import BeautifulSoup
import lxml
from collections import Counter

#Send requests
basic_url='http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
headers ={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
response = requests.get(basic_url, headers=headers, timeout=10)
response.encoding = 'utf-8'
htm = response.text

#Analyze content
soup = BeautifulSoup(htm, 'html.parser')

#get the page content
page = int(soup.find('p', attrs={"class": "pg"}).find_all('strong')[0].text)


#combine the url
url_part = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list'

for i in range(1, page+1):
	url = url_part + '_' + str(i) + '.html'

#Use the combined urls to post the requests
res = requests.get(url, headers=headers, timeout=10)
res.encoding = 'utf-8'
context = res.text
soups = BeautifulSoup(context, 'html.parser')

if soup.table is None:
	print('None')
elif soup.table:
	table_rows = soup.table.find_all('tr')
	for row_num in range(2, len(table_rows)-1):
		row_tds = table_rows[row_num].find_all('td')
		ems = row_tds[2].find_all('em')
		result = row_tds[0].string + ',' + row_tds[1].string + ',' + ems[0].string
		print(result)

#Save the requested files
def  save_to_file(content):
	with open('ssq.txt', 'a', encoding='utf-8') as f:
		f.write(content + '\n')


#Use two paramater to record the red and blue balls
red_num = []
blue_num = []

red_num.append(ems[0].string) #r1
red_num.append(ems[1].string) #r2
red_num.append(ems[2].string) #r3
red_num.append(ems[3].string) #r4
red_num.append(ems[4].string)
red_num.append(ems[5].string)
blue_num.append(ems[6].string) #blue ball





red_count = Counter(red_num)
blue_count = Counter(blue_num)

red_sorted = sorted(red_count.items(), key=lambda x: x[0], reverse=False)
blue_sorted = sorted(blue_count.items(), key=lambda x: x[0],reverse=False)

red = red_sorted[0:6]
blue = blue_sorted[0:3]

red = list(map(lambda x:x[0], red))
blue = list(map(lambda x:x[0], blue))

red.sort()
blue.sort()


print('号码高频-1注：' + str(red)+ '|' + blue[0])
#print('号码高频-2注：' + str(red)+ '|' + blue[1])
#print('号码高频-3注：' + str(red)+ '|' + blue[2])

















