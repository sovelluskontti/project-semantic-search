
import mysql.connector

# Connecting to Manticore
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=9306 
)

if connection.is_connected():
    print("Connection to Manticore successful!")
else:
    print("Connection failed.")
    
connection.close()
