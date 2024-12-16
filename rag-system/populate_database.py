import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embeddings import get_embeddings_function
from langchain_chroma import Chroma

# Constants for database paths and settings
CHROMA_PATH = "chroma"
DATA_PATH = "data"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

def main():
    """
    Main function to handle database reset and populate Chroma with document embeddings.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()

    if args.reset:
        clear_database()

    documents = load_documents()
    if not documents:
        print(f"No documents found in {DATA_PATH}.")
        return

    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    """
    Load PDF documents from the specified data directory.
    """
    try:
        document_loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = document_loader.load()
        print(f"Loaded {len(documents)} documents.")
        return documents
    except Exception as e:
        print(f"Error loading documents: {str(e)}")
        return []

def split_documents(documents: list[Document]):
    """
    Split documents into smaller chunks for embedding.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        print(f"Error splitting documents: {str(e)}")
        return []

def add_to_chroma(chunks: list[Document]):
    """
    Add document chunks to the Chroma database if they don't already exist.
    """
    try:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings_function())
        chunks_with_ids = calculate_chunk_ids(chunks)

        existing_items = db.get(include=["documents"])
        existing_ids = set(existing_items.get("ids", []))

        new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
        if new_chunks:
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            print(f"Added {len(new_chunks)} new chunks.")
        else:
            print("No new documents to add.")
    except Exception as e:
        print(f"Error adding chunks: {str(e)}")

def calculate_chunk_ids(chunks: list[Document]):
    """
    Assign unique IDs to document chunks based on their source and page number.
    """
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", "unknown")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks

def clear_database():
    """
    Clear the Chroma database directory.
    """
    try:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings_function())
        del db  # Release database lock

        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print(f"Cleared database at: {CHROMA_PATH}")
    except Exception as e:
        print(f"Error clearing database: {str(e)}")

if __name__ == "__main__":
    main()
