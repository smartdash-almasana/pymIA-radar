from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from pydantic import ValidationError

from app.core.config import settings
from app.discovery.contracts import DiscoveryResult
from app.discovery.last30days_contracts import (
    Last30DaysAgentExport,
    Last30DaysExecutionTrace,
    Last30DaysSearchResult,
)


class Last30DaysAdapterError(RuntimeError):
    """Base error for last30days integration failures."""


class Last30DaysExecutionError(Last30DaysAdapterError):
    pass


class Last30DaysOutputError(Last30DaysAdapterError):
    pass


class Last30DaysAdapter:
    """Run the audited last30days CLI and normalize agent JSON v1.2."""

    def __init__(
        self,
        repo_path: str | Path | None = None,
        python_executable: str = "python",
        timeout_seconds: int = 300,
    ) -> None:
        self.repo_path = Path(repo_path or settings.last30days_path)
        self.python_executable = python_executable
        self.timeout_seconds = timeout_seconds

    @property
    def entrypoint(self) -> Path:
        return self.repo_path / "skills" / "last30days" / "scripts" / "last30days.py"

    def build_command(
        self,
        query: str,
        *,
        save_dir: str | Path,
        search_sources: list[str] | None = None,
        quick: bool = False,
    ) -> list[str]:
        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("query must not be empty")

        command = [
            self.python_executable,
            str(self.entrypoint),
            normalized_query,
            "--emit=json",
            "--json-profile=agent",
            f"--save-dir={Path(save_dir)}",
        ]
        if search_sources:
            normalized_sources = [source.strip() for source in search_sources if source.strip()]
            if normalized_sources:
                command.append(f"--search={','.join(normalized_sources)}")
        if quick:
            command.append("--quick")
        return command

    def parse_output(self, stdout: str, *, requested_query: str) -> Last30DaysAgentExport:
        if not stdout.strip():
            raise Last30DaysOutputError("last30days returned empty stdout")
        try:
            raw = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise Last30DaysOutputError("last30days stdout is not valid JSON") from exc
        try:
            export = Last30DaysAgentExport.model_validate(raw)
        except ValidationError as exc:
            raise Last30DaysOutputError(f"invalid last30days agent export: {exc}") from exc
        if export.query.strip() != requested_query.strip():
            raise Last30DaysOutputError(
                f"query mismatch: requested {requested_query!r}, received {export.query!r}"
            )
        return export

    def normalize(self, export: Last30DaysAgentExport) -> list[DiscoveryResult]:
        normalized: list[DiscoveryResult] = []
        seen: set[tuple[str, str]] = set()
        for item in export.results:
            key = (item.source, item.candidate_id)
            if key in seen:
                continue
            seen.add(key)

            context = None
            if item.cluster is not None and 0 <= item.cluster < len(export.clusters):
                cluster = export.clusters[item.cluster]
                context = cluster.summary or cluster.title

            normalized.append(
                DiscoveryResult(
                    source=item.source,
                    external_id=item.candidate_id,
                    conversation_url=item.url,
                    author_name=None,
                    title=item.title,
                    text=item.summary,
                    context=context,
                    published_at=item.published_at,
                    query_origin=export.query,
                    engagement=item.engagement,
                )
            )
        return normalized

    def search(
        self,
        query: str,
        *,
        save_dir: str | Path,
        search_sources: list[str] | None = None,
        quick: bool = False,
    ) -> Last30DaysSearchResult:
        if not self.repo_path.exists():
            raise Last30DaysExecutionError(
                f"last30days repository is unavailable at {self.repo_path}"
            )
        if not self.entrypoint.is_file():
            raise Last30DaysExecutionError(
                f"last30days entrypoint is unavailable at {self.entrypoint}"
            )

        command = self.build_command(
            query,
            save_dir=save_dir,
            search_sources=search_sources,
            quick=quick,
        )
        started_at = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise Last30DaysExecutionError(
                f"last30days timed out after {self.timeout_seconds} seconds"
            ) from exc
        except OSError as exc:
            raise Last30DaysExecutionError(f"last30days could not start: {exc}") from exc

        if completed.returncode != 0:
            detail = completed.stderr.strip() or "no stderr"
            raise Last30DaysExecutionError(
                f"last30days exited with code {completed.returncode}: {detail}"
            )

        duration_seconds = time.monotonic() - started_at
        export = self.parse_output(completed.stdout, requested_query=query)
        return Last30DaysSearchResult(
            export=export,
            conversations=self.normalize(export),
            trace=Last30DaysExecutionTrace(
                command=command,
                return_code=completed.returncode,
                stderr=completed.stderr,
                duration_seconds=duration_seconds,
            ),
        )
