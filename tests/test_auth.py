''' This module contains the test code for the user authentication functionality and will test the users modules in controllers and
models '''

from flask import json
from configs import test_client, drop_tables


def test_user_registration(test_client):
    ''' Test the user registration process '''

    # Ensure there are no users in the database for this test run
    drop_tables('users')

    # Test all user data is entered
    user = {"User_Password":"abc",
            "User_Name":"Ken"}

    test_response = test_client.post('/v1/auth/signup',
                                     data=json.dumps(user), content_type='application/json')                 
    assert 'This field cant be left blank!' in json.loads(test_response.data)['message']['User_Email']

    # Test new user creation
    user = {"User_Email":"ken@abc.com",
            "User_Password":"abc",
            "User_Name":"Ken"}

    test_response = test_client.post('/v1/auth/signup', data=json.dumps(user), content_type='application/json')

    assert test_response.status_code == 201
    assert 'Succesfully signed up Ken' in json.loads(test_response.data)['Response']['Success']

    # Test same user cannot be registered twice
    test_response = test_client.post('/v1/auth/signup', data=json.dumps(user), content_type='application/json')

    assert test_response.status_code == 400
    assert 'ken@abc.com is already registered' in json.loads(test_response.data)['Response']['Failure']

def test_user_login(test_client):
    ''' Test the user login process '''

    # Ensure there are no users in the database for this test run
    drop_tables('users')

    # Test a non registered user cannot be logged in
    user = {"User_Email":"ken@abc.com",
            "User_Password":"abc",
            "User_Name":"Ken"}

    test_response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')
    
    assert test_response.status_code == 404 
    assert 'ken@abc.com not found, please sign up' in json.loads(test_response.data)['Response']['Failure']

    # Test wrong password entered will deny access
    test_client.post('/v1/auth/signup', data=json.dumps(user), content_type='application/json')

    user = {"User_Email":"ken@abc.com",
            "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')

    assert test_response.status_code == 400
    assert 'Password is incorrect, try again' in json.loads(test_response.data)['Response']['Failure']

    # Test successfull login and token generation
    user = {"User_Email":"ken@abc.com",
            "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')

    assert test_response.status_code == 200
    assert 'Succesfully signed in Ken' in json.loads(test_response.data)['Response']['Success']
    assert json.loads(test_response.data)['Access_token'] != ''

    # Test new/default user is 'Guest' not 'Admin'
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    test_response = test_client.get('/v1/menus', headers=token_data)

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']
    
def test_user_type_upgrade(test_client):
    ''' Test the user upgrade process '''

    # Ensure there are no users in the database for this test run
    drop_tables('users')

    # Test that a 'Guest' cannot access this feature, if an 'Admin' registered
    user_guest = {"User_Email":"shee@xyz.com",
                  "User_Password":"xyz",
                  "User_Name":"Shee",
                  "User_Type":"Super"}

    user_admin = {"User_Email":"ken@abc.com",
                  "User_Password":"abc",
                  "User_Name":"Ken",
                  "User_Type":"Admin"}
    
    user_unregistered = {"User_Email":"chris@jkl.com",
                         "User_Password":"jkl",
                         "User_Name":"Chris",
                         "User_Type":"Admin"}

        # Signup both users above
    test_client.post('/v1/auth/signup', data=json.dumps(user_admin), content_type='application/json')

    test_client.post('/v1/auth/signup', data=json.dumps(user_guest), content_type='application/json')

        # Log in user_admin
    test_response = test_client.post('/v1/auth/login', data=json.dumps(user_admin), content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

        # Upgrade status to 'Admin' -Tests for successful User_Type upgrade also
    test_response = test_client.put('/v1/auth/update', data=json.dumps(user_admin), headers=token_data, content_type='application/json')

    assert test_response.status_code == 200
    assert 'User updated' in json.loads(test_response.data)['Response']['Success']
 
        # Log out the admin user
    test_response = test_client.post('/v1/auth/logout', headers=token_data)

        # Sign in "Guest" user and attempt to access the update user endpoint
    test_response = test_client.post('/v1/auth/login', data=json.dumps(user_guest), content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    test_response = test_client.put('/v1/auth/update', data=json.dumps(user_guest), headers=token_data, content_type='application/json')

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Test that a user type can only be 'Guest' or 'Admin'
        # Log in the admin user
    test_response = test_client.post('/v1/auth/login', data=json.dumps(user_admin), content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

        # Attempt to upgrade the 'Guest' user to an arbitrary user_type 'Super'
    test_response = test_client.put('/v1/auth/update', data=json.dumps(user_guest), headers=token_data, content_type='application/json')

    assert test_response.status_code == 400
    assert 'Invalid user type' in json.loads(test_response.data)['Response']['Failure']

    # Test that an unregistered user type cannot be upgraded
    test_response = test_client.put('/v1/auth/update', data=json.dumps(user_unregistered), headers=token_data, content_type='application/json')

    assert test_response.status_code == 404
    assert 'chris@jkl.com not found, check and try again' in json.loads(test_response.data)['Response']['Failure']

def test_user_logout(test_client):
    ''' Test the user logout process '''

    user = {"User_Email":"ken@abc.com",
            "User_Password":"abc",
            "User_Name":"Ken",
            "User_Type":"Admin"}

    # Test that a non-logged in user cannot logout
    token_data = ''
    test_response = test_client.post('/v1/auth/logout', headers=token_data)

    assert test_response.status_code == 401
    assert 'Missing Authorization Header' in json.loads(test_response.data)['msg']

    # Test successful logout
        # Log in user above
    test_response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')
   
        # Log out user
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    test_response = test_client.post('/v1/auth/logout', headers=token_data)

    assert test_response.status_code == 200
    assert 'Succesfully signed out Ken' in json.loads(test_response.data)['Response']['Success']

    # Test that a logged out user cannot access any endpoint
        # The 'Guest' above can access the user upgrade endpoint, since this is the only existing user account in the database.
    test_response = test_client.put('/v1/auth/update', data=json.dumps(user), headers=token_data, content_type='application/json')

    assert test_response.status_code == 401
    assert 'Token has been revoked' in json.loads(test_response.data)['msg']
