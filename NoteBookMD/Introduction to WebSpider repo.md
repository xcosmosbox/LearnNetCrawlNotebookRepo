# Introduction to WebSpider #

## 		1.第一章: 网络请求 ##

### *urllib库（已包含在python标准库）* ###

  #### 1.urlopen ####

  ​	返回一个类文件句柄对象，解析网页

  ```python
  resp=request.urlopen('http://www.baidu.com')  
  print(resp.read())
  ```

  

  #### 2.urlretrieve ####

  ​	将页面保存到本地中，取名‘baidu.com'

```python
request.urlretrieve('http://www.baidu,com','baidu.html')
```



  #### 3.urlencode ####

  ​	将字典数据转换为URL编码数据。若网址是中文，浏览器是会将中文编码成‘%+十六进制数’的形式。这是因为服务器是无法识别中文的。

```python
data={'name':'爬虫','great':'hello world','age':100}
qs=parse.urlencode(data)
print(qs)
```



  #### 4.parse_qs ####

  ​	可以将经过编码后的url参数进行解码

```python
qs='xxxxx'
print(parse.parse_qs(qs))
```



  #### 5.urlparse & urlsplit ####

  ​	urlparse & urlsplit 对url进行分割，分成若干部分，返回这些部分urlparse会多返回一个参数params，其它的部分和urlsplit一样。

  #### 6.request.Request类

  ​	用于进行添加请求头的时候，增加一些数据（为了防止反爬虫，比如增加User-Agent）

```python
headers={
        'User-Agent':'xxx'                                  #这是让服务器知道这个浏览器而不是一个爬虫.
        }
req=request.Request('http://www.baidu.com',headers=headers) #加上请求头所余姚的信息发送请求.
```



  #### 7.ProxyHandler处理器(代理设置) ####

  ​	代理的原理：在请求目的服务器之前，先请求代理服务器，然后让代理服务器去请求目的服务器网站,代理服务器拿到目的网站的数据后，再转发给我们的代码

