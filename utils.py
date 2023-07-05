import re
from werkzeug.security import generate_password_hash
from flask import jsonify


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def generate_hashed_password(unhashed_password):
    return generate_password_hash(unhashed_password)


def add_user(to_be_inserted_dict):
    pass


def validate_incoming_arguments(self, email, password='', is_put_req=False):
    if not is_valid_email(email):
        self.app.logger.info(f"Users API POST req given email id {email} is invalid...")
        return {'error': 1, 'message': f"Please enter valid email id"}

    if not is_put_req and len(password) < 6:
        self.app.logger.info(f"Users API POST req for email {email} given password is less than 6 characters.....")
        return {'error': 1, 'message': f"Passwords should be at least 6 characters long"}
    return {}


def validate_incoming_request(request_args, mandatory_args):
    for i in mandatory_args:
        if not request_args.get(i):
            return {'error': 1, 'message': f"{i} is a mandatory field"}
    return {}


def get_users_collection(self, id):
    users_collection = self.cache.getone('users', {'uid': id}, {'_id': 0, 'inserted_epoch': 0, 'updated_epoch': 0,'password':0})
    if not users_collection:
        self.app.logger.info(f"Users API GET req given user id : {id} is not found in DB")
        return {'error': 1, 'message': f"Given user id not found"}
    return users_collection
