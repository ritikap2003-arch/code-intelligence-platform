from app.ingestion import load_code_files, chunk_code

files = load_code_files("sample_codebase")
print("\n--- Files Loaded ---")
for f in files:
    print(f"  {f['filename']}")

chunks = chunk_code(files)
print("\n--- Sample Chunk ---")
print(chunks[0]["chunk"])