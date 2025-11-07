from __future__ import annotations

import json
import os
from pathlib import Path

import typer

from .link_gov.apply_autofix import apply_autofix
from .link_gov.check_links import prepare_for_check, run_checks
from .link_gov.classify_normalize import normalize_links
from .link_gov.extract_links import extract_links
from .link_gov.index_build import build_indexes
from .link_gov.report_csv import make_team_reports
from .link_gov.suggest_corrections import build_suggestions_preview, build_suggestions_scored
from .link_gov.utils import CACHE_DIR

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Gravitee Link Governance CLI",
)

# Use a module-level constant as the default (no function call in default args)
DEFAULT_CONFIG = Path("tools/link_gov/config.yaml")

# Typer option singletons (avoid B008: no function calls in defaults)
CSV_OPT: Path | None = typer.Option(
    None,
    "--csv",
    help="Path to high_confidence_autofix.csv (defaults to tools/.cache/high_confidence_autofix.csv)",
)
BACKUP_DIR_OPT: Path | None = typer.Option(
    None,
    "--backup-dir",
    help="Where to store backups when applying",
)
PREVIEW_OUT_OPT: Path | None = typer.Option(
    None,
    "--preview-out",
    help="Dry-run preview JSON path (default: tools/.cache/autofix_preview.json)",
)
VERBOSE_OPT: bool = typer.Option(
    False,
    "--verbose",
    help="Verbose logs",
)
ALLOW_XPAGE_ANCHORS_OPT: bool = typer.Option(
    False,
    "--allow-cross-page-anchors",
    help="Allow fixing missing anchors by moving links to a different page (still same product/version).",
)
# env default for cross-page anchors (conservative by default)
_CROSS_PAGE_ANCHOR_OK = os.getenv("LG_CROSS_PAGE_ANCHOR_OK", "0").lower() in {"1", "true", "yes"}
# ---- Typer option singletons for 'autofix' command (avoid B008) ----
DRY_RUN_TOGGLE_OPT: bool = typer.Option(
    True,
    "--dry-run/--no-dry-run",
    help="Preview only (default). Use --no-dry-run to write files.",
)

SKIPS_OUT_OPT: Path | None = typer.Option(
    None,
    "--skips-out",
    help="Where to write JSON report of skipped rows (default: tools/.cache/autofix_skipped.json).",
)

SKIPS_CSV_OPT: Path | None = typer.Option(
    None,
    "--skips-csv",
    help="Also write a CSV of non-applied rows and reasons.",
)

EXPLAIN_OPT: bool = typer.Option(
    True,
    "--explain/--no-explain",
    help="Print grouped and per-row reasons for skipped high-confidence rows (default on).",
)


@app.command()
def index(
    config: Path = DEFAULT_CONFIG,  # Typer treats params with defaults as options
):
    """Build or refresh local indexes (placeholders today)."""
    build_indexes(config)
    typer.secho("✅ Indexes built (placeholders).", fg=typer.colors.GREEN)


@app.command()
def extract(
    config: Path = DEFAULT_CONFIG,
):
    """Extract basic links/images/autolinks to JSONL."""
    total = extract_links(config)
    typer.secho(
        f"✅ Extracted {total} link-like items → tools/.cache/links_raw.jsonl",
        fg=typer.colors.GREEN,
    )


@app.command()
def normalize(
    config: Path = DEFAULT_CONFIG,
):
    """Normalize URLs/anchors and classify each link."""
    total = normalize_links(config)
    typer.secho(
        f"✅ Normalized {total} items → tools/.cache/links_norm.jsonl", fg=typer.colors.GREEN
    )


@app.command()
def stage(
    config: Path = DEFAULT_CONFIG,
):
    """Classify links and attach quick existence flags (prep for checking)."""
    total, out_file = prepare_for_check(config)
    typer.secho(
        f"✅ Staged {total} items → {out_file} (plus tools/.cache/links_stats.json)",
        fg=typer.colors.GREEN,
    )


