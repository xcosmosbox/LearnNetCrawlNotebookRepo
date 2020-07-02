'''
    如何去处理不被信任的SSL网站
'''

#导包
import requests

url = '不被信任的SSL证书的网址'

'''只需要加上 verify=False 就能正常输出了'''
response = requests.get(url,verify=False)

print(response.content.decode('utf-8'))