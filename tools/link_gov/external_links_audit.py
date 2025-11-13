#!/usr/bin/env python3
from __future__ import annotations

import csv
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import requests
import typer

from .utils import CACHE_DIR

app = typer.Typer(
    add_completion=False,
    help=(
        "Post-process page_links_audit.external_absolute.csv:\n"
        "  - extract Gravitee GitHub issue links into their own CSV\n"
        "  - group remaining links for evaluation\n"
        "  - (optionally) check external URLs and classify them as healthy / uncertain"
    ),
)

# ---- Input / output paths ----

SOURCE_EXTERNAL_CSV = CACHE_DIR / "page_links_audit.external_absolute.csv"

ISSUES_PREFIX = "https://github.com/gravitee-io/issues/issues/"

ISSUES_CSV = CACHE_DIR / "external_links.changelog_issues.csv"
TO_EVAL_CSV = CACHE_DIR / "external_links.to_evaluate.csv"

HEALTHY_CSV = CACHE_DIR / "external_links.healthy.csv"
UNCERTAIN_CSV = CACHE_DIR / "external_links.uncertain.csv"


# ---- Typer option singletons (avoid Ruff B008 in defaults) ----

SOURCE_SPLIT_OPT: Path = typer.Option(
    SOURCE_EXTERNAL_CSV,
    "--source",
    "-s",
    help="Input external-absolute CSV (from page_links_audit).",
)

ISSUES_OUT_OPT: Path = typer.Option(
    ISSUES_CSV,
    "--issues-out",
    help="CSV for Gravitee GitHub issue links.",
)

TO_EVAL_OUT_OPT: Path = typer.Option(
    TO_EVAL_CSV,
    "--to-eval-out",
    help="CSV for remaining external links to evaluate.",
)

CHECK_SOURCE_OPT: Path = typer.Option(
    TO_EVAL_CSV,
    "--source",
    "-s",
    help="CSV of external links to evaluate (default: external_links.to_evaluate.csv).",
)

DELAY_OPT: float = typer.Option(
    1.0,
    "--delay",
    "-d",
    help="Seconds to sleep between HTTP requests (per unique URL).",
)

TIMEOUT_OPT: float = typer.Option(
    5.0,
    "--timeout",
    help="Per-request timeout in seconds.",
)

LIMIT_OPT: int | None = typer.Option(
    None,
    "--limit",
    "-n",
    help="Max number of unique URLs to check (for quick tests).",
)

DRY_RUN_OPT: bool = typer.Option(
    False,
    "--dry-run",
    help="Only print frequency summary; do not perform HTTP checks or write CSVs.",
)

HEALTHY_OUT_OPT: Path = typer.Option(
    HEALTHY_CSV,
    "--healthy-out",
    help="Output CSV for links classified as healthy (2xx / 3xx).",
)

UNCERTAIN_OUT_OPT: Path = typer.Option(
    UNCERTAIN_CSV,
    "--uncertain-out",
    help="Output CSV for links that are not confidently healthy.",
)


@dataclass
class LinkCheckResult:
    status: int | None
    meaning: str


