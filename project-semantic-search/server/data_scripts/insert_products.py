
import mysql.connector
import json
import os

json_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'productsList.json')

conn = mysql.connector.connect(
    host='manticoresearch',
    port=9306,
    user='',
    password='',
    database='Manticore'
)

cursor = conn.cursor()

with open(json_file, 'r', encoding='utf-8') as f:
    products = json.load(f)

for product in products:
    product_id = product["product_id"]
    name = product["name"].replace("'", "\\'")  
    category = product["category"]
    manufacturer = product["manufacturer"]
    description = product["description"].replace("'", "\\'")  
    price = product["price"]
    currency = product["currency"]
    stock = product["stock"]
    features = json.dumps(product["features"]) 
    average_rating = product["ratings"]["average_rating"]
    review_count = product["ratings"]["review_count"]
    warranty = product["warranty"]
    images = json.dumps(product["images"]) 

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

conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into Manticore successfully!")
