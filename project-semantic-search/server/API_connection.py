import openai
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_openai_api(query):
    """Check the OpenAI API connection and generate embeddings for a query."""
    try:
        print(f"Testing OpenAI API connection with query: {query}")
        response = openai.Embedding.create(
            input=query,
            model="text-embedding-3-small"
        )
        embedding = np.array(response['data'][0]['embedding'])
        print("Embedding generated successfully!")
        print(f"First 10 dimensions of the embedding: {embedding[:10]}")
        return True
    except Exception as e:
        print(f"Error with OpenAI API connection: {e}")
        return False

if __name__ == "__main__":
    test_query = "example query"
    print("Starting OpenAI API connection check...")
    success = check_openai_api(test_query)
    if success:
        print("OpenAI API connection is working!")
    else:
        print("OpenAI API connection failed.")
