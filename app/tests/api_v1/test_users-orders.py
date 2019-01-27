''' This module contains the TDD code for the users orders functionality and will test the users, menus and orders modules in controllers and models '''

import datetime
from flask import json
from instance.tests_config import test_client
from test_dbsetup import TestDbSetup


def test_add_order(test_client):
    ''' Tests the entire add a user order functionality, at the route '/users/orders '''

    # Ensure connection to the test database
    TestDbSetup.check_database()

    # Ensure the test database is clean for this test run
    TestDbSetup.drop_tables('users')
    TestDbSetup.drop_tables('menus')
    TestDbSetup.drop_tables('orders')
    
    # STEP 1 : Test order item retrieval, when a user clicks the 'add to cart button on the: GET ONE '/v1/menus/<Menu_Id>' endpoint

        # Add menu items to be ordered
    order_item_1 = {"Menu_Name":"Autumn pumpkin soup", 
                    "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
                    "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
                    "Menu_Price":20}

    order_item_2 = {"Menu_Name":"Burger with cheddar and bacon", 
                    "Menu_Description":"An incredibly tasty bacon and blue-cheese stuffed burger. Made using a great American technique, which keeps the patty juicy, it's a sure crowd-pleaser.",
                    "Menu_ImageURL":"C:/website/menus/images/bacon-burger.jpg",
                    "Menu_Price":18}

    test_client.post('/v1/menu', data=json.dumps(order_item_1),                                  content_type='application/json')
    test_client.post('/v1/menu', data=json.dumps(order_item_2),                                  content_type='application/json')

        # Fetch the items added. Since the tables are new the ids will also have been reset to 1 & 2 for the first tow new items added. These will be used to query for the items from the database at the route '/menus/<Menu_Id>
        #TODO:Add this functionality
    test_response_get_one_1 = test_client.get('/v1/menus/1')
    test_response_get_one_2 = test_client.get('/v1/menus/2')

        # Test the fetch  was a success
    assert test_response_get_one_1.status_code == 200
    assert test_response_get_one_2.status_code == 200

    item_1 = {'Menu_Name':json.loads(test_response_get_one_1.data)                                               ['Items-found'][0]['Menu_Name'],
            'Menu_Price':json.loads(test_response_get_one_1.data)
                               ['Items-found'][0]['Menu_Price'],
            'Menu_Id':json.loads(test_response_get_one_1.data)
                               ['Items-found'][0]['Menu_Id']
            }

    item_2 = {'Menu_Name':json.loads(test_response_get_one_2.data)                                               ['Items-found'][0]['Menu_Name'],
            'Menu_Price':json.loads(test_response_get_one_2.data)
                               ['Items-found'][0]['Menu_Price'],
            'Menu_Id':json.loads(test_response_get_one_1.data)
                               ['Items-found'][0]['Menu_Id']
            }

    assert 'Autumn pumpkin soup' in item_1['Menu_Name']
    assert  item_2['Menu_Price'] == 18

    # STEP 2: Hold the required info in variables when adding to cart and viewing the cart
    item_1_id = item_1['Menu_Id']
    item_2_id = item_2['Menu_Id']
    item_1_Menu_Price = item_1['Menu_Price']
    item_2_Menu_Price = item_2['Menu_Price']
    item_1_qty = 2
    item_2_qty = 2
    item_1_total = item_1_Menu_Price * item_1_qty
    item_2_total = item_2_Menu_Price * item_2_qty

    # STEP 3: Log in a user on checking out the order. Verify user is registered at the route '/auth/login/<User_Email>
    #TODO:Add this functionality
    User_Id = 0
    response_get_user = test_client.get('/v1/auth/login/ken@abc.com')

        # Test for a 200 response if user is found else register user
    if response_get_user.status_code == 200:
        assert 'ken@abc.com' in json.loads(response_get_user.data)                                                 ['User-found']['User_Email']

        # Save the User_Id of the user placing the order
        User_Id = json.loads(response_get_user.data)                                                 ['User-found']['user_Id']
    else:
        # Collect the details of the user attempting to order and register
        user_details = {"User_Name":"Ken", "User_Password":"abc"}

        response_post_user = test_client.post('/v1/auth/signup/ken@abc.com', data=json.dumps(user_details), content_type='application/json')

        # Test the user was registered successfully
        assert response_post_user.status_code == 201

        # Save the new users id
        response_get_user = test_client.get('/v1/auth/login/ken@abc.com')
        User_Id = json.loads(response_get_user.data)                                                 ['User-found']['user_Id']

    # STEP 4: Prepare the order header on order checkout
    order_header = {

        "User_Id": User_Id,
        "Order_Time": datetime.datetime.now().strftime("%c"),
        "Order_Total":(item_1_total + item_2_total),
        "Order_Status":"New"
    }

        # POST the order header
        #TODO:Add this functionality
    response_post_header = test_client.post('/v1/users/orders', data=json.dumps                                         (order_header),                                                             content_type='application/json')

        # Test the POST was successfull
    assert response_post_header.status_code == 201
    
    # STEP 5: Prepare the order listing  
        # GET the order_id from the headers_table, there should only be one result in the JSON format: #TODO:Add this functionality

        # {
        #     "Orders-found": [
        #         "Order_Id":"some-id"
        #         "User_Name":"some-name"
        #         "Order_Total":"some-total"
        #         "Order_Time":"some-time"
        #         "Order_Status":"some-status"
        #     ]
        # }

    order_response = test_client.get('/v1/users/orders')
    
    assert order_response.status_code == 200
    assert json.loads(order_response.data)['Orders-found']['order_total'] ==                      (item_1_total + item_2_total)

    order_id = json.loads(order_response.data)['Order-found']['order_Id']

        # POST the order lists and test they were successfully created
    order_item_1 = {
        
        "Order_Id":order_id,
        "Menu_Id":item_1_id,
        "Order_ItemQty":item_1_qty,
        "order_item_total":item_1_total

    }
    response_post_list = test_client.post('/v1/users/orders', data=json.dumps                                         (order_item_1),                                                              content_type='application/json')
    assert response_post_list.status_code == 201

    order_item_2 = {
        
        "Order_Id":order_id,
        "Menu_Id":item_2_id,
        "Order_ItemQty":item_2_qty,
        "Order_ItemTotal":item_2_total

    }
    response_post_list = test_client.post('/v1/users/orders', data=json.dumps                                         (order_item_2),                                                              content_type='application/json')
    assert response_post_list.status_code == 201

def test_get_order(test_client):
    ''' Tests the GET user order functionality, at the route '/users/orders '''

    # Ensure connection to the test database
    TestDbSetup.check_database()

    # Verify user registered so that only their orders are retireved
    #TODO:Ensure this functionality is added
    response_get_user = test_client.get('/v1/auth/login/ken@abc.com')

        # Test for a 200 response if user is found GET their details
    if response_get_user.status_code == 200:

        User_Id = json.loads(response_get_user.data)['User-found']['User_Id']
        User_Name = json.loads(response_get_user.data)['User-found']['User_Name']
        
        # Use the details above to fetch the users orders
        #TODO:Confirm that a separate resource will not be required for this
        response_get_user_orders = test_client.get('/v1/users/orders', data=json.dumps(User_Id), content_type='application/json')

        # Test that the right user orders have been retireved
        assert response_get_user_orders.status_code == 200
        assert json.loads(response_get_user_orders.data)['Orders-found']['User_Name'] == User_Name

    else:

        # Test that the user is informed that they are not registered thus have no previous orders
        assert 'User not found' in json.loads(response_get_user.data)












    





