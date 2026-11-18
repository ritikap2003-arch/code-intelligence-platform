
from dotenv import load_dotenv
import os
load_dotenv()
print("KEY:", os.getenv("GROQ_API_KEY")[:10])

from app.ingestion import load_code_files, chunk_code
from app.vectorstore import embed_chunks, build_faiss_index, search_index
from app.agents import analyze_code

print("Step 1: Loading...")
files = load_code_files("sample_codebase")
chunks = chunk_code(files)
print("Step 2: Embedding...")
embeddings, metadata = embed_chunks(chunks)
index = build_faiss_index(embeddings)
print("Step 3: Searching...")
query = "how does the calculator handle division by zero?"
results = search_index(query, index, metadata)
print("Step 4: Matched chunks...")
matched_chunks = [c for c in chunks if any(r["filename"] == c["filename"] for r in results)]
print("Step 5: Asking agent...")
answer = analyze_code(query, matched_chunks)
print("ANSWER:", answer)
