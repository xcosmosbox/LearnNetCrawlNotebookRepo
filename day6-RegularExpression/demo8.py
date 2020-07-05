#导入python中包含了正则表达式的包
import re

text = "abc\nabc"
ret = re.match('abc.*abc',text,re.DOTALL)
print(ret.group())


#分组
text="apple's price $99,orange's price is $10"
ret=re.search('.*(\$\d+).*(\$\d+)',text)
print(ret.group())
#匹配出整个字符串整个正则就是圆括号一个大的分组ret.group()和ret.group(0)是一样的
print(ret.group(1))  #匹配出第一个分组 99
print(ret.group(2))  #匹配出第一个分组 10
print(ret.groups())  #将所有的子分组输出


#find_all方法
text = "apple's price $99,orange's price is $10"
ret = re.findall('\$\d+',text)
print(ret) #结果：['$99', '$10']

#sub方法
text = "apple's price $99,orange's price is $10"
ret = re.sub('\$\d+','0',text,1) #写了1，所以只替换一个
print(ret)
ret = re.sub('\$\d+','0',text) #因为没写1，所有会把所有的都替换掉
print(ret)


#split函数
text = "hello world ni hao"
ret=re.split(' ',text)
print(ret)  #['hello','world','ni','hao']


#compile函数
text="the number is 20.50"
r=re.compile('\d+\.?\d*')
r=re.compile(r"""
	\d+  #小数点前面的数
	\.?  #小数点本身
	\d*  #小数点后面的数字
""",re.VERBOSE)
ret=re.search(r,text)   #re.VERBOSE可以写注释
print(ret.group())


