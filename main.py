from flask import Flask, request
import base62

app = Flask(__name__)

# a dict to store url and token
url_dict = {}

# post url 
@app.route('/', methods=['POST'])
def post_url():
    url = request.args
    if url in url_dict.values():
        return "The url exists", 400
    url_id = base62.base62_encode(len(url_dict))
    # store in the dict
    url_dict[url_id] = url
    shorten_url = url_id
    return shorten_url, 201

@app.route('/<string:url_id>', methods=['GET'])
def get_url(url_id):
    if url_id in url_dict:
        return url_dict[url_id], 301   
    else:
        return "404 Error: The identifier does not exist", 404

@app.route('/', methods=['DELETE'])
def delete():
    return "404 Error"

@app.route('/<string:url_id>', methods=["DELETE"])
def delete_url(url_id):
    if url_id in url_dict:
        del url_dict[url_id]
        return "The identifier has been deleted", 204
    else:
        return "404 Error: The identifier does not exist"

if __name__ == '__main__':
    app.run(debug=True)