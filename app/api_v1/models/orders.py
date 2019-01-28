''' This module describes the API user-orders models '''

from db_setup import DatabaseSetup


class UserOrdersModel(object):
    ''' This class handles the User Orders model '''

    @classmethod
    def insert_order_header(cls, new_order_header):
        ''' Adds a new user order header to the database '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        new_order_header_query = """ INSERT INTO order_headers_table (User_Id,
                                 Order_Time, Order_Total, Order_Status)
                                VALUES (%s, %s, %s, %s); """
        
        new_order_header_data = (new_order_header['User_Id'],                                           new_order_header['Order_Time'],                                         new_order_header['Order_Total'],                                        new_order_header['Order_Status']

        cursor.execute(new_order_header_query, new_order_header_data)
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def insert_order_listing(cls, new_order_listing):
        ''' Adds a new user order listing to the database '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        new_order_header_query = """ INSERT INTO order_listing_table (Order_Id,
                                 Menu_Id, Order_ItemQty, Order_ItemTotal)
                                 VALUES (%s, %s, %s, %s); """
        
        new_order_header_data = (new_order_listing['Order_Id'],                                           new_order_listing['Menu_Id'],              ``                          new_order_listing['Order_Total'],                                       new_order_listing['Order_Status']

        cursor.execute(new_order_header_query, new_order_header_data)
        connection.commit()
        cursor.close()
        connection.close()

