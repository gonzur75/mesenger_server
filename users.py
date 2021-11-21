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
#parser.print_help()

args = parser.parse_args()


def list_user(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


def create_user(cur, username, password):
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
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User removed from database")
    else:
        print("Wrong password!")


if __name__ == '__main__':
    try:
        cnx = connect(database="messenger_server_db", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_password(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            rm_user(args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_user(cursor)
    except OperationalError as err:
        print("Connection Error: ", err)




