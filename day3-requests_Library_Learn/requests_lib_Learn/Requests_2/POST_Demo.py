'''
    post指令爬取拉勾网
'''
import requests

data = {
    'first': 'true',
    'pn': '1',
    'kd': 'python'
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Cookie': 'RECOMMEND_TIP=true; user_trace_token=20200630143347-4fe1cceb-9c7d-42fe-897c-ba981ba81517; LGUID=20200630143347-e9e49985-a336-4f93-acf3-a98ce3f52588; _ga=GA1.2.758683827.1593498827; index_location_city=%E5%85%A8%E5%9B%BD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217303eea68d2bf-097193e2e10f44-4353760-1024000-17303eea68e585%22%2C%22%24device_id%22%3A%2217303eea68d2bf-097193e2e10f44-4353760-1024000-17303eea68e585%22%7D; JSESSIONID=ABAAAECABIEACCA5B8485533D71C3CAE69CD164D2A05C76; WEBTJ-ID=20200702102742-1730d59e8f1f0-0585d8b8d850c3-4353760-1024000-1730d59e8f2a26; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20200702102748-7b0c8bdc-c967-4faa-829c-5c37bb4abe03; PRE_SITE=; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1593498827,1593656863; _gat=1; _gid=GA1.2.884485371.1593656864; TG-TRACK-CODE=index_search; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1593656880; X_HTTP_TOKEN=0218c35ce72e54b53096563951f0ff4f66326310b7; LGRID=20200702102951-fecd4b80-a2b4-4028-b93b-70aad41d78bc; SEARCH_ID=55b1d2fb16a64a849f4dfe7212104589'
}

response  = requests.post('https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',data = data,headers=headers)

print(response.text)

