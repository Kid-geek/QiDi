import requests
from bs4 import BeautifulSoup
import time
def get_url(page_num):
    time.sleep(2)
    url_list=[]
    for num in range(1, int(page_num) + 1):
        url = 'http://www.creditah.gov.cn/remote/480/index_'+str(num)+'.htm'
        header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html = requests.get(url, headers=header).content.decode()
        table_soup = BeautifulSoup(html, 'lxml')
        table=table_soup.find('table',class_='bordered')
        div_soup=BeautifulSoup(str(table),'lxml')
        div=div_soup.find_all('div')
        for item in div:
            a_soup=BeautifulSoup(str(item),'lxml')
            a=a_soup.find('a')['href']
            href='http://www.creditah.gov.cn'+a
            url_list.append(href)
        print('成功解析' + str(len(url_list)) + '个url')
    # print(url_list)
    return url_list

def get_info(url):
    time.sleep(2)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, headers=header).content.decode()
    info_dict = {}
    html_soup = BeautifulSoup(html, 'lxml')

    table=html_soup.find('table',class_='infor')
    td_soup=BeautifulSoup(str(table),'lxml')
    info_dict['统一社会信用代码']=td_soup('td')[1].text.replace(' ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['纳税人识别号']=td_soup.find_all('td')[3].text.replace(' ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['企业名称'] = td_soup.find_all('td')[5].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['评定年限'] = td_soup.find_all('td')[7].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['信用等级'] = td_soup.find_all('td')[9].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['评定机关'] = td_soup.find_all('td')[11].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['评定日期'] = td_soup.find_all('td')[13].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['组织机构代码'] = td_soup.find_all('td')[15].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['工商注册号'] = td_soup.find_all('td')[17].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['统一识别号'] = td_soup.find_all('td')[19].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    print('url:'+url)
    print(info_dict)
    print('----------------------------------')
    print()
    return info_dict

if __name__ == '__main__':
    url_list=get_url(1)
    print('共' + str(len(url_list)) + '个页面')
    for url in url_list:
        get_info(url)