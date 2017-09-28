import requests
import json
import time
from bs4 import BeautifulSoup

# 获取url   参数：一页有20个url    参数为要获取都少页的url
def get_url(page_num):
    url = 'http://www.szcredit.org.cn/web/DoubleGS/Ajax/Ajax.ashx'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    url_list = []
    time.sleep(2)
    date = {'action': 'getXZCFGSList', 'PageIndex':page_num}
    req = requests.post(url, data=date, headers=header).content.decode('gbk')
    dict = json.loads(req)
    info = dict['Data']['Items']
    for dic in info:
        id=dic['Recordid']
        url_list.append('http://www.szcredit.org.cn/web/DoubleGS/Detail.aspx?id='+id+'&type=XZCF')
    return url_list

def get_info(url_list):
    info_dict={}
    for url in url_list:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html=requests.get(url,header).content.decode()
        print(html)
        html_soup=BeautifulSoup(html,'lxml')
        div=html_soup.find('div',class_='d_gs_detail')
        td_soup=BeautifulSoup(str(div),'lxml')

        print(div)
        # info_dict['行政许可决定文书号']=td_soup.find_all('td',class_='value')[0].replace(' ','')
    print(info_dict)
    return info_dict

if __name__ == '__main__':
    for i in range(1,3):
        url_list=get_url(i)
        get_info(url_list)