```python
handler=request.ProxyHandler({"http":"xxxxxx"})   
#传入代理，要构建的代理是要字典的形式表示用ProxyHandler传入代理构建一个handler
opener=request.build_opener(handler)
#用handler创立一个opener
req=request.Request("http:xxxxxx")
resp=opener.open(req)
#调用这个opener去发送请求，就可以以代理的ip地址进行页面的访问请求
print(resp.read())

```



  #### 8.Cookie ####

  ​	将数据给服务器，然后用户的数据再返回给浏览器，让浏览器知道这个用户的身份(大小一般4KB)

  ​	Set-Cookie:NAME=VALUE;Expires/max-age=DATE;Path=PATH;Domain=DOMAIN_NAME;SECURE
  参数意义:

  ​	NAME:cookie的名字

  ​	VALUE:cookie的值

  ​	Expires:cookie过期的时间

  ​	Path:cookie作用的路径

  ​	Domain:cookie作用的域名 (作用的范围）

  ​	SECURE:是否旨在https协议下起作用

  ​	使用Cookie:

```python
from urllib import request
request_url="http://xxxxxxx"
headers={
'User-Agent':"xxxx",                               
#将这个请求模拟成浏览器，而不是一个爬虫机制，防止反爬虫
'cookie':'xxxx'                                    
#加入cookie，将用户信息放入，进行模拟包装，将其更像一个爬虫
}
request.Request(url=request_url,headers=headers)   #发送请求
resp=request.urlopen(req)                          #解析网页
print(resp.read().decode('utf-8'))                 
#将其读取下来，但同时要记得解码！不然会返回的都是经过编码的
with open('xxx.html','w',encoding='utf-8') as fp: 
#注意要加上encoding将str变成bytes,是因为str要以bytes才能写入硬盘当中
#毕竟是机器读写进去的
    #write函数必须写入一个str的数据类型
    #resp.read()读出来的是一个bytes数据类型
    #bytes要通过decode变成str
    #str要通过encode变成bytes
    fp.write(resp.read().decode('utf-8'))          
    #通过utf-8进行解码才能将其中的东西能让人能看的懂

```



  #### 9.http.CookieJar模块 ####

  ​	**1.CookieJar**
  ​		管理储存cookie对象，将其中都存放到内存当中

  ​	**2.FileCookieJar(filename, delayload=None, policy=None)**
  ​		从CookieJar派生而来，用来创建一个文件以来储存cookie，dalayload是表示可以支持延迟访问文件（有需要的时候才去访问文件）

  ​	**3.MozillaCookieJar(filename, delayload=None, policy=None)**
  ​		从FileCookieJar派生而来，创建与Mozilla浏览器cookies.

```python
from urllib import request,parse
from http.CookieJar import CookieJar
headers={
        'User-Agent':'xxxxx'
        }
#1.登陆页面
def get_opener():
    cookiejar=CookieJar()                                      
    #1.1 创建一个CookieJar对象 支持HTTP的请求
    handler=request.HTTPCookieProcessor(cookiejar)             
    #1.2 使用CookieJar创建一个HTTPCookieProcess对象
	#HTTPCookieProcess主要是处理cookie对象,并构建handler对象,这里的handler只是一个承接的作用
    opener=request.bulid_opener(handler)                       
    #1.4 使用上一步创建的handler,调用build_opener()的方法创建一个opener对象,参数是构建的处理对象                                                
    #1.5 使用opener发送登陆的请求
    return opener

def login_the_url(opener):
    data={"name":"xxxxx","password":"xxxxxx"}
    data=parse.urlencode(data).encode('utf-8')                 
    #注意发送请求的信息一定要经过编码才能被服务器接受
    login_url='http//:xxxx'                                    
    #这个页面是有登陆的那个页面
    req=request.Request(login_url,headers=headers,data=data)   
    #在获取个人网页的页面的时候,不要新建一个opener,
    opener.open(req)                                           
    #使用之前的opener就可以了,之前的那个opener已经包含了登陆所需要的cookie

#2.访问主页
def visit_profile(opener):                                     
    #这里的opener的信息也已经包含了cookie,就不需要进行再一次的创建新opener
    url="http://xxxxxx"                                        
    #这个页面是要所爬取信息的页面
    req=request.Request(url,headers=headers)
    resp=opener.open(req)                                      
    #这里不能用request.urlopen,这个发送请求是不支持带参数的,是请求不了里面的
    with open('xxx.html','w',encoding='utf-8') as fp:
        fp.write(resp.read().decode("utf-8"))                  
        #注意写入是要解码显示出来的

if __name__='main':
    opener=get_opener()
    login_the_url(opener)
    visit_profile(opener)

```



### *requests库* ###

#### 0.基本使用方法和示例代码 ####

```python
#导包
import requests

#将要查询的关键字
kw = {
    'wd':'中国'
}

#插入头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

# params 接收一个字典或字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
response = requests.get('http://www.baidu.com/s',params = kw,headers = headers)

#查看相应内容，response.text 返回的是Unicode格式的数据
print(response.text)

#查看相应内容，response.content 返回的字节流数据
print(response.content)

#查看完整url地址
print(response.url)

#查看响应头部字符编码
print(response.encoding)

#查看响应码
print(response.status_code)
```

​			**response.text** 和 **response.content** 的区别：

​				1.response.content：这个是直接从网络上面抓取的数据，没有经过任何解码，所有是一个bytes类型，其实在硬盘上和在网络上传输的字符串都是bytes类型。

​				2.response.text：这个是requests，将response.content进行解码的字符串，解码需要指定一个编码方式，requests会根据自己的猜测来判断编码的方式，所以有时候会猜测错误，猜测错误就会导致解码产生乱码，这时候就应该用`response.content.decode('某个解码模式')`进行手动解码。



#### 	1.发送get请求 ####

​			发送get请求，直接调用‘requests.get’就可以了。想要发送什么类型的请求，就调用什么方法。

​			以下为无参数的情况：

```python
response=request.get("http//:xxx")    #这样就可以进行请求访问网页了
```

​			以下为有参数的情况：

```python
import request
kw={"wd":"xxx"}
headers={"User-Agent":"xxx"}
response=request.get("http//:xxx",params=kw,headers=headers)
#这边这个params是接受一个字典或是字符串的查询参数,字典类型自动转换为url编码,不需要urlencode()
print(response.text)
#查看响应内容,response.text返回的是Unicode格式的数据,即经过Unicode编码的字符串,中文可能会乱码
print(response.content)
#查看响应内容,response.content 返回的是字节流数据
#后面response.content.decode('utf-8')才能看见中文的显示
```



#### 	2.发送POST请求 ####

​			发送Post请求很简单，直接调用`requests.post()`方法就行。不过需要注意的是，如果返回的数据是json数据，那么可以调用`response.json()`来将json字符串转换为字典或列表

```python
		    import request
            url='http://xxx'

            headers={
                'User-Agent':'http//:xxx',      
#这里是用户代理,让服务器知道这里一个浏览器,而不是一个爬虫
                'Referer':'http//:xxx'          
#用来表示从哪儿链接到当前的网页，服务器因此可以获得一些信息用于处理,这样服务器就不会不将其认为是爬虫
            		}

            data={                              #这个是在浏览上面的数据
            'first':'true',
            'pn':1,
            'kd':'python'
           }

            resp=request.post(url,headers=headers,data=data)
            print(resp.json)                       #将其转换成json格式

```



#### 3.使用代理 ####

​			在请求方法中，传递`proxies`参数就可以了

```python
           import requests

            proxy={
            'http':'xxx'                        #代理ip地址
            }

            response=requests.get("http//:xxx",proxies=proxy)
            print(response.text)

```



#### 4.处理cookie并使用Session共享cookie ####

​			如果想要多次请求中共享cookie，那么久应该使用Session。

```python
   			import request
            url="http//:xxx"
            data={
                    "name":"xxx","password":"xxx"
                }
            headers={
                    'User-Agent':"xxx"
            }
            session=requests.session()                             #session的不同就是可以自带cookie
            session.post(url,data=data,headers=headers)
            response=session.get('http//:xxx')
            print(response.text)

```



#### 5.处理不信任的SSL证书

​		    (有一些网站的证书是不会被信任的）网址会有红色的不安全,对于已经信任的证书就可以直接进行request的访问就行了

```python
'''
    如何去处理不被信任的SSL网站
'''

#导包
import requests

url = '不被信任的SSL证书的网址'

'''只需要加上 verify=False 就能正常输出了'''
response = requests.get(url,verify=False)

print(response.content.decode('utf-8'))
```





-- --

## 2.第二章：数据解析 ##

| 解析工具      | 解析速度 | 使用难度 |
| ------------- | -------- | -------- |
| BeautifulSoup | 最慢     | 最简单   |
| lxml          | 快       | 简单     |
| 正则表达式    | 最快     | 最难     |



### *XPath语法* ###

#### 1.选取节点 ####

| 表达式   | 描述                                                         | 示例           | 结果                            |
| -------- | ------------------------------------------------------------ | -------------- | ------------------------------- |
| nodename | 选取此节点的所有子节点                                       | bookstore      | 选取bookstore下所有的子节点     |
| /        | 如果是在最前面，代表从根节点选取。否则选择某节点下的某个节点。 | /bookstore     | 选取根元素下所有的bookstore节点 |
| //       | 从全局节点中选择节点，随便在那个位置                         | //book         | 从全局节点中找到所有的book节点  |
| @        | 选取某个节点的属性                                           | //book[@price] | 选取所有拥有price属性的bok节点  |

示例：

1)nodename(选取此节点的所有子节点)

 eg:bookstore 就会选取bookstore下所有的子节点

 2) / (如果在最前面，代表从根节点选区。否则选择某节点下的某个节点)局部

 eg:/bookstore 就选取到了根元素下所有的bookstore节点

 eg: 在网页上/div 是找不到的,因为这个是在根节点上找的,而在根节点html上面是没有div的

 div是在其中的孙节点body中,/html是可以找到的,但是/html/div 就是找不到的

 3) // (从全局节点中选择节点,随便在哪个位置)全局

 eg: //book 从全局节点中找到所有的book节点

 eg: //head/script 从head中选中局部的script就是单单是head中的script

 eg: //script 从全局当中选中script,不单单是局限与head中的script,也有可以能是body当中的script

4) @ (选区某个节点的属性) 有点类似面向对象的类的属性

```xml
              <book price="xx">       这个price就是book的属性
               eg: //book[@price]     选择所有拥有price属性的book节点

```

```xml
              <div id="xxx">         这个id就是div的属性
           	  eg: //div[@id]         选择所有拥有id属性的div节点

```



#### 2.谓语 ####

谓语是用来查找某个特定的节点或包含某个指定的值的节点，被嵌在方括号中。在下面的表格中，我们列出了带有谓语的一些路径表达式，以及表达式的结果：

| 路径表达式                   | 描述                              |
| ---------------------------- | --------------------------------- |
| /bookstore/book[1]           | 选取bookstore下的第一个子元素     |
| /bookstore/book[last()]      | 选取bookstore下倒数第二个元素     |
| bookstore/book[position()<3] | 选取bookstore下前面两个子元素     |
| //book[@price]               | 选取拥有price属性的book元素       |
| //book[@price=10]            | 选取所有属性price等于10的book元素 |

