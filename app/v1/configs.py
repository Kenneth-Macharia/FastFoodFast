''' This module sets up the main database for use '''

import os
import psycopg2


class DatabaseSetup(object):
    ''' This class sets up the required database for use '''

    db = os.getenv('DATABASE_NAME')
    db_user = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')

    # For testing purposes only, will not be in the final production code
    #TODO:Remove this test code in final prod code
    connection = psycopg2.connect(user=db_user,
                                  password=db_password,
                                  host="127.0.0.1",
                                  port="5432",                                  database=db)

    @classmethod
    def setup(cls, request_type): 
        ''' Setup the database connection and schema '''

        connection = psycopg2.connect(user=DatabaseSetup.db_user,
                                      password=DatabaseSetup.db_password,
                                      host="127.0.0.1",
                                      port="5432",                              database=DatabaseSetup.db)

        cursor = connection.cursor()

        # Create tables if they don't exist, this will be checked before every query to the database is actioned
        create_users_table = """ CREATE TABLE IF NOT EXISTS users_table (

        User_Id             SERIAL PRIMARY KEY,
        User_Name           TEXT NOT NULL,
        User_Password       TEXT NOT NULL,
        User_Email          TEXT UNIQUE NOT NULL,
        User_Type           TEXT NOT NULL

        ) """

        create_token_blacklist_table = """ CREATE TABLE IF NOT EXISTS token_blacklist_table (

        Token_Id            SERIAL PRIMARY KEY,
        Token_jti           TEXT NOT NULL

        ) """

        create_menus_table = """ CREATE TABLE IF NOT EXISTS menus_table (

        Menu_Id             SERIAL PRIMARY KEY,
        Menu_Name           TEXT NOT NULL,
        Menu_Description    TEXT NOT NULL,
        Menu_ImageURL       TEXT UNIQUE NOT NULL,
        Menu_Price          REAL NOT NULL,
        Menu_Availability   TEXT NOT NULL

        ) """
        
        create_order_headers_table = """ CREATE TABLE IF NOT EXISTS order_headers_table (

        Order_Id            INTEGER PRIMARY KEY NOT NULL,
        User_Id             INTEGER REFERENCES users_table(User_Id),
        Order_Time          TIMESTAMP NOT NULL,
        Order_Total         REAL NOT NULL,
        Order_Status        TEXT NOT NULL

        ) """

        create_order_listing_table = """ CREATE TABLE IF NOT EXISTS order_listing_table (

        Order_ItemId        SERIAL PRIMARY KEY,
        Order_Id            INTEGER REFERENCES order_headers_table(Order_Id),
        Menu_Id             INTEGER REFERENCES menus_table(Menu_Id),
        Order_ItemQty       INTEGER NOT NULL,
        Order_ItemTotal     REAL NOT NULL 

        ) """

        # Only run the queries, relating to the request type made
        if request_type == 'users':
            cursor.execute(create_users_table)
            cursor.execute(create_token_blacklist_table)

        elif request_type == 'menus':
            cursor.execute(create_menus_table)

        elif request_type == 'orders':
            cursor.execute(create_order_headers_table)
            cursor.execute(create_order_listing_table)

        connection.commit()
        return connection
