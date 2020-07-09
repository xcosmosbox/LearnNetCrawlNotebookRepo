# 爬取电影天堂
import requests
from lxml import etree

BASE_URL='https://www.dytt8.net/'
url = 'https://www.dytt8.net/html/gndy/dyzz/index.html'
HEADERS = {
        'Referer': 'https://www.dytt8.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.16 Safari/537.36'
    		}
def get_detail_urls(url):
    response = requests.get(url, headers=HEADERS)
    # print(response.text)
    #requests库,默认会使用自己猜测的编码方式将爬取下来的网页进行解码,,然后存到text属性上面
    # 在电影天堂的网页中，因为编码方式，requests库猜错了，所以就会乱码 	 print(response.content.decode(encoding='gbk', errors='ignore'))
    #F12 在console输入document.charset 查看编码方式,要加上这个errors才能让程序跑通 response.content 会是将其中的解码方式改成自己所需要的解码方式
    text = response.content.decode(encoding='gbk', errors='ignore')
    html = etree.HTML(text)  # 解析网页
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    #在含有class=tbspan属性的table标签,因为一个网页有很多的class,
    #这个class=tbspan就是所需要爬取的数据的table的特征特定
    #然后就是这个table属性下的所有a标签中的所有href属性
    #for detail_url in detail_urls:
        #print(BASE_URL + detail_url)
    detail_urls=map(lambda url:BASE_URL+url,detail_urls)
    return detail_urls
    #以上代码就是相当于:
    #def abc(url):
    #    return BASE_URL+url
    #index=0
    #for detail_url in detail_urls:
    #    detail_url=abc(detail_url)
    #    detail_urls[index]=detail_url
    #    index+=1


def spider():
    movies = []
    base_url="https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    # 留一个{}所以就是会将其中槽填上
    for x in range(1,7):
        # for中找到其中的网页的几页
        print("==================================")
        print(x)
        print("==================================")
        # 如果有gbk识别不了的编码的话，就是会有出现错误,因为有一个特殊的字符是gbk识别编译不了
        # 那么解析网页的时候text=response.content.decode('gbk',errors='ignore')
        url=base_url.format(x)
        detail_urls=get_detail_urls(url)
        for detail_url in detail_urls:
            # 这个for循环是为了遍历一个页面中的全部电影详情的url
            # print(detail_url)
            movie = parse_detail_page(detail_url)
            movies.append(movie)
    print(movies)                     #爬完之后才会全部显示出来,时间有点慢的



def parse_detail_page(url):
    movie={}
    response = requests.get(url,headers=HEADERS)
    text = response.content.decode('gbk')     #解码
    html=etree.HTML(text)                     #返回元素
    #titles=html.xpath("//font[@color='#07519a']")
    #将详情页面上面的标题爬取下来,但是单单这样的话就是会将其中的其他的一样的标准的也是会爬取下来,那么就是将其独一无二的标签限定出来
    title=html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]       # 这样规定的div就可以爬取下特定的标题,加上text就会将对象编码的东西里面的文字打印出来
    #print(titles)
    #这样是把获取到的对象列表给打印出来
    #for title in titles:
        #print(etree.tostring(title,encoding='utf-8').decode('utf-8'))
        #以字符串的形式输出,不然就会以字节流的形式
    movie['titile']=title
    zoomE=html.xpath("//div[@id='Zoom']")[0]
    #zoom中含有很多所需要爬取的信息,而xpath中是返回一个列表所以就是要将其取第一个元素
    post_imgs=zoomE.xpath(".//img/@src")
    movie['post_imgs']=post_imgs
    #print(post_imgs)
    infos=zoomE.xpath(".//text()")
    #将zoom下的所有信息拿到
    #print(infos)

    def parse_info(info,rule):
        return info.replace(rule,"").strip()
    #定义一个函数,传入原来的字符串，输出后来修改后的字符串


    #for info in infos:
    for index,info in enumerate(infos):
        # 这样将对应的下表和元素给打印出来
        if info.startswith("◎年　　代"):
            # print(info)
            #info = info.replace("◎年　　代", "").strip()
            # 这个代码和下面那一行函数执行额代码是一样的
            # 将年代替换了之后，再将其中年代左右空格给替换掉
            info=parse_info(info,"◎年　　代")
            movie["year"]=info
        elif info.startswith("◎产　　地"):
            #info=info.replace("◎产　　地","").strip()
            info = parse_info(info, "◎产　　地")
            movie["country"]=info
        elif info.startswith("◎类　　别"):
            #info = info.replace("◎类　　别", "").strip()
            info = parse_info(info, "◎类　　别")
            movie["category"]=info
        elif info.startswith("◎豆瓣评分"):
            info=parse_info(info,"◎豆瓣评分")
            movie["douban_score"]=info
        elif info.startswith("◎片　　长"):
            info=parse_info(info,"◎片　　长")
            movie["duration"]=info
        elif info.startswith("◎导　　演"):
            info=parse_info(info,"◎导　　演")
            movie["director"]=info
        elif info.startswith("◎主　　演"):
            info=parse_info(info,"◎主　　演")
            #因为这个源代码是一行一个列表下标,所以就是比较特殊,要按照下标来进行数据的获取
            actors=[info]
            #要将第一个也搞进去
            for x in range(index+1,len(infos)):
            #index是主演中第一行的位置,那么我们就是应该从第二行开始进行遍历，
            #上面的第一行已经包括进去了
                actor=infos[x].strip()
                #去除两边的空格
                if actor.startswith("◎标　　签"):
                    break
                actors.append(actor)
                #把处理第一个全搞进去
            movie['actors']=actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info, "◎简　　介")
            #这个简介也是和上面演员的一样的
            movie["director"] = info
            for x in range(index+1,len(infos)):
                profile=infos[x].strip()

                if profile.startswith("【下载地址】"):
                    break
            movie["profile"]=profile
    download_url=html.xpath("//td[@bgcolor='#fdfddf']/a/@href")
    movie["download_url"]=download_url
    return movie

if __name__ == '__main__':
    spider()
