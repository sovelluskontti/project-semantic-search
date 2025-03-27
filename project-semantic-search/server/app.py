from flask import Flask, request, jsonify
import pymysql
import os
import openai
import numpy as np
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Establishes a connection to the Manticore Search server."""
    print("Attempting to connect to Manticore Search database...")
    try:
        connection = pymysql.connect(
            host="manticore-search-semantic",
            port=9306,
            user="",
            password="",
            database="Manticore"
        )
        print("Database connection established.")
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

## keyword search 
@app.route('/search', methods=['GET'])
def search_movies():
    """Performs traditional full-text search."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT id, title FROM movies WHERE MATCH(%s) LIMIT 10;"
        cursor.execute(sql, (query,))
        results = cursor.fetchall()
        movies = [{"id": row[0], "title": row[1]} for row in results]
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


## semantic search 
@app.route('/semantic-search', methods=['GET'])
def semantic_search():
    """Performs semantic search using OpenAI embeddings directly."""
    query = request.args.get('query', '')
    print(f"Received query for semantic search: {query}")  

    if not query:
        print("Query parameter is missing.")
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        print(f"Generating embedding for query: {query}")
        response = openai.Embedding.create(
            input=query,
            model="text-embedding-3-small"
        )
        query_embedding = np.array(response['data'][0]['embedding'])
        print(f"Generated embedding: {query_embedding}")

        embedding_str = ','.join(map(str, query_embedding))
        print(f"Embedding formatted for SQL: {embedding_str[:60]}...")

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            sql = f"""
            SELECT title, knn_dist()
            FROM movies
            WHERE knn(embedding, 10, ({embedding_str}));
            """

            print(f"Executing SQL for semantic search: {sql[:120]}...")
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Search results: {results}")

            movies = [{"title": row[0], "similarity": row[1]} for row in results]
            return jsonify(movies)
        except Exception as e:
            print(f"Error during KNN search: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Error generating embedding or connecting to database: {e}")
        return jsonify({"error": str(e)}), 500



# @app.route('/faceted-search', methods=['GET'])
# def faceted_search():
#     """Performs faceted search based on filters, including keyword search."""
#     category = request.args.get('category', '')
#     manufacturer = request.args.get('manufacturer', '')
#     min_price = request.args.get('min_price', '')
#     max_price = request.args.get('max_price', '')
#     search_term = request.args.get('name', '')  # New search term for name and description

#     conditions = []
#     params = []

#     # Apply filters
#     if category:
#         conditions.append("category = %s")
#         params.append(category)
#     if manufacturer:
#         conditions.append("manufacturer = %s")
#         params.append(manufacturer)
#     if min_price:
#         conditions.append("price >= %s")
#         params.append(float(min_price))
#     if max_price:
#         conditions.append("price <= %s")
#         params.append(float(max_price))

#     # Add keyword search for name and description
#     if search_term:
#         conditions.append("MATCH(%s)")
#         params.append(f"@name {search_term} | @description {search_term}")

#     where_clause = " AND ".join(conditions) if conditions else "1=1"
    
#     # Modify the SQL query to include the keyword search
#     sql = f"SELECT product_id, name, category, manufacturer, price, description FROM products WHERE {where_clause} LIMIT 20;"

#     connection = get_db_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(sql, tuple(params))
#         results = cursor.fetchall()
#         products = [{"product_id": row[0], "name": row[1], "category": row[2], "manufacturer": row[3], "price": row[4], "description": row[5]} for row in results]
#         return jsonify(products)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()


@app.route('/faceted-search', methods=['GET'])
def faceted_search():
    """Performs faceted search: first searching by keyword, then applying category and price filters."""
    search_term = request.args.get('name', '')  # First, search by name/description
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')

    conditions = []
    params = []

    # Step 1: Perform full-text search first
    if search_term:
        conditions.append("MATCH(%s)")
        params.append(f"@name {search_term} | @description {search_term}")

    # Step 2: Apply filters only on category and price
    if category:
        conditions.append("category = %s")
        params.append(category)
    if min_price:
        conditions.append("price >= %s")
        params.append(float(min_price))
    if max_price:
        conditions.append("price <= %s")
        params.append(float(max_price))

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    sql = f"""
        SELECT product_id, name, category, manufacturer, price, description 
        FROM products 
        WHERE {where_clause} 
        ORDER BY WEIGHT() DESC
        LIMIT 20;
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, tuple(params))
        results = cursor.fetchall()
        products = [
            {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "manufacturer": row[3],
                "price": row[4],
                "description": row[5],
            }
            for row in results
        ]
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
