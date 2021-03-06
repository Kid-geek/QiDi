import requests
from bs4 import BeautifulSoup
import time
import pymysql

# 福建行政许可

# 获取页码目录所有url
def get_url(page_num):
    time.sleep(2)
    url_list = []
    date = {}

    url = 'http://www.fjcredit.gov.cn/eap/credit.sgszzxklist'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    date['page'] = page_num
    html = requests.post(url, data=date, headers=header).content.decode()

    table_soup = BeautifulSoup(html, 'lxml')
    table = table_soup.find(id='actionlist')
    tbody_soup = BeautifulSoup(str(table), 'lxml')
    tbody = tbody_soup.find('tbody')
    tr_soup = BeautifulSoup(str(tbody), 'lxml')
    tr = tr_soup.find_all('tr')
    for item in tr:
        td_soup = BeautifulSoup(str(item), 'lxml')
        td = td_soup.find('a')['href']
        url_list.append(td)
    print('成功解析' + str(len(url_list)) + '个url')
    return url_list

# 获取数据存入字典
def get_info(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    try:
        html = requests.get(url, headers=header, timeout=60).content.decode()
    except requests.exceptions.ConnectionError:
        print('错误')
        time.sleep(10)
        html = requests.get(url, headers=header, timeout=60).content.decode()

    info_dict = {}

    html_soup = BeautifulSoup(html, 'lxml')
    div = html_soup.find('div', class_='d_gs_detail')
    td_soup = BeautifulSoup(str(div), 'lxml')
    info_dict['行政许可决定文书号'] = td_soup.find_all('td', class_='value')[0].text.replace(' ', '').replace('\r', '').replace( '\n', '').replace('\t', '')
    info_dict['项目名称'] = td_soup.find_all('td', class_='value')[1].text.replace(' ', '').replace('\r', '').replace('\n','').replace('\t', '')
    info_dict['企业名称'] = td_soup.find_all('td', class_='value')[2].text.replace(' ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
    if len(info_dict['企业名称'])<4:
        return None

    info_dict['许可内容'] = td_soup.find_all('td', class_='value')[3].text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['统一社会信用代码'] = td_soup.find_all('td', class_='value')[4].text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['组织机构代码'] = td_soup.find_all('td', class_='value')[5].text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['法人代表姓名'] = td_soup.find_all('td', class_='value')[6].text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['许可决定日期'] = td_soup.find_all('td', class_='value')[7].text.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    info_dict['许可截止日期'] = td_soup.find_all('td', class_='value')[8].text.replace(' ', '').replace('\r', '').replace( '\n', '').replace('\t', '')
    info_dict['许可部门'] = td_soup.find_all('td', class_='value')[9].text.replace(' ', '').replace('\r', '').replace('\n','').replace( '\t', '')
    info_dict['地方编码'] = td_soup.find_all('td', class_='value')[10].text.replace(' ', '').replace('\r', '').replace('\n','').replace('\t', '')
    info_dict['当前状态'] = td_soup.find_all('td', class_='value')[11].text.replace(' ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
    info_dict['备注'] = td_soup.find_all('td', class_='value')[12].text.replace(' ', '').replace('\r', '').replace('\n','').replace('\t', '')

    print('url:' + url)
    print(info_dict)
    print('----------------------------------')
    print()
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


def insert(connection,info_dict,page_num):
    # 获取游标
    cursor = connection.cursor()

    # 插入数据
    cursor = connection.cursor()
    sql = 'INSERT INTO license (document_number, project_name, company_name, license_content, credit_code, organization_code, legal_name, start_date, end_date, license_depart, local_code, current_state, remarks, page_num ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )'
    data = (info_dict['行政许可决定文书号'] ,info_dict['项目名称'] ,info_dict['企业名称'] ,info_dict['许可内容'] ,info_dict['统一社会信用代码'] ,info_dict['组织机构代码'] ,info_dict['法人代表姓名'] ,info_dict['许可决定日期'],info_dict['许可截止日期'] ,info_dict['许可部门'] ,info_dict['地方编码'] ,info_dict['当前状态'] ,info_dict['备注'] ,page_num)
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')


if __name__ == '__main__':

    # 参数为数据库名称
    connection=connect_mysql('fujian')

    # range 第一个参数为开始抓取页码   第二个参数为抓取截止页码+1
    for num in range(165, 1000):
        print('正在解析第' + str(num) + '页')
        url_list = get_url(num)
        print('解析成功，解析出' + str(len(url_list)) + '个URL')
        for url in url_list:
            print('正在解析详情页')

            if get_info(url)!=None:
                info_dict = get_info(url)
                print('解析成功，执行插入语句')
                # 执行插入语句
                insert(connection, info_dict, num)
            else:
                print('个人行为 不记录')
