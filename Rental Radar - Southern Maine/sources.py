from scraper import fetch_mspm, fetch_appfolio_playwright

SOURCES = [
    {
        "name": "mspm",
        "enabled": True,
        "interval": 300,
        "fn": fetch_mspm,
    },
    {
        "name": "foreside_appfolio",
        "enabled": True,
        "interval": 600,
        "fn": lambda: fetch_appfolio_playwright(
            "https://foresidemanagement.appfolio.com/listings",
            "foreside_appfolio"
        ),
    },
]
