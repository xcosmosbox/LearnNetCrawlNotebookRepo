#导入python中包含了正则表达式的包
import re

#贪婪模式和非贪婪模式
text='0123456'
ret=re.match('\d+',text) #此时就是贪婪模式，因为这句的意思是至少匹配出一个，但可以匹配处任意多个字符，甚至一直将全部都匹配出来
print(ret.group())

ret=re.match('\d+?',text) #此时就是非贪婪模式。只要匹配出一个后，就结束了。
print(ret.group())

#贪婪模式举例2：
text='<h1>标题</h1>'
ret=re.match('.+',text)
print(ret.group())