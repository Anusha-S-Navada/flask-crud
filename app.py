from flask import Flask
from flask_restful import Api
from database import DatabaseAPI
from cache import CacheAPI
from userapi import UserAPI
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.environ.get('MONGO_URI')
app_host = os.environ.get('APP_HOST')
app_port = int(os.environ.get('APP_PORT'))
document_limit = int(os.environ.get('DOCUMENT_LIMIT', 10))  # used to limit document in a get all response.

app = Flask(__name__)
api = Api(app)

db = DatabaseAPI(mongo_uri)
cache = CacheAPI(db)

userApi = UserAPI.setApp(app, cache,document_limit)
api.add_resource(userApi, '/users', '/users/<string:id>')

if __name__ == "__main__":
    app.run(host=app_host, port=app_port)
