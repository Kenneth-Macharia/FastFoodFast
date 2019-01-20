''' This module sets up the database for use '''

import os
import psycopg2
# from .config import env_app_configs


class Database_setup(object):
    ''' This class sets up the required database for use '''

    @classmethod
    def setup_conn(cls):
        ''' Setup the connection to the database '''

        app_env = os.getenv('APP_SETTINGS')
        main_db = os.getenv('DATABASE_URL_MAIN')
        test_db = os.getenv('DATABASE_URL_TEST')
        db_user = os.getenv('DATABASE_USERNAMES')
        db_password = os.getenv('DATABASE_PASSWORDS')

        if app_env == 'testing':
            db_to_connect_to = test_db
        else:
            db_to_connect_to = main_db
        
        connection = psycopg2.connect(user = db_user,
                                    password = db_password,
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = db_to_connect_to)

        db_configs = {'connection_obj':connection, 'app_run_env':app_env}
        Database_setup.setup_tables(db_configs)
        return connection

    @classmethod
    def setup_tables(cls, db_configs):
        ''' Setups up the required database tables '''

        connection = db_configs['connection_obj']
        cursor = connection.cursor()

        #Create users tables with auto incrementing IDs - specify INTEGER & PRIMARY KEY

        if db_configs['app_run_env'] == 'testing':
            ''' For testing purpose, use a test db and refresh (drop and re-create) it before every test run, else check if tables exist before creating them, for development, staging and production purposes '''

            # Drop test tables
            # Users
            drop_users_table = """DROP TABLE users_table"""
            cursor.execute(drop_users_table)

            # Orders


            # Menu



            cursor.execute(drop_users_table)
            connection.commit()
            

        # Check if tables exist and create them if they dont

        # Users
        create_users_table = """ CREATE TABLE IF NOT EXISTS users_table (
        Id          SERIAL PRIMARY KEY,
        Name        TEXT NOT NULL,
        Password    TEXT NOT NULL,
        Email       TEXT UNIQUE NOT NULL,
        Type        TEXT NOT NULL
        ) """

        # Orders


        # Menu


        cursor.execute(create_users_table)
        connection.commit()