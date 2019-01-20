''' This module creates the flask app to be ran '''

from flask import Flask
from flask_restful import Api
from .config import env_app_configs
from app.api_v1.controllers.app import Test_app
from app.api_v1.controllers.users import Users, User


def create_app(run_time_config):
    ''' This functions take the app initialized in the app module, wraps
    the environment configuration to use to run it and returns it '''

    app = Flask(__name__)
    app.config.from_object(env_app_configs[run_time_config])

    api = Api(app)
    api.add_resource(Test_app, '/test_api')
    api.add_resource(Users, '/api_v1/users')
    api.add_resource(User, '/api_v1/user/<string:email>')

    return app