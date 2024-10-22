import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

# Loading the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Loading the movie data with embeddings from the CSV file
csv_path = '/mnt/c/Users/saraf/Desktop/project-semantic-search/data/movie_embeddings_fixed.csv'
movies_df = pd.read_csv(csv_path)

# Converting the 'embedding' column from string to numpy arrays
movies_df['embedding'] = movies_df['embedding'].apply(lambda x: np.array(json.loads(x)))

# Function to perform semantic search
def perform_search(query):
    # Generating the embedding for the search query
    query_embedding = model.encode(query)

    # Calculating cosine similarity between the query embedding and all movie embeddings
    similarities = cosine_similarity([query_embedding], list(movies_df['embedding']))

    # Adding similarity scores to the DataFrame
    movies_df['similarity'] = similarities[0]

    # Sorting the movies by similarity score in descending order
    sorted_movies = movies_df.sort_values(by='similarity', ascending=False)

    # Returning the top 5 most similar movies
    return sorted_movies[['title', 'similarity']].head(5)

# Main function to get user input and perform search
if __name__ == "__main__":
    search_query = input("Enter a search query: ")
    results = perform_search(search_query)

    # Displaying the top 5 most relevant movies
    print("Top 5 relevant movies for your search query:")
    for idx, row in results.iterrows():
        print(f"Movie: {row['title']}, Similarity: {row['similarity']:.4f}")
