from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
import os
from typing import List
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
llm = genai.GenerativeModel("models/gemini-flash-latest")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
DATA_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

vector_store = {}

@app.get("/")
def home():
    return {"message": "AI Document Chatbot Backend Running"}

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        doc_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        extracted_text = extract_text_from_pdf(file_path)
        chunks = chunk_text(extracted_text)

        embeddings = embedder.encode(chunks)

        vector_store[doc_id] = {
            "chunks": chunks,
            "embeddings": embeddings
        }

        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "message": "PDF indexed successfully",
            "total_chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(doc_id: str, question: str):
    try:
        if doc_id not in vector_store:
            raise HTTPException(status_code=404, detail="Document not found")

        chunks = vector_store[doc_id]["chunks"]
        embeddings = vector_store[doc_id]["embeddings"]

        query_embedding = embedder.encode([question])
        similarities = cosine_similarity(query_embedding, embeddings)[0]

        top_indices = np.argsort(similarities)[::-1][:3]
        context_chunks = [chunks[i] for i in top_indices]

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are an AI assistant answering questions strictly from the provided document context.

Context:
{context}

Question:
{question}

Answer clearly and concisely. If the answer is not in the context, say so.
"""

        response = llm.generate_content(prompt)

        return {
            "question": question,
            "answer": response.text,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
