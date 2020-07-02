# Introduction to WebSpider #

## 		1.第一章: 网络请求 ##

### *urllib库* ###

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

