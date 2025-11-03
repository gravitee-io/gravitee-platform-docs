from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token

from .utils import CACHE_DIR, load_config

MD_EXTS = {".md", ".mdx"}


# -------------------------
# Helpers: file iteration
# -------------------------
def _iter_docs(dirs: list[str]) -> Iterable[Path]:
    for d in dirs:
        root = Path(d)
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.suffix.lower() in MD_EXTS and p.is_file():
                yield p


# -------------------------
# Helpers: strip code to avoid regex false positives
# -------------------------
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")


def _strip_code(text: str) -> str:
    # remove fenced code blocks and inline code
    no_fences = _FENCE_RE.sub("", text)
    return _INLINE_CODE_RE.sub("", no_fences)


# -------------------------
# Reference-definition parsing
# -------------------------
# Examples:
#   [ref]: https://example.com "Title"
#   [ref]: <https://example.com>
#   [ref]: ./relative.md#slug
_REF_DEF_RE = re.compile(
    r'^\s*\[([^\]]+)\]:\s*(<[^>]+>|"[^"]+"|\([^)]+\)|\S+)(?:\s+"([^"]+)")?\s*$',
    re.MULTILINE,
)


def _parse_reference_definitions(text: str) -> dict[str, str]:
    defs: dict[str, str] = {}
    for m in _REF_DEF_RE.finditer(text):
        label = m.group(1).strip().lower()
        raw_url = (m.group(2) or "").strip()
        if raw_url.startswith("<") and raw_url.endswith(">"):
            raw_url = raw_url[1:-1].strip()
        defs[label] = raw_url
    return defs


# -------------------------
# Inline token extraction
# -------------------------
def _extract_from_inline(inline: Token, file_path: Path) -> list[dict]:
    """Pull links/images/autolinks from an 'inline' token."""
    out: list[dict] = []
    if not inline.children:
        return out

    i = 0
    while i < len(inline.children):
        t = inline.children[i]
        # Links: [text](url)
        if t.type == "link_open":
            href = t.attrGet("href") or ""
            # collect text inside this link
            text_parts: list[str] = []
            j = i + 1
            while j < len(inline.children) and inline.children[j].type != "link_close":
                if inline.children[j].type == "text":
                    text_parts.append(inline.children[j].content)
                j += 1
            text = "".join(text_parts).strip()
            out.append(
                {
                    "kind": "link",
                    "src": file_path.as_posix(),
                    "text": text,
                    "url": href,
                }
            )
            i = j  # jump to the closing token

        # Images: ![alt](url)
        elif t.type == "image":
            src = t.attrGet("src") or ""
            alt = t.attrGet("alt") or ""
            out.append(
                {
                    "kind": "image",
                    "src": file_path.as_posix(),
                    "text": alt,
                    "url": src,
                }
            )

        # Autolinks in text: "<https://…>"
        elif t.type == "text" and t.content.startswith("<") and t.content.endswith(">"):
            candidate = t.content[1:-1].strip()
            if candidate.startswith(("http://", "https://")):
                out.append(
                    {
                        "kind": "autolink",
                        "src": file_path.as_posix(),
                        "text": candidate,
                        "url": candidate,
                    }
                )
        i += 1
    return out


# -------------------------
# Regex pass for reference-style links + hash-only anchors
# -------------------------
# [text][ref]
_REF_LINK_RE = re.compile(r"\[([^\]]+)\]\[([^\]]+)\]")
# Shortcut reference: [ref] where a def exists for 'ref'
_SHORTCUT_REF_RE = re.compile(r"(?<!\!)\[([^\[\]]+)\]")
# Hash-only anchors in prose: (#slug) — we keep it conservative to typical slug charset
_HASH_ONLY_RE = re.compile(r"\(#([a-z0-9][a-z0-9\-._]*)\)")


def _extract_reference_and_hash(text: str, path: Path, ref_defs: dict[str, str]) -> list[dict]:
    out: list[dict] = []
    clean = _strip_code(text)

    # explicit reference: [text][ref]
    for m in _REF_LINK_RE.finditer(clean):
        txt = m.group(1).strip()
        ref = m.group(2).strip().lower()
        out.append(
            {
                "kind": "ref_link",
                "src": path.as_posix(),
                "text": txt,
                "ref": ref,
                "resolved_url": ref_defs.get(ref, ""),
            }
        )

    # shortcut reference: [ref] (only count if a definition exists to avoid false positives)
    for m in _SHORTCUT_REF_RE.finditer(clean):
        label = m.group(1).strip()
        low = label.lower()
        if low in ref_defs:
            out.append(
                {
                    "kind": "ref_link",
                    "src": path.as_posix(),
                    "text": label,  # used as link text
                    "ref": low,
                    "resolved_url": ref_defs.get(low, ""),
                }
            )

    # hash-only anchors in prose: (#some-slug)
    for m in _HASH_ONLY_RE.finditer(clean):
        slug = m.group(1)
        out.append(
            {
                "kind": "hash_only",
                "src": path.as_posix(),
                "text": f"#{slug}",
                "url": f"#{slug}",
            }
        )

    return out


# -------------------------
# Public API
# -------------------------
def extract_links(config_path: Path, out_path: Path | None = None) -> int:
    cfg = load_config(config_path)
    roots = cfg.get("docs_roots", ["docs/"])
    md = MarkdownIt("commonmark")

    out_file = out_path or (CACHE_DIR / "links_raw.jsonl")
    count = 0

    with out_file.open("w", encoding="utf-8") as f:
        for file_path in _iter_docs(roots):
            try:
                text = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            # 1) token-based extraction (links/images/autolinks)
            tokens = md.parse(text)
            for tok in tokens:
                if tok.type == "inline":
                    entries = _extract_from_inline(tok, file_path)
                    for e in entries:
                        f.write(json.dumps(e, ensure_ascii=False) + "\n")
                        count += 1

            # 2) reference-style links + hash-only anchors via regex
            ref_defs = _parse_reference_definitions(text)
            extra = _extract_reference_and_hash(text, file_path, ref_defs)
            for e in extra:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
                count += 1

    return count
