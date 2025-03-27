# import json
# import pymysql

# # File path to JSON data
# json_file = "/app/data/productsList.json"

# # Connect to Manticore
# conn = pymysql.connect(
#     host='manticoresearch',
#     port=9306,
#     user='',
#     password='',
#     database='Manticore'
# )
# cursor = conn.cursor()

# # Load JSON data
# with open(json_file, "r", encoding="utf-8") as f:
#     products = json.load(f)

# # Insert data into Manticore
# for product in products:
#     sql = """
#     INSERT INTO products 
#     (product_id, name, category, manufacturer, description, price, currency, stock, features, average_rating, review_count, warranty, images) 
#     VALUES 
#     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#     """

#     cursor.execute(sql, (
#         product["product_id"],
#         product["name"],
#         product["category"],
#         product["manufacturer"],
#         product["description"],
#         product["price"],
#         product["currency"],
#         product["stock"],
#         json.dumps(product["features"]),  # Convert list to JSON string
#         product["ratings"]["average_rating"],
#         product["ratings"]["review_count"],
#         product["warranty"],
#         json.dumps(product["images"])  # Convert list to JSON string
#     ))

# # Commit and close connection
# conn.commit()
# cursor.close()
# conn.close()

# print("✅ Data inserted into Manticore successfully!")








import mysql.connector
import json
import os

# File path to JSON data
json_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'productsList.json')

# Connect to Manticore
conn = mysql.connector.connect(
    host='manticoresearch',
    port=9306,
    user='',
    password='',
    database='Manticore'
)

cursor = conn.cursor()

# Load JSON data
with open(json_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

# Insert data into Manticore
for product in products:
    # Prepare data to be inserted
    product_id = product["product_id"]
    name = product["name"].replace("'", "\\'")  # Escape single quotes for SQL
    category = product["category"]
    manufacturer = product["manufacturer"]
    description = product["description"].replace("'", "\\'")  # Escape single quotes for SQL
    price = product["price"]
    currency = product["currency"]
    stock = product["stock"]
    features = json.dumps(product["features"])  # Convert list to JSON string
    average_rating = product["ratings"]["average_rating"]
    review_count = product["ratings"]["review_count"]
    warranty = product["warranty"]
    images = json.dumps(product["images"])  # Convert list to JSON string

    # SQL query to insert data into the 'products' table
    query = """
        INSERT INTO products 
        (product_id, name, category, manufacturer, description, price, currency, stock, features, 
        average_rating, review_count, warranty, images) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (
        product_id, name, category, manufacturer, description, price, currency, stock,
        features, average_rating, review_count, warranty, images
    ))

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into Manticore successfully!")
