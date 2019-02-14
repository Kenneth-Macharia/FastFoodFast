''' This module contains the test code for the menu
functionality and will test the menu modules in controllers and
models '''

from flask import json
from tests.v1.configs import test_client, drop_tables


def login_helper(test_client, user):
    ''' Logs in a user passed in as an argument '''

    response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(response.data)["Access_token"])

    assert response.status_code == 200
    return token_data

def get_helper(test_client, token_data):
    ''' Perform the GET/menus request on behalf of the test functions '''

    test_response = test_client.get('/v1/menus', headers=token_data)
    return test_response

def test_menus_get(test_client):
    ''' Tests the menus GET ALL '/v1/menus' test endpoint '''

    # Ensure there are no menus in the database for this test run
    drop_tables('menus')

    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    # Login user & test for access control (This is an admin only fucntion)
    token_data = login_helper(test_client, user)
    test_response = get_helper(test_client, token_data)

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Test for no menu items found
    a_user = {"User_Email":"ken@abc.com",
              "User_Password":"abc"}

    token_data = login_helper(test_client, a_user)
    test_response = get_helper(test_client, token_data)

    assert 'No menu items found' in json.loads(test_response.data)['Response']['Success']
    assert test_response.status_code == 200

def test_menu_post(test_client):
    ''' Tests the menus POST '/v1/menu' test endpoint '''

    # Menu to add data
    menu_item_to_add = {"Menu_Name":"Autumn pumpkin soup", 
                        "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                        "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
                        "Menu_Price":20}

    # Login user & test for access control (This is an admin only function)
    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    token_data = login_helper(test_client, user)
    test_response = test_client.post('/v1/menu', data=json.dumps(menu_item_to_add), headers=token_data, content_type='application/json')

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Login Admin and post a menu
    a_user = {"User_Email":"ken@abc.com",
              "User_Password":"abc"}

    token_data = login_helper(test_client, a_user)

    # Post menu item
    test_response = test_client.post('/v1/menu', data=json.dumps(menu_item_to_add), headers=token_data, content_type='application/json')

    # Test POST responses
    assert 'Menu item succesfully added' in json.loads(test_response.data)['Response']['Success']
    assert test_response.status_code == 201

    # Test POST effect
    test_response = get_helper(test_client, token_data)

    assert json.loads(test_response.data)['Response']['Success']
    assert 'Autumn pumpkin soup' in json.loads(test_response.data)['Response']['Success'][0]['Menu_Name']
    assert json.loads(test_response.data)['Response']['Success'][0]['Menu_Price'] == 20

    # Test posting already existing menu
    test_response = test_client.post('/v1/menu', data=json.dumps(menu_item_to_add), headers=token_data, content_type='application/json')
    
    assert test_response.status_code == 400
    assert 'Menu item appears to already exist, check the menu details' in json.loads(test_response.data)['Response']['Failure']

def test_menu_put(test_client):
    ''' Tests the menus PUT '/v1/menu/<menu_id>' test endpoint '''

    # Update data
    status_update = {"Menu_Availability":"Available"}

    # Test a user cant access this endpoint
    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    token_data = login_helper(test_client, user)
    test_response = test_client.put('/v1/menu/1', data=json.dumps(status_update), headers=token_data, content_type='application/json')

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Login Admin
    a_user = {"User_Email":"ken@abc.com",
              "User_Password":"abc"}
    
    token_data = login_helper(test_client, a_user)

    # Tests to verify update change from default {'Unavailable' to 'Available and vice versa}
    # Verify the item created in POST above has the default status
    test_response = get_helper(test_client, token_data)

    assert 'Unavailable' in json.loads(test_response.data)['Response']['Success'][0]['Menu_Availability']

    # Perform an update
    test_response = test_client.put('/v1/menu/1', data=json.dumps(status_update), headers=token_data, content_type='application/json')
    
    # Test PUT responses
    assert 'Menu item updated' in json.loads(test_response.data)['Response']['Success']
    assert test_response.status_code == 200

    # Test PUT effect
    test_response = get_helper(test_client, token_data)
    assert 'Available' in json.loads(test_response.data)['Response']['Success'][0]['Menu_Availability']

    # Perform a reverse update
    status_update = {"Menu_Availability":"Unavailable"}

    test_client.put('/v1/menu/1', data=json.dumps(status_update), headers=token_data, content_type='application/json')

    # Test reverse PUT effect
    test_response = get_helper(test_client, token_data)
    assert 'Unavailable' in json.loads(test_response.data)['Response']['Success'][0]['Menu_Availability']

    # Test updating a non-existant menu item
    test_response = test_client.put('/v1/menu/10', data=json.dumps(status_update), headers=token_data, content_type='application/json')

    assert test_response.status_code == 404
    assert 'Menu item not found' in json.loads(test_response.data)['Response']['Failure']

def test_menu_delete(test_client):
    ''' Tests the menus DELETE '/v1/menu/<Menu_Id>' test endpoint '''

    # Test a user cant access this endpoint
    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    token_data = login_helper(test_client, user)
    test_response = test_response = test_client.delete('/v1/menu/1', headers=token_data, content_type='application/json')

    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Login Admin
    a_user = {"User_Email":"ken@abc.com",
              "User_Password":"abc"}

    token_data = login_helper(test_client, a_user)

    # Perform a delete
    test_response = test_client.delete('/v1/menu/1', headers=token_data)
    
    # Confirm DELETE responses
    assert 'Menu item deleted' in json.loads(test_response.data)['Response']['Success']
    assert test_response.status_code == 200

    # Test DELETE effect
    test_response = get_helper(test_client, token_data)
    assert 'No menu items found' in json.loads(test_response.data)['Response']['Success']
    assert test_response.status_code == 200

    # Test deleting a non-existant menu item
    test_response = test_client.delete('/v1/menu/1', headers=token_data, content_type='application/json')

    assert test_response.status_code == 404
    assert 'Menu item not found' in json.loads(test_response.data)['Response']['Failure']
    