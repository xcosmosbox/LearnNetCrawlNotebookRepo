#导包
from bs4 import BeautifulSoup

html = """
<ul>
			                                			        				            <li><a href="//live.media.weibo.com/p/admin" target="_blank" title="直播" suda-uatrack="key=tblog_home_edit&amp;value=live_button"><em class="W_ficon ficon_live_v2"></em>直播</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="review" action-data="type=512&amp;action=1&amp;log=dianping&amp;cate=1" title="点评" suda-uatrack="key=mainpub_dianping&amp;value=main_dianping_button"><em class="W_ficon ficon_remark">ï</em>点评</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="settime" action-data="type=511&amp;action=1&amp;log=&amp;cate=1" title="定时发" suda-uatrack="key=tblog_home_edit&amp;value=chick_autopub"><em class="W_ficon ficon_timesend">t</em>定时发</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="plugin" action-data="interactivetype=2&amp;type=503&amp;action=1&amp;log=music&amp;cate=1" title="音乐" suda-uatrack="key=tblog_home_edit&amp;value=music_button"><em class="W_ficon ficon_music">u</em>音乐</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="plugin" action-data="type=14&amp;action=1&amp;log=weigongyi&amp;cate=1" title="微公益" suda-uatrack="key=tblog_home_edit&amp;value=gongyi_button"><em class="W_ficon ficon_public">w</em>微公益</a></li>
			                                			        				            <li><a href="//mp.weibo.com/xian/" target="_blank" title="新鲜事" suda-uatrack="key=tblog_home_edit&amp;value=fresh_button"><em class="W_ficon ficon_freshnews"></em>新鲜事</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="position" action-data="type=535&amp;action=1&amp;log=&amp;cate=1" title="地点" suda-uatrack="key=tblog_home_edit&amp;value=location_button"><em class="W_ficon ficon_cd_place">2</em>地点</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="superTopic" action-data="type=532&amp;action=1&amp;log=&amp;cate=1" title="超话" suda-uatrack="key=tblog_home_edit&amp;value=sg_button"><em class="W_ficon ficon_supertopic"></em>超话</a></li>
			                                			        				            <li><a href="https://weibo.com/ttwenda/p/publisher3in1" target="_blank" title="提问"><em class="W_ficon ficon_ttwenda"></em>提问</a></li>
			        			        </ul><ul>
			                                			        				            <li><a href="//live.media.weibo.com/p/admin" target="_blank" title="直播" suda-uatrack="key=tblog_home_edit&amp;value=live_button"><em class="W_ficon ficon_live_v2"></em>直播</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="review" action-data="type=512&amp;action=1&amp;log=dianping&amp;cate=1" title="点评" suda-uatrack="key=mainpub_dianping&amp;value=main_dianping_button"><em class="W_ficon ficon_remark">ï</em>点评</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="settime" action-data="type=511&amp;action=1&amp;log=&amp;cate=1" title="定时发" suda-uatrack="key=tblog_home_edit&amp;value=chick_autopub"><em class="W_ficon ficon_timesend">t</em>定时发</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="plugin" action-data="interactivetype=2&amp;type=503&amp;action=1&amp;log=music&amp;cate=1" title="音乐" suda-uatrack="key=tblog_home_edit&amp;value=music_button"><em class="W_ficon ficon_music">u</em>音乐</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="plugin" action-data="type=14&amp;action=1&amp;log=weigongyi&amp;cate=1" title="微公益" suda-uatrack="key=tblog_home_edit&amp;value=gongyi_button"><em class="W_ficon ficon_public">w</em>微公益</a></li>
			                                			        				            <li><a href="//mp.weibo.com/xian/" target="_blank" title="新鲜事" suda-uatrack="key=tblog_home_edit&amp;value=fresh_button"><em class="W_ficon ficon_freshnews"></em>新鲜事</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="position" action-data="type=535&amp;action=1&amp;log=&amp;cate=1" title="地点" suda-uatrack="key=tblog_home_edit&amp;value=location_button"><em class="W_ficon ficon_cd_place">2</em>地点</a></li>
			                                			        				            <li><a href="javascript:void(0);" action-type="superTopic" action-data="type=532&amp;action=1&amp;log=&amp;cate=1" title="超话" suda-uatrack="key=tblog_home_edit&amp;value=sg_button"><em class="W_ficon ficon_supertopic"></em>超话</a></li>
			                                			        				            <li><a href="https://weibo.com/ttwenda/p/publisher3in1" target="_blank" title="提问"><em class="W_ficon ficon_ttwenda"></em>提问</a></li>
			        			        </ul>
"""

soup = BeautifulSoup(html,'lxml')

#1.获取所有li标签
trs = soup.find_all('li')
for li in trs:
    #注意，此时被打印的li其实不是字符串类型，而是tag类型
    print(type(li))
    print(li)
    print('='*30)


#获取第2个tr标签
li = soup.find_all('li',limit=2)[1]
print(li)
print('-'*30)

#3.获取所有class等于even的a标签
aTags = soup.find_all('a',class_='even')
#另一种写法:aTags = soup.find_all('a',attrs={'class':"even"})
for aTag in aTags:
    print(aTag)

#4.将所有id等于test。class也等于test的li标签提取出来
aList = soup.find_all('li',id_='test',class_='test')
for a in aList:
    print(a)
    print('*'*30)


#5.获取所有a标签的href属性
aLists = soup.find_all('a')
for a in aLists:
    #1.通过下标操作的方式
    href = a['href']
    print(href)
    #2.通过attrs属性的方法
    href = a.attrs['href']
    print(href)
    print('!'*30)

#6.获取所有的职位信息(纯文本)
trss = soup.find_all('li')[1:]
movies = []
for t in trss:
    tds = t.find_all('li')
    title = tds[0].string
    category = tds[1].string
    names = tds[2].string
    city = tds[3].string

    #简便方法:
    infos = t.strings
    for info in infos:
        print(info)
        print('+'*30)







