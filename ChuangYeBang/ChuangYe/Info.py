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
    company_url_list=[]
    for item in tr:
        company_name=item['data-title']
        company_url = item['data-url']
        company_url_list.append(company_url)
        # print('创业公司:'+company_name+' url:'+company_url)
        # print('--------------------')
    return company_url_list

def get_info(html):
    company_dict={}
    html_soup = BeautifulSoup(html, 'lxml')
    # li=html_soup.find('li',class_='time').text
    company_name = html_soup.find('li', class_='name').text
    company_all_name=html_soup.find('li', class_='time').text
    company_all_name=company_all_name[5:]
    # 标签
    tag_soup=html_soup.find('div',class_='info-tag clearfix')
    time=tag_soup.find_all('li')[0].text
    place=tag_soup.find_all('li')[1].text
    tag=tag_soup.find_all('a')
    tags=''
    for text in tag:
        tags+=text.text

    tags=tags[2:]
    tags=tags.replace('天使轮','').replace('战略投资','').replace('尚未获投','').replace('新三板','').replace('种子轮','').replace('A轮','').replace('B轮','').replace('Pre-A','').replace('IPO','')

    company_href = html_soup.find('a', rel='nofollow').text
    introduction = html_soup.find('div', class_='info-box').text.replace('\n', '').replace('\t', '').replace('\r', '')



    company_dict['公司名称']=company_name
    company_dict['公司全称'] = company_all_name
    company_dict['公司官网'] = company_href
    company_dict['成立时间'] = time
    company_dict['地点'] = place
    company_dict['标签'] = tags
    company_dict['公司简介'] = introduction

    # print('公司名称:' + company_name)
    # print(company_all_name)
    # print('公司官网:' + company_href)
    # print('成立时间'+time)
    # print('地点:'+place)
    # print('融资情况:'+rounds)
    # print('标签:'+tags)
    # print('公司简介:' + introduction)
    print('===============================================')
    return company_dict

# 连接数据库
def connect_mysql(db_name):
    connection = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db=db_name,
        charset='utf8'
    )
    return connection


def insert(connection, company_dict, page_num):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO introduction (company_name, all_name, company_url, time, place, tips, info, page_num ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )'
    data = (company_dict['公司名称'], company_dict['公司全称'] , company_dict['公司官网'] , company_dict['成立时间'] , company_dict['地点'], company_dict['标签'] , company_dict['公司简介'] , page_num)
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')


if __name__ == '__main__':
    # range第一个参数为起始页   第二个为终止页-1
    connection=connect_mysql('chuangye')

    for num in range(1, 2):
        print('正在解析第' + str(num) + '页')
        urllist = get_company_list(num)
        print('解析出'+str(len(urllist))+'个url')
        for company_url in urllist:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            time.sleep(random.randint(2, 4))  # 随机休眠
            # 得到源码
            html = requests.get(company_url, header).content.decode()

            # 取得简介插入 introduction 表
            company_dict=get_info(html)
            print('解析成功,执行插入语句')
            insert(connection, company_dict, num)

