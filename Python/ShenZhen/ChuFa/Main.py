import requests
import json

# 获取url   参数：一页有20个url    参数为要获取都少页的url
def get_url(page_num):
    url = 'http://www.szcredit.org.cn/web/DoubleGS/Ajax/Ajax.ashx'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    Recordid_list = []
    for num in range(1,int(page_num)+1):
        date = {'action': 'getXZCFGSList', 'PageIndex':num}
        req = requests.post(url, data=date, headers=header).content.decode('gbk')
        dict = json.loads(req)
# print(dict['Recordid'])
        info = dict['Data']['Items']
        for dic in info:
            Recordid_list.append(dic['Recordid'])
    #拼接url链接
    url_list=[]
    for id in Recordid_list:
        url_list.append('http://www.szcredit.org.cn/web/DoubleGS/Detail.aspx?id='+id+'&type=XZCF')
    print(url_list)
    return url_list

def get_info(url_list):
    for url in url_list:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html=requests.get(url,header)

if __name__ == '__main__':
    # get_url(3)  # 一页有20个url    参数为要获取都少页的url
    file=open('url.txt','w')
    file.write(str(get_url(3)))

    # print(len(get_url(3)))
