import streamlit as st
from vector_store import add_documents, load_index
from retriever import search_similar
from main import generate_with_context

st.set_page_config(
    page_title="Vector DB Historical Artefacts",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Vector DB — Historical Artefacts")
st.caption("Search similar documents using FAISS + Sentence Transformers")

with st.sidebar:
    st.header("📊 System Status")
    index, docs = load_index()
    if index:
        st.success("✅ FAISS Index Loaded")
        st.metric("Documents Stored", index.ntotal)
    else:
        st.error("❌ No index found!")
    st.divider()
    st.header("➕ Add New Document")
    doc_id = st.text_input("Document ID", placeholder="DEMO-6")
    doc_title = st.text_input("Title", placeholder="New Feature")
    doc_content = st.text_area("Content", placeholder="Describe the feature...")
    if st.button("Add to Vector DB"):
        if doc_id and doc_title and doc_content:
            new_doc = [{"id": doc_id, "title": doc_title, "content": doc_content}]
            add_documents(new_doc)
            st.success(f"✅ Added {doc_id} to FAISS!")
            st.rerun()
        else:
            st.warning("Fill all fields!")

tab1, tab2 = st.tabs(["🔍 Search Documents", "🤖 Generate with Context"])

with tab1:
    st.subheader("🔍 Semantic Search")
    query = st.text_input("Enter your query:", placeholder="Build secure login system...")
    top_k = st.slider("Number of results", 1, 5, 3)
    if st.button("🔍 Search FAISS"):
        if query:
            with st.spinner("Searching vector database..."):
                results = search_similar(query, top_k=top_k)
            st.success(f"Found {len(results)} similar documents!")
            for doc in results:
                score = doc["similarity_score"]
                color = "🟢" if score > 0.5 else "🟡" if score > 0.3 else "🔴"
                with st.expander(f"{color} [{doc['id']}] {doc['title']} — Score: {score:.4f}"):
                    st.write(doc["content"])
        else:
            st.warning("Enter a query first!")

with tab2:
    st.subheader("🤖 Generate Document with Historical Context")
    gen_query = st.text_input("What document do you want to generate?", placeholder="Build payment gateway v2...")
    if st.button("🚀 Generate Document"):
        if gen_query:
            with st.spinner("Searching FAISS + Generating with Gemini..."):
                similar_docs = search_similar(gen_query, top_k=2)
                st.markdown("### 📚 Retrieved Historical Context:")
                for doc in similar_docs:
                    st.info(f"**[{doc['id']}] {doc['title']}** (Score: {doc['similarity_score']:.4f})")
                document = generate_with_context(gen_query, similar_docs)
            st.markdown("### 📄 Generated Document:")
            st.markdown(document)
            st.download_button("💾 Download", document, file_name=f"{gen_query[:20].replace(' ', '_')}.md", mime="text/markdown")
        else:
            st.warning("Enter a query first!")
