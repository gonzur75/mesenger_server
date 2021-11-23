import argparse
from models import User
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from clcrypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password(min 8 characters")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")


args = parser.parse_args()


def list_user(cur):
    """
       List the users.
       The function does the following:
           - loads all user with help of User class from models.py
           - for each user prints name
       :param object psycopg2 cursor
       :rtype: print
       :return: prints all user names from users table in database.
       """
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


def create_user(cur, username, password):
    """
     Create user.
           The function does the following:
            - check if provided password is longer than 8 characters.
            - creates new user with username and password provided in param.
            - saves new user to database with psycopg2 cursor

           :param object psycopg2 cursor
           :param string : username
           :param strring: password

           :rtype: print
           :return: prints success or error messages.
           """
    if len(password) < 8:
        print("Password is too short. It should have minimum 8 characters.")
    else:
        try:
            user = User(username, password)
            user.save_to_db(cur)
            print(f"User added to database")
        except UniqueViolation as e:
            print("Error: " + str(e))


def edit_password(cur, username, password, new_pass):
    """
         Edit password .
               The function does the following:
                - check if user exist
                - check if provided password is correct for provided user.
                - check if provided new password is longer than 8 characters.
                - sets new password to user provided in param.
                - saves new password to database with psycopg2 cursor

               :param object psycopg2 cursor
               :param string : username
               :param strring: password
               :param strring: new password

               :rtype: print
               :return: prints success or error messages.
               """
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("New password is too short!")
        else:
            user.hashed_password = new_pass
            print("Setting new password")
            user.save_to_db(cur)
    else:
        print("Wrong password!")


def rm_user(username, password):
    """
        Removes user from database .
           The function does the following:
            - check if user exist
            - check if provided password is correct for provided user.
            - deletes given user.

           :param object psycopg2 cursor
           :param string : username
           :param strring: password
           :param strring: new password

           :rtype: print
           :return: prints success or error messages.
           """

    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User removed from database")
    else:
        print("Wrong password!")


if __name__ == '__main__':
    #  Establishing connection to database
    try:
        cnx = connect(database="messenger_server_db", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        # Logic to deal with incoming parsed arguments
        if args.username and args.password and args.edit and args.new_pass:
            edit_password(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            rm_user(args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_user(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)




