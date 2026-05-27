import faiss
import numpy as np
import pickle
import os
from embeddings import get_embedding, get_embeddings_batch

# Paths
FAISS_INDEX_PATH = "faiss_index/index.faiss"
DOCUMENTS_PATH = "faiss_index/documents.pkl"

def create_index():
    """Create a new FAISS index"""
    os.makedirs("faiss_index", exist_ok=True)
    dimension = 384  # all-MiniLM-L6-v2 output size
    index = faiss.IndexFlatL2(dimension)
    return index

def save_index(index, documents):
    """Save FAISS index and documents to disk"""
    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(documents, f)
    print(f"Saved {len(documents)} documents to FAISS!")

def load_index():
    """Load existing FAISS index from disk"""
    if not os.path.exists(FAISS_INDEX_PATH):
        print("No existing index found!")
        return None, []
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(DOCUMENTS_PATH, "rb") as f:
        documents = pickle.load(f)
    print(f"Loaded {len(documents)} documents from FAISS!")
    return index, documents

def add_documents(documents: list):
    """Add documents to FAISS index"""
    # Load or create index
    if os.path.exists(FAISS_INDEX_PATH):
        index, existing_docs = load_index()
    else:
        index = create_index()
        existing_docs = []

    # Get embeddings
    texts = [doc["content"] for doc in documents]
    embeddings = get_embeddings_batch(texts)
    embeddings = np.array(embeddings).astype('float32')

    # Add to index
    index.add(embeddings)
    existing_docs.extend(documents)

    # Save
    save_index(index, existing_docs)
    return index, existing_docs

if __name__ == "__main__":
    # Sample historical documents
    sample_docs = [
        {
            "id": "DEMO-1",
            "title": "User Authentication Feature",
            "content": """User Authentication Feature
            Implement secure login system with JWT tokens.
            Technical Details: Use bcrypt for password hashing,
            JWT for session management, role-based access control.
            Implementation: FastAPI endpoints, MongoDB storage."""
        },
        {
            "id": "DEMO-2", 
            "title": "Payment Gateway Integration",
            "content": """Payment Gateway Integration
            Integrate Stripe payment gateway with webhook support.
            Technical Details: Stripe API, webhook handling,
            subscription billing, payment confirmation emails.
            Implementation: FastAPI endpoints, PostgreSQL storage."""
        },
        {
            "id": "DEMO-3",
            "title": "Real-time Notification System",
            "content": """Real-time Notification System
            Build WebSocket based notification system.
            Technical Details: WebSockets, Redis pub/sub,
            push notifications, email alerts.
            Implementation: FastAPI WebSockets, Redis."""
        },
        {
            "id": "DEMO-4",
            "title": "Search and Filter Feature",
            "content": """Search and Filter Feature
            Implement full-text search with filters.
            Technical Details: Elasticsearch, fuzzy search,
            faceted filtering, search suggestions.
            Implementation: Elasticsearch, FastAPI."""
        },
        {
            "id": "DEMO-5",
            "title": "File Upload and Storage",
            "content": """File Upload and Storage System
            Build secure file upload with cloud storage.
            Technical Details: AWS S3, file validation,
            virus scanning, CDN delivery.
            Implementation: FastAPI, AWS S3, boto3."""
        }
    ]

    print("Adding documents to FAISS...")
    index, docs = add_documents(sample_docs)
    print(f"Total documents in index: {index.ntotal}")