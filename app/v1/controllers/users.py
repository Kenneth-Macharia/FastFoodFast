''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, get_jwt_identity, get_raw_jwt, jwt_required, get_jwt_claims)
from ..models.users import UserModel


class User(Resource):
    ''' This class manages the User resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the
        '/auth/signup' route for a new user registration. '''

        User.parser.add_argument('User_Email', type=str, required=True,
                                 help='This field cant be left blank!')
        User.parser.add_argument('User_Password', type=str, required=True,
                                 help='This field cant be left blank!')
        User.parser.add_argument('User_Name', type=str, required=True,
                                 help='This field cant be left blank!')

        json_payload = User.parser.parse_args()
        if not UserModel.find_user_by_User_Email(json_payload['User_Email']):
            
            user_to_add = {'User_Name':json_payload['User_Name'],
                           'User_Password':UserModel.generate_hash(json_payload['User_Password']),
                           'User_Email': json_payload['User_Email'], 'User_Type': 'Guest'}

            UserModel.insert_user(user_to_add)

            return {'Response':'Succesfully signed up'}, 201
        return {'Response':'You are already registered'}, 400

    @jwt_required
    def put(self):
        ''' This function handles PUT requests to the
        '/auth/signup' route for updating user privileges '''

        User.parser.add_argument('User_Email', type=str, required=True,
                                 help='This field cant be left blank!')
        User.parser.add_argument('User_Type', type=str, required=True,
                                 help='This field cant be left blank!')

        if get_jwt_claims()['User_Type'] != 'Admin' and UserModel.check_if_admin_exists():
            return {'Rights Error':'This an admin only function'}

        valid_user_types = ['Admin', 'Guest']
        json_payload = User.parser.parse_args()

        if 'User_Type' not in json_payload.keys():
            message = 'User_Type input missing'
            code = 400

        elif json_payload['User_Type'] not in valid_user_types:
            message = 'Invalid user type'
            code = 400

        elif not UserModel.find_user_by_User_Email(json_payload['User_Email']):
            message = 'Email: {}, not registered'.format(json_payload['User_Email'])
            code = 404
        
        else:
            user_to_update = {'User_Email':json_payload['User_Email'],
                              'User_Type':json_payload['User_Type']}
            UserModel.update_user(user_to_update)
            message = 'User updated'
            code = 200

        return {'Response': message}, code


class UserLogin(Resource):
    ''' This class manages user login '''

    parser = reqparse.RequestParser()
    parser.add_argument('User_Email', type=str, required=True,
                                 help='This field cant be left blank!')
    parser.add_argument('User_Password', type=str, required=True,
                                 help='This field cant be left blank!')

    def post(self):
        ''' This function handles POST requests to the
        '/auth/login' route and ensure all user are logged in '''

        json_payload = UserLogin.parser.parse_args()
        current_user = UserModel.find_user_by_User_Email(json_payload['User_Email'])

        if not current_user:
            message = '{} not found, please sign up'.format(json_payload['User_Email'])
            code = 404
            access_token = ''
        
        elif not UserModel.verify_hash(json_payload['User_Password'],current_user[2]):
            message = 'Password is incorrect, try again'
            code = 400
            access_token = ''
        
        else:
            # Create a complex user identity
            user = {'User_Email':json_payload['User_Email'], 'User_Type':current_user[4]}

            # Generate an access token for the authenticated user, used as follows: 'Bearer <JWT>'
            access_token = create_access_token(user)
            message = 'Succesfully signed in'
            code = 200

        return {'Response': message,
                'Access_token':access_token}, code
      
      
class UserLogout(Resource):
    ''' This class manages user logout '''

    @jwt_required
    def post(self):
        ''' This function handles POST requests to the
        '/auth/logout' route and logs out a user by blacklisting their token '''

        jti = get_raw_jwt()['jti']
        UserModel.add_blacklisted_token(jti)

        return {'Response': 'Succesfully signed out'}

        