示例：

用来查找某个特定的节点或者包含某个指定的值的节点,被嵌在方括号中

 1)

 eg:/bookstore/book[1] 选取bookstore下的第一个子元素

 eg://body/div[1] 获取body当中的第一个div元素

 2)

 eg:/bookstore/book[last()] 选取bookstore下的倒数第二个book元素

 3)

 eg:bookstore/book[position()] 选取bookstore下前面两个子元素

 eg://body/div[position()] 选取body元素的div下的前两个position元素

 4)

 eg://book[@price] 选取拥有price属性的book元素

 5)

 eg://book[@price=10] 选取所有属性price等于10的book元素节点

 eg://div[@class=‘s_position_list’] 可以获取div下的有s_position_list的class节点

 模糊匹配contains:

```xml
 eg:<div class="content_1 f1">            只选取其中的f1属性则有
	//div[contains(@class,"f1")]              
	使用contains进行模糊匹配,匹配到class下的f1属性

```



#### 3.通配符 ####

(*表示通配符)

| 通配符 | 描述                 | 示例         | 结果                       |
| ------ | -------------------- | ------------ | -------------------------- |
| *      | 匹配任意节点         | /bookstore/* | 选取bookstore下所有子元素  |
| @*     | 匹配节点中的任何属性 | //book[@*]   | 选取所有带有属性的book元素 |

 1) * 匹配任意节点

 eg:/bookstore/* 选取bookstore下的所有子元素

 2) @* 匹配节点中的任何属性

 eg://book[@*] 选取所有带有属性的book元素



#### 4.选取多个路径 ####

(通过 | 运算符来选取多个路径)

 1)

 eg://bookstore/book | //book/title

 #选取所有bookstore元素下的book元素以及book元素下的所有所有title元素

 eg://dd[@class=“job_bt”] | //dd[@class=“job-advantage”]

 #选取所有dd下的class的job_bt和job-advantage的所有属性，还有其他运算符 and or之类的。

```xml
//bookstore/book | //book/title
# 选取所有book元素以及book元素下面的title元素
```



#### 5.Summary ####

 1.使用//获取整个页面当中的元素，然后写标签名，然后在写谓词进行提取。

 eg: //div[@class=‘abc’]

 2./只是直接获取子节点,而//是获取子孙节点

 3.contains: 有时候某个属性中包含了多个值,那么可以使用contains函数

 eg: //div[contains(@class,‘xxx’)]



### *lxml库* ###

#### 1.基本使用

1)解析html字符串:使用lxml.etree.HTML进行解析

```python
from lxml import etree    (这是用c语言写的)
text="这里就是代码"                                   
#这里的代码是不规范的不完整的html
html=etree.HTML(text)                                
#利用etree.HTML类,将字符串变成为HTML文档再进行解析,但是这是一个对象
result=etree.tostring(text,encoding='utf-8')         
#按字符串序列化HTML文档,但是这个是bytes类型,为了防止乱码,加上encoding='utf-8'
#那么就是说解析这个网页的时候要用utf-8的形式来进行编码,防止乱码,因为默认是unicode编码
result.decode('utf-8') 
#要解码为了使人可以看懂

```



2)解析html文件: 使用lxml.etree.parse继续解析

```python
#效果和上面一样，但是这个两个方法都是默认使用XML解析器，所以如果碰到一些不规范的HTML代码的时候就会解析错误，这时候就要自己创建HTML解析器了
parser=etree.HTMLParser(encoding='utf-8')               
#构建HTML解析器,防止网页的源代码的缺失
html=etree.parse("tencent.html(放地址)",parser=parser)  
#可以进行这parse就可以直接对其进行解析,但是有时候有些网页不完整
#少一个div之类的,这时候就是会报错,解决方法就是加上parser解析器
result=etree.tostring(text,encoding='utf-8')
result.decode('utf-8')
```



3)创建带有HTML解析器的代码和所有相关示例的演示代码（包含了以腾讯的html为例子，讲解lxml和xpath的结合应用）:

```python
from lxml import etree

parser = etree.HTMLParser(encoding="utf-8")  # 构造HTML解析器,防止网页不完整而解析不了
html = etree.parse("tencent.html", parser=parser)



# xpath函数是返回一个列表
# 1.获取所有的tr标签   //tr
trs = html.xpath("//tr")
for tr in trs:
    # print(tr)  
    # 这样的话是直接返回一个迭代器对象,人是看不懂的,要经过解码才行.
    print(etree.tostring(tr, encoding="utf-8").decode("utf-8"))
    # 就是直接用etree.tostring变成字符串,然后再进行编码,再进行解码
    # 可以用先不用decode试试再加上decode

    
    
# 2.获取第二个tr标签
trs = html.xpath("//tr[2]")     # 这是返回一个元素,迭代器元素
print(trs)
trs = html.xpath("//tr[2]")[0]  # 这就是取这里的第一个元素
print(trs)
print(etree.tostring(trs, encoding='utf-8').decode("utf-8"))
# 以字符串的形式,utf-8的编码方式再解码才能让这个迭代器元素呈现出来,即是网页的源代码



# 3.获取所有class等于even的tr标签
evens = html.xpath("//tr[@class='even']")
for even in evens:
    print(etree.tostring(even, encoding="utf-8").decode("utf-8"))
# 先是写tr标签,再写符合class属性等于even的所有标签



# 4.获取所有a标签的href属性,这边这个是属性,返回属性,href属性其实就是网址域名后面的那一串东西
ass = html.xpath("//a/@href")
print("http://hr.tencent.com/" + ass)  # 就可以直接进行点击网页
# 4.1获取所有href属性的a标签,这边这个是显示a这个容器中的所有东西,毕竟[]
ass = html.xpath("//a[@href]")



# 5.获取所有的职位信息(纯文本)
"""<tr>
<td class="xxx"><a target="xxx" href="xxx">我是第一个文本</a></td>
<td>我是第二个文本</td>
<td>我是第三个文本</td>
</tr>"""
words = html.xpath("//tr[position()>1]")  # 除了第一个tr标签,其他全获取
all_things=[]
for word in words:
    # href=tr.xpath("a")                   
    # 获取a标签,但是这样是默认tr下的直接a标签,但是这时候是获取不到的,
    # 因为a不是tr的直接子标签,td才是直接子标签
    # href=tr.xpath("//a")                 
    # 这样是相当于忽视了前面的tr.的默认,因为加了//就是全局的a标签了
    href = tr.xpath(".//a")                
    # 在某个标签下,再执行xpath函数,获取这个标签的子孙元素,那么//前加了一个点就是相当于是当前这个tr.并且是仅限于该tr.标签下的a标签
    href = tr.xpath(".//a/@href")          
    # 得到第一个a标签的href属性,href就是页面后面的网址的那一部分
    title = tr.xpath(".//a/text()")        
    # 这样就可以获取到a标签下的所有文本即"我是第一个文本"
    title = tr.xpath("./td/text()")        
    # 这样就可以获取到td标签下的所有文本,但是这里只是获取到"我是第二个文本",所以上面的那个"我是第一个文本"这个信息是在a标签下的并不是直接属于td的
    title1 = tr.xpath("./td[1]//text()")   
    # 这里就是第一个td标签,注意这是和python的索引不一样的,这个是从1开始的,python的是从0开始的
    # 因为这里面的文本并不是td的直接子元素,a才是td的直接子元素,所以我们就是要将器变成//text(),而不是/text()
    title2 = tr.xpath("./td[2]//text()")   # 就可以拿到第二个文本,即"我是第三个文本"
    all_thing={
        "first": title1,                   # 将其变成列表形式
        "second": title2
    }
    all_things.append(all_thing)           # 将其放给列表当中
    print(href)
    break

# lxml结合xpath注意事项:
# 反复练习才有用

```



### 小结：豆瓣和电源天堂项目实战 ###

#### 豆瓣： ####

```python
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

```

#### 电影天堂：

```python
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

```



### BeautifulSoup4 ###

和lxml一样，BeautifulSoup也是一个html和xml的解析器，主要功能也是如何提取其中的数据

lxml只是会局部遍历，而BeautifulSoup是基于HTML DOM(Document Object Model)的，会载入整个文档，解析整个DOM树，因此时间和内存开销都会大很多，所以性能要比lxml低

BS用来解析HTML比较简单，API非常人性化，支持CSS选择器，python标准库中的HTML解析器，也支持lxml的XML解析器。

但是BeautifulSoup的底层还是lxml,就像python的底层还是C,所以解析还是要依照第三方的解析器

| 解析器          | 使用方法                                                     | 优势                                                      | 劣势                          |
| --------------- | ------------------------------------------------------------ | --------------------------------------------------------- | ----------------------------- |
| python标准库    | BeautifulSoup(markup，“html.parser”)                         | python内置标准库，执行速度快，容错能力强                  | python3.3之前的版本效果比较差 |
| lxml HTML解析器 | BeautifulSoup(markup,“lxml”)                                 | 速度快，容错能力强                                        | 需要安装C语言库               |
| lxml XML解析器  | BeautifulSoup(markup,[“lxml”，“lxml”])   BeautifulSoup(markup，“xml) | 速度快，唯一支持XML解析器                                 | 需要安装C语言库               |
| html5lib        | BeautifulSoup(markup，”html5lib“)                            | 最好的容错性，以浏览器的方式解析文本，生成HTML5格式的文档 | 速度慢，不依赖外部扩展        |

如果是比较奇葩的网页，建议就用html5lib来进行解析网页，防止报错，他是会自动修复错误存在的。

简单使用：

```python
from bs4 import BeautifulSoup
html="""

		xxxxxx #HTML代码的字符串

	"""

bs=BeautifulSoup(html,"lxml")		#将其变成html模式,补上缺失的成分

print(bs.prettify())				#以比较美观的方式打印出来

```



#### 1.四个常用对象：

BeautifulSoup将复杂的HTML文档换成一个复杂的树形节点,每个节点都是Python对象,所有对象都可以归结为4种:

1. Tag：BeautifulSoup中所有的标签都是Tag类型，并且BeautifulSoup的对象其实本质上也是一个Tag类型。所以其实一些方法比如find、find_all并不是BeautifulSoup的，而是Tag
2. NavigableString：继承自python中的str，用起来就跟python的str是一样的。
3. BeautifulSoup：继承自Tag。用来生成BeautifulSoup树的。对于一些查找方法，比如find、select这些，其实还是Tag的。
4. Comment：这个就是继承自NavigableString。



#### 2.find&find_all

find：

1. 只能提取第一个的标签,只是找到一个就返回了

find_all：

0. 可以提取所有的标签,以列表的形式返回多个元素
1. 在提取标签的时候,第一个参数就是标签的名字。然后如果在提取标签的时候想要使用属性进行过滤,那么可以在这个方法中通过关键字参数的形式,将属性的名字以及对应的值传进去。或者是使用’attrs’属性,将所有的属性以及对应的值放在一个字典中传给’attrs’属性
2. 有些时候,在提取标签的时候,不想提取那么多,那么可以使用’limit’ 限制提取多少个



使用find和find_all的过滤条件：

1. 关键字参数：将属性的名字作为关键字的名字，以及属性的值作为关键字参数的值进行过滤。
2. attrs参数：将属性条件放到一个字典中，传给attrs参数



获取标签的属性：

1. 通过下标的方式：

   ```python
   href = a['href']
   ```

   

2. 通过`attrs`属性获取：

   ```python
   href = a.attrs['href']
   ```

   



#### 3.string，strings，stripped_strings，get_test

string：

获取某个标签下的非标签字符串,只是一个,以普通字符串的形式返回

strings：

获取某个标签下的所有子孙非标签字符串，返回生成器,可以加上list变成列表形式

stripped_strings：

获取某个标签下的所有子孙标签的字符串并且去掉空格,返回生成器,方法上同

get_text：

获取某个标签下的所有子孙非标签字符串,但是不是以列表返回,以普通字符串返回



#### 4.使用BeautifulSoup实现以下需求

1. 获取所有的tr标签
2. 获取2个tr标签
3. 获取所有class等于even的tr标签
4. 将所有id等于test。class也等于test的a标签提取出来
5. 获取所有a标签的href属性
6. 获取所有的职位信息(纯文本)

代码实现：

```python
from bs4 import BeautifulSoup

html="""
xxxxxx
"""
soup=BeautifulSoup(html,"lxml")


#1.获取所有的tr标签
trs=soup.find_all('tr')
for tr in trs:
    print(tr)
    print(type(tr))  
    #这是一个Tag类型,但是BeautifulSoup里面的repr方法将Tag以字符串的形式打印出来


#2.获取2个tr标签
trs=soup.find_all('tr',limit=2)  
#limit最多获取两个元素,返回列表,最后加上[1]才是返回第二个元素


#3.获取所有class等于even的tr标签

trs=soup.find_all('tr',class_='even')  #class是python的关键字,所以bs4当中加上下划线加以区分
for tr in trs:
    print(tr)

trs=soup.find_all('tr',attrs={'class':"even"})  #可以用attrs里面的信息作为参数
for tr in trs:
    print(tr)

#4.将所有id等于test,class也等于test的a标签提取出来
aList=soup.find_all('a',id='test',class_='test')   #有多少个特点也可以一直上去
for a in aList:
    print(a)

aList=soup.find_all('a',attrs={"id":"test","class":"test"})   #有多少个特点也可以一直上去
for a in aList:
    print(a)


#5.获取所有a标签的href属性
aList=soup.find_all('a')    #找到所有的a标签
for a in aList:
    # 1.通过下标的操作
    href=a['href']     		#这种方式比较简单
    print(href)
    #2.通过attrs属性
    href=a.attrs['href']    #获取a标签下的href属性
    print(href)

#6.获取所有的职位信息(纯文本)
trs=soup.find_all('tr')[1:]    #职位信息都在tr标签以内,第一个不是,所以就是要到一以后的就行了
infos_=[]
for tr in trs:
    info={}
    #方法一
    tds=tr.find_all("td")      #找到tr标签下所有的td标签
    title=tds[0]               #title元素都是藏在其中的
    print(title.string)        #就可以将其中的字符串提取出来了
    title=tds[0].string        #tds中的第一个元素就是标题
    category=tds[1].string     #tds中的第二个元素就是分类
    nums=tds[2].string         #tds中的第三个元素就是个数
    city=tds[3].string         #tds中的第四个元素就是城市
    pubtime=tds[4].string      #tds中的第五个元素就是发布时间
    info['title']=title
    info['category']=category
    info['nums']=nums
    info['city']=city
    info['pubtime']=pubtime
    infos_.append(info)

    #方法二
    #infos=tr.strings             
    #可以将其中的纯文本(非标签)给全都爬取下来,这样的话是拿到一个生成器,一个对象
    #for info in infos:
    #    print(info)                  #就可以打印出来了
    #infos = list(tr.string)
    infos=list(tr.stripped_strings)   #可以将其中的字符串中的空格去掉
    info['title']=infos[0]
    info['category']=infos[1]
    info['nums']=infos[2]
    info['city']=infos[3]
    info['pubtime']=infos[4]
    infos_.append(info)               #更加简洁简单

```



#### 5.select方法

有时候选择css选择器会可以更加的方便，使用select方法可以方便的找出元素。但有时候使用`css`选择器的方式可以更加的方便。使用`css`选择器的语法，应该使用`select`方法。以下列出的集中常用的`css`选择器方法：

1. 通过标签名查找：soup.select(‘a’) #寻找a标签

   ```python
   print(soup.select('a'))
   ```

   

2. 通过类名查找：通过类名就是要加上一个.。

   比如要查找class=‘sister’

   soup.select(’.sister’)

   ```python
   print(soup.select('.sister'))
   ```

   

3. 通过id查找：通过id查找就是要加上一个#。

   比如要查找id=‘link’

   soup.select(’#link’)

   ```python
   print(soup.select('#link1'))
   ```

   

4. 组合直线：soup.select(“p #link1”) #这里会找到p中所有的含有link1属性的id标签

   ```python
   print(soup.select("p #link1"))
   ```

   soup.select(“head>titile”)#这里就是会将其中的head下的直接子元素获取到，而不会获取到孙元素

   ```python
   print(soup.select("head > title"))
   ```

   

5. 通过属性查找：查找时还可以加入属性元素，属性需要用中括号括起来。

   soup.select(‘a[href=“http://www.baidu.com”]’)

   ```python
   print(soup.select('a[href="http://example.com/elsie"]'))
   ```

   

6. 获取内容：以上的select方法返回的结果都是列表的形式，可以遍历形式输出，然后用get_text()方法来获取它的内容。

   ```python
   soup = BeautifulSoup(html.'lxml')
   print type(soup.select('title'))
   print soup.select('title')[0].get_text()
   
   for title in soup.select('title'):
   	print title.get_text()
   ```

7. 应用示例代码 ①：

   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title></title>
       <style type="text/css">
           .line1{
               background-color: pink;
           }
           #line2{
               background-color: rebeccapurple;
           }
           .box p{ /*会将全部的子孙元素选取*/
               background-color: azure;
           }
           .box > p{ /*这里是将其中的子元素给搞了,孙元素没有被搞*/
               background-color: aqua;
           }
           input[name='username']
           {
               background-color: coral;
           }
   
       </style>
   </head>
   <body>
   <div class="box">
       <div>
           <p>the zero data</p>  /*这是孙元素*/
       </div>
       <p class="line1">the first data，class可以出现无数次</p>
       <p class="line1">the second data，而class就是要用.</p>
       <p id="line2">the third data，一个网页的id不能一样，这个id就是要用#</p>
       /*这是直接的子元素*/
   </div>
   <p>
           the fourth data
   </p>
   <from>
       <input type="text" name="username">
       <input type="text" name="password">
   </from>
   </body>
   </html>
   ```

   

   应用示例代码 ②：

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Title</title>
       <!--第一种情况-->
   <!--    <style type="text/css">-->
   <!--        #line3{-->
   <!--            background-color : pink;-->
   <!--        }-->
   <!--    </style>-->
   
       <!--第2种情况-->
   <!--    <style type="text/css">-->
   <!--        .box{-->
   <!--            background-color : pink;-->
   <!--        }-->
   <!--    </style>-->
   
        <!--第3种情况-->
   <!--    <style type="text/css">-->
   <!--        p{-->
   <!--            background-color : pink;-->
   <!--        }-->
   <!--    </style>-->
   
            <!--第4种情况-->
   <!--    <style type="text/css">-->
   <!--        .line1{-->
   <!--            background-color : pink;-->
   <!--        }-->
   <!--    </style>-->
   
           <!--第5种情况-->
   <!--    <style type="text/css">-->
   <!--        .box p{-->
   <!--            background-color : pink;-->
   <!--        }-->
   <!--    </style>-->
   
               <!--第6种情况-->
       <style type="text/css">
           .box > p{
               background-color : pink;
           }
       </style>
   </head>
   <body>
       <div class="box">
           <div>
               <p>第零行数据</p>
           </div>
           <p class="line1">第一行数据</p>
           <p class="line1">第二行数据</p>
           <p id="line3">第三行数据</p>
       </div>
       <p>第四行数据</p>
       <form >
           <input type="text" name="username">
           <input type="text" name="password">
       </form>
   </body>
   </html>
   ```



