import argparse as argparse
from psycopg2 import connect, OperationalError
from clcrypto import check_password
from models import User, Message


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="usename")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-t", "--too", help="message to .. ",)
parser.add_argument("-s", "--send", help="message text")
parser.add_argument("-l", "--list", help="list all messages",  action="store_true")

args = parser.parse_args()


def list_messages(cur, username, password):
    user = User.load_user_by_name(cursor, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        messages = Message.load_all_messages(cur)
        if messages:
            for message in messages:
                print(message)
        else:
            print("No messages!")
    else:
        print("Wrong password!!!")


if __name__ == '__main__':
    try:
        cnx = connect(database="messenger_server_db", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()

        if args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)
    except OperationalError as err:
        print("Connection Error: ", err)

