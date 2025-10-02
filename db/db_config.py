from psycopg2 import pool
from decouple import config

connection = pool.SimpleConnectionPool(1, 30, 
                                       
    dbname = config("DB_NAME"),
    host = config("DB_HOST"),
    user = config("DB_USER"),
    password = config("DB_PASSWORD"),
    port = config("DB_PORT"),
    sslmode = "require"                                       
)

def get_connection():
    return connection.getconn()

def close_connectioin():
    return connection.closeall()