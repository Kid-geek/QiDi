import requests
from bs4 import BeautifulSoup
def get_url(page_num):
    url_list = []
    date={}
    for num in range(1, int(page_num) + 1):
        url = 'http://www.fjcredit.gov.cn/eap/credit.sgszzxklist'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        date['page']=num
        html = requests.post(url, data=date,headers=header).content.decode()
        table_soup=BeautifulSoup(html,'lxml')
        table=table_soup.find(id='actionlist')
        tbody_soup=BeautifulSoup(str(table),'lxml')
        tbody=tbody_soup.find('tbody')
        tr_soup=BeautifulSoup(str(tbody),'lxml')
        tr=tr_soup.find_all('tr')
        for item in tr:
            td_soup=BeautifulSoup(str(item),'lxml')
            td=td_soup.find('a')['href']
            url_list.append(td)
    print(url_list)
    return url_list

def get_info(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, headers=header).content.decode()


if __name__ == '__main__':
    print(len(get_url(2)))