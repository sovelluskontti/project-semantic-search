import mysql.connector
import csv
import os
import ast  

conn = mysql.connector.connect(
    host='manticoresearch',
    port=9306,
    user='',
    password='',
    database='Manticore'
)

cursor = conn.cursor()

input_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'embeddings_100.csv')

with open(input_file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader) 
    
    for row in reader:
        id = int(row[0])
        title = row[1].replace("'", "\\'")  
        embedding_str = row[2].strip() 
        
        if embedding_str.startswith("[") and embedding_str.endswith("]"):
            embedding_str = embedding_str.replace("[", "(").replace("]", ")")
        
        embedding_tuple = ast.literal_eval(embedding_str)
        
        query = """
            INSERT INTO movies (id, title, embedding) 
            VALUES (%s, '%s', %s)
        """ % (id, title, str(embedding_tuple))
        
        cursor.execute(query)

conn.commit()

cursor.close()
conn.close()
