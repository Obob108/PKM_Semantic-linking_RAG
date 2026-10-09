
import json

import httpx


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:8b"


def extract_entities(text: str) -> list[dict]:
    if not text or not text.strip():
        return []

    prompt = f"""
Extract entities explicitly mentioned in the text below.

Allowed types:
PERSON, ORGANIZATION, TECHNOLOGY, ALGORITHM,
CONCEPT, DATASET, OTHER

Return a JSON object with this exact structure:
{{
  "entities": [
    {{"name": "Random Forest", "type": "ALGORITHM"}},
    {{"name": "Decision Tree", "type": "ALGORITHM"}}
  ]
}}

Do not invent entities. Do not include explanations.

Text:
{text}
"""

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
            },
        },
        timeout=180.0,
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]

    # Tạm thời giữ các dòng debug để xác định nguyên nhân.
    print("DEBUG raw content:", repr(content))

    data = json.loads(content)

    if not isinstance(data, dict):
        raise ValueError("Ollama response must be a JSON object")

    entities = data.get("entities", [])

    print("DEBUG parsed data:", data)

    if not isinstance(entities, list):
        raise ValueError("'entities' must be a list")

    results = []
    seen = set()

    allowed_types = {
        "PERSON",
        "ORGANIZATION",
        "TECHNOLOGY",
        "ALGORITHM",
        "CONCEPT",
        "DATASET",
        "OTHER",
    }

    for entity in entities:
        if not isinstance(entity, dict):
            continue

        name = entity.get("name")
        entity_type = entity.get("type")

        if not isinstance(name, str) or not name.strip():
            continue

        if not isinstance(entity_type, str):
            continue

        entity_type = entity_type.strip().upper()

        if entity_type not in allowed_types:
            entity_type = "OTHER"

        name = name.strip()
        key = name.casefold()

        if key in seen:
            continue

        seen.add(key)

        results.append({
            "name": name,
            "type": entity_type,
        })

    return results