''' This module describes the API menu models '''

from app.api_v1.models.db_setup import Database_setup


class Menu_model(object):
    ''' This class handles the Menu model '''

    @classmethod
    def insert_menu(cls, new_menu):
        ''' Adds a new menu to the database '''

        connection = Database_setup.setup_conn('menus')
        cursor = connection.cursor()

        new_menu_query = """ INSERT INTO menus_table (Name, Description, Image_url, Price, Availability) VALUES (%s, %s, %s, %s, %s); """

        new_menu_data = (new_menu['name'], new_menu['description'], 
        new_menu['img_url'], new_menu['price'], new_menu['availability'])

        cursor.execute(new_menu_query, new_menu_data)
        connection.commit()
        cursor.close()
        connection.close()