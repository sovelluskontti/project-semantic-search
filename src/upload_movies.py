import mysql.connector

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=9306,  
    user='',    
    password='',
    database='Manticore' 
)

try:
    with connection.cursor() as cursor:

        with open('/mnt/c/Users/saraf/Desktop/project-semantic-search/data/first_2000_movies.tsv', 'r') as f:
            for line in f:
                data = line.strip().split('\t')

                sql = "INSERT INTO movies (id, title) VALUES (%s, %s)"
                cursor.execute(sql, (data[0], data[1]))

    connection.commit()
    print("Data uploaded successfully!")



except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    connection.close()
