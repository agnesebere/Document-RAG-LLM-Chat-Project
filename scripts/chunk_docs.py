from pathlib import Path
import json
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


CLEANED_DOCS_DIR = Path("data/cleaned_docs")
CHUNKS_DIR = Path("data/chunks")


def load_text_files():
    # Find all cleaned text files
    text_files = list(CLEANED_DOCS_DIR.glob("*.txt"))
    print(f"Found {len(text_files)} cleaned text files")

    documents = []

    for file_path in text_files:
        # Load each file into a Document object
        print(f"Loading: {file_path.name}")
        text = file_path.read_text(encoding="utf-8")

        doc = Document(
            text=text,
            metadata={
                "source_file": file_path.name,
                "doc_type": "securebank_doc"
            }
        )
        documents.append(doc)

    return documents


def save_chunks(nodes):
    # Create chunks directory if it doesn't exist
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    chunk_data = []
    for i, node in enumerate(nodes):
        # Format each chunk for JSON storage
        chunk = {
            "chunk_id": f"chunk_{i+1}",
            "text": node.text,
            "metadata": node.metadata
        }
        chunk_data.append(chunk)

    output_path = CHUNKS_DIR / "securebank_chunks.json"
    # Write chunks to a JSON file
    output_path.write_text(
        json.dumps(chunk_data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Saved {len(chunk_data)} chunks to {output_path}")


def main():
    # Start the chunking process
    print("Starting chunking process...")

    if not CLEANED_DOCS_DIR.exists():
        # Check if the input directory exists
        print("Error: cleaned_docs folder not found")
        return

    documents = load_text_files()

    if not documents:
        # Check if any documents were loaded
        print("Error: No documents loaded")
        return

    # Split documents into smaller chunks
    splitter = SentenceSplitter(chunk_size=300, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(documents)

    print(f"Created {len(nodes)} chunks")

    # Save the resulting chunks
    save_chunks(nodes)

    print("Chunking complete!")


if __name__ == "__main__":
    main()