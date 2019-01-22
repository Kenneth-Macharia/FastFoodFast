''' This module describes the API user models '''

from app.api_v1.models.db_setup import Database_setup


class User_model(object):
    ''' This class handles the User model '''

    @classmethod
    def find_user_by_email(cls, email):
        ''' Finds a user matching the email provided as an argument '''
        
        connection = Database_setup.setup_conn()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, email, type FROM users_table WHERE email=%s", (email,))
        query_result = cursor.fetchone()
        cursor.close()
        connection.close()

        return query_result

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
        cursor.close()
        connection.close()