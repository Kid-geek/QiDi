import requests
from bs4 import BeautifulSoup


url='http://www.cyzone.cn/r/20160618/30265.html'
header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
html = requests.get(url, header).content.decode()
html_soup=BeautifulSoup(html,'lxml')
div=html_soup.find('div',class_='live')
stage=div.find_all('td')[4]

print('阶段'+stage)
print(div)