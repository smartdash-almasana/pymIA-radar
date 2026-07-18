from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.session import init_db


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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
