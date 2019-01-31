''' This module creates the flask app to be ran '''

from flask import Flask, Blueprint
from flask_restful import Api
from app.api_v1.models.users import authenticate, identity
from app.api_v1.controllers.users import AddUser, VerifyUser
from app.api_v1.controllers.menus import Menus, AddMenu, MenuMgt
from app.api_v1.controllers.orders import UserOrders
from .config import ENV_APP_CONFIGS


def create_app(run_time_config):
    ''' This functions take the app initialized in the app
    module, wraps the environment configurations and registers
    a blueprint to version the app '''

    v1_blueprint = Blueprint('version1_blueprint', __name__)    
    app = Flask(__name__)

    api = Api(v1_blueprint, prefix='/v1')
    api.add_resource(AddUser, '/auth/signup/<string:User_Email>')
    api.add_resource(VerifyUser, '/auth/login/<string:User_Email>')
    api.add_resource(AddMenu, '/menu')
    api.add_resource(MenuMgt, '/menu/<int:Menu_Id>')
    api.add_resource(Menus, '/menus')
    api.add_resource(UserOrders, '/user/orders')

    app.register_blueprint(v1_blueprint)
    app.config.from_object(ENV_APP_CONFIGS[run_time_config])

    return app