#### 6.CSS选择器

1. 根据标签的名字选择，示例代码如下：

   ```html
   p{
               background-color : pink;
     }
   ```

   

2. 根据类名选择，那么要在类的前面假一个点。示例代码如下：

   ```html
   .line1{
           background-color : pink;
          }
   ```

3. 根据id名字选择，那么要在id的前面加一个#号。

4. 查找子孙元素，那么要在子孙元素中间有一个空格。

5. 查找直接子元素。那么要在父子元素中间有一个 ’>’ 。

6. 根据属性的名字进行查找，那么应该险些标签的名i在，然后再在中括号中写属性的值。

7. 根据类名或id进行查找时，如果还要根据标签名进行过滤。那么可以在类名前或在id的前面加上标签的名字。

8. BeautifulSoup中使用css选择器：在`BeautifulSoup`中，要使用css选择器，那么应该使用`soup.select()`方法。应该传递一个css选择器的字符串给select方法。

9. **contents和children：**

   返回某个标签下的直接子元素，其中也包括字符串。它们两的区别是：contents返回来的是一个列表，children返回的是一个迭代器。



#### 7.爬取中国天气网的今日天气信息，并将所有城市的天气排序，取温度最低的十个城市，并将它们利用pyecharts库进行数据可视化

```python
#爬取所有省份所有城市的最低气温，并进行排名，将排名制作成图表并输出到html中，以供可视化打开。

#导包
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar

ALL_DATA = []

#解析页面的方法
def parse_page(url):
    #注入头部，伪装为正常访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    #使用requests.get去拉去指定url下的页面，并使用上述的头部去伪装为正常的访问
    response = requests.get(url,headers=headers)
    #将拉取到的网页信息以指定的解码形式（避免乱码），存储到text中
    text = response.content.decode('utf-8')
    #以下使用BS4库中的方法，构建lxml框架下的html解析器，解析刚刚拉去到的信息
    #之所以使用html5lib而不是常见的xml，是因为网页中的源代码，由于目的网址程序员的失误，在关于港澳台那一页的天气信息中，<table>标签最后缺少</table>，如果使用xml来提取则会出现许多不需要的错误信息。而html5lib是接近于浏览器的框架，容错率极高，会自动补全那个缺少的</table>以完成程序(但改用此框架后，程序的运行效率会不可避免的下降)。成功后的图片见pic2.png
    soup = BeautifulSoup(text,'html5lib')
    #使用解析器中的find方法，筛选出存储了天气信息z中‘class’等于conMidtab的表，并将表中标签为table的信息存储在tables表中(网页信息中的table表头是以省份为表头)。由于使用了BeautifulSoup库，所以整个网页已经被处理为了 树 的形式，并且被提取出来的信息此时不再是 string 类型，而是 Tag 类型
    conMidtab = soup.find('div',class_ = 'conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1] #之所以从第1个开始取，而不是第0个标签开始取，是因为网页中第0个标签是省份，而我们只取所有的城市
            city = list(city_td.stripped_strings)[0] #此句子将会通过迭代器遍历指定节点下所有的节点，并过滤掉空白的部分，且返回一个生成器,最后转换为一个列表
            # print(city) 此句可以打印出上述列表中的城市列表，其中包含了华北地区城市的名字，效果见 pic1.png
            #接下来几句的作用是获得城市温度,之所以知道倒数第二个 ‘td’ 标签是温度，是根据我们手动从网页源代码中观察得到的
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            # print({'city':city,'min_temp':min_temp}) //以列表的形式输出城市和对应城市的温度
            ALL_DATA.append({'city':city,'min_temp':int(min_temp)}) #最后的min_temp处自所以需要用int强制转换，是因为后面在排序的过程中，默认输出char类型的数据，所以需要强制转换以输出整数数据


#执行方法
def main():
    #将所有连接制成一个列表
    urls = {
        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml"
    }
    #遍历所有的列表爬取城市和温度
    for url in urls:
        parse_page(url)

    #分析数据,根据最低气温进行排序
    '''
        方法一：传递一个方法根据指定的字典元素进行排序
        def sort_key(data):
            min_temp = data['min_temp']
            return min_temp
        ALL_DATA.sort(key=sort_key)
        缺点：sort_key方法在本程序中不需要复用，所以没有必要实例整个方法，造成性能浪费
    '''
    '''方法二：利用lambda表达式使用匿名函数完成同样的功能，代码如下：'''
    ALL_DATA.sort(key=lambda data: data['min_temp'])

    #只取前十名温度最低的城市
    data = ALL_DATA[0:10]

    #使用lambda表达式取筛选需要的信息，接着用map映射得到的数据，并转换为list以便绘图
    cities = list(map(lambda dic:dic['city'],data))
    temps = list(map(lambda dic:dic['min_temp'],data))

    '''绘图'''
    #第一步：创建柱状图对象
    chart = Bar()
    #第二步：设置柱状图的横纵坐标以及名字
    chart.add_xaxis(cities)
    chart.add_yaxis("今日中国最低气温",temps)
    #第三步：输出柱状图到html文件中
    chart.render('Temperature.html')

#程序入口
if __name__ == '__main__':
    main()
```



