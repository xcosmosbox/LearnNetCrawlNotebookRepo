# Introduction to WebSpider #

## 		1.爬虫第一步: 网络请求 ##

### *urllib库* ###

  #### 1.urlopen ####

  ​	返回一个类文件句柄对象，解析网页

  ```java
  resp=request.urlopen('http://www.baidu.com')  
  print(resp.read())
  ```

  

  #### 2.urlretrieve ####

  ​	将页面保存到本地中，取名‘baidu.com'

```java
request.urlretrieve('http://www.baidu,com','baidu.html')
```



  #### 3.urlencode ####

  ​	将字典数据转换为URL编码数据。若网址是中文，浏览器是会将中文编码成‘%+十六进制数’的形式。这是因为服务器是无法识别中文的。

```java
data={'name':'爬虫','great':'hello world','age':100}
qs=parse.urlencode(data)
print(qs)
```



  #### 4.parse_qs ####

  ​	可以将经过编码后的url参数进行解码

```java
qs='xxxxx'
print(parse.parse_qs(qs))
```



  #### 5.urlparse & urlsplit ####

  ​	urlparse & urlsplit 对url进行分割，分成若干部分，返回这些部分urlparse会多返回一个参数params，其它的部分和urlsplit一样。

  #### 6.request.Request类

  ​	用于进行添加请求头的时候，增加一些数据（为了防止反爬虫，比如增加User-Agent）

```java
headers={
        'User-Agent':'xxx'                                  #这是让服务器知道这个浏览器而不是一个爬虫.
        }
req=request.Request('http://www.baidu.com',headers=headers) #加上请求头所余姚的信息发送请求.
```



  #### 7.ProxyHandler处理器(代理设置) ####

  ​	代理的原理：在请求目的服务器之前，先请求代理服务器，然后让代理服务器去请求目的服务器网站,代理服务器拿到目的网站的数据后，在转发给我们的代码

```java
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

```java
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

```java
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



### *request库* ###

