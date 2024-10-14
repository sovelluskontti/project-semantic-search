import os
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'first_20_movies_noheader.tsv')
df = pd.read_csv(data_path, sep='\t', header=None, names=['id', 'title'])

# Initialize the model (you can use different models like 'all-MiniLM-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for movie titles
print("Generating embeddings...")
embeddings = model.encode(df['title'].tolist(), show_progress_bar=True)

# Store the embeddings along with movie ids
df['embedding'] = list(embeddings)

# Save embeddings to a file (or any other format you need)
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'movie_embeddings.csv')
df.to_csv(output_path, index=False)

print(f"Embeddings saved to {output_path}")
