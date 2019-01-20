''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.users import Users_model, User_model


class Users(Resource):
    ''' This class manages the Users resource '''

    def get(self):
        ''' This function handles GET all requests to the '/api_v1/users' route '''

        users = []
        rows_returned = Users_model.find_all_users()

        for row in rows_returned:
            users.append({'Id':row[0], 'Name':row[1], 'Email':row[2], 'Type':row[3]})
        
        return {'All Users':users}, 200
    

class User(Resource):
    ''' This class manages the User resource '''

    parser = reqparse.RequestParser()

    def post(self, email):
        ''' This function handles POST requests to the '/api_v1/user/<email>' route '''

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

    def put(self, email):
        ''' This function handles PUT requests to the '/api_v1/user/<email>' route '''

        User.parser.add_argument('type', type=str, required=True, help='This field cant be left blank!')

        valid_user_types = ['Admin', 'Guest']
        json_payload = User.parser.parse_args()
        user_to_update = {'email':email, 'type':json_payload['type']}
        row_returned = User_model.find_user_by_email(email)

        if not row_returned :
            response = 'User not found'
            code = 400

        elif json_payload['type'] not in valid_user_types:
            response = 'User type can either be "Admin" or "Guest" only'
            code = 400

        elif row_returned[3] == json_payload['type']:
            response = 'User type is already {}'.format(json_payload['type'])
            code = 400

        else:
            User_model.update_user(user_to_update)
            response = 'User updated'
            code = 200

        return {'Response':response}, code   

    def get(self, email):
        ''' This function handles GET one requests to the '/api_v1/user/<email>' route '''

        row_returned = User_model.find_user_by_email(email)

        if row_returned:
            return {'User found':{'Id':row_returned[0], 'Name':row_returned[1], 'Email':row_returned[2], 'Type':row_returned[3]}}, 200
            
        return {'Response':'User not found'}, 404    

    def delete(self, email):
        ''' This function handles DELETE requests to the '/api_v1/user/<email>' route '''

        if not User_model.find_user_by_email(email):
            response = 'User not found'
            code = 400

        else:
            User_model.delete_user(email)
            response = 'User deleted'
            code = 200

        return {'Response':response}, code
        
