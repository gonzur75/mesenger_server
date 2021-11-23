# mesenger_server
A simple application to send messages. 
## General info
This project was created to learn how does postgres, psycopg2, argparse works.
Application have:
database building script --create_db.py
models.py library to manage tables in database using ActiveRecord pattern
users.py application to manage users (lists, create, change password, delete user)
messages.py application to manage messages(list all message to user, sending messages)        

## TECHNOLOGIES
Application is created with:

* Python 3.8
* psycopg2
* argparse
* models library
* clcrypto libray pseudo password hashing library

## Setup
App is using library argparse to mange parameters passed from terminal.
Example of use:
python3 messeges.py --user<USERNAME> --password<PASSWORD> --l


