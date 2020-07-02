'''
    使用requests库去处理cookie
'''

#导包
import requests

response = requests.get('http://www.baidu.com')
print(response.cookies)
print(response.cookies.get_dict())



