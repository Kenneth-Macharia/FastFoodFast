''' This module creates the flask app to be ran '''

from flask import Flask, Blueprint
from flask_restful import Api
from .config import env_app_configs
from app.api_v1.controllers.users import User
from app.api_v1.controllers.menus import Menu


def create_app(run_time_config):
    ''' This functions take the app initialized in the app module, wraps
        the environment configuration '''
    ''' Registers a blueprint to verision the app '''

    v1_blueprint = Blueprint('version1_blueprint', __name__)
    app = Flask(__name__)

    api = Api(v1_blueprint, prefix='/v1')
    api.add_resource(User, '/auth/signup/<string:email>')
    api.add_resource(Menu, '/menu')

    app.register_blueprint(v1_blueprint)
    app.config.from_object(env_app_configs[run_time_config])

    return app