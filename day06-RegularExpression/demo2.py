#导入python中包含了正则表达式的包
import re


'''### 匹配多个字符 ###'''
# 9.1.`*`可以匹配0或是任意多个字符，没有不会报错：
text="0888-88888"
ret=re.match('\d*',text)
print(ret.group())
#9.2.`+`可以匹配1或是任意多个字符，至少要一个，不然报错:
text="abcd"   #text="+abcd"
ret=re.match('\w+',text)
print(ret.group())
#9.3.`？`匹配一个或0个（要么没有，要么只有一个）:
text="abc"  #text="+abcd"
ret=re.match('\w?',text)
print(ret.group())
#9.4.`{m}`匹配到m个:
text="a2bcd"  #text="+abcd"
ret=re.match('\w{2}',text) #此处代表匹配两个
print(ret.group())
#9.5.`{m,n}`匹配m-n个:
text="abc"  #text="+abcd"
ret=re.match('\w{1,5}',text)  #因为我们想要匹配的字符数量超过了总的字符长度，所以我们会将整个字符都匹配出来，而不是报错
print(ret.group())