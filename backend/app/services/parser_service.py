import pathlib 
import pymupdf 

def parse_document(file_path: str) -> str:
    path = pathlib.Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        doc = pymupdf.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    elif suffix in [".md", ".markdown", ".txt"]:
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
        