import pymysql
import pymysql.cursors
import requests
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-

# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='anhui',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()
url='http://www.creditah.gov.cn/AdministrativeLicensing/6871746.htm'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
html = requests.get(url, header).content.decode()
html_soup = BeautifulSoup(html, 'lxml')
table = html_soup.find('table', class_='infor')
table_soup = BeautifulSoup(str(table), 'lxml')
info_dict = {}

print('ok')

info_dict['行政相对人名称'] = table_soup.find_all('td', colspan='3')[4].text.replace('\n', "").replace('  ', " ")
if len(info_dict['行政相对人名称']) > 3:
    info_dict['书文号'] = table_soup.find_all('td', colspan='3')[0].text.replace('\n', "").replace('  ', " ")
    info_dict['项目名称'] = table_soup.find_all('td', colspan='3')[1].text.replace('\n', "").replace('  ', " ")
    info_dict['审批类别'] = table_soup.find_all('td', colspan='3')[2].text.replace('\n', "").replace('  ', " ")
    info_dict['许可内容'] = table_soup.find_all('td', colspan='3')[3].text.replace('\n', "").replace('  ', " ")
    info_dict['统一社会信用代码'] = table_soup.find_all('td', colspan='3')[5].text.replace('\n', "").replace('  '," ")
    info_dict['组织机构代码'] = table_soup.find_all('td', colspan='3')[6].text.replace('\n', "").replace('  '," ")
    info_dict['工商登记码'] = table_soup.find_all('td', colspan='3')[7].text.replace('\n', "").replace(' ',"")
    info_dict['税务登记号'] = table_soup.find_all('td', colspan='3')[8].text.replace('\n', "").replace(' ', "")
    info_dict['居民身份证号'] = table_soup.find_all('td', colspan='3')[9].text.replace('\n', "").replace(' ', "")
    info_dict['法定代表人姓名'] = table_soup.find_all('td', colspan='3')[10].text.replace('\n', "").replace(' ', "")
    info_dict['许可决定日期'] = table_soup.find_all('td', colspan='3')[11].text.replace('\n', "").replace(' ', "")
    info_dict['许可截止期'] = table_soup.find_all('td', colspan='3')[12].text.replace('\n', "").replace(' ', "")
    info_dict['许可机关'] = table_soup.find_all('td', colspan='3')[13].text.replace('\n', "").replace(' ', "")
    info_dict['当前状态'] = table_soup.find_all('td', colspan='3')[14].text.replace('\n', "").replace(' ', "")
    info_dict['地方编码'] = table_soup.find_all('td', colspan='3')[15].text.replace('\n', "").replace(' ', "")
    info_dict['数据更新时间戳'] = table_soup.find_all('td', colspan='3')[16].text.replace('\n', "").replace(' ', "")
    info_dict['备注'] = table_soup.find_all('td', colspan='3')[17].text.replace('\n', "").replace(' ', "")
else:
    del info_dict['行政相对人名称']
# 插入数据
cursor = connect.cursor()
sql = 'INSERT INTO 行政许可 (统一社会信用代码) VALUES ("1")'

cursor.execute(sql )
connect.commit()
print('成功插入', cursor.rowcount, '条数据')