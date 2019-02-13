''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                get_raw_jwt, jwt_required,
                                get_jwt_claims, get_jwt_identity)
from ..models.users import UserModel


class UserRegistration(Resource):
    ''' This class manages the user registration resource '''

    parser = reqparse.RequestParser()

    parser.add_argument('User_Email', type=str, required=True,
                        help='This field cant be left blank!')
    parser.add_argument('User_Password', type=str, required=True,
                        help='This field cant be left blank!')
    parser.add_argument('User_Name', type=str, required=True,
                        help='This field cant be left blank!')

    def post(self):
        ''' This function handles POST requests to the
        '/auth/signup' route for a new user registration. '''

        json_payload = UserRegistration.parser.parse_args()
        
        if not UserModel.find_user_by_user_email(json_payload['User_Email']):
            
            user_to_add = {'User_Name':json_payload['User_Name'],
                           'User_Password':UserModel.generate_hash(json_payload['User_Password']),
                           'User_Email': json_payload['User_Email'], 'User_Type': 'Guest'}

            UserModel.insert_user(user_to_add)

            return {'Response':{'Success':'Succesfully signed up {}'.format             (json_payload['User_Name'])}}, 201
        return {'Response':{'Failure':'{} is already registered'.format                 (json_payload['User_Email'])}}, 400


class UserUpdate(Resource):
    ''' This class manages the user update resource '''

    parser = reqparse.RequestParser()

    parser.add_argument('User_Email', type=str, required=True,
                        help='This field cant be left blank!')
    parser.add_argument('User_Type', type=str, required=True,
                        help='This field cant be left blank!')

    @jwt_required
    def put(self):
        ''' This function handles PUT requests to the
        '/auth/signup' route for updating user privileges '''

        if get_jwt_claims()['User_Type'] != 'Admin' and UserModel.check_if_admin_exists():
            return {'Response':{'Failure':'This an admin only function'}}, 401

        valid_user_types = ['Admin', 'Guest']
        json_payload = UserUpdate.parser.parse_args()

        if json_payload['User_Type'] not in valid_user_types:
            message = {'Failure':'Invalid user type'}
            code = 400

        elif not UserModel.find_user_by_user_email(json_payload['User_Email']):
            message = {'Failure':'{} not found, check and try again'.format(json_payload['User_Email'])}
            code = 404
        
        else:
            user_to_update = {'User_Email':json_payload['User_Email'],
                              'User_Type':json_payload['User_Type']}
            UserModel.update_user(user_to_update)
            message = {'Success':'User updated'}
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
        current_user = UserModel.find_user_by_user_email(json_payload['User_Email'])

        if not current_user:
            message = {'Failure':'{} not found, please sign up'.format(json_payload['User_Email'])}
            code = 404
            access_token = ''
            
        elif not UserModel.verify_hash(json_payload['User_Password'], current_user[2]):
            message = {'Failure':'Password is incorrect, try again'}
            code = 400
            access_token = ''
        
        else:
            # Create a complex user identity
            user = {'User_Email':json_payload['User_Email'], 'User_Type':current_user[4]}

            # Generate an access token for the authenticated user, used as follows: 'Bearer <JWT>'
            access_token = create_access_token(user)
            message = {'Success':'Succesfully signed in {}'.format(current_user[1])}
            code = 200

        return {'Response': message,
                'Access_token':access_token}, code
                
      
class UserLogout(Resource):
    ''' This class manages user logout '''

    @jwt_required
    def post(self):
        ''' This function handles POST requests to the
        '/auth/logout' route and logs out a user by blacklisting their token '''

        current_user = UserModel.find_user_by_user_email(get_jwt_identity())
        jti = get_raw_jwt()['jti']
        UserModel.add_blacklisted_token(jti)

        return {'Response':{'Success':'Succesfully signed out {}'.format(current_user[1])}}, 200
