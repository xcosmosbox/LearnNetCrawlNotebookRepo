#导入python中包含了正则表达式的包
import re

# 1.匹配某个字符串
text='hello'
ret=re.match('he',text)  #这里就是在hello中匹配he,但是只能是在第一个匹配,如果是ahello就会报错匹配不到
print(ret.group()) #group可以将其中的值打出来

# 2.点：匹配任意的字符
text="ab"
ret=re.match('.',text)  #用点的方式只会匹配最前面的那一个字符
print(ret.group())

# 3.\d匹配到任意的数字
text="123"
ret=re.match('\d',text)   #匹配到一个字符
print(ret.group())
ret=re.match('\d\d',text)   #匹配到两个字符
print(ret.group())

# 4.\D匹配任意的非数字
text="+"
ret=re.match('\D',text)   #只能匹配到一个字符
print(ret.group())

# 5.\s 匹配到是空白字符(\n,\t,\r,空格)
text=" "
ret=re.match('\s',text)   #只能匹配到一个字符
print(ret.group())

# 6.\w（小写的）匹配到的是a-z和A-Z以及数字和下划线:
text="_"
ret=re.match('\w',text)   #只能匹配到一个字符
print(ret.group())

# 7.\W匹配的适合\w是相反的:
text="+"
ret=re.match('\W',text)   #只能匹配到一个字符
print(ret.group())

# 8.[] 组合的方式,只要满足中括号里面的字符就可以匹配到:
text="0888-88888"
ret=re.match('[\d\-]+',text)   #匹配到数字和-，加了个+号之后就是会匹配到所有的符合的，直到不满足条件为止
print(ret.group())
'''
    由上可得，我们可以使用中括号代替之前的正则表达式：
    代替：

    \d:[0-9]       [^0-9]^这是非

    \D:0-9

    \w:[0-9a-zA-Z_]     [^0-9a-zA-Z_]

    \W:[0-9a-zA-Z_]
    示例如下：
'''
text="i-z"
ret=re.match('[^0-9]',text)  #在中括号中的‘^’号表达的是“非”（也就是取反），意味着除了数字0-9之外的东西都能取到
print(ret.group())

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

'''### 小案例 ###'''
'''---------------------'''
'''手机号验证规则：
    1.开头必须是1
    2.第二位可能有3、4、5、7、8中的一位
    3.剩下是9位数字
'''
#验证手机号码
text = "13169616005"
ret = re.match('1[34578]\d{9}',text)
print(ret.group())
'''---------------------'''
'''#####################'''
'''---------------------'''
'''邮箱验证规则：
    1.@前面的部分可能存在大小写字母、下划线、数字
    2.必定存在一个@符号
    3.邮箱域名存在数字和字母
    4.最后可能是.com、.cn等等
'''
#验证邮箱
text = "2162381070@qq.com"
ret = re.match('\w+@[a-z0-9]+\.[a-z]+',text)
print(ret.group())
'''---------------------'''
'''#####################'''
'''---------------------'''
'''url验证规则：
    1.最前面必定是http或者https或者是ftp
    2.之后是一个冒号再加上一个斜杠
    3.再后面是任意空白字符
'''
#验证url
text = "https://baike.baidu.com/item/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F/1700215?fr=aladdin"
ret = re.match('(http|https|ftp)://[^\s]+',text)
print(ret.group())
'''---------------------'''
'''#####################'''
'''---------------------'''
'''身份证验证规则：
    1.一共18个数字（前面17个必定是数字，最后一个不确定）
    2.最后一位必定是数字或者大小写形式的x
'''
#验证身份证
text = "12345678911234567X"
ret = re.match('\d{17}[\dxX]',text)
print(ret.group())
'''---------------------'''






