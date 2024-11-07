import os
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load the dataset
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'first_2000_movies.tsv')
df = pd.read_csv(data_path, sep='\t', header=None, names=['id', 'title'])

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for movie titles
print("Generating embeddings...")
embeddings = model.encode(df['title'].tolist(), show_progress_bar=True)

# Format embeddings with () 
df['embedding'] = [f"({', '.join(f'{x:.8f}' for x in emb)})" for emb in embeddings]

# Save the DataFrame to a new CSV file 
output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'generated_embeddings.csv')
df.to_csv(output_path, index=False, header=True, quoting=0) 

print(f"Embeddings saved to {output_path}")
