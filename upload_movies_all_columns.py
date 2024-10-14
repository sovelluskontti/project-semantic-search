import mysql.connector

# Connect to Manticore
connection = mysql.connector.connect(
    host='127.0.0.1',
    port=9306,
    user='',
    password='',
    database='Manticore'
)

def parse_value(value):
    # Convert '\N' to None
    return None if value == '\\N' else value

try:
    with connection.cursor() as cursor:
        # Read your TSV file
        with open('/mnt/c/Users/saraf/Desktop/Manticore_db/first_20_titles.tsv', 'r') as f:
            header = f.readline().strip().split('\t')  # Read the header
            for line in f:
                data = line.strip().split('\t')

                # Print the data for debugging
                print(data)

                # Prepare your SQL INSERT statement
                sql = """
                INSERT INTO movies (id, title, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                # Insert data, converting '\N' to None for missing values
                cursor.execute(sql, (
                    data[0],  # id
                    parse_value(data[2]),  # title (primaryTitle)
                    parse_value(data[3]),  # originalTitle
                    int(parse_value(data[4])),  # isAdult
                    int(parse_value(data[5])) if data[5] != '\\N' else None,  # startYear
                    int(parse_value(data[6])) if data[6] != '\\N' else None,  # endYear
                    int(parse_value(data[7])) if data[7] != '\\N' else None,  # runtimeMinutes
                    parse_value(data[8])  # genres
                ))

    # Commit the transaction
    connection.commit()
    print("Data uploaded successfully!")

finally:
    connection.close()
