import faiss
import numpy as np
from vector_store import load_index
from embeddings import get_embedding

def search_similar(query: str, top_k: int = 3) -> list:
    """Search for most similar documents"""
    
    # Load index
    index, documents = load_index()
    if not index:
        return []

    # Convert query to vector
    query_embedding = get_embedding(query)
    query_embedding = np.array([query_embedding]).astype('float32')

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    # Get results
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            doc = documents[idx]
            results.append({
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "similarity_score": float(1 / (1 + distances[0][i]))
            })

    return results

if __name__ == "__main__":
    # Test searches
    queries = [
        "Build secure login with JWT",
        "Integrate payment system",
        "Send notifications to users"
    ]

    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        results = search_similar(query, top_k=2)
        for r in results:
            print(f"Found: {r['title']} (Score: {r['similarity_score']:.4f})")