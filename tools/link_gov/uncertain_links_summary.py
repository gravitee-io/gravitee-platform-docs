#!/usr/bin/env python3
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import typer

from .utils import CACHE_DIR

app = typer.Typer(
    add_completion=False,
    help="Summarize external_links.uncertain.csv into unique link entries with counts.",
)

# ---- Paths ----
UNCERTAIN_CSV = CACHE_DIR / "external_links.uncertain.csv"
SUMMARY_CSV = CACHE_DIR / "external_links.uncertain_summary.csv"


# ---- Typer option singletons ----
SOURCE_OPT: Path = typer.Option(
    UNCERTAIN_CSV,
    "--source",
    "-s",
    help="Input external_links.uncertain.csv",
)

OUT_OPT: Path = typer.Option(
    SUMMARY_CSV,
    "--out",
    "-o",
    help="Output CSV of summarized unique links.",
)


@dataclass
class SummaryEntry:
    src: str
    url: str
    reason: str
    status_meaning: str
    http_status: str
    count: int


# ---- Helpers ----
def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[SummaryEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    # NEW COLUMN ORDER
    fieldnames = [
        "src",
        "url",
        "reason",
        "status_meaning",
        "http_status",
        "count",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "src": r.src,
                    "url": r.url,
                    "reason": r.reason,
                    "status_meaning": r.status_meaning,
                    "http_status": r.http_status,
                    "count": r.count,
                }
            )


# ---- Command ----
@app.command()
def summarize(
    source: Path = SOURCE_OPT,
    out: Path = OUT_OPT,
):
    """Summarize uncertain links into unique entries with counts."""
    if not source.exists():
        typer.secho(f"Source CSV not found: {source}", fg=typer.colors.RED)
        raise typer.Exit(1)

    rows = _read_csv(source)
    if not rows:
        typer.secho("No rows found in the source CSV.", fg=typer.colors.YELLOW)
        return

    grouped: dict[tuple[str, str, str, str], dict[str, object]] = {}

    for row in rows:
        key = (
            row.get("url", ""),
            row.get("reason", ""),
            row.get("http_status", ""),
            row.get("status_meaning", ""),
        )
        if key not in grouped:
            grouped[key] = {
                "count": 0,
                "src": row.get("src", ""),  # remember one example source file
            }
        grouped[key]["count"] += 1

    summary_entries = [
        SummaryEntry(
            src=v["src"],
            url=k[0],
            reason=k[1],
            status_meaning=k[3],
            http_status=k[2],
            count=v["count"],
        )
        for k, v in grouped.items()
    ]

    # Sort by occurrence (descending), then by URL for stability
    summary_entries.sort(key=lambda e: (-e.count, e.url))

    _write_csv(out, summary_entries)

    typer.secho(
        f"Wrote {len(summary_entries)} unique link entries → {out}",
        fg=typer.colors.GREEN,
    )


if __name__ == "__main__":
    app()
