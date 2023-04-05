import re
import requests
import threading
import heapq
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, inputs

lock = threading.Lock()

# https://stackoverflow.com/questions/8498371/curl-get-and-x-get
# input format: curl url -d "url=" -X GET/PUT/POST/DELETE -v
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
# https://stackoverflow.com/questions/72893180/flask-restful-error-request-content-type-was-not-application-json
parser.add_argument('url', type=str, location='form', help='input example: http(s)://www.google.com/')

mappings = {'0': 'http://www.google.com'}

end = 3
id_pool = list(range(1, end))

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
    global end
    if len(id_pool) == 0:
        id_pool = list(range(end, end + 5))
        end = end + 5
    return str(heapq.heappop(id_pool))

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
        with lock:
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
        with lock:
            if id not in mappings:
                return 404
            del mappings[id]
            heapq.heappush(id_pool, int(id))
            return 204


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
                if url in mappings.values():
                    for k, v in mappings.items():
                        if v == url:
                            return k, 201  
                else:
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
    # https://github.com/pallets/flask/blob/main/src/flask/app.py#L873
    app.run(debug=True)