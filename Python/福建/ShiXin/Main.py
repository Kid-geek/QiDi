import requests
from bs4 import BeautifulSoup
import time
def get_url(page_num):
    time.sleep(2)
    url_list = []
    date={}
    for num in range(1, int(page_num) + 1):
        url = 'http://www.fjcredit.gov.cn/eap/credit.xymlFyJsSxbzxrlistqian'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        date['page']=num
        html = requests.post(url, data=date,headers=header).content.decode()
        table_soup=BeautifulSoup(html,'lxml')
        table=table_soup.find_all('table',class_='tab_info')
        for item in table:
            item_soup=BeautifulSoup(str(item),'lxml')
            a=item_soup.find('a')['href']
            print(a)
            url_list.append(a)
        print('成功解析'+str(len(url_list))+'个url')
    return url_list

def get_info(url):
    time.sleep(2)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, headers=header).content.decode()

    info_dict={}

    html_soup=BeautifulSoup(html,'lxml')
    div=html_soup.find('div',class_='d_gs_detail')
    td_soup=BeautifulSoup(str(div),'lxml')
    info_dict['行政许可决定文书号']=td_soup.find_all('td',class_='value')[0].text.replace(' ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['项目名称']=td_soup.find_all('td',class_='value')[1].text.replace(' ','').replace('\r','').replace('\n','').replace('\t','')
    info_dict['企业名称'] = td_soup.find_all('td', class_='value')[2].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['许可内容'] = td_soup.find_all('td', class_='value')[3].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['统一社会信用代码'] = td_soup.find_all('td', class_='value')[4].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['组织机构代码'] = td_soup.find_all('td', class_='value')[5].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['法人代表姓名'] = td_soup.find_all('td', class_='value')[6].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['许可决定日期'] = td_soup.find_all('td', class_='value')[7].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['许可截止日期'] = td_soup.find_all('td', class_='value')[8].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['许可部门'] = td_soup.find_all('td', class_='value')[9].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['地方编码'] = td_soup.find_all('td', class_='value')[10].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['当前状态'] = td_soup.find_all('td', class_='value')[11].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')
    info_dict['备注'] = td_soup.find_all('td', class_='value')[12].text.replace(' ', '').replace('\r','').replace('\n','').replace('\t','')

    print('url:'+url)
    print(info_dict)
    print('----------------------------------')
    print()
    return info_dict

if __name__ == '__main__':
    url_list=get_url(1)
    print('共'+str(len(url_list))+'个页面')
    # for url in url_list:
    #     get_info(url)