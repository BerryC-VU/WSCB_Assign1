import re
import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs

# https://stackoverflow.com/questions/8498371/curl-get-and-x-get
# input format: curl url -d "url=" -X GET/PUT/POST/DELETE -v
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
# https://stackoverflow.com/questions/72893180/flask-restful-error-request-content-type-was-not-application-json
parser.add_argument('url', type=str, location='form', help='input example: http(s)://www.google.com/')

mappings = {'2': 'http://www.google.com'}

def is_valid(url):
    def check_format(url):
        """
        references:
        1. https://www.makeuseof.com/regular-expressions-validate-url/
        2. https://docs.python.org/3/library/re.html
        """
        regex = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
        r = re.compile(regex)
        if (re.fullmatch(r, url)):
            return True
        else:
            return False
        
    def check_exist(url):
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
        
    return check_format(url) and check_exist(url)


def generate_id(url):
    return 1


class AccessWithID(Resource):
    def get(self, id):
        # 1. 301, url
        # 2. 404
        if id in mappings:
            return mappings[id], 301
        else:
            return 404

       
    def put(self, id):
        # 1. 200
        # 2. 400, "error" (400 Bad Request)
        # 3. 404
        if id not in mappings:
            return 404
        args = parser.parse_args()
        url = args['url']
        if not is_valid(url):
            return 400
        else:
            mappings[id] = url
            return url, 200
    
    def delete(self, id):
        # 1. 204 (204 No Content)
        # 2. 404
        if id not in mappings:
            return 404
        del mappings[id]
        return 204


class AccessWithoutID(Resource):
    def get(self):
        # 1. 200, mapping
        return mappings, 200        
    
    def post(self):
        # 1. 201, id (201 Created)
        # 2. 400, "error"
        args = parser.parse_args()
        url = args['url'] 
        if is_valid(url):
            id = generate_id(url=url)
            mappings[id] = url
            return id, 201
        else:
            return "error", 400
    
    def delete(self):
        # 1. 404
        return 404

api.add_resource(AccessWithoutID, '/')
api.add_resource(AccessWithID, '/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)