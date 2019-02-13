''' This module describes the API user models '''

from passlib.hash import pbkdf2_sha256 as sha256
from ..configs import DatabaseSetup


class UserModel(object):
    ''' This class handles the User model '''

    connection = None
    cursor = None

    @classmethod
    def _init(cls):
        ''' Sets up the database features for this model '''

        # Create a conection object for this model
        UserModel.connection = DatabaseSetup.database_connection()
        # Create a cursor object for this model
        UserModel.cursor = UserModel.connection.cursor()
        # Set up the necessary tables for this model
        DatabaseSetup.database_schema(UserModel.connection, 'users')

    @classmethod
    def _destroy(cls):
        ''' Closes the link to the database '''

        UserModel.cursor.close()
        UserModel.connection.close()

    @classmethod
    def insert_user(cls, new_user):
        ''' Adds a new user to the database '''

        UserModel._init()

        new_user_query = """ INSERT INTO users_table (User_Name, User_Password,
        User_Email, User_Type) VALUES (%s, %s, %s, %s); """
        
        new_user_data = (new_user['User_Name'], new_user['User_Password'], 
                         new_user['User_Email'], new_user['User_Type'])
        UserModel.cursor.execute(new_user_query, new_user_data)

        UserModel.connection.commit()
        UserModel._destroy()

    @classmethod
    def find_user_by_user_email(cls, user_email):
        ''' Finds a user matching the User_Email
        provided as an argument and returend to the autheniticate JWT
        function to generate a token for the user '''

        UserModel._init()

        UserModel.cursor.execute("SELECT User_Id, User_Name, User_Password, \
        User_Email, User_Type FROM users_table WHERE User_Email=%s", (user_email,))
        query_result = UserModel.cursor.fetchone()

        UserModel._destroy()
        return query_result

    @classmethod
    def check_if_admin_exists(cls):
        ''' Checks if a user with the 'Admin' status exist in the database '''

        UserModel._init()

        UserModel.cursor.execute("SELECT User_Email FROM users_table WHERE User_Type=%s", ('Admin',))
        query_result = UserModel.cursor.fetchone()

        UserModel._destroy()
        return query_result

    @classmethod
    def update_user(cls, user_to_update):
        ''' Updates the User_Type '''

        UserModel._init()

        edit_user_query = """ UPDATE users_table SET
                          User_Type=%s WHERE User_Email=%s """

        UserModel.cursor.execute(edit_user_query,
                       (user_to_update['User_Type'],
                        user_to_update['User_Email']))

        UserModel.connection.commit()
        UserModel._destroy()

    @classmethod
    def add_blacklisted_token(cls, jti):
        ''' Adds revoked tokens to the database for cross-checking
        agaist all request tokens, for validity '''

        UserModel._init()

        UserModel.cursor.execute("INSERT INTO token_blacklist_table (Token_jti) VALUES (%s)", (jti,))

        UserModel.connection.commit()
        UserModel._destroy()

    @classmethod
    def is_token_blacklisted(cls, jti):
        ''' Checks all incoming tokens against blacklisted tokens '''

        UserModel._init()

        UserModel.cursor.execute("SELECT * FROM token_blacklist_table WHERE Token_jti=%s", (jti,))
        query_result = UserModel.cursor.fetchone()

        UserModel._destroy()
        return query_result

    @staticmethod
    def generate_hash(password):
        ''' Hashes user passwords '''
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        ''' Verifies hashed user passwords '''
        return sha256.verify(password, hash)
