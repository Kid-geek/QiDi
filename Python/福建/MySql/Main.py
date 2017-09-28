import pymysql
import requests
from bs4 import BeautifulSoup
import time


def connection():
    connection = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='anhui',
        charset='utf8'
    )
    return connection

def insert(connection,info_dict):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO 失信 (法人名称, 案号, 法人代表, 执行程序, 执行法院, 组织机构代码, 案由, 地址, 执行依据, 是否撤销, 撤销日期, 统一社会信用代码, 法院编号, 案由编号, 执行标的金额元, 强制履行金额元， ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", )'
    data = (info_dict['法人名称'],
            info_dict['案号'],
            info_dict['法人代表'] ,
            info_dict['执行程序'],
            info_dict['执行法院'] ,
            info_dict['组织机构代码'],
            info_dict['案由'] ,
            info_dict['地址'] ,
            info_dict['执行依据'] ,
            info_dict['是否撤销'] ,
            info_dict['撤销日期'],
            info_dict['统一社会信用代码'] ,
            info_dict['法院编号'] ,
            info_dict['案由编号'] ,
            info_dict['执行标的金额（元）'] ,
            info_dict['强制履行金额（元）'] ,
            )
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')


def get_url(page_num):
    time.sleep(2)
    url_list=[]
    for num in range(1, int(page_num) + 1):
        url = 'http://www.creditah.gov.cn/remote/484/index_'+str(num)+'.htm'
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
    info_dict['法人名称']=td_soup('td')[1].text.replace('  ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['案号']=td_soup.find_all('td')[3].text.replace('  ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['法人代表'] = td_soup.find_all('td')[5].text.replace('  ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['执行程序'] = td_soup.find_all('td')[7].text.replace('  ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['执行法院'] = td_soup.find_all('td')[9].text.replace('  ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['组织机构代码'] = td_soup.find_all('td')[11].text.replace('  ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['案由'] = td_soup.find_all('td')[13].text.replace('  ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['地址'] = td_soup.find_all('td')[15].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['执行依据'] = td_soup.find_all('td')[17].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['是否撤销'] = td_soup.find_all('td')[19].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['撤销日期'] = td_soup.find_all('td')[21].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t','')
    info_dict['统一社会信用代码'] = td_soup.find_all('td')[25].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t',  '')
    info_dict['法院编号'] = td_soup.find_all('td')[27].text.replace('  ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['案由编号'] = td_soup.find_all('td')[29].text.replace('  ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
    info_dict['执行标的金额（元）'] = td_soup.find_all('td')[31].text.replace('  ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
    info_dict['强制履行金额（元）'] = td_soup.find_all('td')[33].text.replace('  ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
    info_dict['发布日期'] = td_soup.find_all('td')[35].text.replace('  ', '').replace('\r', '').replace('\n', '').replace( '\t', '')

    print('url:'+url)
    print(info_dict)
    print('----------------------------------')
    print()
    return info_dict

if __name__ == '__main__':
    url_list=get_url(1)
    print('共' + str(len(url_list)) + '个页面')
    connection=connection()
    for url in url_list:
        info_dict=get_info(url)
        insert(connection,info_dict)