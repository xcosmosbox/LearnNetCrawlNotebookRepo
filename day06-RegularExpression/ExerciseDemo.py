#正则实例爬取古诗文网
import re,requests

def parse_page(url):
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.16 Safari/537.36'
    }
    response=requests.get(url,headers=headers)
    text=response.text
    titles=re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>',text,re.DOTALL)  #由于网页当中的是有\n的，所以就是会有.就匹配不到这个\n就是停止就是会返回一个空
    # 后面加上一个re.DOTALL 就可以让这个.去匹配所有的字符包括\n   加上?防止非贪婪模式不加的话只能匹配到一个题目
    dynasties=re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>',text,re.DOTALL)  #这个findall是将括号当中的数字给括起来的给爬取下来的
    authors=re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>',text,re.DOTALL)  #因为这里是第二个a标签所以就是要将其中的第一个先获取到，然后再将其中的第二个标签给整好
    content_tag=re.findall(r'<div class="contson" .*?>(.*?)</div>',text,re.DOTALL)     #使用正则表达式就是将其看出字符串而不是网页，就会有什么子元素父元素
    contents=[]
    for content in content_tag:
        #print(content)
        x=re.sub(r'<.*?>',"",content)  # 将其中的标签替换掉
        contents.append(x.strip())
        print(contents)
    poems=[]
    for value in zip(titles,dynasties,authors,contents):
        title, dynasty, author, content=value
        more_peoms={
            'title':title,
            'daynastie':dynasty,
            'authors':author,
            'content':content
        }
        poems.append(more_peoms)
    # for poem in poems:
    #     print(poem)


def main():
    for page in range(10):
        url=f"https://www.gushiwen.org/default_{page}.aspx"
        parse_page(url)

if __name__ == '__main__':
    main()
