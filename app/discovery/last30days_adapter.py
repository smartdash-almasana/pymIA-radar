from pathlib import Path
import json
import subprocess
from app.core.config import settings
from app.discovery.contracts import DiscoveryResult

class Last30DaysAdapter:
    """Adaptador inicial.

    Debe ajustarse luego de auditar el formato real y el comando real del repositorio
    mvanhorn/last30days-skill.
    """

    def __init__(self, repo_path: str | None = None) -> None:
        self.repo_path = Path(repo_path or settings.last30days_path)

    def search(self, query: str) -> list[DiscoveryResult]:
        if not self.repo_path.exists():
            raise RuntimeError(f"last30days-skill no está disponible en {self.repo_path}")

        # Placeholder explícito: se reemplaza por el entrypoint real auditado.
        output_file = self.repo_path / "output.json"
        if not output_file.exists():
            return []

        raw = json.loads(output_file.read_text(encoding="utf-8"))
        results = []
        for item in raw if isinstance(raw, list) else raw.get("results", []):
            results.append(DiscoveryResult(
                source=item.get("source", "unknown"),
                external_id=str(item.get("id") or item.get("url")),
                conversation_url=item["url"],
                author_name=item.get("author"),
                title=item.get("title"),
                text=item.get("text") or item.get("snippet") or "",
                context=item.get("context"),
                query_origin=query,
                engagement=item.get("engagement", {}),
            ))
        return results
