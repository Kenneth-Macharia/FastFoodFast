''' This module defines the menu resources exposed by the API '''

import datetime
from flask import request, json
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_claims)
from app.v1.models.orders import UserOrdersModel 


class UserOrders(Resource):
    ''' This class manages the User orders resource '''

    parser = reqparse.RequestParser()

    @jwt_required
    def post(self):
        ''' This function handles POST requests to the
        /v1/users/orders route and controls creation of a user order. '''

        if get_jwt_claims()['User_Type'] == 'Admin':
            return {'Rights Error':'Only Guest users can place orders'}, 401
        #TODO: Try without reqparse
        # UserOrders.parser.add_argument('Order', action='append',                                               required=True, help='This field \
        #                                cant be left blank!')
        # UserOrders.parser.add_argument('User_Id', type=int,                                                    required=True, help='This field cant                                    be left blank!')

        # order_input = UserOrders.parser.parse_args()
        # order_details = order_input['Order']
        order_details = [
	
                {"Menu_Id":1, "Menu_Price":10, "Order_ItemQty":2},
                {"Menu_Id":2, "Menu_Price":18, "Order_ItemQty":3}
            
        ]

         # Get an order id for the current order
        returned_row = UserOrdersModel.get_last_order_id()
        if returned_row:
            order_number = (returned_row[0] + 1)
        else:
            order_number = 1

        # Prepare the order listing
        final_order_list = []  # Final order list
        item_dict = {}  # Dict to populate the final ordr list
     
        for item in order_details:

            item_dict.update({'Order_Id':order_number})
            item_dict.update({'Menu_Id':item['Menu_Id']})
            item_dict.update({'Order_ItemQty':item['Order_ItemQty']})
            item_dict.update({'Order_ItemTotal':item['Menu_Price']*
                             item['Order_ItemQty']})

            final_order_list.append(item_dict)
            item_dict = {}

        # Prepare the order header data
            # Get the order time
        order_time = datetime.datetime.now().strftime("%c")

            # Get the user id of the user making placing the order
        # user_id = order_input['User_Id']
        user_id = 1 #TODO: How to get the correct user!

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

        pass
        

class UserOrdersList(Resource):
    ''' This class manages the User orders list resource '''

    @jwt_required
    def get(self):
        ''' This function handles GET requests to the
        /v1/users/orders/list route and controls retireval of a user order listing. '''

        if get_jwt_claims()['User_Type'] == 'Admin':
            return {'Rights Error':'This is a Guest only feature'}, 401

        pass