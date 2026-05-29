# Vector DB — Historical Artefacts
### Context-Aware Document Generation using FAISS + Sentence Transformers

A vector database system that stores historical product documents as embeddings
and retrieves the most semantically similar ones to feed into an LLM —
enabling context-aware technical documentation generation.

## What It Does
Old documents stored in FAISS
↓
New request comes in
↓
Convert request to vector (Sentence Transformers)
↓
Search FAISS for similar historical docs
↓
Feed similar docs + request into Gemini AI
↓
AI generates document WITH historical context!
References prior work automatically! ✅

## The Magic — Real Output Example

Query: "Build payment gateway v2 with UPI support"

FAISS Retrieved: DEMO-2 (Stripe Payment Gateway)

Gemini Generated:
"This builds upon the Stripe integration in [DEMO-2].
Webhook handling similar to [DEMO-2].
PostgreSQL as used in [DEMO-2]..."

LLM references real historical work automatically! 🔥

## Tech Stack

- **FAISS** — Facebook AI Similarity Search (vector storage)
- **Sentence Transformers** — all-MiniLM-L6-v2 (text → embeddings)
- **OpenRouter** — Gemini 2.0 Flash (document generation)
- **Streamlit** — interactive UI
- **Python** — core language
- **python-dotenv** — environment management

## Project Structure
Vector-DB-Historical-Artefacts/
├── embeddings.py      # Convert text to 384-dim vectors
├── vector_store.py    # Store/load documents in FAISS
├── retriever.py       # Search similar documents
├── main.py            # Full pipeline runner
├── streamlit_app.py   # Interactive UI
├── faiss_index/       # Stored vector index (auto-generated)
├── requirements.txt   # Dependencies
├── .gitignore
└── .env               # API keys (not committed)

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/NIKHIL-956653/Vector-DB-Historical-Artefacts.git
cd Vector-DB-Historical-Artefacts
```

### 2. Create virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
OPENROUTER_API_KEY=your_openrouter_key

## Run

### Step 1 — Store documents in FAISS
```bash
python vector_store.py
```

### Step 2 — Test retrieval
```bash
python retriever.py
```

### Step 3 — Run full pipeline
```bash
python main.py
```

### Step 4 — Launch Streamlit UI
```bash
streamlit run streamlit_app.py
```

## How It Works

### Embeddings
"JWT authentication"
→ [0.23, 0.87, 0.12...] (384 numbers)
"Login with tokens"
→ [0.21, 0.85, 0.14...] (similar numbers!)
Similar meaning = Similar vectors!

### FAISS Search
Store 5 historical docs as vectors
Query: "Build login system"
↓
Convert to vector
↓
Find closest vectors in FAISS
↓
Return top-3 similar documents!

### Context-Aware Generation
Retrieved docs + New query
↓
Fed into Gemini as context
↓
Gemini generates document that
REFERENCES historical work!

## Results

| Query | Top Result | Score |
|-------|-----------|-------|
| "Build secure login with JWT" | User Authentication (DEMO-1) | 0.6286 ✅ |
| "Integrate payment system" | Payment Gateway (DEMO-2) | 0.5560 ✅ |
| "Send notifications" | Notification System (DEMO-3) | 0.4698 ✅ |

Correct document retrieved FIRST every time! 🎯

## Add Your Own Documents

Use the Streamlit sidebar to add new documents:
1. Enter Document ID (e.g. DEMO-6)
2. Enter Title
3. Enter Content
4. Click "Add to Vector DB"

Document instantly searchable via FAISS!

## Interview Answer

"We built a vector database using FAISS and Sentence Transformers
to store historical product documents as embeddings. When a new
request comes in, we embed it using the same model and search FAISS
for the top-3 most semantically similar past documents. These are
injected into the LLM prompt as context — enabling the AI to generate
documentation that builds on prior work rather than starting from
scratch every time. Proven by real output referencing [DEMO-2] when
asked about payment gateway v2."

## Author

**Nikhil Chandra Sairam Tokala**
AI/ML Engineer | GenAI Engineer | DevOps
Dubai, UAE
[LinkedIn](https://linkedin.com/in/nikhil-chandra-133ncsr200233) |
[GitHub](https://github.com/NIKHIL-956653)