### 正则表达式 ###

#### 什么是正则表达式？ ####

正则表达式(Regular Expression)是一种文本模式，包括普通字符（例如，a 到 z 之间的字母）和特殊字符（称为"元字符"）。

正则表达式使用单个字符串来描述、匹配一系列匹配某个句法规则的字符串。

#### 正则表达式的常用匹配规则:

1. 匹配单个字符：

```python
text='hello'

ret=re.match('he',text)  #这里就是在hello中匹配he,但是只能是在第一个匹配,如果是ahello就会报错匹配不到

print(ret.group()) #group可以将其中的值打出来

>>he
```

以上便可以在`hello`中匹配出`he`



2. 点(.)匹配任意的字符:

```python
text="ab"

ret=re.match('.',text)  #match只能匹配到一个字符

print(ret.group())

>>a
```

但是(.)不能匹配到换行符 text="\n" 就是会报错!



3. \d匹配到任意的数字:

   ```python
   text="123"
   
   ret=re.match('\d',text)   #只能匹配到一个字符
   
   print(ret.group())
   
   >>1
   ```

   

4. \D匹配任意的非数字:

   ```python
   text="+"
   
   ret=re.match('\D',text)   #只能匹配到一个字符
   
   print(ret.group())
   
   >>a
   ```

   

