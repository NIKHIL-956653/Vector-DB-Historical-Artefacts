from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    """Convert text to vector embedding"""
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding

def get_embeddings_batch(texts: list) -> np.ndarray:
    """Convert multiple texts to embeddings at once"""
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

if __name__ == "__main__":
    # Test it
    text1 = "JWT authentication and login system"
    text2 = "User login with tokens and sessions"
    text3 = "How to cook biryani"

    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    emb3 = get_embedding(text3)

    # Calculate similarity
    from numpy.linalg import norm
    
    sim_12 = np.dot(emb1, emb2) / (norm(emb1) * norm(emb2))
    sim_13 = np.dot(emb1, emb3) / (norm(emb1) * norm(emb3))

    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Text 3: {text3}")
    print(f"\nSimilarity 1-2 (should be HIGH): {sim_12:.4f}")
    print(f"Similarity 1-3 (should be LOW):  {sim_13:.4f}")