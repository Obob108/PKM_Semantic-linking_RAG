tìm hiểu venv là gì .venv\Scripts\activate.bat
cài fast api (installl fasstapi univorn sqlalchemy)
file requiremnets txt denpendency basic dung de lam gi 
crud //  nen mong de sau nay electron gui tai lieu backend

POST   /api/documents
GET    /api/documents
GET    /api/documents/{id}
PUT    /api/documents/{id}
DELETE /api/documents/{id}

uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
1. Document API       ✅
2. Note API 
Document đại diện cho tài liệu import vào hệ thống, ví dụ PDF
Note là nội dung người dùng trực tiếp tạo/chỉnh sửa trong PKM 
PDF ──→ Document ──→ Chunk ──→ Embedding
                              ↓
                           Knowledge Graph
                              ↑
Note ─────────────────────────┘
        
3. Parser PDF/MD
4. Chunking
5. Embedding BGE-M3
6. FAISS
7. BM25
8. Entity extraction
9. Relation extraction
10. Knowledge Graph
11. Hybrid Retrieval
12. Reranker
13. RAG + Qwen3