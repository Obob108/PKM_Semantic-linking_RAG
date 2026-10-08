from app.services.chunking_service import chunk_text


text = """
Machine Learning là một nhánh của Artificial Intelligence.

Random Forest sử dụng nhiều Decision Tree để tạo ra
một mô hình ensemble learning.

Mỗi Decision Tree có thể đưa ra một dự đoán khác nhau.
Random Forest kết hợp các dự đoán này để tạo ra kết quả cuối cùng.
"""


chunks = chunk_text(
    text,
    chunk_size=100,
    overlap=20
)


print("Số lượng chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n===== CHUNK {i} =====")
    print(chunk)