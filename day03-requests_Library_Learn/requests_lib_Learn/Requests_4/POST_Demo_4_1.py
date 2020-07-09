'''
    使用requests库去处理cookie，并利用session去共享cookie信息
'''

#导包
import requests

url = 'https://weibo.com/login.php'
data = {
    'username':'username',
    'password':'password'
}
headers = {
    'Cookie': 'SINAGLOBAL=6544828291248.87.1565154199972; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5mNGy4WQB-rPInqPlSgF_i5JpX5KMhUgL.Fozpe0-01h.NS0M2dJLoIEBLxK-LBo.LB.zLxKqL1heLBoeLxK-LBKqL1KqLxKqL1h5LB-2t; UOR=,,login.sina.com.cn; wvr=6; YF-V5-G0=260e732907e3bd813efaef67866e5183; ALF=1625191339; SSOLoginState=1593655340; SCF=AgBAWGQYMCuXz5S0M-ST8cKWGldNMyR5FklMVDC_GL9yhIfBq-ALNiJDrgG5Dk1A3DRUS_AElbbP_b8ciurlO4E.; SUB=_2A25z-TB_DeRhGeRP6FcS-CfLzDuIHXVQjya3rDV8PUNbmtANLULHkW9NUCRPvJeO0a_zISSCi5nSwN0t-cS8PmG8; SUHB=0jB5A1Fo2CmhLZ; _s_tentry=login.sina.com.cn; Apache=9429823647709.996.1593655385238; wb_view_log_2135389777=1280*8002; ULV=1593655404083:91:2:3:9429823647709.996.1593655385238:1593586043367; YF-Page-G0=95d69db6bf5dfdb71f82a9b7f3eb261a|1593657932|1593657932; webim_unReadCount=%7B%22time%22%3A1593660596096%2C%22dm_pub_total%22%3A10%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A11%2C%22msgbox%22%3A0%7D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

#登录
session = requests.Session()
session.post(url,data=data,headers=headers)

#访问个人主页
response = session.get('https://weibo.com/2135389777/profile?topnav=1&wvr=6')

with open('weibo2.html','w',encoding='utf-8') as fp:
    fp.write(response.content.decode('gbk'))



