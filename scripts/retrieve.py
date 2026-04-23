from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant (persistent)
client = QdrantClient(path="qdrant_data")

COLLECTION_NAME = "securebank_docs"


def search(query):
    # Perform a semantic search for the user query
    print(f"\nQuery: {query}")

    # Generate the vector embedding for the query
    query_vector = model.encode(query).tolist()

    # Search in the Qdrant collection
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3
    ).points

    print("\nTop results:\n")

    for i, result in enumerate(results):
        # Print each result with its text content
        print(f"Result {i+1}:")
        print(result.payload["text"])
        print("-" * 50)


if __name__ == "__main__":
    while True:
        # Prompt user for a question
        user_query = input("\nAsk a question (or type 'exit'): ")

        if user_query.lower() == "exit":
            # Exit the loop
            break

        search(user_query)