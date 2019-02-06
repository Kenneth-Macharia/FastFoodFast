''' This module defines the menu resources exposed by the API '''

# import datetime
# from flask import request, json
from flask_restful import Resource, reqparse
# from ..models.orders import UserOrdersModel


class UserOrders(Resource):
    ''' This class adds the User orders resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the
        '/user/orders' route and controls creation of a new user
        order. '''

        # Collect the temp_order list from JavaScript as JSON,
        # with the items to be ordered and the User_Id as the 
        # last item.
        UserOrders.parser.add_argument('Order', action='append',
                                       required=True,
                                       help='This field cant be \
                                       left blank!')
        UserOrders.parser.add_argument('User_Id', type=int,
                                       required=True, 
                                       help='This field cant be \
                                       left blank!')
