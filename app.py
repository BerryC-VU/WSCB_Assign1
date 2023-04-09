from flask import Flask, request
app = Flask(__name__)

@app.route('/<id>', methods = ['GET', 'PUT','DELETE'])
def route_id(id):
    if request.method == 'GET':
        # return the mapping url with this url
        pass
    elif request.method == 'PUT':
        # update the mapping between url and id
        pass
    elif request.method == 'DELETE':
        # delete this mapping
        pass

@app.route('/', methods = ['GET', 'POST','DELETE'])
def route():
    if request.method == 'GET':
        # return 200, get key
        pass
    elif request.method == 'POST':
        # shorten this url?
        pass
    elif request.method == 'DELETE':
        pass






if __name__ == '__main__':
    app.run(debug=True)
