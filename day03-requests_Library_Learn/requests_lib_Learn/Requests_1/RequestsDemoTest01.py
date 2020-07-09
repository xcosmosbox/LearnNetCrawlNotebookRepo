'''
    get指令的学习
'''
#导包
import requests

response = requests.get('http://www.baidu.com')
# 以下两行代码直接输出会出现乱码
# print(type(response.text))
# print(response.text)

#解决乱码的方式是将输出进行编码
print(type(response.content))
#以下这一步不仅进行了编码，并且在编码后立即进行了解码(这是因为虽然编码后不会出现乱码，但编码的内容人类无法读懂)
print(response.content.decode('utf-8'))







