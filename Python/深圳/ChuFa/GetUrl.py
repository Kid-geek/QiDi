import requests
import json
import time
# 获取url   参数：一页有20个url    参数为要获取都少页的url
def get_url(start_num,page_num):

    url = 'http://www.szcredit.org.cn/web/' \
          '+DoubleGS/Ajax/Ajax.ashx'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    url_list = []
    file = open('url.txt', 'w')
    for num in range(int(start_num),int(page_num)+1):
        time.sleep(2)
        date = {'action': 'getXZCFGSList', 'PageIndex':num}
        req = requests.post(url, data=date, headers=header,timeout=60).content.decode('gbk')
        dict = json.loads(req)
        info = dict['Data']['Items']
        for dic in info:
            id=dic['Recordid']
            url_list.append('http://www.szcredit.org.cn/web/DoubleGS/Detail.aspx?id='+id+'&type=XZCF')

        file.write(str(url_list))
        print('解析出'+str(len(url_list))+'个url')
    return url_list

if __name__ == '__main__':
    get_url(1,1000)