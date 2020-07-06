#导包
import json

#将python对象转换为json字符串

persons = [
    {
        'username':'张三',
        'age':18,
        'country':'China'
    },
    {
        'username':'李四',
        'age':18,
        'country':'China'
    }
]

#利用dumps函数将python列表中的内容转换成json字符串
json_str = json.dumps(persons)
print(type(json_str)) #<class 'str'>
print(json_str)

'''将转换成功的json字符串保存为json文件:
#方法一：
with open('person.json','w') as fp:
    fp.write(json_str)
'''

'''方法二：利用python的json库中自带的dump方法将对象转换为字符串的同时一并输出到json文件中'''
with open('person.json','w',encoding='utf-8') as fp: #之所以要加’encoding='utf-8'‘是为了配合下面Unicode码关闭后，如果不指定解码形式，中文会出现乱码
    json.dump(persons,fp,ensure_ascii=False) #之所以要加’ensure_ascii=False‘，是为了在输出的json文件能正常输出正文，如果不加，中文会以Unicode码的形式输出。




