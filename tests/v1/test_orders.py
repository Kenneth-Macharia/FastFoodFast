''' This module contains the TDD code for the users orders
functionality and will test the users, menus and orders modules 
in controllers and models '''

from flask import json
from tests.v1.configs import test_client, drop_tables


# USERS ORDERS TESTS
def login_helper(test_client, user):
    ''' Logs in a user passed in as an argument '''

    response = test_client.post('/v1/auth/login', data=json.dumps(user), content_type='application/json')

    token_data = dict(Authorization="Bearer " + json.loads(response.data)["Access_token"])

    assert response.status_code == 200
    return token_data

def get_helper(test_client, url, token_data):
    ''' Perform the GET/users/menus request on behalf of the test functions '''

    response = test_client.get(url, headers=token_data)
    return response


def test_add_order(test_client):
    ''' Tests the entire add a user order functionality, at the
    route '/users/orders '''

    # Ensure the test database is clean for this test run
    drop_tables('orders')
    drop_tables('menus')

    # Log in the admin to add menu items
    admin_user = {"User_Email":"ken@abc.com",
                  "User_Password":"abc"}

    token_data_admim = login_helper(test_client, admin_user)

        
    # Add items to order
    order_item_1 = {"Menu_Name":"Autumn pumpkin soup", 
                    "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                    "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
                    "Menu_Price":10}

    order_item_2 = {"Menu_Name":"Burger with cheddar and bacon", 
                    "Menu_Description":"An incredibly tasty bacon and blue-cheese stuffed burger. Made using a great American technique, which keeps the patty juicy, it's a sure crowd-pleaser.",
                    "Menu_ImageURL":"C:/website/menus/images/bacon-burger.jpg",
                    "Menu_Price":18}

    test_client.post('/v1/menu', data=json.dumps(order_item_1), headers=token_data_admim, content_type='application/json')
    test_response = test_client.post('/v1/menu', data=json.dumps(order_item_2), headers=token_data_admim, content_type='application/json')

    assert test_response.status_code == 201

    # log in a 'Guest' user to place an order as 'Admin' users can't order
    guest_user = {"User_Email":"shee@xyz.com",
                  "User_Password":"xyz"}

    token_data_guest = login_helper(test_client, guest_user)

    # Fetch the required menu info from HTML via JavaScript
    order_dict = {"current_order": [
        
        {"Order_ItemName":"Chicken breast steak with vegetables",
         "Order_ItemPrice":15,
         "Order_ItemQty":2},
                
        {"Order_ItemName":"Autumn pumpkin soup",
         "Order_ItemPrice":10,
         "Order_ItemQty":3}
            
                                   ]
                 }

        # Test for succesful order creation
    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict), headers=token_data_guest, content_type='application/json')

    assert test_response.status_code == 201
    assert 'Order succesfully added' in json.loads(test_response.data)['Response']['Success']

        # Test for no order details
    order_dict_2 = {}

    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict_2), headers=token_data_guest, content_type='application/json')

    assert test_response.status_code == 400
    assert 'Missing order details' in json.loads(test_response.data)['Response']['Failure']

        # Test an admin can't place an order
    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict), headers=token_data_admim, content_type='application/json')

    assert test_response.status_code == 401
    assert 'This is a Guest only function' in json.loads(test_response.data)['Response']['Failure']

        # Place a second order to test correct order # generation
    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict), headers=token_data_guest, content_type='application/json')
    assert test_response.status_code == 201

def test_get_order(test_client):
    ''' Tests the GET user order functionality, at the route '/user/orders '''

    # Login Admin and try to access a user's orders
    a_user = {"User_Email":"ken@abc.com",
            "User_Password":"abc"}

    token_data = login_helper(test_client, a_user)
    test_response = get_helper(test_client, '/v1/users/orders', token_data)

    assert test_response.status_code == 401
    assert 'This is a Guest only function' in json.loads(test_response.data)['Response']['Failure']

    # Login user to retrive orders for
    user = {"User_Email":"shee@xyz.com",
            "User_Password":"xyz"}

    token_data = login_helper(test_client, user)
        
    # Fetch the user's orders
    test_response = get_helper(test_client, '/v1/users/orders', token_data)

    # Test that the right user orders have been retireved
    assert test_response.status_code == 200
    assert "Shee's orders" in json.loads(test_response.data)['Response']['Success']

    # Test no user order found
    drop_tables('orders')
    test_response = get_helper(test_client, '/v1/users/orders', token_data)
    assert test_response.status_code == 200
    assert "No orders found for Shee" in json.loads(test_response.data)['Response']['Success']


