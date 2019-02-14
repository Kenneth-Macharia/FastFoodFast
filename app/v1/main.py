''' This module hosts the flask app to be ran '''

import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.v1.models.users import UserModel
from app.v1.controllers.users import (UserRegistration, UserUpdate, UserLogin, UserLogout)
from app.v1.controllers.menus import Menus, AddMenu, MenuMgt
from app.v1.controllers.orders import UserOrders, AdminOrders, AdminOrder 

# Ensures a secret key has been set in the os envirnement before the app can run
SECRET = os.getenv('SECRET')
if not SECRET or SECRET == '':
    exit('Set app secret key - See .env sample file')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    ''' Called whenever create_access_token is called and defines
    what custom claims should be added to the access token, in this
    case the user type '''
    return {'User_Type': user['User_Type']}

@jwt.user_identity_loader
def user_identity_lookup(user):
    ''' Called whenever create_access_token is called and defines
    what the identity of the access token should be '''
    return user['User_Email']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    ''' Called whenever a token is presented for authenitcation and ensures it is not blacklisted '''
    jti = decrypted_token['jti']
    return UserModel.is_token_blacklisted(jti)

# Register require endpoints
api = Api(app)
api.add_resource(UserRegistration, '/v1/auth/signup')
api.add_resource(UserUpdate, '/v1/auth/update')
api.add_resource(UserLogin, '/v1/auth/login')
api.add_resource(UserLogout, '/v1/auth/logout')
api.add_resource(AddMenu, '/v1/menu')
api.add_resource(MenuMgt, '/v1/menu/<int:menu_id>')
api.add_resource(Menus, '/v1/menus')
api.add_resource(UserOrders, '/v1/users/orders')
api.add_resource(AdminOrders, '/v1/orders')
api.add_resource(AdminOrder, '/v1/orders/<int:order_id>')
