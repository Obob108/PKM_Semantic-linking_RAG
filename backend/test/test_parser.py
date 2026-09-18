from app.services.parser_service import parse_document


pdf_path = "data/documents/test.md"

text = parse_document(pdf_path)

print("===== MARKDOWN TEXT =====")
print(text[:1000])