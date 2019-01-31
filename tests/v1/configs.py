''' This module contains tests configurations setup '''

import pytest
from app.v1.main import app
from app.v1.configs import DatabaseSetup


@pytest.fixture
def test_client():
    ''' The test client that will simulate the app behaviour to test '''
    app.config['TESTING'] = True
    return app.test_client()

def drop_tables(request_type):

    connection = DatabaseSetup.connection
    cursor = connection.cursor()

    drop_users_table = """ DROP TABLE IF EXISTS users_table CASCADE """

    drop_menus_table = """ DROP TABLE IF EXISTS menus_table CASCADE """

    drop_order_headers_table = """ DROP TABLE IF EXISTS order_headers_table CASCADE """

    drop_order_listing_table = """ DROP TABLE IF EXISTS order_listing_table CASCADE """

    if request_type == 'users':
        cursor.execute(drop_users_table)

    elif request_type == 'menus':
        cursor.execute(drop_menus_table)

    elif request_type == 'orders':
        cursor.execute(drop_order_headers_table)
        cursor.execute(drop_order_listing_table)

    connection.commit()
