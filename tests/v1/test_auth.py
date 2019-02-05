''' This module contains the test code for the user authentication functionality and will test the users modules in controllers and models '''

from flask import json
from configs import test_client, drop_tables


def test_user_registration(test_client):
    ''' Test the user registration process '''

    # Test all user data is entered

    # Test user data entered is str

    # Test new user creation

    # Test same user cannot be registered twice

    # Test new/default user is 'Guest' not 'Admin'


def test_user_login(test_client):
    
    # Test all user data is entered

    # Test user data entered is str

    # Test a non registered user cannot be logged in 

    # Test wrong password entered will deny access

    # Test successfull login and token generation


def test_user_type_upgrade(test_client):
    
    # Test all user data is entered

    # Test user data entered is str

    # Test that a 'Guest' cannot access this feature, if an 'Admin' registered

    # Test that a type status can only be 'Guest' or 'Admin'

    # Test successfull type update


def test_user_logout(test_client):
    
    # Test that a non-logged in user can logout

    # Test successful logout

    #Test that a logged out user cannot access any endpoint






# drop_tables('users')
#  # Sign up a new user, will be a default 'Guest' user
#     new_user = {"User_Email":"ken@abc.com",
#                 "User_Password":"abc",
#                 "User_Name":"ken"}

#     test_response = test_client.post('/v1/auth/signup', data=json.dumps                                          (new_user),                                                                 content_type='application/json')

#     assert test_response.status_code == 201

#     # Login the registered user
#     test_response = test_client.post('/v1/auth/login', data=json.dumps                                           (new_user),                                                                 content_type='application/json')

#     assert test_response.status_code == 200

#     # Upgrade the 'Guest' to 'Admin' to access admin only menu features
#     user_to_update = {"User_Email":"ken@abc.com", "User_Type":"Admin"}

#     token = json.loads(test_response.data)["Access_token"]
#     token_data = dict(Authorization="Bearer " + token)

#     test_response = test_client.put('/v1/auth/update', 
#                                     data=json.dumps(user_to_update),
#                                     headers=token_data,
#                                     content_type='application/json')

#     assert test_response.status_code == 200

#     # Logout user to revoke 'Guest' token
#     test_response = test_client.post('/v1/auth/logout', headers=token_data)

#     assert test_response.status_code == 200

#     # Login to acquire an 'Admin' token
#     test_response = test_client.post('/v1/auth/login', data=json.dumps                                           (new_user),                                                                 content_type='application/json')

#     assert test_response.status_code == 200