import pymongo

client = pymongo.MongoClient(host='127.0.0.1')
db = client.test

db_list = client.list_database_names()
print(db_list)

collections = db.urlMap

# 增加
def add_mapping(id = 1,url = 'https://www.baidu.com'):
    mapping = {
        'url': url,
        'id': id
    }
    result = collections.insert_one(mapping)  # 文档插入集合
    print(result)  # 打印结果
    print(result.inserted_id)  # 打印插入数据的返回 id 标识

# 查询功能
def find_all():
    result = collections.find()
    for a in result:
        print(a)
def search_by_id(id=1):
    result = collections.find({}, {'_id': 0, 'id': id})
    for a in result:
        print(a)

# 删除
def delete_one(id=1):
    query_name = {"id": id}
    collections.delete_one(query_name)
def delete_many(id):
    query_name = {"id": id}
    collections.delete_many(query_name)
def delete_all():
    collections.delete_many({})

add_mapping(1,'https://www.baidu.com')
add_mapping(2,'https://www.baidu.com')
add_mapping(3,'https://www.baidu.com')
# find_all()
# delete_many(1)
# delete_all()
find_all()
