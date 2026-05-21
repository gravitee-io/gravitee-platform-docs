#!/usr/bin/env python3
# Augments `vale --output=JSON` with a `Suggestion` field on docs.Spelling
# alerts so reviewdog can render a "Commit suggestion" button.
#
# Vale's CLI omits spelling candidates from JSON output (the Alert struct
# carries them internally but they aren't serialised), which is why
# to-rdjsonl.jq can emit a deterministic replacement for Vale.Terms,
# Microsoft.Contractions, etc., but not for docs.Spelling. This script fills
# that gap.
#
# Three-stage resolution per misspelled word:
#   1. COMMON_TYPOS map  — short ambiguous typos where pure-frequency picks
#      the wrong neighbour ("dat" -> "data", not "day"; "teh" -> "the").
#   2. pyspellchecker seeded with the project vocabulary at
#      vale/styles/config/vocabularies/docs/accept.txt — so Gravitee terms
#      like OpenTelemetry, Kubernetes, gRPC are reachable as candidates.
#      Length bias filters out shorter neighbours that win on frequency.
#   3. No suggestion — alert passes through unchanged so reviewdog still
#      posts the existing "Did you really mean 'X'?" comment.
#
# Original casing is preserved: accept.txt entries keep their canonical
# casing ("OpenTelemetry"), other suggestions copy the source word's
# leading-cap / all-caps pattern.

import json
import sys
from pathlib import Path

from spellchecker import SpellChecker

ACCEPT_FILE = Path(__file__).resolve().parent / "styles/config/vocabularies/docs/accept.txt"

# Short, high-confidence corrections for typos that pure frequency-based
# correction gets wrong. Keep keys lowercase. Add entries here when a
# real-world PR review surfaces a typo pyspellchecker misroutes.
COMMON_TYPOS = {
    "adn": "and",
    "ahve": "have",
    "alot": "a lot",
    "dat": "data",
    "fro": "for",
    "hte": "the",
    "iwth": "with",
    "jsut": "just",
    "nad": "and",
    "nto": "not",
    "ot": "to",
    "taht": "that",
    "teh": "the",
    "tehn": "then",
    "thier": "their",
    "tihs": "this",
    "wiht": "with",
    "wnat": "want",
    "yoru": "your",
    "youre": "you're",
}


def load_vocab(path):
    """Return (lowercase words, lowercase->original-casing map) from accept.txt."""
    words = []
    case_map = {}
    if not path.exists():
        return words, case_map
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        for tok in line.replace("/", " ").split():
            if tok.isalpha():
                lower = tok.lower()
                words.append(lower)
                case_map.setdefault(lower, tok)
    return words, case_map


def apply_case(source, replacement):
    if not source:
        return replacement
    if len(source) > 1 and source.isupper():
        return replacement.upper()
    if source[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def best_candidate(lower, spell):
    """Return the best pyspellchecker candidate for `lower`, or None."""
    candidates = spell.candidates(lower)
    if not candidates:
        return None
    candidates = {c for c in candidates if c != lower}
    if not candidates:
        return None
    # Length bias: drop candidates shorter than the typo (a shorter real
    # word is rarely what the writer meant — they usually missed or added
    # a letter, not collapsed the whole word).
    same_or_longer = {c for c in candidates if len(c) >= len(lower)}
    pool = same_or_longer if same_or_longer else candidates
    return max(pool, key=lambda c: spell[c])


def render(word, replacement, vocab_case):
    """Apply accept.txt canonical casing first, then source-word casing."""
    if replacement in vocab_case:
        return vocab_case[replacement]
    return apply_case(word, replacement)


def main():
    spell = SpellChecker()
    vocab_words, vocab_case = load_vocab(ACCEPT_FILE)
    if vocab_words:
        spell.word_frequency.load_words(vocab_words)

    data = json.load(sys.stdin)
    for alerts in data.values():
        if not isinstance(alerts, list):
            continue
        for alert in alerts:
            if alert.get("Check") != "docs.Spelling":
                continue
            word = alert.get("Match") or ""
            if not word:
                continue
            lower = word.lower()

            if lower in COMMON_TYPOS:
                alert["Suggestion"] = apply_case(word, COMMON_TYPOS[lower])
                continue

            cand = best_candidate(lower, spell)
            if cand and cand != lower:
                alert["Suggestion"] = render(word, cand, vocab_case)

    json.dump(data, sys.stdout)


if __name__ == "__main__":
    main()
