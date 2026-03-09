import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

SEARCH_QUERIES = [
    "Maine property management rentals",
    "Portland Maine apartments for rent",
    "Southern Maine property management available units",
]

def search_google(query):
    url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, params={"q": query}, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/url?q=" in href:
            clean = href.split("/url?q=")[1].split("&")[0]
            if clean.startswith("http"):
                links.append(clean)

    return links

def looks_like_rental_page(url):
    keywords = [
        "rent",
        "rental",
        "available",
        "apartments",
        "units"
    ]
    return any(k in url.lower() for k in keywords)
