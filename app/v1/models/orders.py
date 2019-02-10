''' This module describes the API user-orders models '''

from ..configs import DatabaseSetup


class UserOrdersModel(object):
    ''' This class handles the User Orders model '''

    @classmethod
    def get_last_order_id(cls):
        ''' Retrieves the last Order_Id from the headers_table '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        cursor.execute("SELECT Order_Id FROM order_headers_table \
                        ORDER BY Order_Id DESC LIMIT 1")
        query_result = cursor.fetchone()

        cursor.close()
        connection.close()
        return query_result


    @classmethod
    def insert_order_header(cls, new_order_header):
        ''' Adds a new user order header to the database '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        new_order_header_query = """ INSERT INTO order_headers_table (Order_Id,
                                 User_Id, Order_Time, Order_Total, Order_Status)
                                 VALUES (%s, %s, %s, %s, %s); """
                                 
        new_order_header_data = (new_order_header['Order_Id'],
                                 new_order_header['User_Id'],
                                 new_order_header['Order_Time'],
                                 new_order_header['Order_Total'],
                                 new_order_header['Order_Status'])

        cursor.execute(new_order_header_query, new_order_header_data)
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def insert_order_listing(cls, new_order_list):
        ''' Adds a new user order listing to the database '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        new_order_listing_query = """ INSERT INTO order_listing_table
                                  (Order_Id, Order_ItemName, Order_ItemPrice, Order_ItemQty, Order_ItemTotal) VALUES (
                                  %(Order_Id)s, %(Order_ItemName)s, 
                                  %(Order_ItemPrice)s, %(Order_ItemQty)s, 
                                  %(Order_ItemTotal)s); """

        cursor.executemany(new_order_listing_query, new_order_list)
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def get_user_orders(cls, user_id):
        ''' Retrieves a users orders '''

        connection = DatabaseSetup.setup('orders')
        cursor = connection.cursor()

        cursor.execute("SELECT order_headers_table.Order_Id, order_headers_table.Order_Time, order_headers_table.Order_Total,order_headers_table.Order_Status, order_listing_table.Order_ItemName, order_listing_table.Order_ItemPrice, order_listing_table.Order_ItemQty,order_listing_table.Order_ItemId \
        FROM order_headers_table \
        INNER JOIN order_listing_table \
        ON order_listing_table.Order_Id=order_headers_table.Order_Id \
        WHERE order_headers_table.User_Id=%s",(user_id,))

        query_result = cursor.fetchall()

        cursor.close()
        connection.close()
        return query_result

        
