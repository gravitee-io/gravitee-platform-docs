from __future__ import annotations

import asyncio
import csv
import json
import random
import re
import socket
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlparse

import aiohttp

from .utils import CACHE_DIR, load_config

# Polite default headers for external probes
_DEFAULT_HEADERS = {
    "User-Agent": "Gravitee-Docs-LinkChecker/1.0 (+docs)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def _resolve_dir_default(p: Path) -> Path | None:
    """If p is a directory (or clearly pointing to one), return its default doc."""
    if p.is_dir():
        for cand in ("README.md", "readme.md", "index.md", "Index.md"):
            cp = p / cand
            if cp.exists():
                return cp
    return None


def _strip_wrapping_quotes(u: str) -> str:
    u = (u or "").strip()
    # Also strip angle brackets (Markdown autolinks like <https://...>)
    u = u.strip("'\"<>")
    # Remove *leading* or *trailing* encoded quotes if present
    if u.startswith(("%22", "%27")):
        u = u[3:]
    if u.endswith(("%22", "%27")):
        u = u[:-3]
    return u


def _clean_url_for_probe(u: str) -> str:
    # conservative clean: only handle common accidental quotes
    return _strip_wrapping_quotes(u)


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


# --- context & domain helpers ---

_CHANGELOG_RE = re.compile(r"(changelog|release[-_]notes|releases?)", re.IGNORECASE)


def _is_changelog_path(p: str) -> bool:
    return bool(_CHANGELOG_RE.search(p or ""))


# Domains that often rate-limit/block HEAD but are valid for changelogs
_SAFE_CHANGELOG_DOMAINS = {
    "github.com",
    "raw.githubusercontent.com",
}

# Per-domain "soft OK" statuses (don’t treat as broken)
_DOMAIN_SOFT_OK = {
    # Heavy bot protection / rate limiting
    "github.com": {429, 403, 503},
    "raw.githubusercontent.com": {429, 403, 503},
    # Common docs/vendor sites that block HEAD or throttle aggressively
    "aws.amazon.com": {403, 429, 503},
    "signin.aws.amazon.com": {403, 429, 503},
    "eksctl.io": {403, 429, 503},
    "artifacthub.io": {403, 429, 503},
    "helm.sh": {403, 429, 503},
    "kubernetes.io": {403, 429, 503},
    "documentation.gravitee.io": {403, 429, 503},
    "aws.github.io": {403, 429, 503},
    "docs.aws.amazon.com": {403, 429, 503},
}

# Hosts where HEAD is often blocked: prefer GET first
_HEAD_BLOCKED_HOSTS = {
    "github.com",
    "raw.githubusercontent.com",
    "aws.amazon.com",
    "signin.aws.amazon.com",
    "eksctl.io",
    "artifacthub.io",
    "helm.sh",
    "kubernetes.io",
    "documentation.gravitee.io",
    "aws.github.io",
    "docs.aws.amazon.com",
}

# Statuses worth retrying with backoff
_RETRYABLE_STATUSES = {408, 425, 429, 500, 502, 503, 504}


def _host_of(url: str) -> str:
    try:
        u = _strip_wrapping_quotes(url)
        parsed = urlparse(u)
        host = (parsed.hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


_IGNORE_EXTERNAL_HOSTS = {
    "example.com",
    "www.example.com",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}

_FAKE_TLDS = (".test", ".example", ".invalid", ".localhost")


def _should_ignore_url(url: str) -> bool:
    url = _clean_url_for_probe(url)
    host = _host_of(url)
    if not host:
        return False
    if host in _IGNORE_EXTERNAL_HOSTS:
        return True
    if host.startswith("localhost") or host.startswith("127."):
        return True
    # ignore any host using well-known “fake” TLDs
    if host.endswith(_FAKE_TLDS):
        return True
    if url.strip().lower().startswith(("mailto:", "javascript:")):
        return True
    return False


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

        # --- NEW: resolve directory defaults (e.g., "installation/") before checks ---
        if path:
            p = Path(path)
            # treat both "looks like a folder" and actual folder on disk
            if str(path).endswith("/") or p.is_dir():
                resolved = _resolve_dir_default(p)
                if resolved:
                    # update both local var and record so downstream code (CSV etc.) sees the final path
                    path = resolved.as_posix()
                    rec = {**rec, "normalized_path": path}
        # --- END NEW ---

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
    """Return final status code (int) or None if network error.

    Strategy (per attempt):
      - If host is known to block HEAD, use GET first; else try HEAD then fallback to GET.
      - On retryable statuses or network errors, back off with jitter and retry.
    """
    host = _host_of(url)  # default
    max_attempts = 1

    # A little leniency for well-known, stricter domains
    if host in _DOMAIN_SOFT_OK or host in _HEAD_BLOCKED_HOSTS:
        max_attempts = 3
    else:
        max_attempts = 2

    for attempt in range(1, max_attempts + 1):
        try:
            if host in _HEAD_BLOCKED_HOSTS:
                # GET first
                async with session.get(
                    url, allow_redirects=True, timeout=timeout_s, headers=_DEFAULT_HEADERS
                ) as resp:
                    await resp.read()
                    status = resp.status
            else:
                # Try HEAD first
                try:
                    async with session.head(
                        url, allow_redirects=True, timeout=timeout_s, headers=_DEFAULT_HEADERS
                    ) as resp:
                        status = resp.status
                except aiohttp.ClientResponseError as e:
                    # If HEAD not allowed, fallback to GET immediately
                    if e.status in (405, 501):
                        async with session.get(
                            url, allow_redirects=True, timeout=timeout_s, headers=_DEFAULT_HEADERS
                        ) as resp:
                            await resp.read()
                            status = resp.status
                    else:
                        status = e.status

            # If we got a retryable status and still have attempts left, back off & retry
            if attempt < max_attempts and status in _RETRYABLE_STATUSES:
                # Exponential backoff with jitter: 0.3, 0.6, 1.2 ...
                await asyncio.sleep(0.3 * (2 ** (attempt - 1)) + random.random() * 0.2)
                continue

            return status

        except aiohttp.ClientResponseError as e:
            # Retry certain statuses
            if attempt < max_attempts and e.status in _RETRYABLE_STATUSES:
                await asyncio.sleep(0.3 * (2 ** (attempt - 1)) + random.random() * 0.2)
                continue
            return e.status
        except Exception:
            # Network/SSL/DNS issues: retry if we can
            if attempt < max_attempts:
                await asyncio.sleep(0.3 * (2 ** (attempt - 1)) + random.random() * 0.2)
                continue
            return None


async def _probe_external_batch(
    urls: list[str], timeout_s: int, max_concurrency: int
) -> dict[str, int | None]:
    """Probe a list of absolute http(s) URLs concurrently (deduped)."""
    sem = asyncio.Semaphore(max_concurrency)
    results: dict[str, int | None] = {}

    async def run(url: str, session: aiohttp.ClientSession):
        async with sem:
            await asyncio.sleep(0)  # small yield
            status = await _probe_one(url, session, timeout_s)
            results[url] = status

    # Prefer IPv4 to avoid odd AAAA-only/CDN paths; cache DNS a bit
    connector = aiohttp.TCPConnector(
        limit_per_host=max_concurrency,
        family=socket.AF_INET,
        ttl_dns_cache=300,
        force_close=True,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(run(u, session)) for u in urls]
        await asyncio.gather(*tasks)

    return results


def _unique_external_urls(rows_iter: Iterable[dict]) -> tuple[list[str], int]:
    seen = set()
    uniq = []
    # local counter so function stays pure; we'll merge in run_checks
    ignored = 0
    for r in rows_iter:
        if r.get("is_external") and not r.get("ignored"):
            raw = (r.get("raw_url") or r.get("url") or "").strip()
            u = _clean_url_for_probe(raw)
            if not u or _should_ignore_url(u):
                ignored += 1
                continue
            if u not in seen:
                seen.add(u)
                uniq.append(u)
    return uniq, ignored


def _read_ready(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _is_success(status: int, ok: set[int], host: str) -> bool:
    if status in ok:
        return True
    soft = _DOMAIN_SOFT_OK.get(host)
    return bool(soft and status in soft)


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
    ok_statuses = set(cfg.get("success_statuses", [200, 301, 302, 307, 308]))
    timeout_s = int(cfg.get("external_timeout_seconds", 12))
    max_conc = int(cfg.get("max_concurrency", 32))

    in_file = in_path or (CACHE_DIR / "links_ready.jsonl")
    out_file = out_csv or (CACHE_DIR / "broken_links.csv")
    debug = {
        "ignored_external_dedup": 0,  # filtered at URL collection time
        "ignored_external_eval": 0,  # filtered during per-record evaluation
        "ignored_changelog": 0,
        "external_checked": 0,
        "external_by_host": Counter(),
        "external_fail_status": Counter(),
        "external_soft_ok": Counter(),
        "external_none_status": 0,
    }

    # First pass: collect records and find external URL set
    ready_rows = list(_read_ready(in_file))
    ext_urls, ignored_dedup = _unique_external_urls(ready_rows)
    debug["ignored_external_dedup"] = ignored_dedup

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
            original = (r.get("raw_url") or r.get("url") or "").strip()
            url = _clean_url_for_probe(original)
            host = _host_of(url)
            if _should_ignore_url(url):
                debug["ignored_external_eval"] += 1
                continue
            src_path = r.get("src", "")

            if _is_changelog_path(src_path) and host in _SAFE_CHANGELOG_DOMAINS:
                debug["ignored_changelog"] += 1
                continue

            http_status = ext_results.get(url)
            debug["external_checked"] += 1
            debug["external_by_host"][host] += 1

            if http_status is None:
                if host in _DOMAIN_SOFT_OK or host in _SAFE_CHANGELOG_DOMAINS:
                    debug["external_soft_ok"][host] += 1
                    continue
                debug["external_none_status"] += 1
                reason = "external_error"
            elif not _is_success(http_status, ok_statuses, host):
                debug["external_fail_status"][str(http_status)] += 1
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
    # dump debug stats for this run
    (CACHE_DIR / "external_check_stats.json").write_text(
        json.dumps(
            {
                **debug,
                "external_by_host": dict(debug["external_by_host"]),
                "external_fail_status": dict(debug["external_fail_status"]),
                "external_soft_ok": dict(debug["external_soft_ok"]),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return (len(broken), out_file)
