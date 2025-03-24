import json
import pymysql

# File path to JSON data
json_file = "/app/data/productsList.json"

# Connect to Manticore
conn = pymysql.connect(
    host='manticoresearch',
    port=9306,
    user='',
    password='',
    database='Manticore'
)
cursor = conn.cursor()

# Load JSON data
with open(json_file, "r", encoding="utf-8") as f:
    products = json.load(f)

# Insert data into Manticore
for product in products:
    sql = """
    INSERT INTO products 
    (product_id, name, category, manufacturer, description, price, currency, stock, features, average_rating, review_count, warranty, image) 
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.execute(sql, (
        product["product_id"],
        product["name"],
        product["category"],
        product["manufacturer"],
        product["description"],
        product["price"],
        product["currency"],
        product["stock"],
        json.dumps(product["features"]),  # Convert list to JSON string
        product["ratings"]["average_rating"],
        product["ratings"]["review_count"],
        product["warranty"],
        json.dumps(product["images"])  # Convert list to JSON string
    ))

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into Manticore successfully!")
