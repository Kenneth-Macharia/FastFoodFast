''' This module defines the menu resources exposed by the API '''

import datetime
from flask import request, json
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_claims, get_jwt_identity)
from app.v1.models.orders import UserOrdersModel 
from app.v1.models.users import UserModel


class UserOrders(Resource):
    ''' This class manages the User orders resource '''

    parser = reqparse.RequestParser()

    @jwt_required
    def post(self):
        ''' This function handles POST requests to the
        /v1/users/orders route and controls creation of a user order. '''

        if get_jwt_claims()['User_Type'] == 'Admin':
            return {'Rights Error':'Only Guest users can place orders'}, 401 

        # Get the order details
        request_data = request.get_json()

        if 'current_order' not in request_data.keys():
            return {'Response':"Missing order details"}, 400
            
        current_order = request_data['current_order']
      
         # Get an order id for the current order
        returned_row = UserOrdersModel.get_last_order_id()
        if returned_row:
            order_number = (returned_row[0] + 1)
        else:
            order_number = 1

        # Prepare the order listing
        final_order_list = []  # Final order list
        item_dict = {}  # Dict to populate the final ordr list
     
        for item in current_order:

            item_dict.update({'Order_Id':order_number})
            item_dict.update({'Order_ItemName':item['Order_ItemName']})
            item_dict.update({'Order_ItemPrice':item['Order_ItemPrice']})
            item_dict.update({'Order_ItemQty':item['Order_ItemQty']})
            item_dict.update({'Order_ItemTotal':int(item['Order_ItemPrice'])*
                             int(item['Order_ItemQty'])})

            final_order_list.append(item_dict)
            item_dict = {}

        # Prepare the order header data
            # Get the order time
        order_time = datetime.datetime.now().strftime("%c")

            # Get the user id of the user making placing the order
        user_email = get_jwt_identity()
        user_id = UserModel.find_user_by_user_email(user_email)[0]

            # Set the order status to default 'New' for all new orders,
            # which can later be updated to 'Processing', 'Cancelled' or #'Complete'
        order_status = 'New'

            # Generate an order total
        order_total = 0
        for item in final_order_list:
            order_total += item['Order_ItemTotal']

            # Compile final header dict
        order_header = {}
        order_header.update({'Order_Id':order_number})
        order_header.update({'User_Id':user_id})
        order_header.update({'Order_Time':order_time})
        order_header.update({'Order_Total':order_total})
        order_header.update({'Order_Status':order_status})
        
        # Send order data to the database
        UserOrdersModel.insert_order_header(order_header)
        UserOrdersModel.insert_order_listing(final_order_list)
        
        return {'Response':'Order succesfully added'}, 201

    @jwt_required
    def get(self):
        ''' This function handles GET requests to the
        /v1/users/orders route and controls retireval of a user order. '''

        if get_jwt_claims()['User_Type'] == 'Admin':
            return {'Rights Error':'This is a Guest only feature'}, 401

        user_email = get_jwt_identity()
        user_details = UserModel.find_user_by_user_email(user_email)
        rows_returned = UserOrdersModel.get_user_orders(user_details[0])

        if rows_returned:
            orders = []

            for row in rows_returned:
                start_order_id = row[0]
                temp_list = []

                if start_order_id not in orders['OrderId']:
                    orders.append({'OrderId':row[0], 'OrderTime':str(row[1]), 'OrderTotal':row[2], 'OrderStatus':row[3]})

                for row in rows_returned:
                    next_order_id = row[0]
                    temp_dict = {}

                    if next_order_id != start_order_id and :
                        start_order_id = next_order_id
                        break

                    temp_dict.update({'OrderItem':row[4],                                        'OrderItemPrice':row[5],                                    'OrderItemQty':row[6]})

                    temp_list.append(temp_dict)
                    
                orders.append({'Order {} listing'.format(start_order_id)                  :temp_list})
                    
                                 
                

            return {"{}'s orders".format(user_details[1]):orders}, 200
        return {'Response':'No orders found for {}'.format(user_details[1])},           404
        

class UserOrdersList(Resource):
    ''' This class manages the User orders list resource '''

    @jwt_required
    def get(self):
        ''' This function handles GET requests to the
        /v1/users/orders/list route and controls retireval of a user order listing. '''

        if get_jwt_claims()['User_Type'] == 'Admin':
            return {'Rights Error':'This is a Guest only feature'}, 401
        pass