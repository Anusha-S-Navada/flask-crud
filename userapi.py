import json

from flask_restful import Resource, reqparse, request
from flask import request as argrequest
from bson.json_util import dumps
from flask import jsonify
import traceback
from utils import is_valid_email, generate_hashed_password, validate_incoming_request, validate_incoming_arguments, get_users_collection
import uuid, time




class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')

        super(UserAPI, self).__init__()

    @classmethod
    def setApp(cls, app, cache,document_limit):
        cls.app = app
        cls.cache = cache
        cls.document_limit = document_limit
        return cls

    def get(self, id=None):
        self.app.logger.info(f"USERS API GET req called and id is : {id}")
        if id:
            users_collection = get_users_collection(self, id)
            if users_collection.get('error'):
                self.app.logger.info(f"Users API GET req given user id : {id} is not found in DB")
                resp = jsonify(users_collection)
                resp.status_code = 404
                return resp

            return jsonify({'error': 0, 'data': json.loads(dumps(users_collection))})
        else:
            page = int(request.args.get('page', 1))

            # Calculate skip value based on page and limit
            skip = (page - 1) * self.document_limit
            # Project the queries so that users see only abstracted value..
            result = self.cache.get('users', {}, {'_id': 0, 'password': 0, 'epoch': 0, 'updated_epoch': 0,'inserted_epoch':0}).skip(
                skip).limit(self.document_limit)
            return jsonify({'error': 0, 'data': json.loads(dumps(result))})

    def post(self):
        self.app.logger.info("USERS API POST req called")
        try:
            args = self.reqparse.parse_args()
        except Exception as e:
            traceback.print_exc()
            self.app.logger.error('UserAPI POST : Exception ' + str(repr(e)))
            return {'error': 1, 'message': 'Error parsing arguments. Please check the arguments.'}

        self.app.logger.info(f"Users API POST args : {args}")
        mandatory_arguments = ['name', 'email', 'password']
        # do some validation
        initial_validation_result = validate_incoming_request(args, mandatory_arguments)
        if initial_validation_result.get('error'):
            resp = jsonify(initial_validation_result)
            resp.status_code = 400
            return resp
        # I am not using get here bcz i am already doing not null condition above
        name = args['name']
        email = args['email']
        password = args['password']

        final_validation_result = validate_incoming_arguments(self, email, is_put_req=True)
        if final_validation_result.get('error'):
            resp = jsonify(final_validation_result)
            resp.status_code = 400
            return resp

        hashed_password = generate_hashed_password(password)
        uid = str(uuid.uuid4())
        to_be_inserted_dict = {'name': name, 'email': email, 'password': hashed_password, 'uid': uid,
                               'inserted_epoch': time.time()}
        result = self.cache.add('users', to_be_inserted_dict, '')

        if not result:
            self.app.logger.info(f"Users API POST req something happened while inserting data to DB")
            resp = jsonify({'error': 1, 'message': f"Something went wrong please try again!"})
            resp.status_code = 500
            return resp
        return jsonify({'error': 0, 'data': "user added successfully", 'user_id': uid})

    def put(self, id):
        self.app.logger.info(f"USERS API PUT req called and user id is : {id}")

        try:
            args = self.reqparse.parse_args()
        except Exception as e:
            traceback.print_exc()
            self.app.logger.error('UserAPI PUT : Exception ' + str(repr(e)))
            return {'error': 1, 'message': 'Error parsing arguments. Please check the arguments.'}

        self.app.logger.info(f"USER req put args : {args}")
        # check if user id exists in db or not..
        users_collection = get_users_collection(self, id)
        if users_collection.get('error'):
            self.app.logger.info(f"Users API PUT req given user id : {id} is not found in DB")
            resp = jsonify(users_collection)
            resp.status_code = 404
            return resp

        mandatory_arguments = ['name', 'email']
        initial_validation_result = validate_incoming_request(args, mandatory_arguments)
        if initial_validation_result.get('error'):
            resp = jsonify(initial_validation_result)
            resp.status_code = 400
            return resp

        name = args['name']
        email = args['email']

        final_validation_result = validate_incoming_arguments(self, email, is_put_req=True)
        if final_validation_result.get('error'):
            resp = jsonify(final_validation_result)
            resp.status_code = 400
            return resp

        users_collection['name'] = name
        users_collection['email'] = email
        users_collection['updated_epoch'] = time.time()
        print(f"Users collection is :{users_collection}")
        ret = self.cache.updateWithPull("users", {'uid': id}, users_collection, {})
        if not ret:
            self.app.logger.info(f"Users API PUT req something happened while Updating data to DB")
            resp = jsonify({'error': 1, 'message': f"Something went wrong please try again!"})
            resp.status_code = 500
            return resp

        return jsonify({'error': 0, 'data': "User data updated successfully."})

    def delete(self, id):
        self.app.logger.info(f"USERS API DELETE req called and user id is : {id}")

        # check if user id exists in db or not..
        users_collection = get_users_collection(self, id)
        if users_collection.get('error'):
            self.app.logger.info(f"Users API DELETE req given user id : {id} is not found in DB")
            resp = jsonify(users_collection)
            resp.status_code = 404
            return resp

        ret = self.cache.deleteone('users', {'uid': id})
        if not ret:
            self.app.logger.info(f"Users API DELETE req something happened while Deleting data from DB")
            resp = jsonify({'error': 1, 'message': f"Something went wrong please try again!"})
            resp.status_code = 500
            return resp
        return jsonify({'error': 0, 'data': "User deleted successfully"})
