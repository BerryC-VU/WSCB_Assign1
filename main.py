import re
import requests
import threading
import heapq
import base62
from flask import Flask
from flask_restful import Resource, Api, reqparse

lock = threading.Lock() # mutex

# https://stackoverflow.com/questions/8498371/curl-get-and-x-get
# input format: curl url -d "url=" -X GET/PUT/POST/DELETE -v
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
# https://stackoverflow.com/questions/72893180/flask-restful-error-request-content-type-was-not-application-json
parser.add_argument('url', type=str, location='form', help='input example: http(s)://www.google.com/')

mappings = {'0': 'http://www.google.com'} # store key-value pairs (identifier: URL)

# https://docs.python.org/3/library/heapq.html
counter = 1 # store the next available id
id_pool = [] # maintain the ID POOL that store the freed ids. It is implemented by the min heap.
heapq.heapify(id_pool)


def is_valid(url):
    """check if url is well formatted and accessible

    Args:
        url (str): input URL
    """
    def check_format(url):
        """
        references:
        1. https://www.makeuseof.com/regular-expressions-validate-url/
        2. https://docs.python.org/3/library/re.html
        """
        regex = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
        r = re.compile(regex)
        if (re.match(regex, url)): # alternative: fullmatch()
            return True
        else:
            return False
        
    def check_exist(url):
        # https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

        
    return check_format(url) and check_exist(url)


def generate_id(url):
    """Generate Identifier for the input URL.
    IF ID POOL is not empty, pick the root value as the returned ID
    ELSE use counter to generate a new ID.
    
    Args:
        url (str): input URL
    Returns:
        str: generated ID
    """
    try: 
        global id_pool
        global counter
        if len(id_pool) > 0:
            return heapq.heappop(id_pool)
        else:
            # transform the base10 number to base62 number to make it shorter
            url_id = base62.base62_encoder(counter) 
            counter += 1
            return url_id
    except:
        print("Generate ID fails.")
    


class AccessWithID(Resource):
    def get(self, id):
        """Handle HTTP GET Request with ID
        Args:
            id (str): input ID
        Returns:
            if ID exists, return corresponding URL and status code 301
            else, return error info and status code 404
        """
        try:
            if id in mappings:
                return mappings[id], 301
            else:
                return "404 Error: The identifier does not exist", 404
        except:
            print("Handle Get with ID fails.")

       
    def put(self, id):
        """Handle HTTP PUT Request with ID
        Args:
            id (str): input ID
        Returns:
            if ID does not exist, return 404 error info and status code 404
            else if ID exist, but it not valid, return 400 error info and status code 400
            else if ID exist and is valid, update the URL, return the old URL, updated URL and status code 200
        """
        try:
            with lock:
                if id not in mappings:
                    return "404 Error: The identifier does not exist", 404
                args = parser.parse_args()
                url = args['url']
                if not is_valid(url):
                    return "400 Error: The URL is not valid", 400
                # else:
                else:
                    old_url = mappings[id]
                    mappings[id] = url
                    return "The URL has been updated. old_url is: " + old_url + " and the updated url is: " + url, 200
        except:
            print("Handle PUT request with ID fails.")

    
    def delete(self, id):
        """Handle HTTP DELETE Request with ID
        Args:
            id (str): input ID
        Returns:
            if ID does not exist, return 404 error info and status code 404
            else, delete the ID and related URL from mappings and add it to ID POOL, return status code 204
        """
        try:
            with lock:
                if id not in mappings:
                    return "404 Error: The identifier does not exist", 404
                del mappings[id]
                heapq.heappush(id_pool, id)
                return "The identifier has been deleted", 204
        except:
            print("Handle DELETE request with ID fails.")


class AccessWithoutID(Resource):
    def get(self):
        """Handle HTTP GET Request without ID

        Returns:
            return all id-URL pairs and status code 200
        """
        try: 
            return mappings,  200   
        except:
            print("Handle GET request without ID fails.")     
    
    def post(self):
        """Handle HTTP POST Request without ID

        Returns:
            IF input URL is not valid, return 400 error info and status code 400
            ELSE IF input URL is valid: 
                IF URL already exists, return ID and status code 400
                ELSE IF URL does not exist, generate new ID, return it and status code 201 (Created)
        """
        
        try:
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
        except:           
            print("Handle POST request with ID fails.")
            
    def delete(self):
        """Handle HTTP DELETE Request without ID

        Returns:
            Not allowed to delete data without specifying ID.
            Return 404 error info and status code 404
        """
        try:
            return "404 Error", 404
        except:
            print("Handle DELETE request with ID fails.")

api.add_resource(AccessWithoutID, '/')
api.add_resource(AccessWithID, '/<string:id>')


if __name__ == '__main__':
    # https://github.com/pallets/flask/blob/main/src/flask/app.py#L873
    app.run(debug=True)