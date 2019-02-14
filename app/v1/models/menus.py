''' This module describes the API menu models '''

from ..configs import DatabaseSetup


class MenuModel(object):
    ''' This class handles the Menu model '''

    connection = None
    cursor = None

    @classmethod
    def _init(cls):
        ''' Sets up the database features for this model '''

        # Create a conection object for this model
        MenuModel.connection = DatabaseSetup.database_connection()
        # Create a cursor object for this model
        MenuModel.cursor = MenuModel.connection.cursor()
        # Set up the necessary tables for this model
        DatabaseSetup.database_schema(MenuModel.connection, 'menus')

    @classmethod
    def _destroy(cls):
        ''' Closes the link to the database '''

        MenuModel.cursor.close()
        MenuModel.connection.close()

    @classmethod
    def find_menu_byid(cls, menu_id):
        ''' Checks to ensure no duplicate menu image url, a duplicate menu risk '''

        MenuModel._init()
       
        MenuModel.cursor.execute("SELECT Menu_Id, Menu_Name, Menu_ImageURL \
        FROM menus_table WHERE Menu_Id=%s", (menu_id,))
        query_result = MenuModel.cursor.fetchone()

        MenuModel._destroy()
        return query_result

    @classmethod
    def insert_menu(cls, new_menu):
        ''' Adds a new menu to the database '''

        MenuModel._init()

        new_menu_query = """ INSERT INTO menus_table (Menu_Name,
                        Menu_Description, Menu_ImageURL, Menu_Price, Menu_Availability)
                        VALUES (%s,%s, %s, %s, %s); """
        
        new_menu_data = (new_menu['Menu_Name'], new_menu['Menu_Description'], 
                         new_menu['Menu_ImageURL'], new_menu['Menu_Price'], 
                         new_menu['Menu_Availability'])

        try:
            MenuModel.cursor.execute(new_menu_query, new_menu_data)
            MenuModel.connection.commit()
        except:
            return "Menu item appears to already exist, check the menu details"
        
        MenuModel._destroy()

    @classmethod
    def update_menu(cls, menu_to_update):
        ''' Updates the Menu_Availability status '''

        MenuModel._init()

        edit_menu_query = """ UPDATE menus_table SET
                          Menu_Availability=%s WHERE Menu_Id=%s """

        MenuModel.cursor.execute(edit_menu_query,
                                 (menu_to_update['Menu_Availability'],
                                  menu_to_update['Menu_Id']))

        MenuModel.connection.commit()
        MenuModel._destroy()

    @classmethod
    def delete_menu(cls, menu_id):
        ''' Deletes a menu item '''

        MenuModel._init()

        delete_menu_query = """ DELETE FROM menus_table WHERE Menu_Id=%s """
        MenuModel.cursor.execute(delete_menu_query, (menu_id,))

        MenuModel.connection.commit()
        MenuModel._destroy()
        

class MenusModel(object):
    ''' This class handles the Menus model '''

    @classmethod
    def all_menu_items(cls):
        ''' Retrieves all menus items '''
        
        MenuModel._init()

        MenuModel.cursor.execute("SELECT Menu_Id, Menu_Name, Menu_Price, Menu_Availability FROM menus_table")
        query_result = MenuModel.cursor.fetchall()
        
        MenuModel._destroy()
        return query_result
        