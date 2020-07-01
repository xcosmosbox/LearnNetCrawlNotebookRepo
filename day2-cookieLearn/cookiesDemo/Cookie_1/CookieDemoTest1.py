#导入urllib包
from urllib import request

'''
情况一：不使用cookie查看我自己的微博主页，无法正常浏览，
       目的服务器会返回一个登录页面。
'''
urlOpened = 'https://weibo.com/2135389777/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1'
headers = {
    #添加一个访问头。不论以后如何爬虫，User-Agent都是必备的
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
req = request.Request(url=urlOpened,headers=headers) #注入网址和访问头，取得一个访问对象
resp = request.urlopen(req) #打开访问对象,并从目的服务器取得想要的信息
# print(resp.read().decode('gbk')) 这种方式是在终端打开所有的源代码，看起来不简洁
# 下面的方法是时使用语句将获取的源代码自动生成为一个html文件并存储这个html文件
with open('weiboTemp.html', 'w') as fp:
    # write函数必须写入一个str类型的数据
    # resp.read()读出来的是一个byte类型的数据
    # bytes --> decode --> str
    # str --> encode --> bytes
    fp.write(resp.read().decode('gbk'))
'''↑↑ 以上代码由于没有cookie信息，所以会被微博自动跳转到登录页面 ↑↑'''

####################################################################

'''
情况一：接下来将使用含有cookie信息的方式访问我自己的主页
'''
urlOpened2 = 'https://weibo.com/2135389777/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1'
headers2 = {
    #添加一个访问头。不论以后如何爬虫，User-Agent都是必备的
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Cookie':'SINAGLOBAL=6544828291248.87.1565154199972; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mNGy4WQB-rPInqPlSgF_i5JpX5KMhUgL.Fozpe0-01h.NS0M2dJLoIEBLxK-LBo.LB.zLxKqL1heLBoeLxK-LBKqL1KqLxKqL1h5LB-2t; UOR=,,login.sina.com.cn; YF-V5-G0=99df5c1ecdf13307fb538c7e59e9bc9d; ALF=1625122012; SSOLoginState=1593586015; SCF=AgBAWGQYMCuXz5S0M-ST8cKWGldNMyR5FklMVDC_GL9yPrrWClVVX_N23YTK4SL3BEtb4H9HDySO5WQ7F6L4Ew8.; SUB=_2A25z-EExDeRhGeRP6FcS-CfLzDuIHXVQjDX5rDV8PUNbmtANLUP9kW9NUCRPvIJelc2R2SvP7bF6jgY6XMChFkFZ; SUHB=08JKvlHm43c6uO; wvr=6; _s_tentry=login.sina.com.cn; Apache=3872115114950.143.1593586042432; wb_view_log_2135389777=1280*8002; ULV=1593586043367:90:1:2:3872115114950.143.1593586042432:1593481808863; YF-Page-G0=02467fca7cf40a590c28b8459d93fb95|1593586050|1593586045; webim_unReadCount=%7B%22time%22%3A1593586622659%2C%22dm_pub_total%22%3A10%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A11%2C%22msgbox%22%3A0%7D'
}
req2 = request.Request(url=urlOpened2,headers=headers2) #注入网址和访问头，取得一个访问对象
resp2 = request.urlopen(req2)
with open('weiboTempSuccess.html', 'w', encoding='utf-8') as fp:
    # write函数必须写入一个str类型的数据
    # resp.read()读出来的是一个byte类型的数据
    # bytes --> decode --> str
    # str --> encode --> bytes
    fp.write(resp2.read().decode('utf-8'))







