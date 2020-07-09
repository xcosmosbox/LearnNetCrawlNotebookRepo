'''
    post指令爬取微博
'''
import requests

data = {
    'data':{"uid":"2135389777","mid":"4522191474140073","keys":"4522111376031838","type":"feedvideo"},
    'key':'H5_8iad8_1593658193724566912',
    'sig':'65dcdc3c60744e43afde8fc7c2b83fbf'
}

headers = {
    'referer': 'https://weibo.com/u/2135389777/home?wvr=5&lf=reg',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

response  = requests.post('https://weibo.com/aj/video/playstatistics?ajwvr=6',data = data,headers=headers)

print(response.content.decode('gbk'))