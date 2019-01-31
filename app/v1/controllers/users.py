''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.users import UserModel


class UserSignUp(Resource):
    ''' This class manages the creation of a User resource '''

    parser = reqparse.RequestParser()

    def post(self, User_Email):
        ''' This function handles POST requests to the
        '/auth/signup/<User_Email>' route and controls creation of a
        new user. '''

        UserSignUp.parser.add_argument('User_Name', type=str, required=True,
                                 help='This field cant be left blank!')
        UserSignUp.parser.add_argument('User_Password', type=str, required=True,
                                 help='This field cant be left blank!')

        if not UserModel.find_user_by_User_Email(User_Email):
            json_payload = UserSignUp.parser.parse_args()

            user_to_add = {'User_Name':json_payload['User_Name'],
                           'User_Password':json_payload['User_Password'],
                           'User_Email': User_Email, 'User_Type': 'Guest'}

            UserModel.insert_user(user_to_add)
            return {'Response':'Succesfully signed up'}, 201
        return {'Response':'You are already registered'}, 400

        