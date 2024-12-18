
import pandas as pd

def convert_ids_in_tsv(input_file, output_file):
    df = pd.read_csv(input_file, sep='\t', header=None, names=['id', 'title'])

    print("Columns in the file:", df.columns)

    df['id'] = df['id'].str.replace('tt', '').astype('int64')

    df.to_csv(output_file, index=False)
    print(f'Converted IDs and saved to {output_file}')

if __name__ == "__main__":
    input_file_path = './data/first_2000_movies.tsv' 
    output_file_path = './data/movies_2000.csv' 
    convert_ids_in_tsv(input_file_path, output_file_path)
