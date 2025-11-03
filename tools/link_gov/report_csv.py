from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from .utils import CACHE_DIR, load_config

# Heuristic labels & short suggestions
_REASON_LABEL = {
    "missing_file": "Internal page not found",
    "missing_anchor": "Anchor not found on page",
}


def _label(reason: str) -> str:
    if reason.startswith("external_http_"):
        return f"External HTTP {reason.split('_')[-1]}"
    if reason == "external_error":
        return "External fetch error"
    return _REASON_LABEL.get(reason, reason)


def _suggestion(row: dict) -> str:
    r = row.get("reason", "")
    if r == "missing_file":
        return "Check path/extension; confirm file exists and relative path is correct."
    if r == "missing_anchor":
        return "Confirm target heading exists (H1–H4) and slug; update link anchor or heading."
    if r.startswith("external_http_"):
        return "Verify external URL or add redirect; if expected, whitelist."
    if r == "external_error":
        return "Retry later; if persistent, fix URL or whitelist."
    return ""


def _gh_link(repo: str, branch: str, src: str) -> str:
    # Don’t guess a line; the file view is enough for triage
    return f"https://github.com/{repo}/blob/{branch}/{src}"


def _read_broken(csv_path: Path) -> list[dict]:
    out: list[dict] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(row)
    return out


def _write_sorted(csv_path: Path, rows: list[dict]) -> int:
    fields = [
        "reason",
        "category",
        "kind",
        "src",
        "text",
        "raw_url",
        "normalized_path",
        "normalized_anchor",
        "http_status",
        "github_link",
        "category_label",
        "suggestion",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    return len(rows)


def make_team_reports(
    config_path: Path,
    in_csv: Path | None = None,
    out_sorted: Path | None = None,
    out_summary: Path | None = None,
) -> tuple[int, Path, Path]:
    cfg = load_config(config_path)
    repo = cfg.get("github_repo", "gravitee-io/gravitee-platform-docs")
    branch = cfg.get("github_default_branch", "main")

    src_csv = in_csv or (CACHE_DIR / "broken_links.csv")
    dst_csv = out_sorted or (CACHE_DIR / "broken_links_sorted.csv")
    dst_json = out_summary or (CACHE_DIR / "broken_links_summary.json")

    rows = _read_broken(src_csv)

    # Enrich rows
    for r in rows:
        r["category_label"] = _label(r.get("reason", ""))
        r["suggestion"] = _suggestion(r)
        r["github_link"] = _gh_link(repo, branch, r.get("src", ""))

    # Sort: reason > src > text (stable, human-friendly)
    rows.sort(key=lambda r: (r.get("reason", ""), r.get("src", ""), r.get("text", "")))

    # Write sorted CSV
    total = _write_sorted(dst_csv, rows)

    # Summary: by reason + by src (top offenders)
    by_reason = Counter(r.get("reason", "") for r in rows)
    by_src = Counter(r.get("src", "") for r in rows)
    top_src = by_src.most_common(50)

    summary = {
        "total_broken": total,
        "by_reason": dict(by_reason),
        "top_src_files": [{"src": s, "count": c} for s, c in top_src],
    }
    dst_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return total, dst_csv, dst_json
