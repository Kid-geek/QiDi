import requests
from bs4 import BeautifulSoup
import time
import pymysql

# 福建 失信被执行人信息

# 获取目录页详细url
def get_url(page_num):
    time.sleep(2)
    url_list = []
    date={}
    url = 'http://www.fjcredit.gov.cn/eap/credit.xymlFyJsSxbzxrlistqian'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    date['page'] = page_num
    html = requests.post(url, data=date, headers=header).content.decode()
    table_soup = BeautifulSoup(html, 'lxml')
    table = table_soup.find_all('table', class_='tab_info')
    for item in table:
        item_soup = BeautifulSoup(str(item), 'lxml')
        a = item_soup.find('a')['href']
        # print(a)
        url_list.append(a)
    # print('成功解析' + str(len(url_list)) + '个url')
    return url_list

# 获取信息传入字典
def get_info(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        html = requests.get(url, headers=header, timeout=60).content.decode()
    except requests.exceptions.ConnectionError:
        print('错误')
        time.sleep(10)
        html = requests.get(url, headers=header, timeout=60).content.decode()

    info_dict={}

    html_soup=BeautifulSoup(html,'lxml')

    table=html_soup.find('table',width='846')
    td_soup=BeautifulSoup(str(table),'lxml')
    info_dict['被执行人名称']=td_soup.find_all('td')[1].text.replace('\\','')
    if len(info_dict['被执行人名称'])<4:
        return None

    info_dict['法定代表人名称']=td_soup.find_all('td')[3].text.replace('\\','')
    info_dict['案件编号'] = td_soup.find_all('td')[5].text.replace('\\','')
    info_dict['立案日期'] = td_soup.find_all('td')[7].text
    info_dict['执行依据文号'] = td_soup.find_all('td')[9].text
    info_dict['执行法院'] = td_soup.find_all('td')[11].text
    info_dict['被执行人履行情况'] = td_soup.find_all('td')[13].text
    info_dict['失信被执行人行为具体情况'] = td_soup.find_all('td')[15].text
    info_dict['生效法律文书确定的义务'] = td_soup.find_all('td')[17].text


    print('url:'+url)
    print(info_dict)
    print('----------------------------------')
    return info_dict

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

# 插入数据库
def insert(connection,info_dict,page_num):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO dishonesty (executed_name, legal_name, case_number, register_date, accord_num, executive_court, performance, dishonesty_info, legal_documents, page_num ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )'
    data = (info_dict['被执行人名称'], info_dict['法定代表人名称'], info_dict['案件编号'], info_dict['立案日期'], info_dict['执行依据文号'] , info_dict['执行法院'],info_dict['被执行人履行情况'], info_dict['失信被执行人行为具体情况'], info_dict['生效法律文书确定的义务'], page_num)
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')


if __name__ == '__main__':

    # 参数为数据库名称
    connection = connect_mysql('fujian')

    # range 第一个参数为开始抓取页码   第二个参数为抓取截止页码+1
    for num in range(32, 2001):
        print('正在解析第'+str(num)+'页')
        url_list = get_url(num)
        print('解析成功，解析出'+str(len(url_list))+'个URL')
        for url in url_list:
            print('正在解析详情页')
            if get_info(url)!=None:
                info_dict = get_info(url)
                print('解析成功，执行插入语句')
                # 执行插入语句
                insert(connection, info_dict, num)
            else:
                print('个人行为 不记录')