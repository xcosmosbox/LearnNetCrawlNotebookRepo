#导入python中包含了正则表达式的包
import re

'''注意，下面我们使用的是re的search方法，不是demo1中的match方法'''
# 1.^(脱字符):表示 以……开始：
text='hello'
ret=re.search('^h',text) #以h开始
print(ret.group())

# 2.$：表示 以……结束
text='xxx@qq.com'
ret=re.search('\w+@qq\.com$',text) #以com结束
print(ret.group())

# 3.|：匹配多个表达式或者字符串
text="https"
ret=re.match('(http|https|ftp)',text)   # 如果组合要用()括起来
print(ret.group())











