import zipfile
import os

zip_file_path = os.path.join('data', 'embeddings_2000.zip')
csv_file_path = os.path.join('data', 'embeddings_2000.csv')

if not os.path.exists(csv_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zipf:
        zipf.extract('embeddings_2000.csv', path='data') 
    
    print(f"File {csv_file_path} has been extracted from {zip_file_path}")
else:
    print(f"File {csv_file_path} already exists.")
