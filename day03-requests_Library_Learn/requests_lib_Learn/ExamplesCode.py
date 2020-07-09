#导包
import requests

#指定将要搜索的内容
params = {
    'wd':'中国'
}

#编写头部，伪装成一个正常的浏览器进行查询
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

#使用requests包中的get方法，指定查询的网址，查询的内容，以及头部
response = requests.get('https://www.baidu.com/s',params=params,headers=headers)

#将查询到的内容信息以‘utf-8’的编码模式写入一个指定的html文件中
with open('baidu.html','w',encoding='utf-8') as fp:
    fp.write(response.content.decode('utf-8'))

#输出在本次查询中进行搜索的实际网址
print(response.url)





