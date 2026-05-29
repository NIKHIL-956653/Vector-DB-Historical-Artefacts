import os
import requests
from dotenv import load_dotenv
from retriever import search_similar

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_with_context(query: str, context_docs: list) -> str:
    
    context = "\n\n".join([
        f"HISTORICAL DOCUMENT [{doc['id']}]:\n{doc['content']}"
        for doc in context_docs
    ])
    
    system_prompt = """You are a senior technical writer.
Use the provided historical documents as context to generate
accurate and consistent technical documentation.
Always reference prior work when relevant."""

    user_prompt = f"""
HISTORICAL CONTEXT FROM VECTOR DB:
{context}

NEW REQUEST:
{query}

Generate a comprehensive technical document 
that builds on the historical context above.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.0-flash-lite-001",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]


def run_pipeline(query: str):
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")

    # Step 1: Search similar docs
    print("\nStep 1: Searching FAISS for similar documents...")
    similar_docs = search_similar(query, top_k=2)
    for doc in similar_docs:
        print(f"Found: {doc['title']} (Score: {doc['similarity_score']:.4f})")

    # Step 2: Generate with context
    print("\nStep 2: Generating document with historical context...")
    document = generate_with_context(query, similar_docs)

    # Step 3: Save output
    filename = f"output_{query[:20].replace(' ', '_')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {query}\n\n")
        f.write(document)

    print(f"\nStep 3: Saved to {filename}")
    print(f"\nGENERATED DOCUMENT (first 500 chars):")
    print("="*60)
    print(document[:500] + "...")
    return document


if __name__ == "__main__":
    run_pipeline("Build a secure login system with JWT tokens")