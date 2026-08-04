#!/usr/bin/env python3
"""Generate one scheduled wallpaper with the OpenAI Images API."""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = (
    "A serene futuristic alpine lake at blue hour, cinematic wide wallpaper, subtle reflections, no text, no logo",
    "An elegant abstract landscape made of flowing translucent glass and warm light, cinematic wide wallpaper, no text, no logo",
    "A quiet space observatory above clouds under a richly detailed star field, cinematic wide wallpaper, no text, no logo",
    "A minimalist East Asian mountain landscape at sunrise with atmospheric mist, cinematic wide wallpaper, no text, no logo",
)


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    now = datetime.now(timezone.utc)
    item_id = f"ai-{now:%Y-%m-%d}"
    output = ROOT / "wallpapers" / f"{item_id}.png"
    if output.exists():
        print(f"{output.name} already exists; nothing to generate")
        return 0
    payload = json.dumps({
        "model": os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2"),
        "prompt": PROMPTS[now.toordinal() % len(PROMPTS)],
        "size": "1536x1024",
        "quality": "medium",
        "output_format": "png",
    }).encode()
    request = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"OpenAI API failed ({error.code}): {error.read().decode()}") from error
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(result["data"][0]["b64_json"]))
    print(f"generated {output.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
