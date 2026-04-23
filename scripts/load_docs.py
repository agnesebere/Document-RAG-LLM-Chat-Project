from pathlib import Path
from docx import Document

RAW_DOCS_DIR = Path("data/raw_docs")
CLEANED_DOCS_DIR = Path("data/cleaned_docs")


def extract_text_from_docx(file_path: Path) -> str:
    doc = Document(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def save_cleaned_text(filename: str, text: str) -> None:
    CLEANED_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CLEANED_DOCS_DIR / f"{Path(filename).stem}.txt"
    output_path.write_text(text, encoding="utf-8")


def main():
    # Start document processing
    print("Starting document processing...")

    if not RAW_DOCS_DIR.exists():
        # raw_docs folder not found
        print("Error: raw_docs folder not found")
        return

    docx_files = list(RAW_DOCS_DIR.glob("*.docx"))
    # Found documents
    print(f"Found {len(docx_files)} document(s)")

    if not docx_files:
        # No .docx files found
        print("Error: No .docx files found")
        return

    for file in docx_files:
        # Processing file
        print(f"Processing: {file.name}")
        text = extract_text_from_docx(file)
        save_cleaned_text(file.name, text)
        # Saved file
        print(f"Saved: {file.name}")

    # Done processing all documents
    print("Done processing all documents!")


if __name__ == "__main__":
    main()