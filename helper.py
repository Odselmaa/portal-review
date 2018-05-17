from flask import jsonify
import requests

def send_request(URL, method, json):
    result = {}
    if method == 'GET':
        result = requests.get(URL, json=json)
    elif method == 'POST':
        result = requests.post(URL, json=json)
    elif method == 'PUT':
        result = requests.put(URL, json=json)
    elif method == 'DELETE':
        result = requests.delete(URL, json=json)
    return jsonify(result.json()), result.status_code