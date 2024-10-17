import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        port=9306 
    )
    return connection
