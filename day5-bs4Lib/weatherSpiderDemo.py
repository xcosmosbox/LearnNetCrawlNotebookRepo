#爬取所有省份所有城市的最低气温，并进行排名，将排名制作成图表并输出到html中，以供可视化打开。

import requests
from bs4 import BeautifulSoup
import html5lib
from pyecharts.charts import Bar

ALL_Data = []


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 79.0.3945.16Safari / 537.36',
        'Referer': 'http: // www.weather.com.cn / forecast / index.shtml'
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    conMidTab = soup.find('div', class_='contentboxTab1')  # 找到div中第一个class='contentboxTab1'里面的第一个
    # print(conMidTab)
    tables = conMidTab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):  # 这里会返回下标和值
            tds = tr.find_all('td')  # 获取其中的td标签，这个是返回一个列表
            city_td = tds[0]  # 城市就是第一个标签
            if index == 0:
                city_td = tds[1]  # 由于其中的结构问题，要将第一个下标的值变成第一个(哈尔滨 市) 而不是（黑龙江 省）
            city = list(city_td.stripped_strings)[0]  # 由于返回的是生成器所以就是要将其转换成列表的形式，然后就是将其中的第零个元素取出来
            temp_td = tds[-2]  # 最低气温就是td标签的倒数第二个
            min_temp = list(temp_td.stripped_strings)[0]  # 将其中的其中所有的文字都抓取下来
            ALL_Data.append({"city": city, "min_temp": int(min_temp)})
            # print({"city": city, "min_temp": min_temp})


def main():
    urls = ["hb", "db", "hd", "hn", "xb", "xn", "gat"]
    for id in urls:
        url = f'http://www.weather.com.cn/textFC/{id}.shtml#'
        # 港澳台的from，table比较不同,与其他相比不一样，不太规范 table标签不完整源代码没有，只是浏览器自动补充了,所以要用html5lib来进行完善
        parse_page(url)
    # 分析数据
    # 根据最低气温进行排序
    # def sort_key(data):
    #    min_temp = data['min_temp']
    #    return min_temp
    # ALL_Data.sort(key=sort_key)
    # 将其中的key=sort_key，将其返回的值作为key进行排序

    # 下面的数据可视化有点问题啊
    ALL_Data.sort(key=lambda data: data['min_temp'])  # 这个和上面那个函数一样，冒号后面是返回的值
    data = ALL_Data[0:10]
    # for value in data:
    # city=value['city']
    # cities.append(city)
    # 将城市名字提取出来
    cities_ = list(map(lambda x: x['city'], data))
    # 列表data当中的每一项都传给lambda表达式然后将其分解
    temps_ = list(map(lambda x: x['min_temp'], data))
    chart = Bar()  # 标题
    chart.add_yaxis(series_name="thetitle", xaxis_index=cities_, yaxis_data=temps_)
    # chart.add_dataset('', cities_, temps_)  # 数据
    chart.render('temperature.html')  # 渲染


if __name__ == '__main__':
    main()
