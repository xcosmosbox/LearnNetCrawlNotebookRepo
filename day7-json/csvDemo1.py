#导包
import csv

def read_csv_demo1():
    with open('vgsales.csv','r',encoding='utf-8') as fp:
        # reader是一个迭代器
        readers = csv.reader(fp)
        next(readers) #使用这个语句就能跳过第0行，因为第0行只是列出了分别由那些类型的数据，而不是数据本身
        for x in readers:
            name = x[1] #获得姓名
            grade = x[-2] #获得这个人的其它成绩
            print({'name':name,'grade':grade})


'''如果想要在获取数据的时候同标题来获取，那么可以使用`DicReader`。示例代码如下：'''
def read_csv_demo2():
    with open('vgsales.csv', 'r',encoding='utf-8') as fp:
        #用DictReader创建的reader对象，不会包含标题那行的数据
        #reader是一个迭代器，遍历这个迭代器，返回的是一个字典。
        #以下这种方法更安全，因为是跟着标签走，不管那一列的数据如何移动，都不会影响我们读取数据。
        reader = csv.DictReader(fp)
        for x in reader:
            value = {'Name':x['Name'],'Year':x['Year']}
            print(value)


if __name__ == '__main__':
    read_csv_demo2()





