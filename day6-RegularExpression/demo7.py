#导入python中包含了正则表达式的包
import re

#转义字符和原生字符串

text = 'apple price is $299'
ret = re.search('\$\d+',text)
print(ret.group())

text = '\\n'
rett = re.match('\\\\n',text) #利用多次转义消除最开始的转义符号的影响，最终输出字符串’\n‘
print(rett.group())
rett = re.match(r'\\n',text) #或者是使用python的原生字符串，直接将转义一次后的结果进行查询
print(rett.group())