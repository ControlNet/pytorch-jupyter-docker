#!/usr/bin/env python3
"""
Append a single build result row to the GitHub Actions job summary.
Expects the following environment variables:
  TAG, KIND, EXISTS, PUSH_LATEST, GITHUB_STEP_SUMMARY
"""
from __future__ import annotations

import os
from pathlib import Path

TAG = os.environ.get("TAG", "")
KIND = os.environ.get("KIND", "")
EXISTS = os.environ.get("EXISTS", "").lower() == "true"
PUSH_LATEST = os.environ.get("PUSH_LATEST", "").lower() == "true"
SUMMARY_PATH = Path(os.environ.get("GITHUB_STEP_SUMMARY", "summary.md"))


def main() -> int:
    built_status = "skipped (exists)" if EXISTS else "built"
    latest_status = "yes" if PUSH_LATEST else "no"

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    content = SUMMARY_PATH.read_text() if SUMMARY_PATH.exists() else ""

    if "| Tag |" not in content:
        content += "| Tag | Kind | Built | Latest |\n"
        content += "| --- | --- | --- | --- |\n"

    content += f"| {TAG} | {KIND} | {built_status} | {latest_status} |\n"
    SUMMARY_PATH.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
