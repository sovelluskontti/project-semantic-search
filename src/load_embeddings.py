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
cursor.execute("SELECT id, title FROM movies LIMIT 2000;")  
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




# import mysql.connector
# import json
# import csv
# import warnings

# warnings.filterwarnings("ignore", category=FutureWarning)

# # Database connection configuration
# db_config = {
#     'user': 'sarafarahabadi',
#     'password': 'Mj@0018238726',
#     'host': 'localhost',
#     'port': 9306,
#     'database': 'Manticore'
# }

# # Connect to the Manticore database
# connection = mysql.connector.connect(**db_config)
# cursor = connection.cursor()

# # Path to your CSV data file
# csv_file_path = '../data/movie_embeddings_fixed.csv'

# # Read the CSV file, processing the first 1000 rows
# with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     rows = [row for idx, row in enumerate(reader) if idx < 1000]

# # Process each row
# for row in rows:
#     try:
#         title = row['title']
#         embedding_json = row['embedding']  # Use the embedding directly

#         # Debugging information
#         print(f"Updating movie with title: '{title}' and embedding: {embedding_json}")

#         # Update the database based on title
#         cursor.execute(
#             "UPDATE movies SET embedding = %s WHERE title = %s;",
#             (embedding_json, title)
#         )

#         # Print the number of affected rows
#         if cursor.rowcount > 0:
#             print(f"Successfully updated movie with title: '{title}'.")
#         else:
#             print(f"No rows updated for movie title: '{title}'.")

#     except Exception as e:
#         print(f"Error processing row {row}: {e}")

# # Commit the changes to the database
# connection.commit()

# # Check the results after the updates (fetch the first 10 entries)
# cursor.execute("SELECT id, title, embedding FROM movies LIMIT 10;")
# updated_rows = cursor.fetchall()
# for row in updated_rows:
#     print(row)

# # Close the database connection
# cursor.close()
# connection.close()

# print("Update process completed.")


