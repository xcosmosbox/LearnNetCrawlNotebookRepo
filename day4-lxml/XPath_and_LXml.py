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
trs = html.xpath("//tr[2]")  # 这是返回一个元素,迭代器元素
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
all_things = []
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
    title2 = tr.xpath("./td[2]//text()")  # 就可以拿到第二个文本,即"我是第三个文本"
    all_thing = {
        "first": title1,  # 将其变成列表形式
        "second": title2
    }
    all_things.append(all_thing)  # 将其放给列表当中
    print(href)
    break

# lxml结合xpath注意事项:
# 反复练习才有用
