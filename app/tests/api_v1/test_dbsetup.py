''' This module sets up the test databse for test runs '''

from app.api_v1.models.db_setup import DatabaseSetup


class TestDbSetup(object):

    @classmethod
    def check_database(cls):
        if DatabaseSetup.db == 'devdb':
            assert False, 'Not connected to the test database'

    @classmethod
    def drop_tables(cls, request_type):

        connection = DatabaseSetup.connection
        cursor = connection.cursor()

        drop_users_table = """ DROP TABLE IF EXISTS users_table """

        drop_menus_table = """ DROP TABLE IF EXISTS menus_table """

        drop_order_headers_table = """ DROP TABLE IF EXISTS order_headers_table """

        drop_order_listing_table = """ DROP TABLE IF EXISTS order_listing_table """

        if request_type == 'users':
            cursor.execute(drop_users_table)

        elif request_type == 'menus':
            cursor.execute(drop_menus_table)

        elif request_type == 'orders':
            cursor.execute(drop_order_headers_table)
            cursor.execute(drop_order_listing_table)

        connection.commit()
