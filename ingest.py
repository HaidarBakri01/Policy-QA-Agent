"""
Ingest policy documents into ChromaDB.
"""

import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions


# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#if not OPENAI_API_KEY:
#    raise RuntimeError("OPENAI_API_KEY not found in environment")

# -----------------------------
# Constants
# -----------------------------
DATA_DIR = "./chroma_store"
COLLECTION_NAME = "policy_docs"
FOLDER = "sample_docs"  # relative to project root
COUNTRY_DEFAULT = "GLOBAL"

# -----------------------------
# ChromaDB Setup
# -----------------------------
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

client = chromadb.Client(
    chromadb.config.Settings(persist_directory=DATA_DIR)
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_fn
)

# -----------------------------
# Text Chunking Function
# -----------------------------
def chunk_text(text: str, size: int = 400):
    """Split text into chunks of N words."""
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i+size])

# -----------------------------
# Main Ingestion Loop
# -----------------------------
if __name__ == "__main__":
    if not os.path.exists(FOLDER):
        raise FileNotFoundError(f"Folder '{FOLDER}' not found.")

    for fname in os.listdir(FOLDER):
        file_path = os.path.join(FOLDER, fname)
        if not fname.endswith(".txt"):
            print(f"Skipping non-text file: {fname}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = list(chunk_text(text))

        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            ids.append(f"{fname}_{i}")
            documents.append(chunk)
            metadatas.append({
                "doc_name": fname,
                "page": 1,           # You can customize if you have page info
                "section": "section", # Optional
                "country": COUNTRY_DEFAULT
            })

        # Add chunks to ChromaDB
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        print(f"✅ Ingested '{fname}' with {len(chunks)} chunks")

    print("🎉 All documents ingested into ChromaDB successfully!")
