''' This module defines the user resources exposed by the API '''

from flask_restful import Resource, reqparse
from app.api_v1.models.users import User, Users


class Users(Resource):
    ''' This class manages the Users resource '''

    def get(self):
        ''' This function handles GET all requests to the '/users' route '''

        users = []
        rows_returned = Users.all_users()

        if rows_returned:
            for row in rows_returned:
                users.append({'name':row[1], 'email':row[3], 'user_type':row[4]})

        return {'All Users':users}, 200
    

class User(Resource):
    ''' This class manages the User resource '''

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cant be left blank!')
    parser.add_argument('password', type=str, required=True, help='This field cant be left blank!')
    parser.add_argument('email', type=str, required=True, help='This field cant be left blank!')
    parser.add_argument('user_type', type=str, required=True, help='This field cant be left blank!')

    def post(self, email):
        ''' This function handles POST requests to the '/user<email>' route '''

        if User.find_user_by_email(email):
            return {'Response':'You are already registered'}, 400

        user_data = User.parser.parse_args()
        user_to_add = {'name':response_data['name'],
        'password':response_data['password'], 'email': email, 'user_type':
        'Guest'}

        User.insert_user(user_data)
        return {'Response':'Succesfully signed up'}, 201

    def put(self, email):
        ''' This function handles PUT requests to the '/user/<email>' route '''

        valid_user_types = ['Admin', 'Guest']
        response_data = User.parser.parse_args()
        user_to_update = {'email':email, 'user_type':response_data['user_type']}

        if not User.find_user_by_email(email):
            response = 'User not found'
            code = 400

        elif response_data['user_type'] not in valid_user_types:
            response = 'User type can either be "Admin" or "Guest" only'
            code = 400

        else:
            User.update_user(user_to_update)
            response = 'User updated'
            code = 200

        return {'Response':response}, code   

    def delete(self, email):
        ''' This function handles DELETE requests to the '/user/<name>' route '''

        if not User.find_user_by_email(email):
            response = 'User not found'
            code = 400

        else:
            User.delete_user(email)
            response = 'User deleted'
            code = 200

        return {'Response':response}, code

    def get(self, email):
        ''' This function handles GET one requests to the '/user/<name>' route '''

        row_returned = User.find_user_by_email(email)

        if row_returned:
            return {'Response':{'name':row[1], 'email':row[3], 'user_type':row[4]}}, 200
        return {'Response':'User not found'}, 404
        
