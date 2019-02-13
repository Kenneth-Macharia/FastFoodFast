''' This module describes the API user-orders models '''

from ..configs import DatabaseSetup


class UserOrdersModel(object):
    ''' This class handles the User Orders model '''

    connection = None
    cursor = None

    @classmethod
    def _init(cls):
        ''' Sets up the database features for this model '''

        # Create a conection object for this model
        UserOrdersModel.connection = DatabaseSetup.database_connection()
        # Create a cursor object for this model
        UserOrdersModel.cursor = UserOrdersModel.connection.cursor()
        # Set up the necessary tables for this model
        DatabaseSetup.database_schema(UserOrdersModel.connection, 'orders')

    @classmethod
    def _destroy(cls):
        ''' Closes the link to the database '''

        UserOrdersModel.cursor.close()
        UserOrdersModel.connection.close()

    @classmethod
    def get_last_order_id(cls):
        ''' Retrieves the last Order_Id from the headers_table '''

        UserOrdersModel._init()

        UserOrdersModel.cursor.execute("SELECT Order_Id FROM                                                   order_headers_table ORDER BY Order_Id                                   DESC LIMIT 1")

        query_result = UserOrdersModel.cursor.fetchone()
        UserOrdersModel._destroy()
        return query_result

    @classmethod
    def insert_order_header(cls, new_order_header):
        ''' Adds a new user order header to the database '''

        UserOrdersModel._init()

        new_order_header_query = """ INSERT INTO order_headers_table (Order_Id,
                                 User_Id, Order_Time, Order_Total, Order_Status)
                                 VALUES (%s, %s, %s, %s, %s); """
                                 
        new_order_header_data = (new_order_header['Order_Id'],
                                 new_order_header['User_Id'],
                                 new_order_header['Order_Time'],
                                 new_order_header['Order_Total'],
                                 new_order_header['Order_Status'])

        UserOrdersModel.cursor.execute(new_order_header_query,                                                 new_order_header_data)

        UserOrdersModel.connection.commit()
        UserOrdersModel._destroy()

    @classmethod
    def insert_order_listing(cls, new_order_list):
        ''' Adds a new user order listing to the database '''

        UserOrdersModel._init()

        new_order_listing_query = """ INSERT INTO order_listing_table
                                  (Order_Id, Order_ItemName, Order_ItemPrice, Order_ItemQty, Order_ItemTotal) VALUES (
                                  %(Order_Id)s, %(Order_ItemName)s, 
                                  %(Order_ItemPrice)s, %(Order_ItemQty)s, 
                                  %(Order_ItemTotal)s); """

        UserOrdersModel.cursor.executemany(new_order_listing_query,                                                new_order_list)

        UserOrdersModel.connection.commit()
        UserOrdersModel._destroy()

    @classmethod
    def get_user_orders(cls, user_id):
        ''' Retrieves a users orders '''

        UserOrdersModel._init()

        UserOrdersModel.cursor.execute(
            "SELECT \
                order_headers_table.Order_Id, order_headers_table.Order_Time, order_headers_table.Order_Total,order_headers_table.Order_Status, order_listing_table.Order_ItemName, order_listing_table.Order_ItemPrice, order_listing_table.Order_ItemQty,order_listing_table.Order_ItemId, order_listing_table.Order_ItemTotal \
            FROM order_headers_table \
            INNER JOIN order_listing_table \
            ON order_listing_table.Order_Id=order_headers_table.Order_Id \
            WHERE order_headers_table.User_Id=%s", (user_id,))

        query_result = UserOrdersModel.cursor.fetchall()

        UserOrdersModel._destroy()
        return query_result

        
class AdminOrdersModel(object):
    ''' This class handles the Admin Orders model '''

    connection = None
    cursor = None

    @classmethod
    def _init(cls):
        ''' Sets up the database features for this model '''

        # Create a conection object for this model
        AdminOrdersModel.connection = DatabaseSetup.database_connection()
        # Create a cursor object for this model
        AdminOrdersModel.cursor = AdminOrdersModel.connection.cursor()
        # Set up the necessary tables for this model
        DatabaseSetup.database_schema(AdminOrdersModel.connection, 'orders')

    @classmethod
    def _destroy(cls):
        ''' Closes the link to the database '''

        AdminOrdersModel.cursor.close()
        AdminOrdersModel.connection.close()

    @classmethod
    def get_all_orders(cls):
        ''' Retrieves all orders '''
        
        AdminOrdersModel._init()

        AdminOrdersModel.cursor.execute(
            "SELECT \
                order_headers_table.Order_Id, users_table.User_Name, order_headers_table.Order_Time, order_headers_table.Order_Total,order_headers_table.Order_Status \
            FROM users_table \
            INNER JOIN order_headers_table \
            ON order_headers_table.User_Id=users_table.User_Id")

        query_result = AdminOrdersModel.cursor.fetchall()
        
        AdminOrdersModel._destroy()
        return query_result

    @classmethod
    def get_one_order_byid(cls, order_id):
        ''' Retrieves an order by it's id '''

        AdminOrdersModel._init()

        AdminOrdersModel.cursor.execute(
            "SELECT \
               order_listing_table.Order_ItemName, order_listing_table.Order_ItemPrice, order_listing_table.Order_ItemQty, order_listing_table.Order_ItemTotal \
            FROM order_headers_table \
            INNER JOIN order_listing_table \
            ON order_listing_table.Order_Id=order_headers_table.Order_Id \
            WHERE order_headers_table.Order_Id=%s", (order_id,))

        query_result = AdminOrdersModel.cursor.fetchall()

        AdminOrdersModel._destroy()
        return query_result

    @classmethod
    def update_order(cls, update_data):
        ''' Updates the order status defined by the order id inputed '''

        AdminOrdersModel._init()

        edit_order_query = """ UPDATE order_headers_table SET
                          Order_Status=%s WHERE Order_Id=%s """

        AdminOrdersModel.cursor.execute(edit_order_query, (update_data['update_status'], update_data['order_id']))

        AdminOrdersModel.connection.commit()
        AdminOrdersModel._destroy()