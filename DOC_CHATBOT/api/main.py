from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import os
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai

# Load env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

print("GEMINI KEY LOADED:", bool(API_KEY))

# IMPORTANT: Correct model
llm = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        doc_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

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
You are an AI assistant answering strictly from the provided document.

Context:
{context}

Question:
{question}

Rules:
- Only answer from the context.
- If not found, say: "Not found in the document."
"""

        try:
            response = llm.generate_content(prompt)
            answer_text = response.text.strip()
        except Exception as llm_error:
            print("LLM ERROR:", llm_error)
            return {
                "question": question,
                "answer": "LLM failed. Check API key, quota, or internet.",
                "timestamp": datetime.now().isoformat()
            }

        return {
            "question": question,
            "answer": answer_text,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
