import requests
from bs4 import BeautifulSoup
import json
import re


# 参数为页码
def get_company_list(page_num):
    url = 'http://www.cyzone.cn/vcompany/list-0-0-' + str(page_num) + '-0-0/0'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html=requests.get(url,header).content.decode()
    # 下载成功
    html_soup=BeautifulSoup(html,'lxml')
    tr=html_soup.find_all('tr',class_='table-plate item')
    indect={}
    company_url_list=[]
    for item in tr:
        company_name=item['data-title']
        company_url = item['data-url']
        company_url_list.append(company_url)
        print('创业公司:'+company_name+' url:'+company_url)
        print('--------------------')
    return company_url_list

# 公司简介+工商信息
def get_info(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, header).content.decode()
    html_soup=BeautifulSoup(html,'lxml')
    # li=html_soup.find('li',class_='time').text
    company_name=html_soup.find('li',class_='name').text
    company_href=html_soup.find('a',rel='nofollow').text
    introduction=html_soup.find('div',class_='info-box').text.replace('  ','')

    bussess_info=html_soup.find('div',class_='qcc')
    registered_num=bussess_info.find_all('p')[0].text
    state=bussess_info.find_all('p')[1].text
    legal_repre=bussess_info.find_all('p')[2].text
    shareholder = bussess_info.find_all('p')[3].text.replace(' ','')
    company_type = bussess_info.find_all('p')[4].text
    found = bussess_info.find_all('p')[5].text
    egistered_capital = bussess_info.find_all('p')[6].text
    address = bussess_info.find_all('p')[7].text


    # print('公司名称:'+company_name)
    # print('公司官网:'+company_href)
    # print('公司简介:'+introduction)
    # print('工商信息:')
    # print(registered_num)
    # print(state)
    # print(legal_repre)
    # print(shareholder)
    # print(company_type)
    # print(found)
    # print(egistered_capital)
    # print(address)
    # print('===============================================')

    return company_name

# 公司招聘职位:
def get_recruitment(company_name):
    url='http://api.lagou.com/cooperation/data/api/AD__cyzone_words?companyName='+company_name
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, header).content.decode().replace('success_jsonpCallback(', '').replace(')', '')
    list = json.loads(html)
    for info in list:
        # info_dict=json.loads(info)
        print('招聘公司:' + info['companyName'])
        print('招聘职位:' + info['positionName'])
        print('招聘链接:' + info['posiitonDetailUrl'])
        print('所属行业:' + info['industryField'])
        print('薪资:' + info['salary'])
        print('城市:' + info['city'])
        print('----------------')

# 公司动态获取
def get_trend(company_url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(company_url, header).content.decode()
    html_soup = BeautifulSoup(html, 'lxml')
    div = html_soup.find('div', class_='list')
    items = div.find_all('div', class_='item')
    for item in items:
        date = item.find('span', class_='time').text
        title = item.find('div', class_='title').text
        info = item.find('p').text
        print('日期:' + date)
        print('标题:' + title)
        print('内容:' + info)
        print('===============')

if __name__ == '__main__':
    # url='http://www.cyzone.cn/r/20160618/27526.html'
    # get_info(url)

    # range第一个参数为起始页   第二个为终止页-1
    for num in range(1, 2):
        print('正在解析第' + str(num) + '页')
        urllist = get_company_list(num)

        # for url in urllist:
        #     company_name=get_info(url)
        #     get_trend(company_name)
            # get_recruitment(company_name)