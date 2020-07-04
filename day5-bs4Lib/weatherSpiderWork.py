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


