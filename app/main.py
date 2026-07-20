from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse

from app.api.routes import router
from app.htmx_ui import router as htmx_router
from app.presumptive_candidate_ui import router as presumptive_candidate_router
from app.db.session import init_db


BASE_DIR = Path(__file__).resolve().parent
LAB_TEMPLATE_FILE = BASE_DIR / "templates" / "lab.txt"
STYLE_FILE = BASE_DIR / "static" / "radar.css.txt"
SCRIPT_FILE = BASE_DIR / "static" / "radar.js.txt"
LAB_STYLE_FILE = BASE_DIR / "static" / "lab.css.txt"
LAB_SCRIPT_FILE = BASE_DIR / "static" / "lab.js.txt"
RADAR_UI_STYLE_FILE = BASE_DIR / "static" / "radar-ui.css.txt"
RADAR_UI_SCRIPT_FILE = BASE_DIR / "static" / "radar-ui.js.txt"


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
app.include_router(htmx_router)
app.include_router(presumptive_candidate_router)


@app.get("/lab", response_class=HTMLResponse)
def lab() -> HTMLResponse:
    return HTMLResponse(LAB_TEMPLATE_FILE.read_text(encoding="utf-8"))


@app.get("/static/radar.css", response_class=PlainTextResponse)
def radar_css() -> PlainTextResponse:
    return PlainTextResponse(STYLE_FILE.read_text(encoding="utf-8"), media_type="text/css")


@app.get("/static/radar.js", response_class=PlainTextResponse)
def radar_js() -> PlainTextResponse:
    return PlainTextResponse(
        SCRIPT_FILE.read_text(encoding="utf-8"),
        media_type="application/javascript",
    )


@app.get("/static/radar-ui.css", response_class=PlainTextResponse)
def radar_ui_css() -> PlainTextResponse:
    return PlainTextResponse(
        RADAR_UI_STYLE_FILE.read_text(encoding="utf-8"),
        media_type="text/css",
    )


@app.get("/static/radar-ui.js", response_class=PlainTextResponse)
def radar_ui_js() -> PlainTextResponse:
    return PlainTextResponse(
        RADAR_UI_SCRIPT_FILE.read_text(encoding="utf-8"),
        media_type="application/javascript",
    )


@app.get("/static/lab.css", response_class=PlainTextResponse)
def lab_css() -> PlainTextResponse:
    return PlainTextResponse(
        LAB_STYLE_FILE.read_text(encoding="utf-8"), media_type="text/css"
    )


@app.get("/static/lab.js", response_class=PlainTextResponse)
def lab_js() -> PlainTextResponse:
    return PlainTextResponse(
        LAB_SCRIPT_FILE.read_text(encoding="utf-8"),
        media_type="application/javascript",
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
