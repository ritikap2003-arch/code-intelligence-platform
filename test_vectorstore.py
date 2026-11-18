from app.ingestion import load_code_files, chunk_code
from app.vectorstore import embed_chunks, build_faiss_index, search_index

# Step 1: Load and chunk
files = load_code_files("sample_codebase")
chunks = chunk_code(files)

# Step 2: Embed and index
embeddings, metadata = embed_chunks(chunks)
index = build_faiss_index(embeddings)

# Step 3: Search
query = "how does the calculator handle division by zero?"
results = search_index(query, index, metadata)

print("\n--- Search Results ---")
for r in results:
    print(f"  File: {r['filename']} | Score: {r['score']:.4f}")