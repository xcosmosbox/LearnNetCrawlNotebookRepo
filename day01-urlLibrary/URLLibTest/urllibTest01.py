from urllib import request
from urllib import parse

#urlretrieve使用方法示例
request.urlretrieve('http://www.baidu.com','baidu.html')
request.urlretrieve('https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1876397236,3115234655&fm=26&gp=0.jpg','temp.jpg')

#urlencode使用方法示例 ①
params = {'name':'张三','age':18,'greet':'hello world'}
result = parse.urlencode(params)
print(result)

#urlencode使用方法示例 ②
url = 'http://www.baidu.com/s'
params2 = {'wd':'爬虫'}
qs = parse.urlencode(params2)
url = url + '?' +qs
resp = request.urlopen(url)
print(resp.readlines())

#parse_qs使用方法示例
params = {'name':'张三','age':18,'greet':'hello world'}
result = parse.urlencode(params)
qs = parse.parse_qs(result)
print(qs)

#urlparse和urlsplit使用方法示例，urlparse与urlsplit基本一致，但urlparse比urlsplit多一个params属性
url = 'https://fanyi.baidu.com/?aldtype=16047#en/zh/greet'
result = parse.urlparse(url)
result2 = parse.urlsplit(url)
print(result) #一次性全部打印urlparse
print(result2) #一次性全部打印urlsplit
print('scheme:',result.scheme) #打印指定的部分urlparse
print('netloc:',result.netloc) #打印指定的部分urlparse
print('query:',result.query) #打印指定的部分urlparse

#使用 request.Request 方法插入header头，伪装成正常的访问，防止被反爬虫
url = 'https://www.bilibili.com/v/channel/4610466?spm_id_from=333.158.b_7072696d61727950616765546162.4&tab=multiple'
# resp = request.urlopen(url)
# print(resp.read())
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
req = request.Request(url,headers=headers)
resp = request.urlopen(req)
print(resp.read())

'''
使用 ProxyHandler 方法进行ip代理，防止被反爬虫:
    i.代理的原理：在请求目的网站之前，先请求代理服务器，然后让代理服务器去请求目的网站，
      代理服务器拿到目的网站的数据后，再转发给我们的代码。
    ii.http：//httpbin.org：这个网站可以方便的查看http请求的一些参数
    iii.在代码中使用代理：
        * 使用‘urllib.request.ProxyHandler’，传入一个代理，这个代理是一个字典，字典
          的key依赖于代理服务器能够接收的类型，一般是‘http’或者‘https’，值是‘ip:port’
        * 使用上一步创建的‘handler’，以及‘request.build_opener’创建一个‘opener’对象
        * 使用上一步创建的‘opener’调用‘open’函数发起请求
    示例代码如下：    
'''
url = 'http://httpbin.org/ip'
# 1.使用ProxyHandler，传入代理构建一个handler
handler = request.ProxyHandler({"http":"113.195.223.117:9999"})
# 2.使用上面创建的handler构建一个opener
opener = request.build_opener(handler)
# 3.使用opener发起请求
resp = opener.open(url)
print(resp.read())























