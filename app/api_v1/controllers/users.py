''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.users import User_model

    
class User(Resource):
    ''' This class manages the User resource '''

    parser = reqparse.RequestParser()

    def post(self, email):
        ''' This function handles POST requests to the '/auth/signup/<email>' route and controls creation of a new user. '''

        User.parser.add_argument('name', type=str, required=True, help='This field cant be left blank!')
        User.parser.add_argument('password', type=str, required=True, help='This field cant be left blank!')

        if not User_model.find_user_by_email(email):
            json_payload = User.parser.parse_args()

            user_to_add = {'name':json_payload['name'],
            'password':json_payload['password'], 'email': email, 'type':
            'Guest'}

            User_model.insert_user(user_to_add)
            return {'Response':'Succesfully signed up'}, 201

        return {'Response':'You are already registered'}, 400