''' This module contains the test code for the menu functionality and will test the menu modules in controllers and models '''

from flask import json
from configs import test_client, drop_tables


def login_helper(test_client):
    ''' This function will login a registered user '''

    # Sign up a user
    new_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc",
                "User_Name":"Ken"}

    test_client.post('/v1/auth/signup', data=json.dumps                                          (new_user),                                                                 content_type='application/json') 

    # Sign in the new user
    new_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login', data=json.dumps                                           (new_user),                                                                 content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    # Upgrade new user to 'Admin' status
    user_to_update = {"User_Email":"ken@abc.com", "User_Type":"Admin"}

    test_client.put('/v1/auth/update', data=json.dumps(user_to_update),
                    headers=token_data,
                    content_type='application/json')
    
    # Sign out user to revoke 'Guest' token
    test_response = test_client.post('/v1/auth/logout', headers=token_data)

    # Login again to acquire an 'Admin' token
    test_response = test_client.post('/v1/auth/login', data=json.dumps                                           (new_user),                                                                 content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    return token_data

def test_menus_get(test_client):
    ''' Tests the menus GET ALL '/v1/menus' test endpoint '''

    # Ensure there are no menus in the database for this test run
    drop_tables('menus')

    # Login user
    token_data = login_helper(test_client)

    # Test for no menu items found
    test_response = test_client.get('/v1/menus', headers=token_data)

    assert 'No items found' in json.loads(test_response.data)
    assert test_response.status_code == 200

def test_menu_post(test_client):
    ''' Tests the menus POST '/v1/menu' test endpoint '''

    # Login user
    token_data = login_helper(test_client)

    # Test for items found
    Menu_item_to_add = {"Menu_Name":"Autumn pumpkin soup", 
                        "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                        "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
                        "Menu_Price":20}

    test_response = test_client.post('/v1/menu', data=json.dumps                                                 (Menu_item_to_add),
                                           headers=token_data,                  content_type='application/json')
    # Test POST responses
    assert 'Menu item succesfully added' in json.loads(test_response.data)                                                    ['Response']
    assert test_response.status_code == 201

    # Test POST effect
    test_response = test_client.get('/v1/menus', headers=token_data)

    assert 'Items found' in json.loads(test_response.data)
    assert 'Autumn pumpkin soup' in json.loads(test_response.data)                                                     ['Items found'][0]                                                          ['Menu_Name']
    assert json.loads(test_response.data)['Items found'][0]['Menu_Price'] == 20

def test_menu_put(test_client):
    ''' Tests the menus PUT '/v1/menu/<menu_id>' test endpoint '''
    
    # Item to update not found will not be a possibility, as the the update buttons will be on the same row as an existing item in the admin dashboard.
    # Update to where menu item status is set to something other than than 'Available or 'Unavailable' will also not be possible as there will two buttons on the item row to either activate one or the other.
    # Check that a status value has been supplied will also be enforced by the button status, one of the buttons must be selected by default.

    # Login user
    token_data = login_helper(test_client)

    # Tests to verify update change from default {'Unavailable' to 'Available and vice versa}
    # Verify the item created in POST above has the default status
    test_response = test_client.get('/v1/menus', headers=token_data)

    assert 'Unavailable' in json.loads(test_response.data)['Items found'][0]                                   ['Menu_Availability']
    # Perform an update
    status_update = {"Menu_Availability":"Available"}

    test_response = test_client.put('/v1/menu/1', data=json.dumps                                               (status_update),
                                        headers=token_data,                  content_type='application/json')
    
    # Test PUT responses
    assert 'Menu item updated' in json.loads(test_response.data)['Response']
    assert test_response.status_code == 200

    # Test PUT effect
    test_response = test_client.get('/v1/menus', headers=token_data)
    assert 'Available' in json.loads(test_response.data)['Items found'][0]                                   ['Menu_Availability']

    # Perform a reverse update
    status_update = {"Menu_Availability":"Unavailable"}

    test_client.put('/v1/menu/1', data=json.dumps(status_update),                               headers=token_data, content_type='application/json')

    # Test reverse PUT effect
    test_response = test_client.get('/v1/menus', headers=token_data)
    assert 'Unavailable' in json.loads(test_response.data)['Items found'][0]                                      ['Menu_Availability']

def test_menu_delete(test_client):
    ''' Tests the menus DELETE '/v1/menu/<Menu_Id>' test endpoint '''

    # Login user
    token_data = login_helper(test_client)

    # Perform a delete
    test_response = test_client.delete('/v1/menu/1', headers=token_data)
    
    # Confirm DELETE responses
    assert 'Menu item deleted' in json.loads(test_response.data)                                                  ['Response']
    assert test_response.status_code == 200

    # Test DELETE effect
    test_response = test_client.get('/v1/menus', headers=token_data)
    assert 'No items found' in json.loads(test_response.data)
    assert test_response.status_code == 200
    