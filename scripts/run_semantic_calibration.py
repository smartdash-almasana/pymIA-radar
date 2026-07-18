from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import settings
from app.semantics.calibration import run_semantic_calibration
from app.semantics.calibration_io import load_calibration_corpus
from app.semantics.llm_classifier import assess_with_optional_llm


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run RADAR semantic calibration against a labeled corpus."
    )
    parser.add_argument(
        "--corpus",
        default="config/semantic_calibration_corpus.v1.json",
    )
    parser.add_argument(
        "--report",
        default="data/calibration/semantic_calibration_report.v1.json",
    )
    parser.add_argument("--score-tolerance", type=int, default=20)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    corpus = load_calibration_corpus(args.corpus)

    def runner(text: str):
        return assess_with_optional_llm(
            text,
            enabled=settings.semantic_llm_enabled,
            model_name=settings.semantic_llm_model or settings.openai_model,
            provider_name=settings.semantic_llm_provider,
            base_url=settings.semantic_llm_base_url,
            api_key=settings.semantic_llm_api_key or settings.openai_api_key,
        )

    report = run_semantic_calibration(
        corpus.cases,
        runner=runner,
        score_tolerance=args.score_tolerance,
        corpus_human_validated=corpus.human_validated,
    )
    target = Path(args.report)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(target)
    print(
        f"cases={report.case_count} action_accuracy={report.action_accuracy:.3f} "
        f"false_positive_rate={report.false_positive_rate:.3f} "
        f"human_validated={report.corpus_human_validated} "
        f"ready_for_pilot={report.ready_for_pilot}"
    )
    return 0 if report.ready_for_pilot else 2


if __name__ == "__main__":
    raise SystemExit(main())
