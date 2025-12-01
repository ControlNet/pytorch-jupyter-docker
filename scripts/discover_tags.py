#!/usr/bin/env python3
"""
Helper for GitHub Actions: emit available PyTorch runtime tags (>=1.13) and
the "latest" tag (highest torch version, lowest CUDA for that version) to
GITHUB_OUTPUT. Falls back to printing JSON when GITHUB_OUTPUT is not set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def get_tags() -> list[str]:
    out = subprocess.check_output(
        [sys.executable, "scripts/list_pytorch_runtime_tags.py"], text=True
    )
    return json.loads(out)


def main() -> int:
    tags = get_tags()
    latest = tags[0] if tags else ""

    out_path = os.environ.get("GITHUB_OUTPUT")
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(f"tags={json.dumps(tags, separators=(',',':'))}\n")
            f.write(f"latest={latest}\n")
    else:
        print(json.dumps({"tags": tags, "latest": latest}, separators=(",", ":")))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
