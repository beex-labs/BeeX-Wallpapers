#!/usr/bin/env python3
"""Synchronize index.json with wallpaper assets in this repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.json"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".mkv"}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def title_from_id(item_id: str) -> str:
    return re.sub(r"[-_]+", " ", item_id).strip().title()


def matching_thumb(item_id: str) -> str | None:
    thumb_dir = ROOT / "thumbs"
    for extension in (".jpg", ".jpeg", ".png", ".webp", ".avif"):
        candidate = thumb_dir / f"{item_id}{extension}"
        if candidate.is_file():
            return relative(candidate)
    return None


def discover() -> list[dict]:
    items: list[dict] = []
    wallpaper_dir = ROOT / "wallpapers"
    if wallpaper_dir.exists():
        for path in sorted(p for p in wallpaper_dir.iterdir() if p.is_file()):
            extension = path.suffix.lower()
            if extension not in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
                continue
            item = {
                "id": path.stem,
                "name": title_from_id(path.stem),
                "kind": "video" if extension in VIDEO_EXTENSIONS else "image",
                "file": relative(path),
            }
            thumb = matching_thumb(path.stem)
            if thumb:
                item["thumb"] = thumb
            item["sizeMB"] = round(path.stat().st_size / 1024 / 1024, 2)
            items.append(item)

    web_dir = ROOT / "web"
    if web_dir.exists():
        for directory in sorted(p for p in web_dir.iterdir() if p.is_dir()):
            entry = directory / "index.html"
            if not entry.is_file():
                continue
            item = {
                "id": directory.name,
                "name": title_from_id(directory.name),
                "kind": "web",
                "dir": relative(directory),
                "entry": "index.html",
            }
            thumb = matching_thumb(directory.name)
            if thumb:
                item["thumb"] = thumb
            items.append(item)
    return items


def merge(existing: dict, found: dict) -> dict:
    # Filesystem-derived fields are authoritative; descriptive metadata is retained.
    result = dict(existing)
    for key in ("id", "kind", "file", "dir", "entry", "thumb", "sizeMB"):
        result.pop(key, None)
    result.setdefault("name", found["name"])
    result.update({key: value for key, value in found.items() if key != "name"})
    order = ("id", "name", "kind", "file", "dir", "entry", "thumb", "tags", "sizeMB")
    return {key: result[key] for key in order if key in result} | {
        key: value for key, value in result.items() if key not in order
    }


def render() -> str:
    current = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}
    existing = {item["id"]: item for item in current.get("items", [])}
    items = [merge(existing.get(item["id"], {}), item) for item in discover()]
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate wallpaper id discovered")
    return json.dumps(
        {"version": current.get("version", 1), "items": items},
        ensure_ascii=False,
        indent=2,
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if index.json is stale")
    args = parser.parse_args()
    expected = render()
    actual = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    if args.check:
        if actual != expected:
            print("index.json is stale; run: python scripts/sync_index.py", file=sys.stderr)
            return 1
        print("index.json is up to date")
        return 0
    if actual != expected:
        INDEX.write_text(expected, encoding="utf-8", newline="\n")
        print("updated index.json")
    else:
        print("index.json is already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
