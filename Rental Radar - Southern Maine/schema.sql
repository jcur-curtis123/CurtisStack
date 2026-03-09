CREATE TABLE IF NOT EXISTS listings (
    source TEXT,
    listing_id TEXT,
    title TEXT,
    url TEXT,
    price INTEGER,
    fetched_at TEXT,
    PRIMARY KEY (source, listing_id)
);

CREATE TABLE IF NOT EXISTS price_history (
    source TEXT,
    listing_id TEXT,
    old_price INTEGER,
    new_price INTEGER,
    changed_at TEXT
);

CREATE TABLE IF NOT EXISTS scrape_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT,
    finished_at TEXT,
    status TEXT,
    listings_found INTEGER,
    new_listings INTEGER,
    error TEXT
);

CREATE TABLE IF NOT EXISTS source_health (
    source TEXT PRIMARY KEY,
    last_success TEXT,
    last_failure TEXT,
    consecutive_failures INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS discovered_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    discovered_at TEXT,
    tested INTEGER DEFAULT 0,
    valid INTEGER DEFAULT 0
);
