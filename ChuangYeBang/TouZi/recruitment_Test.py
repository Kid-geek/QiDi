import requests
import json
url='http://api.lagou.com/cooperation/data/api/AD__cyzone_words?companyName=英雄互娱'
header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
html = requests.get(url, header).content.decode().replace('success_jsonpCallback(','').replace(')','')
list=json.loads(html)
for info in list:
    # info_dict=json.loads(info)
    print('招聘公司:'+info['companyName'])
    print('招聘职位:'+info['positionName'])
    print('招聘链接:'+info['posiitonDetailUrl'])
    print('所属行业:'+info['industryField'])
    print('薪资:'+info['salary'])
    print('城市:'+info['city'])
    print('----------------')