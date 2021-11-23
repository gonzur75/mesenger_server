from clcrypto import hash_password
from psycopg2 import connect


class User:
    """
    A class to represent a User.
    Uses coderslab clcrypto to hash, salt and check passwords.
    Uses psycopg2 library to connect with database.
    Attributes
    ----------
    username : str The variable argument is used to store username.
    password : str The variable argument is used to store password.
    salt : str  The variable argument is used to store salt if provided.
    _id : int The variable argument is used to store user _id,
    """
    def __init__(self, username="", password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        """ id():
            Returns users id."""
        return self._id

    @property
    def hashed_password(self):
        """hashed_password():
            Returns hashed password of the user instance."""
        return self._hashed_password

    def set_password(self, password, salt=None):
        """set_password:
                Adds salt, hashes new password, sets it for user."""
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        """ hashed_password setter:
                Sets new password for user."""
        self.set_password(password)

    def save_to_db(self, cursor):
        """ save_to_db(cursor):
                It saves user to database."""
        if self._id == -1:
            sql = """INSERT INTO users(user_name, hashed_password) VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET user_name=%s, hashed_password=%s WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        """ load_user_by_id:
                Load user by id, from database."""
        sql = "SELECT id, user_name, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_name(cursor, username):
        """ load_user_by_name:
                Load user by name, from database."""
        sql = "SELECT id, user_name, hashed_password FROM users WHERE user_name=%s"
        cursor.execute(sql, (username,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        """load_all_users:
                Load all users, from database."""
        sql = "SELECT id, user_name, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        """delete:
                Delete user from database"""
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    """
      A class to represent a Message.
      Uses coderslab clcryp to check passwords.
      Uses psycopg2 library to connect with database.
      Attributes
      ----------
      from_id : str The variable argument is used to store id of user that send the message.
      to_id : str The variable argument is used to id of user that message is addressed too.
      text : str  The variable argument is used to store message content up to 255 characters.
      _id : int The variable argument is used to store message _id.
      creation_date : The variable argument is used to store time of message creation.
      """
    def __init__(self, from_id="", to_id="", text="", creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        """ id():
                   Returns users id."""
        return self._id

    def save_to_db(self, cursor):
        """ save_to_db(cursor):
                       It saves user to database, using psycopg2 cursor."""
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text) VALUES(%s, %s, %s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self.creation_date = cursor.fetchone()  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE message SET from_id=%s, to_id=%s, text=%s  WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        """load_all_users:
                       Load all users, from database using psycopg2 cursor."""
        messages = []
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s;"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages;"
            cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.text = text
            loaded_message.creation_date = creation_date
            messages.append(loaded_message)
        return messages


if __name__ == "__main__":

    USER = "postgres"
    HOST = "localhost"
    PASSWORD = "coderslab"
    DATABASE = "messenger_server_db"
    cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    user = User.load_user_by_name(cursor, 'Asmith')
    #print(user.id)








