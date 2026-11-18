from pathlib import Path


def load_code_files(directory):
    code_files = []
    path = Path(directory)
    for file_path in path.rglob("*.py"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            code_files.append({"filename": str(file_path), "content": content})
    print(f"Loaded {len(code_files)} Python files from {directory}")
    return code_files


def chunk_code(code_files, chunk_size=500):
    chunks = []
    for file in code_files:
        content = file["content"]
        filename = file["filename"]
        lines = content.split("\n")
        current_chunk = []
        current_size = 0
        for line in lines:
            current_chunk.append(line)
            current_size += len(line)
            if current_size >= chunk_size:
                chunks.append({"filename": filename, "chunk": "\n".join(current_chunk)})
                current_chunk = []
                current_size = 0
        if current_chunk:
            chunks.append({"filename": filename, "chunk": "\n".join(current_chunk)})
    print(f"Created {len(chunks)} chunks from {len(code_files)} files")
    return chunks