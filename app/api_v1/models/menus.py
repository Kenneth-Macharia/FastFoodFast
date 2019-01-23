''' This module describes the API menu models '''

from app.api_v1.models.db_setup import DatabaseSetup


class MenuModel(object):
    ''' This class handles the Menu model '''

    @classmethod
    def insert_menu(cls, new_menu):
        ''' Adds a new menu to the database '''

        connection = DatabaseSetup.setup_conn('menus')
        cursor = connection.cursor()

        new_menu_query = """ INSERT INTO menus_table (Name,
                        Description, Image_url, Price, Availability)
                        VALUES (%s,%s, %s, %s, %s); """
        
        new_menu_data = (new_menu['name'], new_menu['description'], 
                         new_menu['img_url'], new_menu['price'], 
                         new_menu['availability'])

        cursor.execute(new_menu_query, new_menu_data)
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def update_menu(cls, menu_to_update):
        ''' Updates the menu availability status '''

        connection = DatabaseSetup.setup_conn('menus')
        cursor = connection.cursor()

        edit_menu_query = """ UPDATE menus_table SET
                          Availability=%s WHERE menu_Id=%s """

        cursor.execute(edit_menu_query,
                       (menu_to_update['availability'],
                        menu_to_update['menu_id']))

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def delete_menu(cls, menu_id):
        ''' Deletes a menu item '''

        connection = DatabaseSetup.setup_conn('menus')
        cursor = connection.cursor()

        delete_menu_query = """ DELETE FROM menus_table WHERE menu_id=%s """
        cursor.execute(delete_menu_query, (menu_id,))

        connection.commit()
        cursor.close()
        connection.close()


class MenusModel(object):
    ''' This class handles the Menus model '''

    @classmethod
    def all_menu_items(cls):
        ''' Retrieves all menus items '''
        
        connection = DatabaseSetup.setup_conn('menus')
        cursor = connection.cursor()

        cursor.execute("SELECT menu_Id, name, Price, Availability FROM menus_table")
        query_result = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return query_result
        