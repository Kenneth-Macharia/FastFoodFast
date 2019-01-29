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
        UserOrders.parser.add_argument('order_payload', action='append',                                       required=True, 
                                       help='This field cant be left blank!')
        UserOrders.parser.add_argument('User_Id', type=str,                                                    required=True, help='This field cant \                                  be left blank!')
        # Parse the JOSN payload
        json_payload = UserOrders.parser.parse_args()

        # Compile order listing data
        temp_order_list = (json_payload['order_payload'])
        
        item_dict = {}
        item_no = 0

        # Get the last Order_Id and generate the next one
        returned_row = UserOrdersModel.get_last_order_id()
   
        if returned_row:
            next_order_number = (returned_row[0] + 1)
        else:
            next_order_number = 1

        ordering_user_id = json_payload['User_Id']
        order_list = []

        print(temp_order_list)
        # Create a final order list
        for item in temp_order_list:
            item_dict.update({'Order_Id':(next_order_number)})
            item_dict.update({'Menu_Id':item[item_no]['Menu_Id']})
            item_dict.update({'Order_ItemQty':item[item_no]['Order_ItemQty']})
            item_dict.update({'Order_ItemTotal':item[item_no]['Menu_Price'] *                    item[item_no]['Order_ItemQty']})

            order_list.append(item_dict)
            item_no += 1
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
        order_header.update({'Order_Id':next_order_number})
        order_header.update({'User_Id':ordering_user_id})
        order_header.update({'Order_Time':order_time})
        order_header.update({'Order_Total':order_total})
        order_header.update({'Order_Status':'New'})
        

        # Send order data to the database
        UserOrdersModel.insert_order_listing(order_list)
        UserOrdersModel.insert_order_header(order_header)

        return {'Response':'Order succesfully added'}, 201