**AI-Powered Document Chatbot (RAG-Based)**

An end-to-end Generative AI application that allows users to upload PDF documents and ask natural language questions, with answers strictly grounded in the uploaded content using a Retrieval-Augmented Generation (RAG) pipeline.

**Features**

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

**How It Works (RAG Pipeline)**

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

**Tech Stack**

| Layer                  | Technology            |

| ---------------------- | --------------------- |

| Backend                | FastAPI, Python       |

| LLM                    | Google Gemini         |

| Embeddings             | Sentence Transformers |

| Vector Search          | Cosine Similarity     |

| Frontend               | HTML, CSS, JavaScript |

| PDF Parsing            | PyPDF                 |

| Environment Management | python-dotenv         |


**Screenshots**

**Upload PDF**

<img width="1918" height="1078" alt="Upload" src="https://github.com/user-attachments/assets/55324880-5de4-4fde-991c-976edd78a564" />


**Chat Interface**

![Chat](https://github.com/user-attachments/assets/466db2fe-5c58-4d28-9694-94c7bd923f09)


**Swagger API**

![API](https://github.com/user-attachments/assets/8e05d6e6-6726-4f0f-b606-b5b8dfe92487)














