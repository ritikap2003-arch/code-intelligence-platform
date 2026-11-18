import faiss
import numpy as np
from fastembed import TextEmbedding

# Load embedding model once
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def embed_chunks(chunks: list[dict]) -> tuple:
    """
    Embeds code chunks using FastEmbed.
    Returns embeddings and metadata.
    """
    texts = [chunk["chunk"] for chunk in chunks]
    metadata = [chunk["filename"] for chunk in chunks]

    print("⏳ Generating embeddings...")
    embeddings = list(embedding_model.embed(texts))
    embeddings_np = np.array(embeddings).astype("float32")
    print(f"✅ Generated {len(embeddings_np)} embeddings")
    return embeddings_np, metadata


def build_faiss_index(embeddings_np: np.ndarray) -> faiss.Index:
    """
    Builds a FAISS index from embeddings.
    """
    dim = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings_np)
    print(f"✅ FAISS index built with {index.ntotal} vectors")
    return index


def search_index(query: str, index: faiss.Index, metadata: list, top_k: int = 3) -> list:
    """
    Searches the FAISS index for similar code chunks.
    """
    query_embedding = list(embedding_model.embed([query]))
    query_np = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_np, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            results.append({
                "filename": metadata[idx],
                "score": float(distances[0][i])
            })
    return results