#导包
import requests

#使用代理服务器只需要在请求的方法中（如get或post）传递 proxies参数就行，

#指定代理服务器
proxy = {
    'http':'1.198.72.185:9999'
}

response  = requests.get('http://httpbin.org/ip',proxies=proxy)

print(response.text)