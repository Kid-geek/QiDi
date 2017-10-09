import requests

proxies={"http":"114.232.81.197:26011"}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url='http://www.whatismyip.com.tw/'
r =  requests.get(url, header).content.decode()
print(r)