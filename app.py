from flask import Flask, request

app = Flask(__name__)


# this is root url
@app.route('/')
def hello_world():  # put application's code here
    return 'hello 000 world!'


# 1. debug mode
#  no need to rerun

# 2. change host
# let other people connect to my flask project

# 3. change port
# edit configuration- port


# GET is path, no parameters
@app.route('/GET')
def get():
    return "200"

# url with parameter
@app.route('/GET/int:<id>')
def get_id(id):
    return "301, The id is: %s" %id

# /GET/id: return some id
# /GET/id?id=2: return id 2
@app.route('/GET/id')
def get_id2():
    id = request.args.get("id", default=1, type=int)
    return f"301, your id is {id}"

# is what the "error" means?
@app.route('/PUT/<id>')
def put_id(id):
    return "400"

@app.route('/PUT')
def put():
    return "400"


@app.route('/POST')
def post():
    return "201"

@app.route('/DELETE/<id>')
def delete_id(id):
    return "404"

@app.route('/DELETE')
def delete():
    return "404"

if __name__ == '__main__':
    app.run()
