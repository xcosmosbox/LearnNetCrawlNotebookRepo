import requests
from lxml import etree
# 1.将目标网站上的页面抓取下来

headers={
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.16 Safari/537.36",
    # 仿照浏览器,将该爬虫包装成一个浏览器
    'Referer': "https://www.baidu.com/s?wd=%E8%B1%86%E7%93%A3&rsv_spt=1&rsv_iqid=0xded42b9000078acc&issp=1&f=8&rsv_bp"
               "=1&rsv_idx=2&ie=utf-8&tn=62095104_19_oem_dg&rsv_enter=1&rsv_dl=ib&rsv_sug3=8&rsv_sug1=5&rsv_sug7=100"
               "&rsv_sug2=0&inputT=1250&rsv_sug4=1784 "
    # 告诉服务器该网页是从哪个页面链接过来的,服务器因此可以获得一些信息用于处理,一般用于多网页的爬取
}
url = 'https://movie.douban.com/'
response = requests.get(url, headers=headers)
text = response.text                              #将其网页爬取下来了
#text=open("Douban.text",'r',encoding="utf-8")
# print(response.text)

# response.text: 返回的是一个经过解码后的字符串,是str(unicode)类型,有可能会发生乱码,因为解码方式可能不一样而导致乱码
# response.content: 返回的是一个原生的字符串,就是从网页上抓取下来,没有经过处理,bytes类型

# 2.将抓取的数据根据一定的规则进行提取
html = etree.HTML(text)                      # 对网页进行解析,对text进行解码
print(html)
#html = html.xpath("//ul/li/a/@href")获取a标签下的href属性值
#html = html.xpath("//ul/li/a/text()")获取a标签下的文本

ul = html.xpath("//ul")[0]
print(ul)
lts=ul.xpath("./li")
for li in lts:
    title=li.xpath("@data-title")
    data_release=li.xpath("@data-release")
    #data_duration=li.xpath("@data-ticket data-duration")
    data_region=li.xpath("@data-region")
    data_actors=li.xpath("@data-actors")
    post=li.xpath(".//img/@scr")
    print(data_actors)
    print(post)
    movie={
        'title':title,
        'data_release':data_release
    }
