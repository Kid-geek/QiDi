import requests
from bs4 import BeautifulSoup
import time

def get_url(page_num):
    time.sleep(2)
    url_list = []
    for num in range(1, int(page_num) + 1):
        url = 'http://www.creditah.gov.cn/AdministrativePenalty/index_' + str(page_num) + '.htm'
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html = requests.get(url, header).content.decode()
        html_soup = BeautifulSoup(html, 'lxml')
        url_list_item = html_soup.find_all('td', width='45%')
        for item in url_list_item:
            url_soup = BeautifulSoup(str(item), 'lxml')
            url = url_soup.find('a')['href']
            url_list.append(url)
    return url_list




def get_info(url):
    # 休眠2秒 防封
    time.sleep(2)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, header).content.decode()

    # 判断是否需要输入验证码
    if '验证' in html:
        return '访问频繁需要验证'

    html_soup=BeautifulSoup(html,'lxml')
    table=html_soup.find('table',class_='infor')
    table_soup=BeautifulSoup(str(table),'lxml')


    info_dict={}
    info_dict['书文号'] = table_soup.find_all('td', colspan='3')[0].text.replace('\n', "").replace(' ', "")
    info_dict['处罚名称'] = table_soup.find_all('td', colspan='3')[1].text.replace('\n', "").replace(' ', "")
    info_dict['处罚类别1'] = table_soup.find_all('td', colspan='3')[2].text.replace('\n', "").replace(' ', "")
    info_dict['处罚类别2'] = table_soup.find_all('td', colspan='3')[3].text.replace('\n', "").replace(' ', "")
    info_dict['处罚事由'] = table_soup.find_all('td', colspan='3')[4].text.replace('\n', "").replace(' ', "")
    info_dict['处罚依据'] = table_soup.find_all('td', colspan='3')[5].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人名称'] = table_soup.find_all('td')[13].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人代码_1(统一社会信用代码)'] = table_soup.find_all('td', colspan='3')[6].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人代码_2(组织机构代码)'] = table_soup.find_all('td', colspan='3')[7].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人代码_3(工商登记码)'] = table_soup.find_all('td', colspan='3')[8].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人代码_4(税务登记号)'] = table_soup.find_all('td', colspan='3')[9].text.replace('\n', "").replace(' ', "")
    info_dict['行政相对人代码_5(居民身份证号)'] = table_soup.find_all('td', colspan='3')[10].text.replace('\n', "").replace(' ', "")
    info_dict['法定代表人姓名'] = table_soup.find_all('td', colspan='3')[11].text.replace('\n', "").replace(' ', "")
    info_dict['处罚结果'] = table_soup.find_all('td', colspan='3')[12].text.replace('\n', "").replace(' ', "")
    info_dict['处罚决定日期'] = table_soup.find_all('td', colspan='3')[13].text.replace('\n', "").replace(' ', "")
    info_dict['处罚机关'] = table_soup.find_all('td', colspan='3')[14].text.replace('\n', "").replace(' ', "")
    info_dict['当前状态'] = table_soup.find_all('td', colspan='3')[15].text.replace('\n', "").replace(' ', "")
    info_dict['地方编码'] = table_soup.find_all('td', colspan='3')[16].text.replace('\n', "").replace(' ', "")
    info_dict['数据更新时间戳'] = table_soup.find_all('td', colspan='3')[17].text.replace('\n', "").replace(' ', "")
    # info_dict['备注'] = table_soup.find_all('td', colspan='3')[18].text.text.replace('\n', "").replace(' ', "")
    return info_dict

if __name__ == '__main__':
    url_list=get_url(1)
    # dict={}
    for url in url_list:
        print(get_info(url))
        print('-----------------------------')