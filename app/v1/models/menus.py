''' This module describes the API menu models '''

from ..configs import DatabaseSetup


class MenuModel(object):
    ''' This class handles the Menu model '''

    @classmethod
    def find_menu_byid(cls, menu_id):
        ''' Checks to ensure no duplicate menu image url, a duplicate menu risk '''
        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        cursor.execute("SELECT Menu_Id, Menu_Name, Menu_ImageURL \
        FROM menus_table WHERE Menu_Id=%s", (menu_id,))
        query_result = cursor.fetchone()

        cursor.close()
        connection.close()
        return query_result


    @classmethod
    def insert_menu(cls, new_menu):
        ''' Adds a new menu to the database '''

        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        new_menu_query = """ INSERT INTO menus_table (Menu_Name,
                        Menu_Description, Menu_ImageURL, Menu_Price, Menu_Availability)
                        VALUES (%s,%s, %s, %s, %s); """
        
        new_menu_data = (new_menu['Menu_Name'], new_menu['Menu_Description'], 
                         new_menu['Menu_ImageURL'], new_menu['Menu_Price'], 
                         new_menu['Menu_Availability'])

        try:
            cursor.execute(new_menu_query, new_menu_data)
            connection.commit()
        except:
            return ("Menu item appears to already exist, check the menu details")
        
        cursor.close()
        connection.close()

    @classmethod
    def update_menu(cls, menu_to_update):
        ''' Updates the Menu_Availability status '''

        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        edit_menu_query = """ UPDATE menus_table SET
                          Menu_Availability=%s WHERE Menu_Id=%s """

        cursor.execute(edit_menu_query,
                       (menu_to_update['Menu_Availability'],
                        menu_to_update['Menu_Id']))

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def delete_menu(cls, menu_id):
        ''' Deletes a menu item '''

        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        delete_menu_query = """ DELETE FROM menus_table WHERE Menu_Id=%s """
        cursor.execute(delete_menu_query, (menu_id,))

        connection.commit()
        cursor.close()
        connection.close()


class MenusModel(object):
    ''' This class handles the Menus model '''

    @classmethod
    def all_menu_items(cls):
        ''' Retrieves all menus items '''
        
        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        cursor.execute("SELECT Menu_Id, Menu_Name, Menu_Price, Menu_Availability FROM menus_table")
        query_result = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return query_result
        