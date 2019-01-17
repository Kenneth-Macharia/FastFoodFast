''' This module describes the API user models '''

from app.api_v1.models.db_setup import Db_setup


class User(object):
    ''' This class handles the User model '''

    @classmethod
    def find_user_by_email(cls, email):
        ''' Finds a user matching the email provided as an argument '''
        
        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        get_user_query = "SELECT * FROM users_table WHERE email=?"
        result = cursor.execute(get_user_query, (email,))
        row = result.fetchone()

        connection.close()

        return row

    @classmethod
    def insert_user(cls, new_user):
        ''' Adds a new user to the database '''

        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        new_user_query = "INSERT INTO users_table VALUES (?, ?, ?, ?)"
        cursor.execute(new_user_query, (new_user['name'], \ 
        new_user['password'], new_user['email'], new_user['user_type']))

        connection.commit()
        connection.close()

    @classmethod
    def update_user(cls, user_to_update):
        ''' Updates the user type '''

        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        edit_user_query = "UPDATE users_table SET user_type=? WHERE email=?"
        cursor.execute(edit_user_query,
        (user_to_update['user_type'], user_to_update['email']))

        connection.commit()
        connection.close()

    @classmethod
    def delete_user(cls, email):
        ''' Deletes a user '''

        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        delete_item_query = "DELETE FROM users_table WHERE email=?"
        cursor.execute(delete_item_query, (email,))

        connection.commit()
        connection.close()


class Users(object):
    ''' This class handles the User model '''

    @classmethod
    def all_users(cls):
        ''' Retrieves all users '''
        
        connection = Db_setup.setup_conn()
        cursor = connection.cursor()

        get_all_query = "SELECT * FROM users_table"
        result = cursor.execute(get_all_query)
    
        connection.close()

        return result


    