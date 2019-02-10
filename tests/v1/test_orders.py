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
        
    # Fetch the user's orders
    test_response = test_client.get('/v1/users/orders', headers=token_data)

    # Test that the right user orders have been retireved
    assert test_response.status_code == 200
    assert "Shee's orders" in json.loads(test_response.data)


def test_get_all_order(test_client):
    ''' Tests the GET all orders admin functionality, at the route '/orders '''

    # Log a Guest user and test that they can't access this endpoint
    guest_user = {"User_Email":"shee@xyz.com",
                "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(guest_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])
    
    test_response = test_client.get('/v1/orders', headers=token_data)
    
    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)                                                         ['Rights Error']

    # Log in an admin and test for successful orders retrival
    admin_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(admin_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])
    
    test_response = test_client.get('/v1/orders', headers=token_data)

    assert test_response.status_code == 200
    assert 'Orders found' in json.loads(test_response.data)
        # Check respsonse list is not empty
    assert json.loads(test_response.data)['Orders found']

    # Test for no orders found
    drop_tables('orders')

    test_response = test_client.get('/v1/orders', headers=token_data)
    assert test_response.status_code == 404
    assert 'No orders items found' in json.loads(test_response.data)['Response']

def test_get_order_byid(test_client):
    ''' Tests the GET an order admin functionality, at the route '/orders/<orderId> '''

    # Log in a 'Guest'
    guest_user = {"User_Email":"shee@xyz.com",
                "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(guest_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])

    # Test they can't access this endpoint
    test_response = test_client.get('/v1/orders/1', headers=token_data)
    
    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)                                                         ['Rights Error']

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

    test_response = test_client.post('/v1/users/orders', data=json.dumps                                         (order_dict), headers=token_data_guest,                                     content_type='application/json')

    assert test_response.status_code == 201

    # Fetch the order id for the order created above and save it
    test_response = test_client.get('/v1/users/orders', headers=token_data)
    order_id = json.loads(test_response.data)["Chris's orders"]['OrderId']

    # Log in an 'Admin' and retrieve the user order above using the id saved
    admin_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(admin_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])

    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    # Test for succesful retrival i.e correct order id
    assert test_response.status_code == 200
    assert "Shee's orders" in json.loads(test_response.data)
    assert json.loads(test_response.data)["Shee's orders"]

    # Test for failed retrival
        # No exsisting order
    order_id = 2
    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    assert test_response.status_code == 404
    assert "Order not found, confirm id and try again!" in json.loads(test_response.data)

        #Invalid order id formats
    order_id = 2.1
    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    assert test_response.status_code == 400
    assert "Invalid order ID, confirm id and try again!" in json.loads(test_response.data)

    order_id = '2r'
    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    assert test_response.status_code == 400
    assert "Invalid order ID, confirm id and try again!" in json.loads(test_response.data)

    order_id = '%'
    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    assert test_response.status_code == 400
    assert "Invalid order ID, confirm id and try again!" in json.loads(test_response.data)

    order_id = ''
    test_response = test_client.get('/v1/orders/{}'.format(order_id),                                           headers=token_data)

    assert test_response.status_code == 400
    assert "No order ID inputed!" in json.loads(test_response.data)

def test_update_order(test_client):
    ''' Tests the PUT an order admin functionality, at the route '/orders/<orderId> '''

    # Log a Guest user and test that they can't access this endpoint
    guest_user = {"User_Email":"shee@xyz.com",
                "User_Password":"xyz"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(guest_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])
    
    test_response = test_client.put('/v1/orders/1', headers=token_data)
    
    assert test_response.status_code == 401
    assert 'This an admin only function' in json.loads(test_response.data)                                                         ['Rights Error']

    # Log in an 'Admin'
    admin_user = {"User_Email":"ken@abc.com",
                "User_Password":"abc"}

    test_response = test_client.post('/v1/auth/login',
                                     data=json.dumps(admin_user),              content_type='application/json')

    assert test_response.status_code == 200
    token_data = dict(Authorization="Bearer " + json.loads(test_response.data)                    ["Access_token"])

    # Test new orders have the default 'New' status
    test_response = test_client.get('/v1/orders/1',                                                              headers=token_data)

    assert test_response.status_code == 200
    assert json.loads(test_response.data)["Chris's orders"]
    ['OrderStatus'] == 'New'

    # Test for succesful order status update from the default 'New' to 'Processing'
    # This feature will be via input buttons thus an invalid status can't be set
    # Check that a status value has been supplied will also be enforced by the button status, one of the buttons must be selected by default.
    status_update = 'Processing'
    test_response = test_client.put('/v1/orders/1', headers=token_data,                                         data=json.dumps(status_update),                                             content_type='application/json')

    assert test_response.status_code == 200
    assert 'Order updated' in json.loads(test_response.data)['Response']

    # Test update effect
    test_response = test_client.get('/v1/orders/1',                                                              headers=token_data)

    assert test_response.status_code == 200
    assert json.loads(test_response.data)["Shee's orders"]
    ['OrderStatus'] == 'Processing'
    