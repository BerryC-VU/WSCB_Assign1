from flask import Flask, request
import base62
import re
import heapq

app = Flask(__name__)

# a dict to store url and token
url_dict = {}

# reference for checking validity: https://www.makeuseof.com/regular-expressions-validate-url/
url_pattern = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"

counter = 0

# store deleted id
id_pool = []

# post url and get shortened_id 
@app.route('/', methods=['POST'])
def post_url():
    global counter
    # get url
    url = request.args['url']
    # check whether url already exists
    values = list(url_dict.values())
    if url in values:
        keys = list(url_dict.keys())
        url_id = keys[values.index(url)]
        return ("The url already exists, the shortened identifier is " + url_id), 400
    else:
        print("TRUE")
        # if the url is valid, then return id and add it to the dict
        if (re.match(url_pattern, url)):
            # if we can get an id in the id_pool
            if len(id_pool) > 0:
                url_id = id_pool[0]
            else:
                # encode to get identifier
                url_id = base62.base62_encoder(counter)
                # update counter
                counter += 1
            # store in the dict
            url_dict[url_id] = url
            return url_id, 201
    # if the url is not valid
        else:
            return "400 Error: The URL is not valid", 400

@app.route('/', methods=['GET'])
def get():
    # get keys from dict
    keys = list(url_dict.keys())
    return keys, 200

# get url based on id
@app.route('/<string:url_id>', methods=['GET'])
def get_url(url_id):
    if url_id in url_dict:
        return url_dict[url_id], 301   
    else:
        return "404 Error: The identifier does not exist", 404

# delete /
@app.route('/', methods=['DELETE'])
def delete():
    return "404 Error"

# delete based on the id
@app.route('/<string:url_id>', methods=["DELETE"])
def delete_url(url_id):
    if url_id in url_dict:
        # delete the entry with id
        del url_dict[url_id]
        # update id pool
        id_pool.append(url_id)
        heapq.heapify(id_pool)
        return "The identifier has been deleted", 204
    else:
        return "404 Error: The identifier does not exist", 404

# put based on id
@app.route('/<string:url_id>', methods=["PUT"])
def put_url(url_id):
    if url_id in url_dict:
        # get new url
        new_url = request.args['url'] 
        # check validity
        if (re.match(url_pattern, new_url)):
            # update url to the given identifier
            url_dict[url_id] = new_url
            return "The URL has been updated", 200
        else:
            return "400 Error: The URL is not valid", 400
    else:
        return "404 Error: The identifier does not exist", 404


if __name__ == '__main__':
    app.run(debug=True)