@app.command()
def check(
    config: Path = DEFAULT_CONFIG,
):
    """Run internal existence checks and external HTTP probes. Write broken_links.csv."""
    broken_count, csv_path = run_checks(config)
    try:
        stats = json.loads((CACHE_DIR / "external_check_stats.json").read_text(encoding="utf-8"))
        typer.secho(
            f"↳ externals: checked={stats.get('external_checked',0)}, "
            f"ignored(dedup)={stats.get('ignored_external_dedup',0)}, "
            f"ignored(eval)={stats.get('ignored_external_eval',0)}, "
            f"ignored(changelog)={stats.get('ignored_changelog',0)}, "
            f"none_status={stats.get('external_none_status',0)}",
            fg=typer.colors.BLUE,
        )
    except Exception:
        pass
    if broken_count == 0:
        typer.secho("✅ No broken links detected.", fg=typer.colors.GREEN)
    else:
        typer.secho(f"⚠️  Found {broken_count} broken items → {csv_path}", fg=typer.colors.YELLOW)


@app.command()
def report(
    config: Path = DEFAULT_CONFIG,
):
    """Produce a sorted CSV with GitHub links and a JSON summary."""
    total, csv_path, json_path = make_team_reports(config)
    typer.secho(
        f"✅ Report ready: {total} rows → {csv_path} (summary: {json_path})",
        fg=typer.colors.GREEN,
    )


@app.command()
def suggest(config: Path = DEFAULT_CONFIG):
    """
    Build suggestions for missing anchors/pages. Writes:
      - tools/.cache/suggestions_preview.json
      - tools/.cache/suggestions_scored.json
    """
    prev = build_suggestions_preview(config)
    scored = build_suggestions_scored(config)

    typer.secho(f"🔎 Suggestions preview → {prev}", fg=typer.colors.CYAN)
    typer.secho(f"🧮 Suggestions scored  → {scored}", fg=typer.colors.CYAN)


@app.command()
def score(
    config: Path = DEFAULT_CONFIG,
):
    """Generate scored suggestions with confidence labels."""
    path = build_suggestions_scored(config)
    typer.secho(f"✅ Scored suggestions → {path}", fg=typer.colors.GREEN)


@app.command()
def gate(
    config: Path = DEFAULT_CONFIG,
):
    """Split suggestions into high/needs_review/low with STRICT version rules."""
    # Try the direct API first
    try:
        from .link_gov.split_confidence import build_gate_files_strict  # type: ignore[attr-defined]

        hi, med, lo = build_gate_files_strict(config)
    except Exception:
        # Fallback: execute module as CLI with clean argv
        import csv as _csv
        import runpy
        import sys

        from .link_gov.utils import CACHE_DIR

        def _count_rows(p: Path) -> int:
            if not p.exists():
                return 0
            with p.open("r", encoding="utf-8-sig", newline="") as f:
                r = _csv.reader(f)
                try:
                    next(r)
                except StopIteration:
                    return 0
                return sum(1 for _ in r)

        argv_bak = sys.argv[:]
        try:
            # Prefer split_confidence; pass config if it supports -i/--input
            sys.argv = ["tools.link_gov.split_confidence", "-i", str(config)]
            try:
                runpy.run_module("tools.link_gov.split_confidence", run_name="__main__")
            except SystemExit:
                # Some scripts call sys.exit()—that's fine.
                pass
        except Exception:
            # Older layout: try suggest_corrections as a script
            try:
                sys.argv = ["tools.link_gov.suggest_corrections", "-i", str(config)]
                runpy.run_module("tools.link_gov.suggest_corrections", run_name="__main__")
            except SystemExit:
                pass
        finally:
            sys.argv = argv_bak

        # Count outputs the script(s) should have written
        hi_file = CACHE_DIR / "high_confidence_autofix.csv"
        med_file = CACHE_DIR / "needs_review_autofix.csv"
        lo_file = CACHE_DIR / "low_confidence_autofix.csv"
        hi, med, lo = (_count_rows(hi_file), _count_rows(med_file), _count_rows(lo_file))

    typer.secho(f"✅ Split complete: {hi} high | {med} medium | {lo} low", fg=typer.colors.GREEN)


