''' This module defines the menu resources exposed by the API '''

from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_claims)
from ..models.menus import MenuModel, MenusModel


class AddMenu(Resource):
    ''' This class adds the Menu resource '''

    parser = reqparse.RequestParser()

    @jwt_required
    def post(self):
        ''' This function handles POST requests to the
        '/menu'route and controls creation of a new menu. '''

        if get_jwt_claims()['User_Type'] != 'Admin':
            return {'Response':{'Failure':'This is an admin only function'}}, 401

        AddMenu.parser.add_argument('Menu_Name', type=str, required=True,
                                    help='This field cant be left blank!')
        AddMenu.parser.add_argument('Menu_Description', type=str,
                                    required=True, help='This field cant be \
                                    left blank!')
        AddMenu.parser.add_argument('Menu_ImageURL', type=str, required=True,
                                    help='This field cant be left blank!')
        AddMenu.parser.add_argument('Menu_Price', type=int, required=True,
                                    help='This field cant be left blank!')

        json_payload = AddMenu.parser.parse_args()

        menu_to_add = {'Menu_Name':json_payload['Menu_Name'],
                       'Menu_Description':json_payload['Menu_Description'],
                       'Menu_ImageURL': json_payload['Menu_ImageURL'],
                       'Menu_Price':json_payload['Menu_Price'],
                       'Menu_Availability':'Unavailable'}

        response = MenuModel.insert_menu(menu_to_add)

        if response:
            return {'Response':{'Failure':response}}, 400
        return {'Response':{'Success':'Menu item succesfully added'}}, 201


class MenuMgt(Resource):
    ''' This class manages the Menu resource '''

    parser = reqparse.RequestParser()

    @jwt_required
    def put(self, menu_id):
        ''' This function handles PUT requests to the '/menu/<Menu_Id>'
        route '''

        if get_jwt_claims()['User_Type'] != 'Admin':
            return {'Response':{'Failure':'This is an admin only function'}}, 401

        elif not MenuModel.find_menu_byid(menu_id):
            return {'Response':{'Failure':'Menu item not found'}}, 404

        MenuMgt.parser.add_argument('Menu_Availability', type=str,
                                    required=True, help='This field cant be left blank!')

        json_payload = MenuMgt.parser.parse_args()

        menu_to_update = {'Menu_Id':menu_id,
                          'Menu_Availability':json_payload['Menu_Availability']}

        MenuModel.update_menu(menu_to_update)
        return {'Response':{'Success':'Menu item updated'}}, 200

    @jwt_required
    def delete(self, menu_id):
        ''' This function handles DELETE requests to the '/api_v1/menu/<Menu_Id>' route '''

        if get_jwt_claims()['User_Type'] != 'Admin':
            return {'Response':{'Failure':'This is an admin only function'}}, 401

        elif not MenuModel.find_menu_byid(menu_id):
            return {'Response':{'Failure':'Menu item not found'}}, 404

        MenuModel.delete_menu(menu_id)
        return {'Response':{'Success':'Menu item deleted'}}, 200


class Menus(Resource):
    ''' This class manages the Menus resource '''

    def get(self):
        ''' This function handles GET all requests to the '/menus' route '''

        menus = []
        rows_returned = MenusModel.all_menu_items()

        if rows_returned:
            for row in rows_returned:
                menus.append({'Menu_Id':row[0], 'Menu_Name':row[1], 'Menu_Price':row[2], 'Menu_Availability':row[3]})
            return {'Response':{'Success':menus}}, 200
        return {'Response':{'Success':'No menu items found'}}, 200
        