import pandas as pd

def convert_ids_in_csv(input_file, output_file):
    # Reading the CSV file
    df = pd.read_csv(input_file)

    # Processing the 'id' column to convert from string to BIGINT
    df['id'] = df['id'].str.replace('tt', '').astype('int64')  # Remove 'tt' and convert to int

    # Saving the modified DataFrame back to a new CSV file named "movies_embeddings_modified.csv"
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file_path = '/mnt/c/Users/saraf/Desktop/project-semantic-search/data/movie_embeddings.csv'
    output_file_path = '/mnt/c/Users/saraf/Desktop/project-semantic-search/data/movie_embeddings_modified.csv'
    
    convert_ids_in_csv(input_file_path, output_file_path)
    print(f'Converted IDs and saved to {output_file_path}')
