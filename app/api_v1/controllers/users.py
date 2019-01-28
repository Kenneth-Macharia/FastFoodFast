''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.users import UserModel

class VerifyUser(Resource):
    ''' This class manges the verification of a User resource '''

    def get(self, User_Email):
        ''' This function handles GET requests to the route '/auth/login/<email> and returns a registered user '''

        row_returned = UserModel.find_user_by_User_Email(User_Email)

        if row_returned:
            return {'User-found':{'User_Id':row_returned[0], 'User_Name':row_returned[1], 'User_Email':row_returned[2], 'User_Type':row_returned[3]}}, 200
            
        return {'Response':'User not found'}, 404    


class AddUser(Resource):
    ''' This class manages the creation of a User resource '''

    parser = reqparse.RequestParser()

    def post(self, User_Email):
        ''' This function handles POST requests to the
        '/auth/signup/<User_Email>' route and controls creation of a
        new user. '''

        AddUser.parser.add_argument('User_Name', type=str, required=True,
                                 help='This field cant be left blank!')
        AddUser.parser.add_argument('User_Password', type=str, required=True,
                                 help='This field cant be left blank!')

        if not UserModel.find_user_by_User_Email(User_Email):
            json_payload = AddUser.parser.parse_args()

            user_to_add = {'User_Name':json_payload['User_Name'],
                           'User_Password':json_payload['User_Password'],
                           'User_Email': User_Email, 'User_Type': 'Guest'}

            UserModel.insert_user(user_to_add)
            return {'Response':'Succesfully signed up'}, 201
        return {'Response':'You are already registered'}, 400
        