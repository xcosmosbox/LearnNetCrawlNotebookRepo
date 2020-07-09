#导包
import csv

'''这个方法使用列表，以及writerow方法和writerows方法分别写入表头和数据'''
def write_csv_demo1():
    #表头
    headers = ['username','age','height']
    #表头标签对应的数据
    values = [
        ('张三',18,180),
        ('李四',19,170),
        ('王五',20,190)
    ]

    #需要使用encoding进行编码，不然会乱码
    #newline的作用是去除空行，因为writer方法是默认写一行然后跳一行再继续写下一行
    #我们将newline=的值设为空，就不会跳行了
    with open('writedFile.csv','w',encoding='utf-8',newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        writer.writerows(values)

'''方法二是使用字典的方式写入'''
def write_csv_demo2():
    # 表头
    headers = ['username', 'age', 'height']
    # 用字典的方式写入数据
    values = [
        {'username':'张三', 'age':18, 'height':180},
        {'username': '李四', 'age': 19, 'height': 170},
        {'username': '王五', 'age': 20, 'height': 190}
    ]
    # 需要使用encoding进行编码，不然会乱码
    # newline的作用是去除空行，因为writer方法是默认写一行然后跳一行再继续写下一行
    # 我们将newline=的值设为空，就不会跳行了
    with open('writedFile.csv', 'w', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp,headers)
        #使用方法二时，需要用writeheader写入表头
        writer.writeheader()
        writer.writerows(values)

if __name__ == '__main__':
    write_csv_demo2()











