from __future__ import annotations

import asyncio
import csv
import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path

import aiohttp

from .utils import CACHE_DIR, load_config


# ---------- helpers ----------
def _read_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def _load_indexes() -> tuple[dict, dict]:
    files_idx_path = CACHE_DIR / "files_index.json"
    headings_idx_path = CACHE_DIR / "headings_index.json"
    files_index = json.loads(files_idx_path.read_text(encoding="utf-8"))
    headings_index = json.loads(headings_idx_path.read_text(encoding="utf-8"))
    return files_index, headings_index


def _categorize(rec: dict) -> str:
    if rec.get("ignored"):
        return "ignored"
    if rec.get("kind") == "image":
        # image links are still interesting (404s), but tracked separately
        return "image"
    if rec.get("is_external"):
        return "external"
    if rec.get("kind") == "hash_only":
        return "internal_anchor"
    if rec.get("kind") == "ref_link" and rec.get("unresolved_ref"):
        return "unresolved_ref"
    # internal doc link: with or without anchor
    if rec.get("normalized_anchor"):
        return "internal_anchor"
    return "internal_page"


# ---------- main ----------
def prepare_for_check(
    config_path: Path, in_path: Path | None = None, out_path: Path | None = None
) -> tuple[int, Path]:
    """
    Read links_norm.jsonl, categorize each record, and attach quick
    existence flags (file_known / anchor_known) using Step-1 indexes.
    Output links_ready.jsonl and a small stats JSON.
    """
    _ = load_config(config_path)  # reserved for future toggles

    files_index, headings_index = _load_indexes()
    in_file = in_path or (CACHE_DIR / "links_norm.jsonl")
    out_file = out_path or (CACHE_DIR / "links_ready.jsonl")
    stats_file = CACHE_DIR / "links_stats.json"

    per_cat = Counter()
    totals = Counter()
    sample_missing = defaultdict(int)

    def enrich(rec: dict) -> dict:
        cat = _categorize(rec)
        per_cat[cat] += 1
        totals["all"] += 1

        path = rec.get("normalized_path", "")
        anchor = rec.get("normalized_anchor", "")

        file_known = bool(path) and (path in files_index)
        anchor_known = False
        if anchor:
            key = f"{path}#{anchor}"
            anchor_known = key in headings_index

        if cat == "internal_page":
            if not file_known:
                sample_missing["page"] += 1
        elif cat == "internal_anchor":
            if not anchor_known:
                sample_missing["anchor"] += 1

        return {
            **rec,
            "category": cat,
            "file_known": file_known,
            "anchor_known": anchor_known,
        }

    total = _write_jsonl(out_file, (enrich(r) for r in _read_jsonl(in_file)))

    # small stats dump
    stats = {
        "total": total,
        "by_category": dict(per_cat),
        "missing_counts": dict(sample_missing),  # quick pulse, not full report yet
    }
    stats_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

    return total, out_file


# ---------- Step 2.5: actual checks & CSV report ----------
async def _probe_one(url: str, session: aiohttp.ClientSession, timeout_s: int) -> int | None:
    """Return final status code (int) or None if network error."""
    try:
        # Try HEAD first (fast), then fallback to GET if method not allowed
        async with session.head(url, allow_redirects=True, timeout=timeout_s) as resp:
            return resp.status
    except aiohttp.ClientResponseError as e:
        if e.status in (405, 501):  # method not allowed/not implemented
            try:
                async with session.get(url, allow_redirects=True, timeout=timeout_s) as resp:
                    # read small body to allow reuse of connection
                    await resp.read()
                    return resp.status
            except Exception:
                return None
        return e.status
    except Exception:
        return None


async def _probe_external_batch(
    urls: list[str], timeout_s: int, max_concurrency: int
) -> dict[str, int | None]:
    """Probe a list of absolute http(s) URLs concurrently (deduped)."""
    sem = asyncio.Semaphore(max_concurrency)
    results: dict[str, int | None] = {}

    async def run(url: str):
        async with sem:
            # small stagger to avoid thundering herd
            await asyncio.sleep(0)
            status = await _probe_one(url, session, timeout_s)
            results[url] = status

    connector = aiohttp.TCPConnector(limit_per_host=max_concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(run(u)) for u in urls]
        await asyncio.gather(*tasks)

    return results


def _unique_external_urls(rows_iter: Iterable[dict]) -> list[str]:
    seen = set()
    uniq = []
    for r in rows_iter:
        if r.get("is_external") and not r.get("ignored"):
            url = (r.get("raw_url") or r.get("url") or "").strip()
            if url and url not in seen:
                seen.add(url)
                uniq.append(url)
    return uniq


def _read_ready(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _is_success(status: int, ok: set[int]) -> bool:
    return status in ok


def _reason_for_internal(rec: dict) -> str | None:
    cat = rec.get("category")
    if cat == "internal_page" and not rec.get("file_known"):
        return "missing_file"
    if cat == "internal_anchor":
        if not rec.get("file_known"):
            return "missing_file"
        if not rec.get("anchor_known"):
            return "missing_anchor"
    return None


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "src",
        "kind",
        "category",
        "text",
        "raw_url",
        "normalized_path",
        "normalized_anchor",
        "http_status",
        "reason",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def run_checks(
    config_path: Path, in_path: Path | None = None, out_csv: Path | None = None
) -> tuple[int, Path]:
    """
    Evaluate internal existence & external HTTP status.
    Write only *broken* items to CSV.
    """
    cfg = load_config(config_path)
    ok_statuses = set(cfg.get("success_statuses", [200, 301, 302, 308]))
    timeout_s = int(cfg.get("external_timeout_seconds", 12))
    max_conc = int(cfg.get("max_concurrency", 32))

    in_file = in_path or (CACHE_DIR / "links_ready.jsonl")
    out_file = out_csv or (CACHE_DIR / "broken_links.csv")

    # First pass: collect records and find external URL set
    ready_rows = list(_read_ready(in_file))
    ext_urls = _unique_external_urls(ready_rows)

    # Probe externals (deduped)
    ext_results: dict[str, int | None] = {}
    if ext_urls:
        try:
            ext_results = asyncio.run(_probe_external_batch(ext_urls, timeout_s, max_conc))
        except RuntimeError:
            # if running inside an event loop (rare), use fallback
            loop = asyncio.get_event_loop()
            ext_results = loop.run_until_complete(
                _probe_external_batch(ext_urls, timeout_s, max_conc)
            )

    # Evaluate each record
    broken: list[dict] = []
    for r in ready_rows:
        # Skip ignored outright
        if r.get("ignored"):
            continue

        reason = _reason_for_internal(r)
        http_status = None

        if reason is None and r.get("is_external"):
            url = (r.get("raw_url") or r.get("url") or "").strip()
            http_status = ext_results.get(url)
            if http_status is None:
                reason = "external_error"
            elif not _is_success(http_status, ok_statuses):
                reason = f"external_http_{http_status}"

        if reason:
            broken.append(
                {
                    **r,
                    "http_status": http_status if http_status is not None else "",
                    "reason": reason,
                }
            )

    _write_csv(out_file, broken)
    return (len(broken), out_file)