5. \s 匹配到是空白字符(\n,\t,\r,空格):

```python
text=" "

ret=re.match('\s',text)   #只能匹配到一个字符

print(ret.group())

>> 
```



6. \w（小写的）匹配到的是a-z和A-Z以及数字和下划线:

   ```python
   text="_"
   
   ret=re.match('\w',text)   #只能匹配到一个字符
   
   print(ret.group())
   
   >>_
   ```

   而如果是要匹配到一个其他字符，那么就匹配不到:

   ```python
   text="+"
   
   ret=re.match('\w',text)   #只能匹配到一个字符
   
   print(ret.group())
   
   >>报错
   ```

   

7. \W（大写的）匹配的适合\w是相反的:

   ```python
   text="+"
   
   ret=re.match('\W',text)   #只能匹配到一个字符
   
   print(ret.group())
   
   >>+
   ```

   

8. [] 组合的方式,只要满足中括号里面的字符就可以匹配到:

   ```python
   text="0888-88888"
   
   ret=re.match('[\d\-]+',text)   #匹配到数字和-，加了个+号之后就是会匹配到所有的符合的，直到不满足条件为止
   
   print(ret.group())
   
   >>0888-88888
   ```

   ```python
   代替
   
   \d:[0-9]       [^0-9]防在中括号中‘^’这是非
   
   \D:0-9
   
   \w:[0-9a-zA-Z_]     [^0-9a-zA-Z_]
   
   \W:[0-9a-zA-Z_]
   
   ```

   ```python
   text="0888-88888"
   
   ret=re.match('[^0-9]',text)   
   
   print(ret.group())
   
   >>-
   ```

   

