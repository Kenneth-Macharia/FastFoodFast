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

        UserOrders.parser.add_argument('User_Id', type=str, required=True,
                                 help='This field cant be left blank!')

        json_payload = UserOrders.parser.parse_args()
        order_time = datetime.datetime.now().strftime("%c")

        order_header_to_add = {'User_Id':json_payload['User_Id'],
                              'Order_Time':Order_time,
                              'Order_Total': #TODO: add order_total,
                              'Order_Status':'New'

        UserOrdersModel.insert_order_header(order_header_to_add)
        return {'Response':'Order header succesfully added'}, 201