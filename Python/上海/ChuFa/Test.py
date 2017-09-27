import requests
import json

url='http://cxw.shcredit.gov.cn:8081/sh_xyxxzc/sgsinfo/getcfinfo.action?cfid=574E0B604EE74ED5E0530100007F4218'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
html = requests.get(url, header).content.decode()
html=html.replace('[','').replace(']','')

info_dict=json.loads(html)
# print(info_dict)

print('处罚文书号：'+info_dict['cfwsh']+'  处罚名称：'+info_dict['cfmc']+' 处罚类别：'+info_dict['cflb']+
              ' 处罚事由：'+info_dict['cfsy']+' 处罚依据：'+info_dict['cfyj']+' 行政相对人'+info_dict['xzxdr']+' 处罚决定日期：'+info_dict['cfjdrq']+' 处罚机关：'+info_dict['cfjguan'])
