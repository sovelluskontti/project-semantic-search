import mysql.connector
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)



# Database connection configuration
db_config = {
    'user': 'sarafarahabadi',
    'password': 'Mj@0018238726',
    'host': 'localhost',
    'port': 9306,
    'database': 'Manticore' 
}

# Connecting to the Manticore database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Loading the model
model = SentenceTransformer('all-MiniLM-L6-v2') 

# Fetching all rows from your table
cursor.execute("SELECT id, title FROM movies;")  
rows = cursor.fetchall()

# Processing each row
for row in rows:
    id, title = row
    # Generating the embedding
    embedding = model.encode(title)  

    if embedding is not None: 
        # Converting to a list, and then to JSON string
        embedding_json = json.dumps(embedding.tolist())  

        # Manual data entering for test
        # try:
        #     cursor.execute(
        #     "UPDATE movies SET embedding = %s WHERE id = %s;", 
        #     (json.dumps([0.1, 0.2, 0.3]), 1)  # Use a valid ID from your table
        #     )
        #     print("Update successful")
        try:
            cursor.execute(
                "UPDATE movies SET embedding = %s WHERE id = %s;", 
                (embedding_json, id)
            )
        except mysql.connector.Error as err:
            print(f"Error updating movie ID {id}: {err}")

# Commiting the changes and closing the connection
connection.commit()
cursor.close()
connection.close()