# ADMIN ORDERS TESTS
def test_get_all_order(test_client):
    ''' Tests the GET all orders admin functionality, at the route '/orders '''

    # Log a Guest user
    guest_user = {"User_Email":"shee@xyz.com",
                  "User_Password":"xyz"}

    token_data = login_helper(test_client, guest_user)
    
    # Create an order for the guest (All orders were dropped in previous test)
    order_dict = {"current_order": [

        {"Order_ItemName":"Chicken breast steak with vegetables",
         "Order_ItemPrice":15,
         "Order_ItemQty":2},
                
        {"Order_ItemName":"Autumn pumpkin soup",
         "Order_ItemPrice":10,
         "Order_ItemQty":3}
            
                                   ]
                 }

    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict), headers=token_data, content_type='application/json')

    assert test_response.status_code == 201

    # Test that a 'Guest' can't access this endpoint
    test_response = get_helper(test_client, '/v1/orders', token_data)
    
    assert test_response.status_code == 401
    assert 'This is an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Log in an admin and test for successful orders retrival
    admin_user = {"User_Email":"ken@abc.com",
                  "User_Password":"abc"}

    token_data = login_helper(test_client, admin_user)
    
    test_response = get_helper(test_client, '/v1/orders', token_data)

    assert test_response.status_code == 200
    assert 'Orders found' in json.loads(test_response.data)['Response']['Success']
        # Check respsonse list is not empty
    assert json.loads(test_response.data)['Response']['Success']['Orders found']

    # Test for no orders found
    drop_tables('orders')

    test_response = get_helper(test_client, '/v1/orders', token_data)
    assert test_response.status_code == 200
    assert 'No orders items found' in json.loads(test_response.data)['Response']['Success']

def test_get_order_byid(test_client):
    ''' Tests the GET an order admin functionality, at the route '/orders/<orderId> '''

    # Log in a 'Guest'
    guest_user = {"User_Email":"shee@xyz.com",
                  "User_Password":"xyz"}

    token_data = login_helper(test_client, guest_user)

    # Test they can't access this endpoint
    test_response = get_helper(test_client, '/v1/orders/1', token_data)
    
    assert test_response.status_code == 401
    assert 'This is an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Create an order for the guest (All orders were dropped in previous test)
    order_dict = {"current_order": [

        {"Order_ItemName":"Chicken breast steak with vegetables",
         "Order_ItemPrice":15,
         "Order_ItemQty":2},
                
        {"Order_ItemName":"Autumn pumpkin soup",
         "Order_ItemPrice":10,
         "Order_ItemQty":3}
            
                                   ]
                 }

    test_response = test_client.post('/v1/users/orders', data=json.dumps(order_dict), headers=token_data, content_type='application/json')

    assert test_response.status_code == 201

    # Since orders table had been dropped prior to this test, the above new order will be # 1
    # Log in an 'Admin' and retrieve the user order above using the id saved
    admin_user = {"User_Email":"ken@abc.com",
                  "User_Password":"abc"}

    token_data = login_helper(test_client, admin_user)

    test_response = get_helper(test_client, '/v1/orders/1', token_data)

    # Test for succesful retrival i.e correct order id
    assert test_response.status_code == 200
    assert "Order # 1 found" in json.loads(test_response.data)['Response']['Success']
    assert json.loads(test_response.data)['Response']['Success']["Order # 1 found"]

    # Test for failed retrival
        # No exsisting order # 2
    test_response = get_helper(test_client, '/v1/orders/2', token_data)

    assert test_response.status_code == 404
    assert "Order # 2 does not exist!" in json.loads(test_response.data)['Response']['Failure']

def test_update_order(test_client):
    ''' Tests the PUT an order admin functionality, at the route '/orders/<orderId> '''

    # Log a Guest user and test that they can't access this endpoint
    guest_user = {"User_Email":"shee@xyz.com",
                  "User_Password":"xyz"}

    token_data_guest = login_helper(test_client, guest_user)
    
    test_response = test_client.put('/v1/orders/1', headers=token_data_guest)
    
    assert test_response.status_code == 401
    assert 'This is an admin only function' in json.loads(test_response.data)['Response']['Failure']

    # Log in an 'Admin'
    admin_user = {"User_Email":"ken@abc.com",
                  "User_Password":"abc"}

    token_data_admin = login_helper(test_client, admin_user)

    # Test new orders have the default 'New' status
    test_response = get_helper(test_client, '/v1/users/orders', token_data_guest)

    assert test_response.status_code == 200
    assert json.loads(test_response.data)['Response']['Success']["Shee's orders"][0]['OrderStatus'] == 'New'

    # Test for succesful order status update from the default 'New' to 'Processing'
    status_update = {"Order_Status":"Processing"}
    test_response = test_client.put('/v1/orders/1', headers=token_data_admin, data=json.dumps(status_update), content_type='application/json')

    assert test_response.status_code == 200
    assert 'Order updated' in json.loads(test_response.data)['Response']['Success']

    # Test update effect
    test_response = get_helper(test_client, '/v1/users/orders', token_data_guest)

    assert test_response.status_code == 200
    assert json.loads(test_response.data)['Response']['Success']["Shee's orders"][0]
    ['OrderStatus'] == 'Processing'

    # Test for order not found
    test_response = test_client.put('/v1/orders/10', headers=token_data_admin, data=json.dumps(status_update), content_type='application/json')
    
    assert test_response.status_code == 404
    assert 'Order not found' in json.loads(test_response.data)['Response']['Failure']