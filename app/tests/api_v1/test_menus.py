''' This module contains the test code for the menu functionality and will test the menu modules in controllers and models '''

from flask import json
from instance.tests_config import test_client
from test_dbsetup import TestDbSetup

def test_menus(test_client):
    '''Tests the menus GET ALL '/v1/menus' test endpoint '''

    # Ensure connection to the test database
    TestDbSetup.check_database()

    # Test for no items found
    TestDbSetup.drop_tables('menus')
    test_response1 = test_client.get('/v1/menus')
    assert 'No-items-found' in json.loads(test_response1.data)
    assert test_response1.status_code == 200

    # Test for items found
    Menu_item_to_add = {"name":"Autumn pumpkin soup", 
                        "description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                        "img_url":"C:/website/menus/images/a_pumkin_soup.jpg",
                        "price":20}

    test_client.post('/v1/menu', data=json.dumps(Menu_item_to_add),                                 content_type='application/json')

    test_response2 = test_client.get('/v1/menus')

    assert 'Items-found' in json.loads(test_response2.data)
    assert 'Autumn pumpkin soup' in json.loads(test_response2.data)                                                        ["Items-found"][0]['Name']
    assert json.loads(test_response2.data)["Items-found"][0]['Price'] == 20
    