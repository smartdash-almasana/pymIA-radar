import httpx
from app.core.config import settings

class RelaticleClient:
    def __init__(self) -> None:
        self.base_url = settings.relaticle_base_url.rstrip("/")
        self.headers = {}
        if settings.relaticle_api_token:
            self.headers["Authorization"] = f"Bearer {settings.relaticle_api_token}"

    async def create_candidate(self, payload: dict) -> dict:
        """La ruta exacta debe validarse durante la auditoría de Relaticle."""
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/api/people",
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
