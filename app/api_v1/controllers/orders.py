''' This module defines the menu resources exposed by the API '''

import datetime
from flask import request, json
from flask_restful import Resource, reqparse
from ..models.orders import UserOrdersModel


class UserOrders(Resource):
    ''' This class adds the User orders resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the
        '/user/orders' route and controls creation of a new user order. '''

        # Collect the temp_order list from JavaScript as JSON, with the items to be ordered and the User_Id as the last item.
        UserOrders.parser.add_argument('Order', action='append',                                               required=True,
                                       help='This field cant be left blank!')
        UserOrders.parser.add_argument('User_Id', type=int,                                                    required=True, help='This field cant                                    be left blank!')

        # Parse the JSON payload
        json_payload = UserOrders.parser.parse_args()
        
        # res = json.loads(json_payload)
        # print(json_payload)

        # print("")
        # print('______________________________')
        # orders = []
       
        # for i in json_payload['Order']:
        #     i.encode(encoding='UTF-8',errors='strict')
        #     orders.append(i)

        # f_order = [unicode(s).encode("utf-8") for s in json_payload['Order']]
        # print(list(f_order))

        # list = [
            
        #     {'Menu_Id': 1, 'Menu_Price': 10, 'Order_ItemQty': 2}, 
        #     {'Menu_Id': 2, 'Menu_Price': 18, 'Order_ItemQty': 3}

        # ]

        # print(list[0]['Menu_Id'])
        # print(json_payload['User_Id'])
        # print(json_payload['Order'])
        # x = json_payload['Order'][0]
        # print(x)

        # mydict = {k: unicode(v).encode("utf-8") for k,v in x.iteritems()}
        # print(mydict['Menu_Id'])


        # Get the last Order_Id and generate the next one
        returned_row = UserOrdersModel.get_last_order_id()

        if returned_row:
            next_order_number = (returned_row[0] + 1)
        else:
            next_order_number = 1

        # Create a final order list
        order_list = []
        item_dict = {}

        for list_index in range(0, len(list)):
            for list_item in list[list_index]:
                item_dict.update({'Order_Id':(next_order_number)})
                item_dict.update({'Menu_Id':list_item['Menu_Id']})
                item_dict.update({'Order_ItemQty':list_item['Order_ItemQty']})
                item_dict.update({'Order_ItemTotal':list_item['Menu_Price']*list_item['Order_ItemQty']})

                order_list.append(item_dict)
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
        ordering_user_id = json_payload['User_Id']

        order_header.update({'Order_Id':next_order_number})
        order_header.update({'User_Id':ordering_user_id})
        order_header.update({'Order_Time':order_time})
        order_header.update({'Order_Total':order_total})
        order_header.update({'Order_Status':'New'})
        
        # Send order data to the database
        UserOrdersModel.insert_order_listing(order_list)
        UserOrdersModel.insert_order_header(order_header)

        return {'Response':'Order succesfully added'}, 201