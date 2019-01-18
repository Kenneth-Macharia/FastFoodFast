''' This module describes the API user models '''

from app.api_v1.models.db_setup import Database_setup


class Users_model(object):
    ''' This class handles the User model '''

    @classmethod
    def all_users(cls):
        ''' Retrieves all users '''
        
        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, email, type FROM users_table")
        query_result = cursor.fetchall()
        connection.close()

        return query_result


class User_model(object):
    ''' This class handles the User model '''

    @classmethod
    def find_user_by_email(cls, email):
        ''' Finds a user matching the email provided as an argument '''
        
        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        query_result = cursor.execute(("SELECT id, name, email, type FROM users_table WHERE email=%s"), (email,))
        query_result.fetchall()
        connection.close()
        
        return row

    @classmethod
    def insert_user(cls, new_user):
        ''' Adds a new user to the database '''

        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        new_user_query = """ INSERT INTO users_table (Name, Password, Email, Type) VALUES (%s, %s, %s, %s); """

        new_user_data = (new_user['name'], new_user['password'], 
        new_user['email'], new_user['type'])

        cursor.execute(new_user_query, new_user_data)
        connection.commit()
        connection.close()

    @classmethod
    def update_user(cls, user_to_update):
        ''' Updates the user type '''

        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        edit_user_query = "UPDATE users_table SET user_type=? WHERE email=?"
        cursor.execute(edit_user_query,
        (user_to_update['user_type'], user_to_update['email']))

        connection.commit()
        connection.close()

    @classmethod
    def delete_user(cls, email):
        ''' Deletes a user '''

        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        delete_item_query = "DELETE FROM users_table WHERE email=?"
        cursor.execute(delete_item_query, (email,))

        connection.commit()
        connection.close()

    