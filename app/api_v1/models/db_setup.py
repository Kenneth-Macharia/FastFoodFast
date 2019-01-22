''' This module sets up the database for use '''

import os
import psycopg2


class Database_setup(object):
    ''' This class sets up the required database for use '''

    @classmethod
    def setup_conn(cls, request_type):
        ''' Setup the connection to the database '''
        ''' Database configurations set and fetched from the OS '''

        app_env = os.getenv('APP_SETTINGS')
        main_db = os.getenv('DATABASE_URL_MAIN')
        test_db = os.getenv('DATABASE_URL_TEST')
        db_user = os.getenv('DATABASE_USERNAMES')
        db_password = os.getenv('DATABASE_PASSWORDS')

        # Testing code while app is in development, will not be included in the production version
        if app_env == 'testing':
            db_to_connect_to = test_db
        else:
            db_to_connect_to = main_db
        
        connection = psycopg2.connect(user = db_user,
                                    password = db_password,
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = db_to_connect_to)

        # Testing code
        db_configs = {'conn_obj':connection, 'run_env':app_env, 'req_type':request_type}

        Database_setup.setup_tables(db_configs)
        return connection

    @classmethod
    def setup_tables(cls, db_configs):
        ''' Setups up the required database tables '''

        connection = db_configs['conn_obj']
        cursor = connection.cursor()

        # Testing code while app is in development, will not be included in the production version
        if db_configs['run_env'] == 'testing':

            # Drop test tables, before a test run if connected to the test db
            drop_users_table = """ DROP TABLE users_table """
            cursor.execute(drop_users_table)

            drop_menus_table = """ DROP TABLE menus_table """
            cursor.execute(drop_menus_table)

            connection.commit()
            
        # Create tables if they dont exist
        # For testing only they are always re-created
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
        
        # Do not close database connection as the model classes will still use it after this
        if db_configs['req_type'] == 'users':
            cursor.execute(create_users_table)

        elif db_configs['req_type'] == 'menus':
             cursor.execute(create_menus_table)

        elif db_configs['req_type'] == 'orders':
            pass
            # cursor.execute(create_orders_table)

        connection.commit()