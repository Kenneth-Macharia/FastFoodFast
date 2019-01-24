''' This module sets up the main database for use '''

import os
import psycopg2


class DatabaseSetup(object):
    ''' This class sets up the required database for use '''

    db = os.getenv('DATABASE_URL')
    db_user = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')

    # For testing purposes only, will not be in the final production code
    connection = psycopg2.connect(user=db_user,
                                  password=db_password,
                                  host="127.0.0.1",
                                  port="5432",                                  database=db)

    @classmethod
    def setup_conn(cls, request_type):
        ''' Setup the connection to the database '''

        connection = psycopg2.connect(user=DatabaseSetup.db_user,
                                      password=DatabaseSetup.db_password,
                                      host="127.0.0.1",
                                      port="5432",                              database=DatabaseSetup.db)

        cursor = connection.cursor()

        # Create table queries
        create_users_table = """ CREATE TABLE IF NOT EXISTS users_table (
        user_Id     SERIAL PRIMARY KEY,
        Name        TEXT NOT NULL,
        Password    TEXT NOT NULL,
        Email       TEXT UNIQUE NOT NULL,
        Type        TEXT NOT NULL
        ) """
        
        create_menus_table = """ CREATE TABLE IF NOT EXISTS menus_table (
        menu_Id         SERIAL PRIMARY KEY,
        Name            TEXT NOT NULL,
        Description     TEXT NOT NULL,
        Image_url       TEXT UNIQUE NOT NULL,
        Price           INTEGER NOT NULL,
        Availability    TEXT NOT NULL 
        ) """

        # Only run the query, relating to the request type made
        if request_type == 'users':
            cursor.execute(create_users_table)

        elif request_type == 'menus':
            cursor.execute(create_menus_table)

        elif request_type == 'orders':
            cursor.execute(create_orders_table)

        connection.commit()
        return connection
