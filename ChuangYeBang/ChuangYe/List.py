import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random

# 参数为页码
def get_company_list(page_num):
    url = 'http://www.cyzone.cn/vcompany/list-0-0-' + str(page_num) + '-0-0/0'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html=requests.get(url,header).content.decode()
    # 下载成功
    html_soup=BeautifulSoup(html,'lxml')
    tr=html_soup.find_all('tr',class_='table-plate item')
    indect={}
    for item in tr:
        company_name=item['data-title']
        rounds = item.find('td',class_='table-stage').text
        industry =item.find('td',class_='table-type').text
        date = item.find('td',class_='table-time').text
        company_url = item['data-url']

        indect['创业公司']=company_name
        indect['融资阶段']=rounds
        indect['创业领域']=industry
        indect['成立时间']=date

        # print('创业公司:'+company_name)
        # print('融资阶段:'+rounds)
        # print('创业领域:' + industry)
        # print('成立时间:'+date)
        # print('url:'+company_url)
        # print('--------------------')
    return indect

# 连接数据库
def connect_mysql(table_name):
    connection = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db=table_name,
        charset='utf8'
    )
    return connection


def insert(connection,info_dict,page_num):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO company_list (company_name, rounds, industry, date, page_num ) VALUES ("%s", "%s", "%s", "%s", "%s" )'
    data = ( info_dict['创业公司'], info_dict['融资阶段'] , info_dict['创业领域'] , info_dict['成立时间'] , page_num)
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')

if __name__ == '__main__':

    connection=connect_mysql('chuangye')

    # range第一个参数为起始页   第二个为终止页-1
    for num in range(656,1000):

        # s=requests.session()
        proxixy={'http':'114.99.84.57:31284'}

        # time.sleep(random.randint(2,4))

        print('正在解析第'+str(num)+'页')
        url = 'http://www.cyzone.cn/vcompany/list-0-0-' + str(num) + '-0-0/0'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html = requests.get(url, header, proxies=proxixy).content.decode()
        print(html)
        # 下载成功
        html_soup = BeautifulSoup(html, 'lxml')
        tr = html_soup.find_all('tr', class_='table-plate item')
        info_dict = {}
        for item in tr:
            company_name = item['data-title']
            rounds = item.find('td', class_='table-stage').text
            industry = item.find('td', class_='table-type').text
            date = item.find('td', class_='table-time').text
            company_url = item['data-url']

            info_dict['创业公司'] = company_name
            info_dict['融资阶段'] = rounds
            info_dict['创业领域'] = industry
            info_dict['成立时间'] = date

            print('解析成功,执行插入语句')
            insert(connection,info_dict,page_num=num)
            # print('创业公司:'+company_name)
            # print('融资阶段:'+rounds)
            # print('创业领域:' + industry)
            # print('成立时间:'+date)
            # print('url:'+company_url)
            # print('--------------------')
