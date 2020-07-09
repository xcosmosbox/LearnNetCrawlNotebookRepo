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