9. 匹配多个字符:

   1. `*`可以匹配0或是任意多个字符，没有不会报错：

      ```python
      text="0888-88888"
      
      ret=re.match('\d*',text)   
      
      print(ret.group())
      
      >>0888
      ```

      

   2. `+`可以匹配1或是任意多个字符，至少要一个，不然报错:

      ```python
      text="abcd"   #text="+abcd"
      
      ret=re.match('\w+',text)   
      
      print(ret.group())
      
      >>abcd     #>>ab  
      ```

      

   3. `？`匹配一个或0个（要么没有，要么只有一个）:

      ```python
      text="abcd"  #text="+abcd"
      
      ret=re.match('\w?',text)   
      
      print(ret.group())
      
      >>a			#>>   匹配到0个
      ```

      

   4. `{m}`匹配到m个:

      ```python
      text="abcd"  #text="+abcd"
      
      ret=re.match('\w{2}',text)   
      
      print(ret.group())
      
      >>ab   #只是会匹配到两个
      ```

      

   5. `{m,n}`匹配m-n个:

      ```python
      text="abcd"  #text="+abcd"
      
      ret=re.match('\w{1,5}',text)    #匹配最多的
      
      print(ret.group())
      
      >>abcd    #>>报错
      ```

      

10. 小案例

    1. 验证手机号码

       ```python
       text="13070970070" 
       
       ret=re.match('1[34578]\d{9}',text)    #验证,第一位是1,第二位是34578里面当中的一个后面九个随便
       
       print(ret.group())
       ```

       

    2. 验证邮箱

       ```python
       text="together13_@11.com" 
       
       ret=re.match('\w+@[a-z0-9]+\.[a-z]+',text)    #第一位w匹配到任意的字符,然后就是至少要有一位,所以要是有+号,直到匹配到异常@即不属于w的匹配,然后就是要有@而只有一个@,然后再匹配@后面的一个或者多个字符,然后就是\.匹配任意字符来匹配.最后的com就是用一个[a-z]来匹配，也可能会有+号
       
       print(ret.group())
       ```

       

    3. 验证url

       ```python
       text="http://www.baidu.com" 
       
       ret=re.match('(http|https|ftp)://[^\s]+',text)    #前面用圆括号阔了起来，然后就是http,https,ftp三个里面的选择一个,然后就是//匹配到非空的就行了
       
       print(ret.group())
       ```

       

    4. 验证身份证

       ```python
       text="12345678909876543x" 
       
       ret=re.match('\d{17}[\dxX]',text)    #前面的十七位可以是数字，然后后面一个可能是数字也可能是数字，也可能是x或是X，就用一个中括号括起来
       
       print(ret.group())
       ```

       

