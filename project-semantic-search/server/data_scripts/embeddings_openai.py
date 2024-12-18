import openai
import pandas as pd
import os
import time
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

openai.api_key = os.getenv('OPENAI_API_KEY')

def test_openai_connection():
    """Test the OpenAI API connection by making a single embedding request."""
    try:
        test_text = "This is a test."
        response = openai.Embedding.create(
            input=test_text,
            model="text-embedding-3-small" 
        )
        embedding = response['data'][0]['embedding']
        print("API connection successful. Test embedding received:")
        print(embedding)
        return True
    except Exception as e:
        print(f"Error testing API connection: {e}")
        return False

def generate_embeddings(input_file, output_file):
    df = pd.read_csv(input_file)

    if df['title'].isnull().any():
        print("Some titles are missing. Please check your input file.")
        return

    embeddings = []
    
    for index, row in df.iterrows():
        title = row['title']
        
        try:
            response = openai.Embedding.create(
                input=title,
                model="text-embedding-3-small" 
            )
            
            embedding = response['data'][0]['embedding']
            embeddings.append(embedding)
            
            if (index + 1) % 10 == 0:
                print(f"Processed {index + 1}/{len(df)} titles.")

            time.sleep(0.2)

        except Exception as e:
            print(f"Error processing movie {title}: {e}")
            embeddings.append(None)  

    df['embedding'] = embeddings

    df.to_csv(output_file, index=False)
    print(f"Embeddings saved to {output_file}")

if __name__ == "__main__":
    if test_openai_connection():
        input_file_path = '/app/data/movies_2000.csv' 
        output_file_path = '/app/data/embeddings_2000.csv' 

        generate_embeddings(input_file_path, output_file_path)
    else:
        print("API connection failed. Please check your API key or network connection.")
