#!/usr/bin/env python3
"""
Extract bookmark entries from a Netscape bookmark HTML file (Edge/Chrome export).

Output is a CSV with columns:
  标题,网址,备注(来自浏览器DESCRIPTION，如有)

Notes:
- This script does not classify categories.
- De-dup is optional; default is enabled to avoid identical URLs.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.parse import unquote


DT_A_PATTERN = re.compile(
    r"<DT>\s*<A\s+HREF=\"(?P<href>[^\"]+)\"(?P<attrs>[^>]*)>(?P<title>.*?)</A>",
    re.IGNORECASE | re.DOTALL,
)

DESC_PATTERN = re.compile(r'DESCRIPTION=\"(?P<desc>[^\"]*)\"', re.IGNORECASE)

TAG_PATTERN = re.compile(r"<[^>]+>")


def strip_tags(s: str) -> str:
    return TAG_PATTERN.sub("", s)


def clean_text(s: str) -> str:
    s = html.unescape(s)
    s = s.replace("\u200b", "").replace("\ufeff", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_entries(html_text: str) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    for m in DT_A_PATTERN.finditer(html_text):
        href = m.group("href")
        attrs = m.group("attrs") or ""
        title_raw = m.group("title") or ""

        desc_m = DESC_PATTERN.search(attrs)
        desc_raw = desc_m.group("desc") if desc_m else ""

        title = clean_text(strip_tags(title_raw))
        href_clean = clean_text(href)
        desc = clean_text(desc_raw)

        # Keep URL exactly as in HREF, only strip whitespace.
        entries.append({"标题": title, "网址": href_clean, "备注": desc})
    return entries


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Netscape bookmark HTML file path")
    ap.add_argument("--output", required=True, help="CSV output path")
    ap.add_argument("--dedup", action="store_true", help="Deduplicate by exact URL (default on)")
    ap.add_argument("--no-dedup", action="store_true", help="Disable dedup")
    args = ap.parse_args()

    inp = Path(args.input)
    outp = Path(args.output)

    dedup = True
    if args.no_dedup:
        dedup = False
    if args.dedup:
        dedup = True

    text = inp.read_text(encoding="utf-8", errors="ignore")
    entries = extract_entries(text)

    if dedup:
        seen = set()
        uniq: List[Dict[str, str]] = []
        for e in entries:
            url = e["网址"]
            if url in seen:
                continue
            seen.add(url)
            uniq.append(e)
        entries = uniq

    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["标题", "网址", "备注"])
        w.writeheader()
        w.writerows(entries)

    print(f"extracted={len(entries)} output={outp}")


if __name__ == "__main__":
    main()

