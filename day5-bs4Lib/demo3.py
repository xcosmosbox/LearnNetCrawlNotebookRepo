#select和css选择器提取元素
"""
    目标：
        1. 获取所有的p标签
        2. 获取2个p标签
        3. 获取所有class等于even的p标签
        4. 将所有id等于test。class也等于test的a标签提取出来#此功能在css选择器中无法实现#
        5. 获取所有div标签的text属性
        6. 获取所有的职位信息(纯文本)
"""

#导包
from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!--第一种情况-->
    <style type="text/css">
        #line3{
            background-color : pink;
        }
    </style>

    <!--第2种情况-->
    <style type="text/css">
        .box{
            background-color : pink;
        }
    </style>

     <!--第3种情况-->
    <style type="text/css">
        p{
            background-color : pink;
        }
    </style>

         <!--第4种情况-->
    <style type="text/css">
        .line1{
            background-color : pink;
        }
    </style>

        <!--第5种情况-->
    <style type="text/css">
        .box p{
            background-color : pink;
        }
    </style>

            <!--第6种情况-->
    <style type="text/css">
        .box > p{
            background-color : pink;
        }
    </style>
</head>
<body>
    <div class="box">
        <div>
            <p>第零行数据</p>
        </div>
        <p class="line1">第一行数据</p>
        <p class="line1">第二行数据</p>
        <p id="line3">第三行数据</p>
    </div>
    <p>第四行数据</p>
    <form >
        <input type="text" name="username">
        <input type="text" name="password">
    </form>
</body>
</html>
"""

soup = BeautifulSoup(html,'lxml')

#1. 获取所有的tr标签
ps = soup.select('p')
for p in ps:
    print(p)
    print("="*30)

#2. 获取2个p标签
p = soup.select('p')[1]
print(p)
print("*"*30)

#3. 获取所有class等于
# 第一种写法：ps = soup.select("p.line1")
#第二种写法:
ps = soup.select("p[class='line1']")
for p in ps:
    print(p)
    print("!"*30)

#4. 将所有id等于test。
#此功能在css选择器中无法实现!!!!

#5. 获取所有div标签的text属性
divList = soup.select("text")
for div in divList:
    text = div['text']
    print(text)

#6. 获取所有的职位信息(纯文本)
ps = soup.select('p')
for p in ps:
    infos = list(p.stripped_strings)
    print(infos)







