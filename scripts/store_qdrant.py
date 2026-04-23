from pathlib import Path
import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

# Paths
CHUNKS_PATH = Path("data/chunks/securebank_chunks.json")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant (persistent local storage on disk)
client = QdrantClient(path="qdrant_data")

COLLECTION_NAME = "securebank_docs"


def create_collection():
    # Recreate the Qdrant collection for SecureBank documents
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,  # embedding size for this model
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
    points = []

    for chunk in chunks:
        # Generate an embedding for each chunk of text
        embedding = model.encode(chunk["text"]).tolist()

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
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