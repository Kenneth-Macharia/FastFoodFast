''' This module contains the TDD code for the users orders functionality and will test the users, menus and orders modules in controllers and models '''

from flask import json
from tests.v1.configs import test_client, drop_tables


def test_add_order(test_client):
    ''' Tests the entire add a user order functionality, at the route '/users/orders '''

    # Ensure the test database is clean for this test run
    drop_tables('orders')
    drop_tables('menus')

    # Log in the admin to add menu items
    admin_user = {"User_Email":"ken@abc.com",
            "User_Password":"abc"}
    test_response = test_client.post('/v1/auth/login', data=json.dumps                                          (admin_user),                                                               content_type='application/json')

    assert test_response.status_code == 200
    token_data_admim = dict(Authorization="Bearer " + json.loads                                       (test_response.data)["Access_token"])
        
    # Add items to order
    order_item_1 = {"Menu_Name":"Autumn pumpkin soup", 
                    "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                    "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
                    "Menu_Price":10}

    order_item_2 = {"Menu_Name":"Burger with cheddar and bacon", 
                    "Menu_Description":"An incredibly tasty bacon and blue-cheese stuffed burger. Made using a great American technique, which keeps the patty juicy, it's a sure crowd-pleaser.",
                    "Menu_ImageURL":"C:/website/menus/images/bacon-burger.jpg",
                    "Menu_Price":18}

    test_client.post('/v1/menu', data=json.dumps(order_item_1),                                  headers=token_data_admim, content_type='application/json')
    test_response = test_client.post('/v1/menu', data=json.dumps(order_item_2),                                  headers=token_data_admim,                                                   content_type='application/json')

    assert test_response.status_code == 201

    # log in a 'Guest' user to place an order as 'Admin' users can't order
    guest_user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(guest_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data_guest = dict(Authorization="Bearer " + json.loads                                        (test_response.data)["Access_token"])

    # Fetch the required menu info from HTML via JavaScript
        # Menu_Ids saved as #id attributes in the HTML menu_box class
        # Price saved in the HTML meal_price class
        # Qty will be collected from input elements on checkout modal

    order_dict = {"Current_Order": [
            {
                "Menu_Id":1, 
                "Menu_Price":10,
                "Order_ItemQty":2
            },
         
            {
                "Menu_Id":2,
                "Menu_Price":18,
                "Order_ItemQty":3
            }
        ]
    }

        # Test for succesful order creation
    test_response = test_client.post('/v1/users/orders', data=json.dumps                                         (order_dict), headers=token_data_guest,                                     content_type='application/json')

    assert test_response.status_code == 201
    assert 'Order succesfully added' in json.loads(test_response.data)                                                         ['Response']

        # Test for no order details
    order_dict_2 = {}

    test_response = test_client.post('/v1/users/orders', data=json.dumps                                         (order_dict_2), headers=token_data_guest,                                   content_type='application/json')

    assert test_response.status_code == 400
    assert 'Missing order details' in json.loads(test_response.data)                                                         ['Response']

        # Test an admin can't place an order
    test_response = test_client.post('/v1/users/orders', data=json.dumps                                         (order_dict), headers=token_data_admim,                                     content_type='application/json')

    assert test_response.status_code == 401
    assert 'Only Guest users can place orders' in json.loads(test_response.data)                                                         ['Rights Error']


def test_get_order(test_client):
    ''' Tests the GET user order functionality, at the route '/user/orders '''

    # Login user to retrive orders for
    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])
    
    # User id to retrieve orders for
    user_id = json.loads(test_response.data)['User-found']['User_Id']
        
    # Fetch the user's orders
    test_response = test_client.get('/v1/users/orders', 
                                    data=json.dumps(User_Id), content_type='application/json', headers=token_data)

    # Test that the right user orders have been retireved
    assert test_response.status_code == 200
    assert 'Shee' in json.loads(test_response.data)['User_Name']