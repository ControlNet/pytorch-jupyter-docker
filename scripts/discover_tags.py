#!/usr/bin/env python3
"""
Helper for GitHub Actions: emit available PyTorch runtime tags (>=2.1) and
the "latest" tag (highest torch version, lowest CUDA for that version) to
GITHUB_OUTPUT. Falls back to printing JSON when GITHUB_OUTPUT is not set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Set
import urllib.request

TARGET_REPO = os.getenv("TARGET_REPO", "controlnet/pytorch-jupyter")


def latest_runtime(tags: list[str]) -> str:
    return tags[0] if tags else ""


def fetch_existing_tags(repo: str) -> Set[str]:
    """
    Fetch existing tags from a Docker Hub repo, returning a set of tag names.
    """
    tags: Set[str] = set()
    url = f"https://hub.docker.com/v2/repositories/{repo}/tags?page_size=100"
    while url:
        with urllib.request.urlopen(url) as resp:  # nosec B310
            data = json.load(resp)
        for item in data.get("results", []):
            name = item.get("name")
            if name:
                tags.add(name)
        url = data.get("next")
    return tags


def get_tags(kind: str) -> list[str]:
    out = subprocess.check_output(
        [sys.executable, "scripts/list_pytorch_runtime_tags.py", "--kind", kind],
        text=True,
    )
    return json.loads(out)


def main() -> int:
    runtime_tags = get_tags("runtime")
    latest = latest_runtime(runtime_tags)

    existing = fetch_existing_tags(TARGET_REPO)

    builds = []
    for t in runtime_tags:
        exists = t in existing
        will_build = not exists
        builds.append(
            {
                "tag": t,
                "push_latest": t == latest,
                "kind": "runtime",
                "exists": exists,
                "will_build": will_build,
            }
        )

    out_path = os.environ.get("GITHUB_OUTPUT")
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(f"runtime_tags={json.dumps(runtime_tags, separators=(',',':'))}\n")
            f.write(f"latest={latest}\n")
            f.write(f"builds={json.dumps(builds, separators=(',',':'))}\n")
    if not os.environ.get("GITHUB_STEP_SUMMARY"):
        print(
            json.dumps(
                {
                    "runtime_tags": runtime_tags,
                    "latest": latest,
                    "builds": builds,
                },
                separators=(",", ":"),
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
