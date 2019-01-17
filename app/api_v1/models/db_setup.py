''' Thsi module set up the database for use '''

import psycopg2


class Db_setup(object):
    ''' This class sets up the required database for use '''

    @classmethod
    def setup_conn(cls, db_credentials):
        ''' Setup the connection to the database '''

        connection = psycopg2.connect(user = "sysadmin",
                                    password = "pynative@#29",
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "postgres_db")

        return connection

    @classmethod
    def setup_tables(cls):
        ''' Setups up the required database tables '''

        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        #Create users tables with auto incrementing IDs - specify INTEGER & PRIMARY KEY
        # Set up the users table
        create_users_table = "CREATE TABLE IF NOT EXISTS users_table \
        (id INTEGER PRIMARY KEY, name text, password text, email text, \
        user_type text)"
        cursor.execute(create_users_table)

        # Set up the orders table



        # Set up the menu table



        connection.commit()
        connection.close()