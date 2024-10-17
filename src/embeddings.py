import os
import pandas as pd
from sentence_transformers import SentenceTransformer

# Loading the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'first_20_movies_noheader.tsv')
df = pd.read_csv(data_path, sep='\t', header=None, names=['id', 'title'])

# Initializing the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generating embeddings for movie titles
print("Generating embeddings...")
embeddings = model.encode(df['title'].tolist(), show_progress_bar=True)

# Storing the embeddings with movie ids
df['embedding'] = list(embeddings)

# Saving embeddings to a file named "movies_embeddings.csv"
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'movie_embeddings.csv')
df.to_csv(output_path, index=False)

print(f"Embeddings saved to {output_path}")
