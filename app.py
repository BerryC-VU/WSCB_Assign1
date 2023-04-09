from flask import Flask, request
import mangoDB
app = Flask(__name__)

def check_exist(id):
    res = mangoDB.find_all()
    for i in range(len(res)):
        if id in res[i]:
            print('this id already used')
            return res[i]
        else:
            print('this id is available')
            return False

@app.route('/<id>', methods = ['GET', 'PUT','DELETE'])
def route_id(id):
    if request.method == 'GET':
        # return the mapping url with this url
        if check_exist(id)!=True:
            return check_exist(id)
        else:
            return(301, id)
    elif request.method == 'PUT':
        # update the mapping between url and id
        url = "https://translate.google.com" # get a new url
        mangoDB.add_mapping(id,url)
    elif request.method == 'DELETE':
        # delete this mapping
        mangoDB.delete_many(id)
        return 404


def generate_id():
    pass


@app.route('/string:<url>', methods = ['GET', 'POST','DELETE'])
def route(url):
    if request.method == 'GET':
        # return 200, get key
        mappings = mangoDB.find_all()
        return(200, mappings)
    elif request.method == 'POST':
        # create a url-id mapping
        id = generate_id()
        mangoDB.add_mapping(id, url)
    elif request.method == 'DELETE':
        return 404


if __name__ == '__main__':
    app.run(debug=True)