import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import json

# Loading the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'first_2000_movies.tsv')  # Update if using a different file
df = pd.read_csv(data_path, sep='\t', header=None, names=['id', 'title'])

# Initializing the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generating embeddings for movie titles
print("Generating embeddings...")
embeddings = model.encode(df['title'].tolist(), show_progress_bar=True)

# Storing the embeddings with movie ids
df['embedding'] = [json.dumps(embedding.tolist(), separators=(',', ':')) for embedding in embeddings]

# Saving embeddings to a file named "movie_embeddings_fixed.csv"
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'initial_embeddings_2000.csv')  # Update output file name
df.to_csv(output_path, index=False)

print(f"Embeddings saved to {output_path}")
