from dataclasses import dataclass
from typing import Optional

@dataclass
class Listing:
    source: str
    listing_id: str
    title: str
    url: str
    price: Optional[int]
    fetched_at: str
