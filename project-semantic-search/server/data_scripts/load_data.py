
import mysql.connector
import csv
import os


conn = mysql.connector.connect(
    host='manticoresearch',
    port=9306,
    user='sarafarahabadi',
    password='Mj@0018238726',
    database='Manticore'
)

cursor = conn.cursor()

sql_insert_commands = []


with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'embeddings.csv'), 'r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:

        id = int(row[0]) 
        title = row[1].replace("'", "\\'")
        embedding_str = row[2]  

        query = "INSERT INTO movies (id, title, embedding) VALUES (%s, '%s', %s)" % (id, title, embedding_str)
        sql_insert_commands.append(query)

for command in sql_insert_commands:
    cursor.execute(command)

conn.commit()

cursor.close()
conn.close()



