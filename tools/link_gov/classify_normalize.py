from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, urlunparse

from .utils import CACHE_DIR, load_config


def _resolve_dir_default(p: Path) -> Path | None:
    """
    If p is a directory (or treated as one), return its default document if present.
    We prefer README.md over index.md to match common GitBook/GitHub flows.
    """
    for cand in ("README.md", "readme.md", "index.md", "Index.md"):
        cp = p / cand
        if cp.exists():
            return cp
    return None


IGNORE_DEFAULT = {"mailto", "tel", "javascript"}


def _read_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            count += 1
    return count


def _collapse_posix(base: str, rel: str) -> str:
    """
    Join base directory with a relative path, and collapse '.' / '..'.
    Returns a POSIX path (forward slashes).
    """
    base_dir = PurePosixPath(base).parent
    candidate = PurePosixPath(rel.replace("\\", "/"))

    # If candidate is absolute (starts with '/'), keep as-is (docs root-relative)
    if str(candidate).startswith("/"):
        combined = candidate
    else:
        combined = base_dir.joinpath(candidate)

    parts = []
    for p in combined.parts:
        if p in (".", ""):
            continue
        if p == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append("..")
        else:
            parts.append(p)
    return "/".join(parts)


def _split_url(url: str) -> tuple[str, str]:
    """Return (path, anchor) with lowercased anchor and no leading '#'."""
    if not url:
        return "", ""
    p = urlparse(url)
    anchor = (p.fragment or "").strip().lstrip("#").lower()
    # strip query and fragment for normalized path
    norm = p._replace(params="", query="", fragment="")
    norm_path = urlunparse(norm)
    return norm_path, anchor


def _normalize_record(rec: dict, ignore_schemes: set[str]) -> dict:
    kind = rec.get("kind", "")
    src = rec.get("src", "")
    _ = rec.get("text", "")  # keep for potential logging

    # choose the working URL
    raw_url = ""
    unresolved_ref = False
    if kind == "ref_link":
        resolved = (rec.get("resolved_url") or "").strip()
        raw_url = resolved
        if not resolved:
            unresolved_ref = True
            # keep the original ref label for later suggestion logic
    else:
        raw_url = (rec.get("url") or "").strip()

    # classify/ignore
    parsed = urlparse(raw_url) if raw_url else None
    scheme = parsed.scheme.lower() if parsed else ""
    ignored = scheme in ignore_schemes

    is_external = False
    normalized_path = ""
    normalized_anchor = ""
    raw_path = ""
    raw_anchor = ""

    if kind == "hash_only":
        # (#slug) means: same file, slug anchor
        raw_anchor = raw_url.lstrip("#").lower()
        normalized_anchor = raw_anchor
        normalized_path = src  # anchor within same file
    elif parsed and parsed.netloc:
        # absolute http(s) URL
        is_external = scheme in {"http", "https"}
        raw_path, raw_anchor = _split_url(raw_url)
        normalized_path = raw_path.replace("\\", "/")
        normalized_anchor = raw_anchor
    else:
        # internal or empty
        raw_path, raw_anchor = _split_url(raw_url)
        if raw_path:
            normalized_path = _collapse_posix(src, raw_path)
        else:
            # empty path + maybe anchor -> same file
            normalized_path = src
        normalized_path = normalized_path.lstrip("./").replace("\\", "/")
        normalized_anchor = raw_anchor

    return {
        **rec,
        "raw_url": raw_url,
        "scheme": scheme,
        "ignored": ignored,
        "unresolved_ref": unresolved_ref,
        "is_external": is_external,
        "normalized_path": normalized_path,
        "normalized_anchor": normalized_anchor,
    }


def normalize_links(
    config_path: Path, in_path: Path | None = None, out_path: Path | None = None
) -> int:
    cfg = load_config(config_path)
    raw_schemes = cfg.get("ignore_schemes", [])
    # flatten possible list-of-dicts or plain list
    schemes = []
    for item in raw_schemes:
        if isinstance(item, dict):
            schemes.extend(item.keys())
        elif isinstance(item, str):
            schemes.append(item)
    ignore_schemes = set(schemes) or set(IGNORE_DEFAULT)

    in_file = in_path or (CACHE_DIR / "links_raw.jsonl")
    out_file = out_path or (CACHE_DIR / "links_norm.jsonl")

    rows = (_normalize_record(rec, ignore_schemes) for rec in _read_jsonl(in_file))
    total = _write_jsonl(out_file, rows)
    return total
