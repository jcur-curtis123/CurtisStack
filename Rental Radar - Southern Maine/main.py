import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from db import db_connect
from scheduler import run_scrape_loop

load_dotenv()

app = FastAPI()
conn = db_connect()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scrape_loop(conn))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    rows = conn.execute(
        "SELECT source, title, url, price, fetched_at FROM listings ORDER BY fetched_at DESC"
    ).fetchall()

    listings = [
        {
            "source": r[0],
            "title": r[1],
            "url": r[2],
            "price": r[3],
            "fetched_at": r[4],
        }
        for r in rows
    ]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "listings": listings},
    )

@app.get("/jobs")
def job_history():
    rows = conn.execute(
        "SELECT started_at, finished_at, status, listings_found, new_listings, error FROM scrape_jobs ORDER BY id DESC"
    ).fetchall()

    return [
        {
            "started_at": r[0],
            "finished_at": r[1],
            "status": r[2],
            "listings_found": r[3],
            "new_listings": r[4],
            "error": r[5],
        }
        for r in rows
    ]


@app.get("/health")
def source_health():
    rows = conn.execute(
        "SELECT source, last_success, last_failure, consecutive_failures FROM source_health"
    ).fetchall()

    return [
        {
            "source": r[0],
            "last_success": r[1],
            "last_failure": r[2],
            "failures": r[3],
        }
        for r in rows
    ]
