
import mysql.connector

# Try connecting to Manticore
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=9306  # Manticore's default MySQL port
)

if connection.is_connected():
    print("Connection to Manticore successful!")
else:
    print("Connection failed.")
    
connection.close()