@app.command("autofix-from-scored")
def autofix_from_scored(
    config: Path = DEFAULT_CONFIG,
    reasons: str = "fuzzy_same_page",
):
    """
    Create an apply_autofix-compatible CSV from suggestions_scored.json
    keeping only anchor suggestions whose reason is in `reasons`
    (comma-separated; default: 'fuzzy_same_page').
    """
    # import here to avoid circulars at module import
    from .link_gov.split_confidence import build_autofix_csv_from_scored

    allowed = tuple(r.strip() for r in reasons.split(",") if r.strip())
    path = build_autofix_csv_from_scored(config, reasons=allowed)
    typer.secho(f"✅ Built CSV from scored → {path}", fg=typer.colors.GREEN)


@app.command("autofix")
def autofix_cli(
    csv: Path | None = CSV_OPT,
    dry_run: bool = DRY_RUN_TOGGLE_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    preview_out: Path | None = PREVIEW_OUT_OPT,
    verbose: bool = VERBOSE_OPT,
    allow_cross_page_anchors: bool = ALLOW_XPAGE_ANCHORS_OPT,
    skips_out: Path | None = SKIPS_OUT_OPT,
    skips_csv: Path | None = SKIPS_CSV_OPT,
    explain: bool = EXPLAIN_OPT,
):
    """
    Apply (or preview) conservative auto-fixes based on high_confidence_autofix.csv.
    Exit codes:
      0 = success and changes exist (or preview has changes)
      2 = no changes to make
      1 = error
    """
    try:
        files, links, report_md, preview_json = apply_autofix(
            high_csv=csv,
            dry_run=dry_run,
            backup_dir=backup_dir,
            preview_out=preview_out,
            verbose=verbose,
            allow_cross_page_anchors=allow_cross_page_anchors,
            skips_out=skips_out,
            explain=explain,
            skips_csv=skips_csv,
        )

        if dry_run:
            if files > 0 or links > 0:
                typer.secho(
                    f"📝 DRY-RUN: would change {links} links across {files} files.",
                    fg=typer.colors.BLUE,
                )
                if preview_json:
                    typer.secho(f"Preview → {preview_json}", fg=typer.colors.BLUE)
                raise SystemExit(0)
            else:
                typer.secho("DRY-RUN: no changes to make.", fg=typer.colors.YELLOW)
                raise SystemExit(2)
        else:
            typer.secho(
                f"✅ Applied changes: {links} links across {files} files.",
                fg=typer.colors.GREEN,
            )
            typer.secho(f"Report → {report_md}", fg=typer.colors.GREEN)
            raise SystemExit(0 if (files > 0 or links > 0) else 2)

    except SystemExit as e:
        raise e
    except Exception as e:
        typer.secho(f"❌ autofix failed: {e}", fg=typer.colors.RED)
        raise SystemExit(1) from e


@app.command("apply")
def apply_cmd(
    csv: Path | None = CSV_OPT,
    backup_dir: Path | None = BACKUP_DIR_OPT,
    verbose: bool = VERBOSE_OPT,
    allow_cross_page_anchors: bool = ALLOW_XPAGE_ANCHORS_OPT,
):
    """Alias for: tools.cli autofix --apply [--csv ...] [--backup-dir ...]"""
    files, links, report_md, _ = apply_autofix(
        high_csv=csv,
        dry_run=False,
        backup_dir=backup_dir,
        preview_out=None,
        verbose=verbose,
        allow_cross_page_anchors=allow_cross_page_anchors,
    )
    typer.secho(
        f"✅ APPLIED: {links} links across {files} files → {report_md}", fg=typer.colors.GREEN
    )
    raise SystemExit(0 if (files > 0 or links > 0) else 2)


if __name__ == "__main__":
    app()
