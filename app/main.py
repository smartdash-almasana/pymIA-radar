from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.api.routes import router
from app.db.session import init_db


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_FILE = BASE_DIR / "templates" / "dashboard.txt"
STYLE_FILE = BASE_DIR / "static" / "radar.css.txt"
SCRIPT_FILE = BASE_DIR / "static" / "radar.js.txt"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Inlak'ech Radar",
    version="0.1.0",
    description="Prospección conversacional y precalificación para Inlak'ech",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    return HTMLResponse(TEMPLATE_FILE.read_text(encoding="utf-8"))


@app.get("/static/radar.css", response_class=PlainTextResponse)
def radar_css() -> PlainTextResponse:
    return PlainTextResponse(STYLE_FILE.read_text(encoding="utf-8"), media_type="text/css")


@app.get("/static/radar.js", response_class=PlainTextResponse)
def radar_js() -> PlainTextResponse:
    return PlainTextResponse(
        SCRIPT_FILE.read_text(encoding="utf-8"),
        media_type="application/javascript",
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
