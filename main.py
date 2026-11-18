from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ingestion import load_code_files, chunk_code
from app.vectorstore import embed_chunks, build_faiss_index, search_index
from app.agents import analyze_code

app = FastAPI(title='Code Intelligence Platform')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'OPTIONS'],
    allow_headers=['*'],
)

files = load_code_files('sample_codebase')
chunks = chunk_code(files)
embeddings, metadata = embed_chunks(chunks)
index = build_faiss_index(embeddings)

class QueryRequest(BaseModel):
    question: str

@app.get('/')
def root():
    return {'message': 'Code Intelligence Platform is running!'}

@app.post('/analyze')
def analyze(request: QueryRequest):
    results = search_index(request.question, index, metadata)
    matched_chunks = [c for c in chunks if any(r['filename'] == c['filename'] for r in results)]
    answer = analyze_code(request.question, matched_chunks)
    return {
        'question': request.question,
        'answer': answer,
        'sources': [r['filename'] for r in results]
    }