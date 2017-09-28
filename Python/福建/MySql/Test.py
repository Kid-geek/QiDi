import requests
from bs4 import BeautifulSoup
import time
import pymysql

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


def get_info(url):
    time.sleep(2)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, headers=header).content.decode()

    info_dict = {}

    html_soup = BeautifulSoup(html, 'lxml')
    div = html_soup.find('div', class_='d_gs_detail')
    td_soup = BeautifulSoup(str(div), 'lxml')
    info_dict['行政许可决定文书号'] = td_soup.find_all('td', class_='value')[0].text.replace(' ', '').replace('\r', '').replace( '\n', '').replace('\t', '')
    info_dict['项目名称'] = td_soup.find_all('td', class_='value')[1].text.replace(' ', '').replace('\r', '').replace('\n','').replace('\t', '')
    info_dict['企业名称'] = td_soup.find_all('td', class_='value')[2].text.replace(' ', '').replace('\r', '').replace('\n', '').replace( '\t', '')
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
    sql = 'INSERT INTO license (document_number, project_name, company_name, license_content, credit_code, organization_code, legal_name, start_date, end_date, license_department, local_code, current_state, remarks, page_num ) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )'
    data = (info_dict['行政许可决定文书号'] ,
    info_dict['项目名称'] ,
    info_dict['企业名称'] ,
    info_dict['许可内容'] ,
    info_dict['统一社会信用代码'] ,
    info_dict['组织机构代码'] ,
    info_dict['法人代表姓名'] ,
    info_dict['许可决定日期'],
    info_dict['许可截止日期'] ,
    info_dict['许可部门'] ,
    info_dict['地方编码'] ,
    info_dict['当前状态'] ,
    info_dict['备注'] ,
    page_num
            )
    cursor.execute(sql % data)
    connection.commit()
    print('成功插入', cursor.rowcount, '条数据')


if __name__ == '__main__':
    url_list = []
    info_dict={}
    connection=connect_mysql('anhui')

    for num in range(1, 3):
        url_list = get_url(num)
        for url in url_list:
            info_dict=get_info(url)
            insert(connection,info_dict,num)
