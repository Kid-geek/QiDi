import requests
from bs4 import BeautifulSoup
import re
# 参数为页码
def get_company_list(page_num):
    url='http://www.cyzone.cn/event/list-764-0-'+str(page_num)+'-0-0-0-0/'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html=requests.get(url,header).content.decode()
    # 下载成功
    html_soup=BeautifulSoup(html,'lxml')
    tr=html_soup.find_all('tr',class_='table-plate3')
    company_urllist=[]
    for item in tr:
        company_url=item.find_all('a')[1]['href']
        company_name=item.find_all('a')[1].text
        company_allName=item.find('span',class_='tp2_com').text
        money=item.find('div',class_='money').text
        investment=item.find('td',class_='tp3')['title'].replace(' ','').replace(',','')
        industry =re.search('href="[\s\S]{40,46}">([\s\S]{0,6})</a>',str(item)).group(1)
        rounds = re.search('</div>[\s\S]{0,18}</td>[\s\S]{0,15}<td>([\s\S]{0,6})</td>', str(item)).group(1)
        date = re.search('<td>([\s\S]{10})</td>',str(item)).group(1)
        print('公司名称:'+company_name)
        print('公司全称:'+company_allName)
        print('金额:'+money)
        print('投资方:'+investment)
        print('轮次:'+rounds)
        print('行业:' + industry)
        print('时间:'+str(date))
        print('url:'+company_url)
        company_urllist.append(company_url)
        print('--------------------')
    return company_urllist


def get_info(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, header).content.decode()



if __name__ == '__main__':

    # range第一个参数为起始页   第二个为终止页-1
    for num in range(1,2):
        print('正在解析第'+str(num)+'页')
        urllist=get_company_list(num)
        for url in urllist:

            print()