# ---------- Helpers ----------


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path.as_posix()}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        # write header only so file exists and is inspectable
        with path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = [
                "src",
                "line",
                "text",
                "url",
                "pv_product",
                "pv_version",
                "reason",
                "normalized_target",
                "http_status",
                "status_meaning",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _summarize_counts(rows: list[dict]) -> None:
    counter = Counter(r["url"] for r in rows)
    typer.secho("\nUnique external URLs (most → least frequent):", fg=typer.colors.BLUE)
    for url, count in counter.most_common():
        typer.echo(f"{count:5d}  {url}")
    typer.echo("")  # blank line


# ---------- HTTP checking ----------


def _status_meaning(status: int | None, error: str | None) -> str:
    if status is None:
        return error or "no_response"

    if 200 <= status < 300:
        return "success (2xx)"
    if 300 <= status < 400:
        return "redirect (3xx)"
    if status == 400:
        return "bad request (400)"
    if status == 401:
        return "unauthorized (401)"
    if status == 403:
        return "forbidden (403)"
    if status == 404:
        return "not found (404)"
    if status == 410:
        return "gone (410)"
    if 400 <= status < 500:
        return f"client error ({status})"
    if 500 <= status < 600:
        return f"server error ({status})"
    return f"other status ({status})"


def _check_single_url(url: str, timeout: float) -> LinkCheckResult:
    """
    Carefully check a URL:

    - Try HEAD first to avoid full downloads
    - If HEAD returns 405/501, fall back to GET
    - Follow redirects
    """
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code in (405, 501):
            resp = requests.get(url, allow_redirects=True, timeout=timeout)
        status = resp.status_code
        meaning = _status_meaning(status, None)
        return LinkCheckResult(status=status, meaning=meaning)
    except requests.RequestException as exc:
        err = f"request_error: {type(exc).__name__}"
        return LinkCheckResult(status=None, meaning=err)


# ---------- Commands ----------


@app.command()
def split(
    source: Path = SOURCE_SPLIT_OPT,
    issues_out: Path = ISSUES_OUT_OPT,
    to_eval_out: Path = TO_EVAL_OUT_OPT,
):
    """
    Split page_links_audit.external_absolute.csv into:

    - Gravitee issue links (…/gravitee-io/issues/issues/…) → issues_out
    - All other external links → to_eval_out

    The input CSV is never modified.
    """
    rows = _read_csv(source)

    issues_rows: list[dict] = []
    eval_rows: list[dict] = []

    for row in rows:
        url = row.get("url", "")
        if url.startswith(ISSUES_PREFIX):
            issues_rows.append(row)
        else:
            eval_rows.append(row)

    _write_csv(issues_out, issues_rows)
    _write_csv(to_eval_out, eval_rows)

    typer.secho(
        f"Split {len(rows)} rows → {len(issues_rows)} issue links, "
        f"{len(eval_rows)} links to evaluate.",
        fg=typer.colors.GREEN,
    )
    typer.echo(f"Issue links CSV:      {issues_out.as_posix()}")
    typer.echo(f"Links to evaluate CSV: {to_eval_out.as_posix()}")


@app.command()
def check(
    source: Path = CHECK_SOURCE_OPT,
    delay: float = DELAY_OPT,
    timeout: float = TIMEOUT_OPT,
    limit: int | None = LIMIT_OPT,
    dry_run: bool = DRY_RUN_OPT,
    healthy_out: Path = HEALTHY_OUT_OPT,
    uncertain_out: Path = UNCERTAIN_OUT_OPT,
):
    """
    For the given external-links CSV:

    1. Print each unique URL with the number of occurrences (most → least).
    2. Optionally, perform slow, careful HTTP checks (HEAD/GET with delay).
    3. Write:
         - healthy_out   → links with 2xx/3xx responses
         - uncertain_out → everything else (4xx/5xx/errors/timeouts)
    """
    rows = _read_csv(source)
    if not rows:
        typer.secho("No rows found in input CSV.", fg=typer.colors.YELLOW)
        return

    # Group rows by URL
    by_url: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_url[row.get("url", "")].append(row)

    # 1. Frequency summary
    _summarize_counts(rows)

    if dry_run:
        typer.secho("Dry run → not performing HTTP checks.", fg=typer.colors.BLUE)
        return

    # 2. HTTP checks per unique URL (with caching and delay)
    typer.secho("Checking external URLs over the network…", fg=typer.colors.BLUE)
    url_results: dict[str, LinkCheckResult] = {}

    unique_urls = list(by_url.keys())
    if limit is not None:
        unique_urls = unique_urls[:limit]

    for idx, url in enumerate(unique_urls, 1):
        typer.echo(f"[{idx}/{len(unique_urls)}] {url}")
        result = _check_single_url(url, timeout=timeout)
        url_results[url] = result
        typer.echo(
            f"  → {result.status if result.status is not None else 'ERROR'} : {result.meaning}"
        )
        if idx != len(unique_urls):
            time.sleep(delay)

    # 3. Classify rows into healthy vs uncertain
    healthy_rows: list[dict] = []
    uncertain_rows: list[dict] = []

    for url, rows_for_url in by_url.items():
        result = url_results.get(url)
        if result is None:
            # Shouldn't happen, but be defensive
            result = LinkCheckResult(status=None, meaning="not_checked")

        is_healthy = result.status is not None and 200 <= result.status < 400

        for row in rows_for_url:
            out_row = dict(row)  # copy
            out_row["http_status"] = result.status if result.status is not None else ""
            out_row["status_meaning"] = result.meaning

            if is_healthy:
                healthy_rows.append(out_row)
            else:
                uncertain_rows.append(out_row)

    _write_csv(healthy_out, healthy_rows)
    _write_csv(uncertain_out, uncertain_rows)

    typer.secho(
        f"\nHTTP check complete: {len(unique_urls)} unique URLs tested.",
        fg=typer.colors.GREEN,
    )
    typer.echo(f"Healthy links:   {len(healthy_rows)} rows → {healthy_out.as_posix()}")
    typer.echo(f"Uncertain links: {len(uncertain_rows)} rows → {uncertain_out.as_posix()}")


if __name__ == "__main__":
    app()
