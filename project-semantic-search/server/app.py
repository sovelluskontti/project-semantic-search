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


## faceted search
# @app.route('/faceted-search', methods=['GET'])
# def faceted_search():
#     """Performs faceted search: first searching by keyword, then applying category and price filters."""
#     search_term = request.args.get('name', '')  
#     category = request.args.get('category', '')
#     min_price = request.args.get('min_price', '')
#     max_price = request.args.get('max_price', '')
#     in_stock = request.args.get('in_stock', '')

#     conditions = []
#     params = []

#     if search_term:
#         conditions.append("MATCH(%s)")
#         params.append(f"@name {search_term} | @description {search_term}")

#     if category:
#         conditions.append("category = %s")
#         params.append(category)
#     if min_price:
#         conditions.append("price >= %s")
#         params.append(float(min_price))
#     if max_price:
#         conditions.append("price <= %s")
#         params.append(float(max_price))
#     if in_stock == "1": 
#         conditions.append("stock > 0")


#     where_clause = " AND ".join(conditions) if conditions else "1=1"

#     # First query: SELECT products
#     sql_1 = f"""
#         SELECT product_id, name, category, manufacturer, price, stock, description 
#         FROM products 
#         WHERE {where_clause} 
#         ORDER BY WEIGHT() DESC
#         LIMIT 20;
#     """

#     # Second query: SELECT count
#     sql_2 = f"""
#         SELECT COUNT(*) 
#         FROM products 
#         WHERE {where_clause};
#     """

#     # Third query: FACET category
#     sql_3 = f"""
#         FACET category 
#         WHERE {where_clause};
#     """

#     connection = get_db_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(sql_1, tuple(params))
#         results = cursor.fetchall()
#         products = [
#             {
#                 "product_id": row[0],
#                 "name": row[1],
#                 "category": row[2],
#                 "manufacturer": row[3],
#                 "price": row[4],
#                 "stock": row[5],
#                 "description": row[6],
#             }
#             for row in results
#         ]
        
#         # select count
#         cursor.execute(sql_2, tuple(params))
#         total_count = cursor.fetchone()[0]


#         # facet category count
#         cursor.execute(sql_3, tuple(params))
#         facet_results = cursor.fetchall()
#         category_counts = {row[0]: row[1] for row in facet_results}


#         return jsonify({
#             "total_count": total_count,  
#             "products": products,
#             "category_counts": category_counts  

#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cursor.close()
#         connection.close()



@app.route('/faceted-search', methods=['GET'])
def faceted_search():
    """Performs faceted search: First searches by keyword, then applies filters."""
    search_term = request.args.get('name', '')  
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    in_stock = request.args.get('in_stock', '')

    base_conditions = []
    params = []

    if search_term:
        base_conditions.append("MATCH(%s)")
        params.append(f"@name {search_term} | @description {search_term}")

    base_where_clause = " AND ".join(base_conditions) if base_conditions else "1=1"

    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # 1️⃣ **Get category counts from the initial search**
        sql_category_counts = f"""
            SELECT COUNT(*) FROM products WHERE {base_where_clause} FACET category;
        """
        cursor.execute(sql_category_counts, tuple(params))
        cursor.nextset()  # Move to FACET results
        category_counts = {row[0]: row[1] for row in cursor.fetchall()}

        # 2️⃣ **Now apply filters**
        if category:
            base_conditions.append("category = %s")
            params.append(category)
        if min_price:
            base_conditions.append("price >= %s")
            params.append(float(min_price))
        if max_price:
            base_conditions.append("price <= %s")
            params.append(float(max_price))
        if in_stock == "1": 
            base_conditions.append("stock > 0")

        final_where_clause = " AND ".join(base_conditions) if base_conditions else "1=1"

        # 3️⃣ **Get final products after filtering**
        sql_products = f"""
            SELECT product_id, name, category, manufacturer, price, stock, description 
            FROM products 
            WHERE {final_where_clause} 
            ORDER BY WEIGHT() DESC
            LIMIT 20;
        """

        # Second query: SELECT count
        sql_2 = f"""
            SELECT COUNT(*) 
            FROM products 
            WHERE {final_where_clause};
        """


        cursor.execute(sql_products, tuple(params))
        results = cursor.fetchall()

        products = [
            {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "manufacturer": row[3],
                "price": row[4],
                "stock": row[5],
                "description": row[6],
            }
            for row in results if row[0] is not None
        ]



        # select count
        cursor.execute(sql_2, tuple(params))
        total_count = cursor.fetchone()[0]


        return jsonify({
            "total_count": total_count,  
            "products": products,
            "category_counts": category_counts  # ✅ Shows category counts **before filtering**
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




