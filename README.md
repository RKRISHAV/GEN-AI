\*\*📄 AI-Powered Document Chatbot (RAG-Based)\*\*

An end-to-end Generative AI application that allows users to upload PDF documents and ask natural language questions, with answers strictly grounded in the uploaded content using a Retrieval-Augmented Generation (RAG) pipeline.







\*\*🚀 Features\*\*

Upload PDF documents

Automatic text extraction and chunking

Semantic embeddings using Sentence Transformers

Vector similarity search using cosine similarity

Context-aware answer generation using Google Gemini

Hallucination-free responses (grounded in document)

Real-time chat interface

Clean UI

FastAPI backend

Frontend using HTML, CSS, JavaScript





\*\*🧠 How It Works (RAG Pipeline)\*\*

User uploads a PDF

Text is extracted

Text is chunked into overlapping segments

Each chunk is converted into embeddings

Embeddings are stored in memory

User asks a question

Query is embedded

Semantic similarity search retrieves relevant chunks

Relevant context is injected into Gemini

Gemini generates a grounded answer





\*\*🛠️ Tech Stack\*\*







| Layer                  | Technology            |



| ---------------------- | --------------------- |



| Backend                | FastAPI, Python       |



| LLM                    | Google Gemini         |



| Embeddings             | Sentence Transformers |



| Vector Search          | Cosine Similarity     |



| Frontend               | HTML, CSS, JavaScript |



| PDF Parsing            | PyPDF                 |



| Environment Management | python-dotenv         |











---







\\## 📸 Screenshots







\\### Upload PDF



!\\\[Upload UI](screenshots/upload.png)







\\### Chat Interface



!\\\[Chat UI](screenshots/chat.png)







\\### Swagger API



!\\\[API Docs](screenshots/api.png)













