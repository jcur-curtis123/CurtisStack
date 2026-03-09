import re
import hashlib
import requests
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin
from models import Listing
from playwright.sync_api import sync_playwright


PRICE_RE = re.compile(r"\$([0-9,]+)")


def parse_price(text):
    if not text:
        return None
    m = PRICE_RE.search(text)
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def stable_id(text):
    return hashlib.sha256(text.encode()).hexdigest()[:32]


# ==============================
# MSPM (Static HTML Scraper)
# ==============================

def fetch_mspm():
    url = "https://mainestreetpropertymanagement.com/maine-rental-listings/long-term-rentals/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://mainestreetpropertymanagement.com/",
    }

    session = requests.Session()
    session.headers.update(headers)

    # First warm-up request to homepage
    session.get("https://mainestreetpropertymanagement.com/", timeout=15)

    r = session.get(url, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    listings = []

    for h in soup.find_all(["h2", "h3"]):
        title = h.get_text(strip=True)
        if not title:
            continue

        sibling = h.find_next_sibling()
        price = parse_price(sibling.get_text(" ", strip=True) if sibling else "")

        link = h.find("a")
        listing_url = urljoin(url, link["href"]) if link else url

        listings.append(
            Listing(
                source="mspm",
                listing_id=stable_id(listing_url),
                title=title,
                url=listing_url,
                price=price,
                fetched_at=now_iso(),
            )
        )

    return listings


# ==============================
# AppFolio (Playwright Scraper)
# ==============================

def _run_appfolio(base_url, source_name):
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(base_url, timeout=30000)
        page.wait_for_timeout(3000)

        # Get all detail anchors (one per listing)
        anchors = page.query_selector_all("a[href*='/listings/detail']")

        seen = set()

        for anchor in anchors:
            try:
                href = anchor.get_attribute("href")
                if not href:
                    continue

                # Prevent duplicates
                if href in seen:
                    continue
                seen.add(href)

                if href.startswith("/"):
                    full_url = base_url.rstrip("/") + href
                else:
                    full_url = href

                # Extract price directly
                price_el = anchor.query_selector(".js-listing-blurb-rent")
                price_text = price_el.inner_text().strip() if price_el else None
                price = parse_price(price_text)

                # Extract address from image alt tag
                img = anchor.query_selector("img")
                title = img.get_attribute("alt") if img else "AppFolio Listing"

                listings.append(
                    Listing(
                        source=source_name,
                        listing_id=stable_id(full_url),
                        title=title,
                        url=full_url,
                        price=price,
                        fetched_at=now_iso(),
                    )
                )

            except Exception:
                continue

        browser.close()

    return listings


async def fetch_appfolio_playwright(base_url, source_name):
    return await asyncio.to_thread(_run_appfolio, base_url, source_name)
