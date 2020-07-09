#导入urllib包和http.cookiejar包
from urllib import request
from urllib import parse
from http.cookiejar import CookieJar

'''
思路：
    1.登录
        1.1创建一个cookiejar对象
        1.2使用cookiejar创建一个HTTPCookieProcess对象
        1.3使用handler创建一个opener
        1.4使用opener发送登录请求（包含账户和密码）
    2.访问个人主页
'''
#以headers的作用来讲，可以作为一个全局变量
headers = {
        # 添加一个访问头。不论以后如何爬虫，User-Agent都是必备的
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

def get_opener():
    # 1.登录
    # 1.1创建一个cookiejar对象
    cookiejar = CookieJar()
    # 1.2使用cookiejar创建一个HTTPCookieProcess对象
    handler = request.HTTPCookieProcessor(cookiejar)
    # 1.3使用handler创建一个opener
    opener = request.build_opener(handler)
    return opener

def login_info(opener):
    # 1.4使用opener发送登录请求（包含账户和密码）
    data = {
        # 账户信息
        'username': 'username',
        'password': 'password'
    }
    login_url = 'https://weibo.com/'
    req = request.Request(login_url, data=parse.urlencode(data).encode('gbk'), headers=headers)
    opener.open(req)

def visit_profile(opener):
    # 2.访问个人主页
    urlOpened = 'https://weibo.com/2135389777/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1'
    # 获取个人主页的页面的时候，不要新建opener，而应该使用之前创建的opener，因为之间的那个opener已经包含了登录所需要的cookie信息
    req = request.Request(urlOpened, headers=headers)
    resp = opener.open(req)
    with open('weiboOpendTemp.html', 'w', encoding='gbk') as fp:
        # write函数必须写入一个str类型的数据
        # resp.read()读出来的是一个byte类型的数据
        # bytes --> decode --> str
        # str --> encode --> bytes
        fp.write(resp.read().decode('gbk'))

#用main函数运行以上方法
if __name__ == '__main__':
    opener = get_opener()
    login_info(opener)
    visit_profile(opener)




