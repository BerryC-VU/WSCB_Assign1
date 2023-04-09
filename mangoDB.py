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
    res = []
    for a in result:
        res.append([a['id'],a['url']])
        # print(a['id'], a['url'])
    return res
def search_id(id):
    result = collections.find({}, {'_id': 0, 'id': id})
    res = []
    for a in result:
        res.append(a['id'])
        # print(a)
    return res
def search_url(url = 'https://www.baidu.com'):
    result = collections.find({}, {'_id': 0, 'url': url})
    res = []
    for a in result:
        res.append(a['url'])
        # print(a)
    return res

def search_mapping(id =1, url = 'https://www.baidu.com'):
    result = collections.find({}, {'_id': 0, 'id': id ,'url': url})
    res = []
    for a in result:
        res.append([a['id'],a['url']])
        # print(a)
    return res
# 删除
def delete_one(id=1):
    query_name = {"id": id}
    collections.delete_one(query_name)

def delete_many(id):
    query_name = {"id": id}
    collections.delete_many(query_name)
def delete_all():
    collections.delete_many({})

# add_mapping(1,'https://www.baidu.com')
# add_mapping(2,'https://www.baidu.com')
# add_mapping(3,'https://www.baidu.com')

# print(res,type(res),res[0],type(res[0]))
# print(find_all())




