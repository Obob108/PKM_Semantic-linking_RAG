
import json

import httpx

from app.services.entity_extraction_service import (
    MODEL_NAME,
    OLLAMA_URL
)


ALLOWED_RELATIONS = {
    "uses",
    "based_on",
    "part_of",
    "is_a",
    "related_to"
}


def extract_relations(
    text: str,
    entities: list[dict]
) -> list[dict]:
    if not text.strip() or len(entities) < 2:
        return []

    prompt = f"""
Extract relationships between the supplied entities
using only evidence from the text.

Allowed relation types:
{sorted(ALLOWED_RELATIONS)}

Return JSON only, using this schema:
{{
  "relationships": [
    {{
      "source": "Random Forest",
      "relation": "uses",
      "target": "Decision Tree"
    }}
  ]
}}

Rules:
- source and target must match supplied entity names.
- Use only the allowed relation types.
- Do not invent relationships.
- Do not infer a relationship without textual evidence.
- Return an empty list if no relationship is supported.

Entities:
{json.dumps(entities, ensure_ascii=False)}

Text:
{text}
"""

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0
            }
        },
        timeout=180.0
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]
    data = json.loads(content)

    entity_names = {
        entity["name"].strip().casefold()
        for entity in entities
    }

    valid_relations = []

    for relation in data.get("relationships", []):
        if not isinstance(relation, dict):
            continue

        source = relation.get("source")
        target = relation.get("target")
        relation_type = relation.get("relation")

        if not all(
            isinstance(value, str)
            for value in (source, target, relation_type)
        ):
            continue

        if source.strip().casefold() not in entity_names:
            continue

        if target.strip().casefold() not in entity_names:
            continue

        if relation_type not in ALLOWED_RELATIONS:
            continue

        if source.strip().casefold() == target.strip().casefold():
            continue

        valid_relations.append({
            "source": source.strip(),
            "relation": relation_type,
            "target": target.strip()
        })

    return valid_relations