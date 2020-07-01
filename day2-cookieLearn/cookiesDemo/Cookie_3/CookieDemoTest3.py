#这个代码的目的是将cookie信息保存到本地

#导包
from urllib import request
from http.cookiejar import MozillaCookieJar

#创建一个用以保存的cookie，并且指定文件的位置和名字
cookiejar = MozillaCookieJar('cookie.txt')
#将cookie加载到头中
handler = request.HTTPCookieProcessor(cookiejar)
#利用handler创建opener对象
opener = request.build_opener(handler)

#利用opener对象打开指定网址
resp = opener.open('http://www.baidu.com')

#保存cookie信息
cookiejar.save()
'''
对于哪种程序结束后就会自动过期的cookie信息，可以使用以下代码保存:
    cookiejar.save(ignore_discard=True)
'''

#加载并打印cookie信息
cookiejar.load()
for cookie in cookiejar:
    print(cookie)
'''
对于哪种程序结束后就会自动过期的cookie信息，可以使用以下代码进行加载:
    cookiejar.load(ignore_discard=True)
'''

