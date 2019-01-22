''' This module defines the menu resources exposed by the API '''

from flask_restful import Resource, reqparse
from ..models.menus import Menu_model, Menus_model

    
class Menu(Resource):
    ''' This class manages the Menu resource '''

    parser = reqparse.RequestParser()

    def post(self):
        ''' This function handles POST requests to the '/menu' route and controls creation of a new menu. '''

        Menu.parser.add_argument('name', type=str, required=True, help='This field cant be left blank!')
        Menu.parser.add_argument('description', type=str, required=True, help='This field cant be left blank!')
        Menu.parser.add_argument('img_url', type=str, required=True, help='This field cant be left blank!')
        Menu.parser.add_argument('price', type=int, required=True, help='This field cant be left blank!')

        json_payload = Menu.parser.parse_args()

        menu_to_add = {'name':json_payload['name'],
        'description':json_payload['description'], 
        'img_url': json_payload['img_url'], 'price':json_payload['price'],
        'availability':'unavailble'}

        Menu_model.insert_menu(menu_to_add)
        return {'Response':'Menu item succesfully added'}, 201


class Menus(Resource):
    ''' This class manages the Menus resource '''

    def get(self):
        ''' This function handles GET all requests to the '/menus' route '''

        menus = []
        rows_returned = Menus_model.all_menu_items()

        for row in rows_returned:
            menus.append({'Menu_Id':row[0], 'Name':row[1], 'Price':row[2], 'Availability':row[3]})
        
        return {'All menu items':menus}, 200

