#!/usr/bin/env python3
"""
List pytorch/pytorch tags of a given kind (runtime or devel) with version >= MIN_VERSION.
Sorted so that the first element is:
  - the latest (highest) PyTorch version
  - with the earliest CUDA version available for that PyTorch release
This lets CI mark "latest" as the most recent torch with the lowest CUDA floor.
Outputs a compact JSON array.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from typing import List, Tuple, Optional

REPO = "pytorch/pytorch"
PAGE_SIZE = 100
MIN_VERSION: Tuple[int, ...] = (1, 13)  # minimum major.minor
EXCLUDED_SUBSTRINGS = ("rocm",)


def fetch_page(url: str) -> dict:
    with urllib.request.urlopen(url) as resp:  # nosec B310 - simple JSON fetch
        return json.load(resp)


def parse_version(name: str) -> Optional[Tuple[int, ...]]:
    """
    Extract dotted version prefix from a tag (e.g., '2.9.1' from '2.9.1-cuda12.6-cudnn9-runtime').
    Returns a tuple of ints for comparison or None if it cannot be parsed.
    """
    match = re.match(r"(?P<ver>\d+(?:\.\d+)+)", name)
    if not match:
        return None
    try:
        return tuple(int(part) for part in match.group("ver").split("."))
    except ValueError:
        return None


def parse_cuda_version(name: str) -> Optional[Tuple[int, ...]]:
    """
    Extract CUDA version tuple (e.g., (11, 8) from 'cuda11.8').
    """
    m = re.search(r"cuda(\d+(?:\.\d+)*)", name)
    if not m:
        return None
    try:
        return tuple(int(part) for part in m.group(1).split("."))
    except ValueError:
        return None


def is_valid_tag(name: str, required_substr: str) -> bool:
    if required_substr not in name:
        return False
    if any(excl in name for excl in EXCLUDED_SUBSTRINGS):
        return False
    version = parse_version(name)
    if version is None:
        return False
    if parse_cuda_version(name) is None:
        return False
    # Compare only first len(MIN_VERSION) components
    prefix = version[: len(MIN_VERSION)]
    return prefix >= MIN_VERSION


def collect_tags(required_substr: str) -> List[str]:
    url = (
        f"https://registry.hub.docker.com/v2/repositories/{REPO}/tags"
        f"?page_size={PAGE_SIZE}&ordering=last_updated"
    )
    tags: List[str] = []
    seen: set[str] = set()

    while url:
        data = fetch_page(url)
        for item in data.get("results", []):
            name = item.get("name", "")
            if name in seen:
                continue
            if is_valid_tag(name, required_substr):
                seen.add(name)
                tags.append(name)
        url = data.get("next")

    def sort_key(name: str) -> Tuple:
        # Negative version for descending order
        ver = parse_version(name) or (0,)
        cuda = parse_cuda_version(name) or (99,)
        # Descending torch version, ascending cuda version
        return tuple([-v for v in ver]) + (cuda,)

    tags.sort(key=sort_key)
    return tags


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--kind",
        choices=["runtime", "devel"],
        default="runtime",
        help="Which PyTorch image flavor to list",
    )
    args = parser.parse_args()

    tags = collect_tags(args.kind)
    # Compact JSON (no spaces) for easy use in GitHub Actions outputs
    print(json.dumps(tags, separators=(",", ":")))
    return 0 if tags else 1


if __name__ == "__main__":
    sys.exit(main())
