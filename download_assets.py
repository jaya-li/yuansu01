#!/usr/bin/env python3
"""
Download remote assets referenced in figma-onboarding-interactive-demo.html
and rewrite URLs to local ./assets paths for portable GitHub sharing.
"""

from __future__ import annotations

import mimetypes
import re
import ssl
import sys
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "figma-onboarding-interactive-demo.html"
ASSETS = ROOT / "assets"


URL_RE = re.compile(r'https://[^\s"\'\)]+')


def ext_from_content_type(content_type: str) -> str:
    if not content_type:
        return ""
    ctype = content_type.split(";", 1)[0].strip().lower()
    if ctype == "image/svg+xml":
        return ".svg"
    guessed = mimetypes.guess_extension(ctype) or ""
    if guessed == ".jpe":
        return ".jpg"
    return guessed


def safe_stem(name: str) -> str:
    stem = Path(name).stem or "asset"
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", stem)


def main() -> int:
    if not HTML.exists():
        print(f"[ERROR] Missing file: {HTML}")
        return 1

    text = HTML.read_text(encoding="utf-8")
    urls = sorted(set(URL_RE.findall(text)))
    if not urls:
        print("[INFO] No remote URLs found.")
        return 0

    ASSETS.mkdir(parents=True, exist_ok=True)
    ssl_ctx = ssl.create_default_context()
    url_to_local: dict[str, str] = {}
    failed: list[tuple[str, str]] = []

    for idx, url in enumerate(urls, start=1):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, context=ssl_ctx, timeout=45) as resp:
                data = resp.read()
                content_type = resp.headers.get("Content-Type", "")

            parsed = urlparse(url)
            basename = Path(parsed.path).name or f"asset_{idx}"
            ext = Path(basename).suffix.lower()
            if not ext:
                ext = ext_from_content_type(content_type)

            filename = f"{safe_stem(basename)}{ext}"
            out = ASSETS / filename

            # Avoid accidental overwrite with different content
            if out.exists() and out.read_bytes() != data:
                stem = out.stem
                suffix = out.suffix
                n = 1
                while True:
                    candidate = ASSETS / f"{stem}_{n}{suffix}"
                    if not candidate.exists() or candidate.read_bytes() == data:
                        out = candidate
                        break
                    n += 1

            if not out.exists():
                out.write_bytes(data)

            url_to_local[url] = f"./assets/{out.name}"

        except (URLError, HTTPError, TimeoutError, OSError) as e:
            failed.append((url, str(e)))

    new_text = text
    for remote, local in url_to_local.items():
        new_text = new_text.replace(remote, local)
    HTML.write_text(new_text, encoding="utf-8")

    print(f"[DONE] total_urls={len(urls)} downloaded={len(url_to_local)} failed={len(failed)}")
    if failed:
        print("[WARN] Failed URLs:")
        for u, err in failed:
            print(f" - {u}\n   {err}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