11. 本章知识拾遗并小结

    1. $ 表示以。。。结尾

       ```python
       text="xxx@163.com"
       
       ret=re.match('\w+@163.com$',text)   # 以163.com结尾就可以更好验证邮箱
       
       print(ret.group())
       ```

       

    2. ^脱字号:表示以…开始（如果是在中括号当中就是取反的意思）

       ```python
       text="hello"
       
       ret=re.match('^a',text)   # 这个match是自带脱字号的
       
       print(ret.group())
       
       >>h
       ```

       ```python
       text="hello"
       
       ret=re.search('o',text)   # 这个search是全局去找
       
       print(ret.group())
       
       >>o
       ```

       ```python
       text="hello"
       
       ret=re.match('^o',text)   # 脱字号第一个不是o如果是^h就可以找到h
       
       print(ret.group())
       
       >>报错
       
       ```

       

    3. | 匹配多个字符串或是表达式

       ```python
       text="https"
       
       ret=re.match('http|https|ftp',text)   # 如果组合要用()括起来
       
       print(ret.group())
       ```

       

    4. 贪婪模式与非贪婪模式

       ```python
       #导入python中包含了正则表达式的包
       import re
       
       #贪婪模式和非贪婪模式
       text='0123456'
       ret=re.match('\d+',text) #此时就是贪婪模式，因为这句的意思是至少匹配出一个，但可以匹配处任意多个字符，甚至一直将全部都匹配出来
       print(ret.group())
       
       ret=re.match('\d+?',text) #此时就是非贪婪模式。只要匹配出一个后，就结束了。
       print(ret.group())
       
       #贪婪模式举例2：
       text='<h1>标题</h1>'
       ret=re.match('.+',text)
       print(ret.group())
       ```

       

    5. 小练习：匹配0-100之间的数字

       ```python
       #导入python中包含了正则表达式的包
       import re
       
       '''匹配0-100之间的数字
           可以出现的：0、9、1、10、100、99
           不能出现的：09、01
           三种情况：
               一位数字
               两位数字
               三位数字，但只能等于100
       '''
       text='32'
       ret=re.match('0$|[1-9]\d?$|100$',text)
       print(ret.group())
       ```

       

    6. 原生字符串和转义字字符

       ```python
       #转义字符和原生字符串
       
       text = 'apple price is $299'
       ret = re.search('\$\d+',text)
       print(ret.group())
       
       text = '\\n'
       rett = re.match('\\\\n',text) #利用多次转义消除最开始的转义符号的影响，最终输出字符串’\n‘
       print(rett.group())
       rett = re.match(r'\\n',text) #或者是使用python的原生字符串，直接将转义一次后的结果进行查询
       print(rett.group())
       ```

       

    7. match：

       1. 从开始的位置进行匹配。如果开始的位置没有匹配到。就直接失败了。示例代码如下：

          ```python
          text='hello'
          ret=re.match('he',text)  #这里就是在hello中匹配he,但是只能是在第一个匹配,如果是ahello就会报错匹配不到
          print(ret.group()) #group可以将其中的值打出来
          ```

          

       2. 如果第一个字母不是`h`，那么就会失败：

          ```python
          text='ahello'
          ret=re.match('he',text)  #这里就是在hello中匹配he,但是只能是在第一个匹配,如果是ahello就会报错匹配不到
          print(ret.group()) #group可以将其中的值打出来
          >> 失败
          ```

          

       3. 如果想要匹配换行的数据，那么久要传入一个`flag=re.DOTALL`，就可以匹配换行符了。示例如下：

          ```python
          text = "abc\nabc"
          ret = re.match('abc.*abc',text,re.DOTALL)
          print(ret.group())
          ```

          

    8. 分组：在正则表达式中，可以对过滤到的字符串进行分组。分组使用圆括号的方式。

       1. `group`：和`group(0)`是等价的，返回的是整个满足条件的字符串。

       2. `groups`：返回的是里面的子组。索引从1开始。

       3. `group(1)`：返回的是第一个子组，可以传入多个。

          ```python
            #分组
          text="apple's price $99,orange's price is $10"
          ret=re.search('.*(\$\d+).*(\$\d+)',text)
          print(ret.group())
          #匹配出整个字符串整个正则就是圆括号一个大的分组ret.group()和ret.group(0)是一样的
          print(ret.group(1))  #匹配出第一个分组 99
          print(ret.group(2))  #匹配出第一个分组 10
          print(ret.groups())  #将所有的子分组输出
          ```

          

    9. findall函数:找出所有满足条件的，返回的是一个列表

       ```python
       #find_all方法
       text = "apple's price $99,orange's price is $10"
       ret = re.findall('\$\d+',text)
       print(ret) #结果：['$99', '$10']
       ```

       

    10. sub函数：

        1. 简单示例：

           ```python
           #sub方法
           text = "apple's price $99,orange's price is $10"
           ret = re.sub('\$\d+','0',text,1) #写了1，所以只替换一个
           print(ret)
           ret = re.sub('\$\d+','0',text) #因为没写1，所有会把所有的都替换掉
           print(ret)
           ```

           

        2. 利用sub函数删除网页文件中的标签，只留下中文信息：

           ```python
           html = """ 网页文件中的所有内容 """
           ret = re.sub(<.+?>,"",html) #为了避免我们需要的中文信息被删除，所有需要加一个`?`，形成非贪婪模式
           print(set)
           ```

           

    11. split函数：使用正则表达式来分割字符串

        ```python
        text = "hello world ni hao"
        ret=re.split(' ',text)
        print(ret)  #['hello','world','ni','hao']
        ```

        

    12. comlie函数：对于一些经常要用到的正则表达式，可以使用`compile`来进行编译，后期再使用的时候可以直接拿过来用，执行效率会更快。而且`compile`还可以指定`flag=re.VERBOSE`，在写正则表达式的时候可以做好注释。示例代码如下：

    ```python
        #compile函数
        text="the number is 20.50"
        r=re.compile('\d+\.?\d*')
        r=re.compile(r"""
        	\d+  #小数点前面的数
        	\.?  #小数点本身
        	\d*  #小数点后面的数字
        """,re.VERBOSE)
        ret=re.search(r,text)   #re.VERBOSE可以写注释
        print(ret.group())
    ```

#### 正则表达式练习:

```python
#正则表达式实例：爬取古诗文网
import re,requests

#爬取页面信息并进行处理
def parse_page(url):
    #注入头部
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    #拉去指定网址并返回一个对象
    response = requests.get(url,headers=headers)
    #将对象中的内容转换为string类型
    text = response.text

    #获取标题
    """
    #从div标签之后开始，之所以采用非贪婪模式，是因为这样才能提取所有的题目，但注意，这里只是从div标签开始之后，其实还没有达到题目的位置
    #作家的名字存储在 <b></b>标签之间，采用非贪婪模式才能把每一个都提取出来
    """
    #获取标题
    # 由于网页当中的是有\n的，所以就是会有.就匹配不到这个\n就是停止就是会返回一个空
    # 后面加上一个re.DOTALL 就可以让这个.去匹配所有的字符包括\n   加上?防止非贪婪模式不加的话只能匹配到一个题目
    titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL) #因为前端文件是会换行的，所以需要使用DOTALL来跳过所有的换行


    #获取朝代
    # 这个findall是将括号当中的数字给括起来的给爬取下来的
    dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL) #因为前端文件是会换行的，所以需要使用DOTALL来跳过所有的换行

    #获取作者
    # 因为这里是第二个a标签所以就是要将其中的第一个先获取到，然后再将其中的第二个标签给整好
    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL) #因为前端文件是会换行的，所以需要使用DOTALL来跳过所有的换行

    #获取古诗内容
    # 使用正则表达式就是将其看出字符串而不是网页，就会有什么子元素父元素
    content_tag = re.findall(r'<div class="contson" .*?>(.*?)</div>',text,re.DOTALL) #因为前端文件是会换行的，所以需要使用DOTALL来跳过所有的换行

    #创建一个列表存储内容
    contents = []
    for content in content_tag:
        #因为拉取到的内容包含了一些如换行和<r></r>之类的标签需要去除，所以使用sub方法
        x = re.sub(r'<.*?>',"",content)
        #去除掉x中的换行符，将剩下的纯文本存入contents列表中
        contents.append(x.strip('\n'))

    #创建古诗列表
    poems = []
    for value in zip(titles,dynasties,authors,contents):
        title,dynasty,author,content = value
        poem = {
            'title':title,
            'dynasty':dynasty,
            'author':author,
            'content':content
        }
        poems.append(poem)

    #输出所有的古诗
    for poem in poems:
        print(poem)
        print('*'*30)

#执行程序
def main():
    #将前十页的故事都爬取下来
    for x in range(1,11):
        url = 'https://www.gushiwen.org/default_%s.aspx' % x
        parse_page(url)

#程序入口
if __name__ == '__main__':
    main()

```

------



## 3.第三章：数据存储 ##

### 1. JSON文件处理

#### JSON支持的数据格式：

1. 对象（字典）：使用花括号
2. 数组（列表）：使用方括号
3. 整数、浮点型、布尔类型还要null类型
4. 字符串类型（字符串必须要用双引号，不能用单引号）

注意：多个数据之间需要使用都好分开，json本质上就是字符串。

