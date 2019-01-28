''' This module defines the menu resources exposed by the API '''

import datetime
from flask_restful import Resource, reqparse
from ..models.orders import UserOrdersModel


class UserOrders(Resource):
    ''' This class adds the User orders resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the
        '/user/orders' route and controls creation of a new user order. '''

        # Collect the temp_order list from JavaScript as JSON, with the items to be ordered and the User_Id as the last item.
        UserOrders.parser.add_argument('temp_order', type=list, required=True,
                                 help='This field cant be left blank!')
        
        # Compile order listing data
        temp_order_list = UserOrders.parser.parse_args()
        item_dict = {}
        item_no = 0
        order_number = UserOrdersModel.get_last_order_id()[0]
        ordering_user_id = temp_order_list[len(temp_order_list)-1]['User_Id']
        order_list = []

        # Create a final order list
        for item in temp_order_list:
            item_dict.update({'Order_Id':(order_number + 1)})
            item_dict.update({'Menu_Id':item[item_no]['Menu_Id']})
            item_dict.update({'Order_ItemQty':item[item_no]['Order_ItemQty']})
            item_dict.update({'Order_ItemTotal':item[item_no]['Menu_Price'] * item[item_no]['Order_ItemQty']})

            order_list.append(item_dict)
            item_no += 1
            order_number += 1
            item_dict = {}

        # Compile order header data
        order_header = {}
        order_time = datetime.datetime.now().strftime("%c")
        order_total = 0
        item_no = 0

        for item in order_list:
            order_total += item[item_no]['Order_ItemTotal']
            item_no +=1

        # Create order header data
        order_header.update({'User_Id':ordering_user_id})
        order_header.update({'Order_Time':order_time})
        order_header.update({'Order_Total':order_total})
        order_header.update({'Order_Status'}:'New')
        order_header.update({'Order_Id':})

        # Send order data to the database
        UserOrdersModel.insert_order_header(order_header)
        UserOrdersModel.insert_order_listing(order_list)

        return {'Response':'Order header succesfully added'}, 201