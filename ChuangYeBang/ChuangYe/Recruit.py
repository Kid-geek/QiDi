import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random

def get_re(html):
    bussess_dict = {}
    html_soup = BeautifulSoup(html, 'lxml')
    div=html_soup.find('div',class_='qcc')

    regis_num=div.find_all('p')[0].text
    regis_num=regis_num.replace('注册号:','')
    bussess_dict['注册号']=regis_num

    state=div.find_all('p')[1].text
    state=state.replace('经营状态:','')
    bussess_dict['经营状态'] = state

    legal=div.find_all('p')[2].text
    legal=legal.replace('法定代表:','')
    bussess_dict['法定代表'] = legal

    clearfix=div.find_all('p')[3].text
    clearfix = clearfix.replace('股东:', '').replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
    bussess_dict['股东'] = clearfix

    type=div.find_all('p')[4].text
    type=type.replace('公司类型:','')
    bussess_dict['公司类型'] = type

    time=div.find_all('p')[5].text
    time=time.replace('成立日期:','')
    bussess_dict['成立日期'] = time

    regis_money=div.find_all('p')[6].text
    regis_money=regis_money.replace('注册资本:','')
    bussess_dict['注册资本'] = regis_money

    place=div.find_all('p')[7].text
    place=place.replace('住所:','')
    bussess_dict['住所'] = place

    return bussess_dict



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


def insert_bussess_info(connection, bussess_dict,page_num):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO bussess_info (regis_num, state, legal_repre, shareholder, company_type, date, regis_capital, place, page_num) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )'
    data = (bussess_dict['注册号'], bussess_dict['经营状态'], bussess_dict['法定代表'], bussess_dict['股东'], bussess_dict['公司类型'],
            bussess_dict['成立日期'], bussess_dict['注册资本'], bussess_dict['住所'], page_num)
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据到bussess_info')


if __name__ == '__main__':
    connection=connect_mysql('chuangye')

    company_url='http://www.cyzone.cn/r/20170928/57301.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(company_url, header).content.decode()
    bussess_dict=get_bussess(html)
    insert_bussess_info(connection,bussess_dict,1)