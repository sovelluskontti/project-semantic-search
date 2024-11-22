
from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 


def get_db_connection():
    return pymysql.connect(
        host="manticore-search-semantic",  
        port=9306,
        user="",
        password="",  
        database="Manticore"
    )

@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Perform the full-text search
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)