
from app.services.entity_extraction_service import extract_entities
from app.services.relation_extraction_service import extract_relations


def main():
    text = """
    Random Forest sử dụng nhiều Decision Tree
    để tạo ra mô hình ensemble.
    """

    print("=== INPUT TEXT ===")
    print(text)

    # Step 1: Extract entities
    entities = extract_entities(text)

    print("\n=== ENTITIES ===")
    print(entities)

    # Step 2: Extract relationships
    relations = extract_relations(text, entities)

    print("\n=== RELATIONSHIPS ===")
    print(relations)


if __name__ == "__main__":
    main()