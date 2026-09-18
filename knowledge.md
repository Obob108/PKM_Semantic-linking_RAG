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
     - tầng chịu trách nhiệm: nhận file đọc file - > text.txt
   pip install pymupdf
   python -m test.test_parser

5. Chunking
6. Embedding BGE-M3
7. FAISS
8. BM25
9. Entity extraction
10. Relation extraction
11. Knowledge Graph
12. Hybrid Retrieval
13. Reranker
14. RAG + Qwen3
