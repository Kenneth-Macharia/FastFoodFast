''' This module contains the test code for the menu functionality and will test the menu modules in controllers and models '''

from flask import json
from configs import test_client, drop_tables


def login_helper(test_client):
    ''' This function will login a registered user '''

    # This user must exist in the database for this test suite
    new_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login', data=json.dumps                                           (new_user),                                                                 content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)["Access_token"])

    return token_data

def test_menus_get(test_client):
    ''' Tests the menus GET ALL '/v1/menus' test endpoint '''

    # Ensure the test database is clean for this test run
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

    test_response_post = test_client.post('/v1/menu', data=json.dumps                                                 (Menu_item_to_add),
                                           headers=token_data,                  content_type='application/json')
    # Test POST responses
    assert 'Menu item succesfully added' in json.loads(test_response_post.data)                                                    ['Response']
    assert test_response_post.status_code == 201

    # Test POST effect
    test_response_get = test_client.get('/v1/menus', headers=token_data)

    assert 'Items found' in json.loads(test_response_get.data)
    assert 'Autumn pumpkin soup' in json.loads(test_response_get.data)                                                     ['Items found'][0]                                                          ['Menu_Name']
    assert json.loads(test_response_get.data)['Items found'][0]['Menu_Price'] == 20

def test_menu_put(test_client):
    ''' Tests the menus PUT '/v1/menu/<menu_id>' test endpoint '''
    
    # Item to update not found will not be a possibility, as the the update buttons will be on the same row as an existing item in the admin dashboard.
    # Update to where menu item status is set to something other than than 'Available or 'Unavailable' will also not be possible as there will two buttons on the item row to either activate one or the other.
    # Check that a status value has been supplied will also be enforced by the button status, one of the buttons must be selected by default.

    # Login user
    token_data = login_helper(test_client)

    # Tests to verify update change from default {'Unavailable' to 'Available and vice versa}
    # Verify the item created in POST above has the default status
    test_response_get = test_client.get('/v1/menus', headers=token_data)

    assert 'Unavailable' in json.loads(test_response_get.data)['Items found'][0]                                   ['Menu_Availability']
    # Perform an update
    status_update = {"Menu_Availability":"Available"}

    test_response_put = test_client.put('/v1/menu/1', data=json.dumps                                               (status_update),
                                        headers=token_data,                  content_type='application/json')
    
    # Test PUT responses
    assert 'Menu item updated' in json.loads(test_response_put.data)['Response']
    assert test_response_put.status_code == 200

    # Test PUT effect
    test_response_get = test_client.get('/v1/menus', headers=token_data)
    assert 'Available' in json.loads(test_response_get.data)['Items found'][0]                                   ['Menu_Availability']

    # Perform a reverse update
    status_update = {"Menu_Availability":"Unavailable"}

    test_client.put('/v1/menu/1', data=json.dumps(status_update),                               headers=token_data, content_type='application/json')

    # Test reverse PUT effect
    test_response_get = test_client.get('/v1/menus', headers=token_data)
    assert 'Unavailable' in json.loads(test_response_get.data)['Items found'][0]                                      ['Menu_Availability']

def test_menu_delete(test_client):
    ''' Tests the menus DELETE '/v1/menu/<Menu_Id>' test endpoint '''

    # Login user
    token_data = login_helper(test_client)

    # Perform a delete
    test_response_delete = test_client.delete('/v1/menu/1', headers=token_data)
    
    # Confirm DELETE responses
    assert 'Menu item deleted' in json.loads(test_response_delete.data)                                                  ['Response']
    assert test_response_delete.status_code == 200

    # Test DELETE effect
    test_response_get = test_client.get('/v1/menus', headers=token_data)
    assert 'No items found' in json.loads(test_response_get.data)
    assert test_response_get.status_code == 200
    