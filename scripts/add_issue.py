#!/usr/bin/env python3
"""Add or replace one issue in the static site's data.

Usage: python3 scripts/add_issue.py path/to/issue.json

issue.json = {"issue": {...issue doc, must include "date"...}, "items": [ {...item doc...}, ... ]}
Writes data/days/<date>.json and refreshes data/index.json (newest first).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ISSUE_KEYS = ("number", "headline", "brief", "generated_at", "item_count")


def main(path):
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    issue = payload["issue"]
    day = issue.get("id") or issue["date"]
    items = sorted(payload.get("items", []), key=lambda x: x.get("rank", 99))
    if not items:
        sys.exit("refusing to publish an issue with no stories")
    for i, it in enumerate(items, 1):
        it.setdefault("id", f"{day}-{i:02d}")
        it.setdefault("date", day)
    entry = {"id": day, **{k: issue.get(k) for k in ISSUE_KEYS}, "zh": issue.get("zh", {})}
    entry["item_count"] = entry.get("item_count") or len(items)

    os.makedirs(os.path.join(DATA, "days"), exist_ok=True)
    with open(os.path.join(DATA, "days", f"{day}.json"), "w", encoding="utf-8") as f:
        json.dump({"issue": entry, "items": items}, f, ensure_ascii=False, indent=1)

    index_path = os.path.join(DATA, "index.json")
    try:
        with open(index_path, encoding="utf-8") as f:
            issues = json.load(f).get("issues", [])
    except FileNotFoundError:
        issues = []
    issues = [i for i in issues if i.get("id") != day] + [entry]
    issues.sort(key=lambda i: i["id"], reverse=True)
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"issues": issues}, f, ensure_ascii=False, indent=1)
    print(f"published {day}: {len(items)} stories, {len(issues)} issues total")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
