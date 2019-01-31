''' This module hosts the flask app to be ran '''

import os
from flask import Flask, Blueprint
from flask_restful import Api
from controllers.users import UserSignUp
from controllers.menus import Menus, AddMenu, MenuMgt
from controllers.orders import UserOrders

SECRET = os.getenv('SECRET')
if not SECRET:
    assert False, 'Set app secret key ie. "set SECRET=<your secret key>"'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET

api = Api(app)

# TODO: Remove 'v1' from URLs after blueprints implementation
api.add_resource(UserSignUp, '/v1/auth/signup/<string:User_Email>')
api.add_resource(AddMenu, '/v1/menu')
api.add_resource(MenuMgt, '/v1/menu/<int:Menu_Id>')
api.add_resource(Menus, '/v1/menus')
api.add_resource(UserOrders, '/v1/user/orders')

