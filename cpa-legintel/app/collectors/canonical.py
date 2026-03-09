import json

def canonical_law_text(doc: dict) -> str:
    payload = {
        "title": doc.get("title"),
        "abstract": doc.get("abstract"),
        "action": doc.get("action"),
        "publication_date": doc.get("publication_date"),
        "agencies": sorted(a.get("name") for a in doc.get("agencies", [])),
    }
    return json.dumps(payload, sort_keys=True)
