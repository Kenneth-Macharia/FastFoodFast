''' This module describes the API user models '''

from passlib.hash import pbkdf2_sha256 as sha256
from ..configs import DatabaseSetup


class UserModel(object):
    ''' This class handles the User model '''

    @classmethod
    def insert_user(cls, new_user):
        ''' Adds a new user to the database '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        new_user_query = """ INSERT INTO users_table (User_Name, User_Password,
        User_Email, User_Type) VALUES (%s, %s, %s, %s); """
        
        new_user_data = (new_user['User_Name'], new_user['User_Password'], 
                         new_user['User_Email'], new_user['User_Type'])
        cursor.execute(new_user_query, new_user_data)

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def find_user_by_user_email(cls, user_email):
        ''' Finds a user matching the User_Email
        provided as an argument and returend to the autheniticate JWT
        function to generate a token for the user '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("SELECT User_Id, User_Name, User_Password, \
        User_Email, User_Type FROM users_table WHERE User_Email=%s", (user_email,))
        query_result = cursor.fetchone()

        cursor.close()
        connection.close()
        return query_result

    @classmethod
    def check_if_admin_exists(cls):
        ''' Checks if a user with the 'Admin' status exist in the database '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("SELECT User_Email FROM users_table WHERE User_Type=%s", ('Admin',))
        query_result = cursor.fetchone()

        cursor.close()
        connection.close()
        return query_result

    @classmethod
    def update_user(cls, user_to_update):
        ''' Updates the User_Type '''

        connection = DatabaseSetup.setup('menus')
        cursor = connection.cursor()

        edit_user_query = """ UPDATE users_table SET
                          User_Type=%s WHERE User_Email=%s """

        cursor.execute(edit_user_query,
                       (user_to_update['User_Type'],
                        user_to_update['User_Email']))

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def add_blacklisted_token(cls, jti):
        ''' Adds revoked tokens to the database for cross-checking
        agaist all request tokens, for validity '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO token_blacklist_table (Token_jti) VALUES (%s)", (jti,))

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def is_token_blacklisted(cls, jti):
        ''' Checks all incoming tokens against blacklisted tokens '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM token_blacklist_table WHERE Token_jti=%s", (jti,))
        query_result = cursor.fetchone()

        cursor.close()
        connection.close()
        return query_result

    @staticmethod
    def generate_hash(password):
        ''' Hashes user passwords '''
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        ''' Verifies hashed user passwords '''
        return sha256.verify(password, hash)
