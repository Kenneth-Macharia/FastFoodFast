''' This module defines the menu resources exposed by the API '''

import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_claims, get_jwt_identity)
from app.v1.models.users import UserModel
from app.v1.models.orders import (UserOrdersModel, AdminOrdersModel)


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
        
        # Persist order data to the database
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
        orders = []

        if rows_returned:

            for row in rows_returned:
                orders.append({'OrderId':row[0], 'OrderTime':str(row[1]), 'OrderItemTotal':row[8], 'OrderStatus':row[3], 'OrderItem':row[4], 'OrderItemPrice':row[5], 'OrderItemQty':row[6], 'OrderTotal':row[2]})

            return {"{}'s orders".format(user_details[1]):orders}, 200
        return {'Response':'No orders found for {}'.format(user_details[1])}, 404

    
class AdminOrders(Resource):
    ''' This class manages the Admin orders resource '''

    @jwt_required
    def get(self):
        ''' This function handles GET requests to the
        /v1/orders route and controls retireval of all orders. '''
    
        if get_jwt_claims()['User_Type'] != 'Admin':
                return {'Rights Error':'This an admin only function'}, 401

        orders = []
        rows_returned = AdminOrdersModel.get_all_orders()

        if rows_returned:
            for row in rows_returned:
                orders.append({'OrderId':row[0], 'UserName':row[1], 'OrderTime':str(row[2]), 'OrderItemTotal':row[3], 'OrderStatus':row[4]})

            return {'Orders found':orders}, 200
        return {'Response':'No orders items found'}, 404


class AdminOrder(Resource):
    ''' This class manages the Admin order resource '''

    parser = reqparse.RequestParser()
    parser.add_argument('Order_Status', type=str, required=True,
                        help='This field cant be left blank!')

    @jwt_required
    def get(self, order_id):
        ''' This function handles GET requests to the
        /v1/orders/<order_id> route and controls retireval of an order by order_id.'''

        if get_jwt_claims()['User_Type'] != 'Admin':
            return {'Rights Error':'This an admin only function'}, 401
        
        rows_returned = AdminOrdersModel.get_one_order_byid(order_id)
        order = []

        if rows_returned:
            for row in rows_returned:
                order.append({'OrderItemName':row[0], 'OrderItemPrice':row[1], 'OrderItemQty':row[2], 'OrderItemTotal':row[3]})

            return {'Order # {} found'.format(order_id):order}, 200
        return {'Response':'Order # {} does not exist!'.format(order_id)}, 404

    @jwt_required
    def put(self, order_id):
        ''' This function handles PUT requests to the
        /v1/orders/<order_id> route and controls the updating of an order status. '''
        
        if get_jwt_claims()['User_Type'] != 'Admin':
            return {'Rights Error':'This an admin only function'}, 401

        status_update = AdminOrder.parser.parse_args()['Order_Status']

        order_update_data = {'order_id':order_id, 'update_status':status_update}

        AdminOrdersModel.update_order(order_update_data)
        return {'Response':'Order updated'}, 200