import requests
import json

def get_url(page_num):
    id_list = []
    url_list=[]
    for num in range(1,int(page_num)+1):
        url='http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/cflist/cfgrid.action?search=false&rows=15&page='+str(num)+'&sidx=&sord=asc'
        header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        html=requests.get(url,header).content.decode()
        html=json.loads(html)
        gridModel=html['gridModel']
        # 获取ID
        for item in gridModel:
            if len(item['xzxdr'])>3:
                id_list.append(item['cfid'])
        # 获取url
        for id in id_list:
            url_list.append('http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/sgsinfo/getcfinfo.action?cfid='+id)
    # print(url_list)
    return url_list

def get_info(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    html = requests.get(url, header).content.decode()
    dice={}
    html=html.replace('[','').replace(']','')

    info_dict = json.loads(html)

    return info_dict


if __name__ == '__main__':
    url_list=get_url(10)
    for url in url_list:
        info_dict=get_info(url)
        print('链接为：'+url)
        print('处罚文书号：' + info_dict['cfwsh'] + '  处罚名称：' + info_dict['cfmc'] + ' 处罚类别：' + info_dict['cflb'] +
              ' 处罚事由：' + info_dict['cfsy'] + ' 处罚依据：' + info_dict['cfyj'] + ' 行政相对人：' + info_dict['xzxdr'] + ' 处罚决定日期：' +
              info_dict['cfjdrq'] + ' 处罚机关：' + info_dict['cfjguan'])
        print('---------------------------------------------------------')
