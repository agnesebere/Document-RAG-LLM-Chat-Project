from pathlib import Path
import json
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from mistralai.client import Mistral
import uuid

# Load environment variables
load_dotenv()

# Mistral Client for embeddings
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
EMBED_MODEL = "mistral-embed"

# Paths
CHUNKS_PATH = Path("data/chunks/securebank_chunks.json")

# Connect to Qdrant (Cloud)
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "securebank_docs"


def create_collection():
    # Recreate the Qdrant collection for SecureBank documents
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=1024,  # embedding size for mistral-embed
            distance=Distance.COSINE
        )
    )
    print("Collection created.")


def load_chunks():
    # Load the processed text chunks from the JSON file
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def store_embeddings(chunks):
    # Prepare points to be stored in the vector database
    print("Generating embeddings using Mistral API...")
    
    texts = [chunk["text"] for chunk in chunks]
    
    # Generate embeddings in one batch request
    resp = mistral_client.embeddings.create(model=EMBED_MODEL, inputs=texts)
    embeddings = [item.embedding for item in resp.data]
    
    points = []
    for i, chunk in enumerate(chunks):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embeddings[i],
            payload={
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            }
        )
        points.append(point)

    # Upsert the generated points into the Qdrant collection
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Stored {len(points)} chunks in Qdrant.")


def main():
    # Start the process of storing data in Qdrant
    print("Starting Qdrant storage...")

    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    create_collection()
    store_embeddings(chunks)

    print("Done.")


if __name__ == "__main__":
    main()