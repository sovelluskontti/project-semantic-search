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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
