#导包
import json

#将json字符串load成python对象
json_str = '[{"username": "张三", "age": 18, "country": "China"}, {"username": "李四", "age": 18, "country": "China"}]'
persons = json.loads(json_str)
print(type(persons))
for person in persons:
    print(person)

#直接从json文件中load成python对象
with open('person.json','r',encoding='utf-8') as fp: #添加’encoding='utf-8'‘是为了让打印出的数据不出现乱码
    persons = json.load(fp)
    print(type(persons))
    for person in persons:
        print(person)











