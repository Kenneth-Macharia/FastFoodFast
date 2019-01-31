''' This module describes the API user models '''

from ..configs import DatabaseSetup


class UserModel(object):
    ''' This class handles the User model '''

    @classmethod
    def find_user_by_User_Email(cls, User_Email):
        ''' Finds a user matching the User_Email
        provided as an argument and returend to the autheniticate JWT function to generate a token for the user '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("SELECT User_Id, User_Name, User_Email, User_Type FROM \
        users_table WHERE User_Email=%s", (User_Email,))
        query_result = cursor.fetchone()

        if query_result:
            user = query_result
        else:
            user = None

        cursor.close()
        connection.close()

        return user

    @classmethod
    def find_user_by_User_Id(cls, User_Id):
        ''' Finds a user matching the User_Id provided as an argument and used by th identity JWT function to get the user represented by the token generated '''

        connection = DatabaseSetup.setup('users')
        cursor = connection.cursor()

        cursor.execute("SELECT User_Id, User_Name, User_Email, User_Type FROM \
        users_table WHERE User_Id=%s", (User_Id,))
        query_result = cursor.fetchone()

        if query_result:
            user = query_result
        else:
            user = None

        cursor.close()
        connection.close()

        return user

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