''' This module defines the menu resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.menus import MenuModel, MenusModel


class AddMenu(Resource):
    ''' This class manages the AddMenu resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the
        '/menu'route and controls creation of a new menu. '''

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

        MenuModel.insert_menu(menu_to_add)
        return {'Response':'Menu item succesfully added'}, 201

        
class EditMenu(Resource):
    ''' This class manages the AddMenu resource '''

    parser = reqparse.RequestParser()

    def put(self, Menu_Id):
        ''' This function handles PUT requests to the '/menu/<Menu_Id>'
        route '''

        EditMenu.parser.add_argument('Menu_Availability', type=str,
                                 required=True, help='This field cant be left blank!')

        json_payload = EditMenu.parser.parse_args()

        menu_to_update = {'Menu_Id':Menu_Id,
                          'Menu_Availability':json_payload['Menu_Availability']}

        MenuModel.update_menu(menu_to_update)
        return {'Response':'Menu item updated'}, 200

    def delete(self, Menu_Id):
        ''' This function handles DELETE requests to the '/api_v1/menu/<Menu_Id>' route '''

        MenuModel.delete_menu(Menu_Id)
        return {'Response':'Menu item deleted'}, 200


class Menus(Resource):
    ''' This class manages the Menus resource '''

    def get(self):
        ''' This function handles GET all requests to the '/menus' route '''

        menus = []
        rows_returned = MenusModel.all_menu_items()

        if rows_returned:
            for row in rows_returned:
                menus.append({'Menu_Id':row[0], 'Menu_Name':row[1], 'Menu_Price':row[2], 'Menu_Availability':row[3]})
            return {'Items-found':menus}, 200
        return {'No-items-found':menus}, 200