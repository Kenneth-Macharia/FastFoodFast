''' This module contains the TDD code for the users orders functionality and will test the users, menus and orders modules in controllers and models '''

from flask import json
from tests.v1.configs import test_client, drop_tables


# def test_add_order(test_client):
#     ''' Tests the entire add a user order functionality, at the route '/users/orders '''

#     # Ensure the test database is clean for this test run
#     drop_tables('orders')
#     drop_tables('menus')
#     drop_tables('users')
        
#     # STEP 1 : Add items to order as all tables have been dropped for this test run at the route '/menu
#     order_item_1 = {"Menu_Name":"Autumn pumpkin soup", 
#                     "Menu_Description":"This lovely autumn pumpkin soup is packed with flavour and perfect for when the nights begin to draw in. Best served with some crusty bread.",
#                     "Menu_ImageURL":"C:/website/menus/images/a_pumkin_soup.jpg",
#                     "Menu_Price":10}

#     order_item_2 = {"Menu_Name":"Burger with cheddar and bacon", 
#                     "Menu_Description":"An incredibly tasty bacon and blue-cheese stuffed burger. Made using a great American technique, which keeps the patty juicy, it's a sure crowd-pleaser.",
#                     "Menu_ImageURL":"C:/website/menus/images/bacon-burger.jpg",
#                     "Menu_Price":18}

#     test_client.post('/v1/menu', data=json.dumps(order_item_1),                                  content_type='application/json')
#     test_client.post('/v1/menu', data=json.dumps(order_item_2),                                  content_type='application/json')

#     # STEP 2: Verify user is registered at the route '/auth/login/<User_Email> and retrieve their ID, if not found, register them first
#     user_id = 0

#     response_get_user = test_client.get('/v1/auth/login/ken@abc.com')

#         # Test for a 200 response if user is found else register user
#     if response_get_user.status_code == 200:
#         assert 'ken@abc.com' in json.loads(response_get_user.data)                                                 ['User-found']['User_Email']

#         # Save the User_Id of the user placing the order
#         user_id = json.loads(response_get_user.data)                                                 ['User-found']['User_Id']
#     else:
#         # Collect the details of the user attempting to order and register, these will be via JavaScript from an input form modal
#         user_details = {"User_Name":"Ken", "User_Password":"abc"}

#         response_post_user = test_client.post('/v1/auth/signup/ken@abc.com', data=json.dumps(user_details), content_type='application/json')

#         # Test the user was registered successfully
#         assert response_post_user.status_code == 201

#         # Retrieve their details
#         response_get_user = test_client.get('/v1/auth/login/ken@abc.com')
#         assert 'User-found' in json.loads(response_get_user.data)

#         # Save the new user's id
#         user_id = json.loads(response_get_user.data)                                                 ['User-found']['User_Id']

#     # STEP 3: Fetch the required menu info from HTML via JavaScript
#         # User_Id will be queried from the database when user logs in
#         # Menu_Ids saved as #id attributes in the HTML menu_box class
#         # Price saved in the HTML meal_price class
#         # Qty will be collected from input elements on checkout modal

#     order_dict = {"Order": [
#             {
#                 "Menu_Id":1, 
#                 "Menu_Price":10,
#                 "Order_ItemQty":2
#             },
         
#             {
#                 "Menu_Id":2,
#                 "Menu_Price":18,
#                 "Order_ItemQty":3
#             }
#         ],

#         "User_Id":user_id
#     }

#         # POST the order
#     response_post_order = test_client.post('/v1/user/orders', data=json.dumps                                         (order_dict),                                                               content_type='application/json')

#         # Test succesful order creation
#     assert response_post_order.status_code == 201
#     assert 'Order succesfully added' in json.loads(response_get_user.data)                                                     ['Response']

# def test_get_order(test_client):
#     ''' Tests the GET user order functionality, at the route '/user/orders '''

#     # Ensure connection to the test database
#     TestDbSetup.check_database()

#     # Verify user registered so that only their orders are retireved
#  
#     response_get_user = test_client.get('/v1/auth/login/ken@abc.com')

#         # Test for a 200 response if user is found GET their details
#     if response_get_user.status_code == 200:

#         User_Id = json.loads(response_get_user.data)['User-found']['User_Id']
#         User_Name = json.loads(response_get_user.data)['User-found']['User_Name']
        
#         # Use the details above to fetch the users orders
#        
#         response_get_user_orders = test_client.get('/v1/users/orders', data=json.dumps(User_Id), content_type='application/json')

#         # Test that the right user orders have been retireved
#         assert response_get_user_orders.status_code == 200
#         assert json.loads(response_get_user_orders.data)['Orders-found']['User_Name'] == User_Name

#     else:

#         # Test that the user is informed that they are not registered thus have no previous orders
#         assert 'User not found' in json.loads(response_get_user.data)












    





