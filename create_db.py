from psycopg2 import connect, OperationalError, DatabaseError


CREATE_DB = "CREATE DATABASE messenger_server_db;"

CREATE_TB_USERS = """CREATE TABLE users(
                    id serial PRIMARY KEY, 
                    user_name VARCHAR(255) UNIQUE, 
                    hashed_password VARCHAR(80)
                    );
                    """

CREATE_TB_MESSAGES = """CREATE TABLE messages(
                     id serial PRIMARY KEY, 
                     from_id INT REFERENCES users(id) ON DELETE CASCADE , 
                     to_id INT REFERENCES users(id) ON DELETE CASCADE, 
                     creation_date timestamp, text VARCHAR(255)
                     );
"""
USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
DATABASE = "messenger_server_db"
try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_DB)
        print("Data base has been created")
    except DatabaseError as ex:
        print("ERROR " + str(ex))
    cnx.close
except OperationalError as ex:
    print(f"Something went wrong!" + str(ex))

try:
    cnx = connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()
    try:
        cursor.execute(CREATE_TB_USERS)
        print("Added table 'users'")
    except DatabaseError as ex:
        print(f"ERROR: " + str(ex))

    try:
        cursor.execute(CREATE_TB_MESSAGES)
        print("Added table 'messages'")
    except DatabaseError as ex:
        print(f"ERROR: " + str(ex))
    cnx.close()
except OperationalError as ex:
    print(f"Something went wrong!" + str(ex))
















