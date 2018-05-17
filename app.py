import json
from functools import wraps

import bson
import datetime

import mongoengine
from bson import ObjectId
from flask import Flask
from flask_mongoengine import MongoEngine
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from flask import jsonify, request
from contoller import *
from helper import send_request

app = Flask(__name__)
app.config['MONGODB_DB'] = 'Portal'
app.config[
    'MONGODB_HOST'] = 'mongodb://admin_remine:WinniePooh8@remineme-shard-00-00-h4vdb.mongodb.net:27017,remineme-shard-00-01-h4vdb.mongodb.net:27017,remineme-shard-00-02-h4vdb.mongodb.net:27017/Portal?ssl=true&replicaSet=RemineMe-shard-0&authSource=admin'
app.config['MONGODB_USERNAME'] = 'admin_remine'
app.config['MONGODB_PASSWORD'] = 'WinniePooh8'
db = MongoEngine()
db.init_app(app)


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         auth_header = (request.headers.get('Authorization'))
#         if auth_header is None:
#            raise BadRequest
#         bearer, access_token = auth_header.split()
# 
#         if bearer != 'Bearer':
#             raise BadRequest
#         #sending request to UserService to check access tokens
#         response, code = send_request('http://localhost:5001/api/check_authorization/' + access_token, method='GET', json={})
# 
#         if code == 200:
#             return f(*args, **kwargs)
#         else:
#             return response, code
#     return decorated_function
@app.route('/api/review/department/report')
def dep_review_report():
    reports = get_dep_review_report()
    print(reports)
    return jsonify({'response': reports, 'statusCode': 200}), 200


@app.route('/api/review/department', methods=["GET", "POST"])
def dep_reviews():
    if request.method == 'POST':
        payload = request.json.get('payload', None)
        print(payload)
        if payload:
            response = add_review(payload)

            return jsonify({'response': response, 'statusCode': 201}), 201
        else:
            raise BadRequest
    elif request.method == 'GET':
        l = request.args.get('limit', 10)
        s = request.args.get('skip', 0)
        lang = request.args.get('lang', 'en')
        reviews = get_all_review(l, s).to_json()
        return jsonify({'response':  {'reviews': json.loads(reviews)}, 'statusCode': 200}), 200


@app.route('/api/review/chair', methods=["GET", "POST"])
def chair_reviews():
    if request.method == 'POST':
        payload = request.json.get('payload', None)
        if payload:
            response = add_chair_review(payload)

            return jsonify({'response': response, 'statusCode': 201}), 201
        else:
            raise BadRequest


@app.route('/api/review/department/<int:_id>', methods=["GET"])
def department_review(_id):
    if request.method == 'GET':
        l = int(request.args.get('limit', 10))
        s = int(request.args.get('skip', 0))
        reviews = get_review_department(_id, l, s).to_json()
        avg = get_avg_department(_id)
        return jsonify({'response':  {'reviews': json.loads(reviews), 'average': avg}, 'statusCode': 200}), 200


@app.route('/api/review/chair/<int:_id>', methods=["GET"])
def chair_review(_id):
    if request.method == 'GET':
        l = int(request.args.get('limit', 10))
        s = int(request.args.get('skip', 0))
        reviews = get_review_chair(_id, l, s).to_json()
        avg = get_avg_chair(_id)

        return jsonify({'response':  {'reviews': json.loads(reviews), 'average': avg}, 'statusCode': 200}), 200


@app.route('/api/review/<string:_id>', methods=["GET", "PUT", "DELETE"])
def spec_review(_id):
    if request.method == 'GET':
        review = get_review(_id)
        if review is None:
            raise NotFound
        else:
            review = json.loads(review.to_json())
        return jsonify({'response': review, 'statusCode': 200})
    elif request.method == 'PUT':
        review_json = request.json['payload']
        affected_row = update_review(_id, review_json)
        if affected_row > 0:
            return jsonify({'response': 'OK', 'statusCode': 200}), 200
        else:
            return jsonify({'response': 'NOT OK', 'statusCode': 404}), 404

    elif request.method == 'DELETE':
        delete_review(_id)
        return jsonify({'response': 'OK'}), 200



@app.errorhandler(BadRequest)
def gb_bad_request(e):
    return jsonify({'statusCode': 400, 'response': str(e)}), 400


@app.errorhandler(bson.errors.InvalidId)
def gb_not_found1(e):
    return jsonify({'statusCode': 404, 'response': 'Not found ' + e}), 404


@app.errorhandler(NotFound)
def gb_not_found2(e):

    return jsonify({'statusCode': 404, 'response': 'Not found'}), 404


@app.errorhandler(mongoengine.errors.FieldDoesNotExist)
def gb_not_found(e):
    return jsonify({'statusCode': 400, 'response': str(e)}), 400


@app.errorhandler(mongoengine.errors.ValidationError)
def gb_not_validation_err(e):
    return jsonify({'statusCode': 500, 'response': str(e)}), 500


@app.errorhandler(mongoengine.errors.InvalidQueryError)
def gb_not_invalid(e):
    return jsonify({'statusCode': 500, 'response': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5004)
