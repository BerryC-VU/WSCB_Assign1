import re
import requests
import threading
import heapq
import base62
from flask import Flask
from flask_restful import Resource, Api, reqparse

lock = threading.Lock()

# https://stackoverflow.com/questions/8498371/curl-get-and-x-get
# input format: curl url -d "url=" -X GET/PUT/POST/DELETE -v
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
# https://stackoverflow.com/questions/72893180/flask-restful-error-request-content-type-was-not-application-json
parser.add_argument('url', type=str, location='form', help='input example: http(s)://www.google.com/')

mappings = {'0': 'http://www.google.com'}

# https://docs.python.org/3/library/heapq.html
counter = 1
id_pool = []
heapq.heapify(id_pool)

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
    global id_pool
    global counter
    if len(id_pool) > 0:
        return heapq.heappop(id_pool)
    else:
        url_id = base62.base62_encoder(counter)
        counter += 1
        return url_id
    


class AccessWithID(Resource):
    def get(self, id):
        # 1. 301, url
        # 2. 404
        if id in mappings:
            return mappings[id], 301
        else:
            return "404 Error: The identifier does not exist", 404

       
    def put(self, id):
        # 1. 200
        # 2. 400, "error" (400 Bad Request)
        # 3. 404
        with lock:
            if id not in mappings:
                return "404 Error: The identifier does not exist", 404
            args = parser.parse_args()
            url = args['url']
            if not is_valid(url):
                return "400 Error: The URL is not valid", 400
            else:
                mappings[id] = url
                return "The URL has been updated", 200
    
    def delete(self, id):
        # 1. 204 (204 No Content)
        # 2. 404
        with lock:
            if id not in mappings:
                return "404 Error: The identifier does not exist", 404
            del mappings[id]
            heapq.heappush(id_pool, id)
            return "The identifier has been deleted", 204


class AccessWithoutID(Resource):
    def get(self):
        # 1. 200, mapping
        return mappings, 200        
    
    def post(self):
        # 1. 201, id (201 Created)
        # 2. 400, "error"
        with lock:
            args = parser.parse_args()
            url = args['url'] 
            if is_valid(url):
                 # check whether url already exists
                values = list(mappings.values())
                if url in values:
                    keys = list(mappings.keys())
                    id = keys[values.index(url)]
                    return ("The url already exists, the shortened identifier is " + id), 400
                else:
                    id = generate_id(url=url)
                    mappings[id] = url
                    return id, 201
            else:
                return "400 Error: The URL is not valid", 400 
    
    def delete(self):
        # 1. 404
        return "404 Error", 404

api.add_resource(AccessWithoutID, '/')
api.add_resource(AccessWithID, '/<string:id>')


if __name__ == '__main__':
    # https://github.com/pallets/flask/blob/main/src/flask/app.py#L873
    app.run(debug=True)