import requests
from datetime import date
from typing import Iterator, Dict

BASE_URL = "https://www.federalregister.gov/api/v1/documents.json"

def fetch_documents(start: date, end: date) -> Iterator[Dict]:
    page = 1
    while True:
        resp = requests.get(
            BASE_URL,
            params={
                "conditions[publication_date][gte]": start.isoformat(),
                "conditions[publication_date][lte]": end.isoformat(),
                "per_page": 1000,
                "page": page,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        for doc in results:
            yield doc
        if len(results) < 1000:
            break
        page += 1
