from __future__ import annotations

from pathlib import Path

import typer

from .link_gov.apply_autofix import apply_autofix
from .link_gov.check_links import prepare_for_check, run_checks
from .link_gov.classify_normalize import normalize_links
from .link_gov.extract_links import extract_links
from .link_gov.index_build import build_indexes
from .link_gov.report_csv import make_team_reports
from .link_gov.suggest_corrections import build_suggestions_preview, build_suggestions_scored

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Gravitee Link Governance CLI",
)

# Use a module-level constant as the default (no function call in default args)
DEFAULT_CONFIG = Path("tools/link_gov/config.yaml")


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
def suggest(
    config: Path = DEFAULT_CONFIG,
    limit: int = typer.Option(
        500, "--limit", "-n", help="Max broken internal links to process for preview"
    ),
):
    """Generate a preview of suggested fixes (no changes made)."""
    count, path = build_suggestions_preview(config, limit=limit)
    typer.secho(f"✅ Suggestions preview for {count} items → {path}", fg=typer.colors.GREEN)


@app.command()
def score(
    config: Path = DEFAULT_CONFIG,
    limit: int = typer.Option(2000, "--limit", "-n", help="Max broken internal links to score"),
):
    """Generate scored suggestions with confidence labels."""
    count, path = build_suggestions_scored(config, limit=limit)
    typer.secho(f"✅ Scored {count} suggestions → {path}", fg=typer.colors.GREEN)


@app.command()
def gate(
    config: Path = DEFAULT_CONFIG,
):
    """Split suggestions into high/needs_review/low with STRICT version rules."""
    from .link_gov.suggest_corrections import build_gate_files_strict  # <- make it relative

    hi, med, lo = build_gate_files_strict(config)
    typer.secho(f"✅ Split complete: {hi} high | {med} medium | {lo} low", fg=typer.colors.GREEN)


@app.command()
def autofix(
    apply: bool = typer.Option(False, "--apply", help="Write changes to files (default: dry-run)"),
):
    """Apply high-confidence fixes. Default is DRY-RUN; pass --apply to write."""
    files, links, report = apply_autofix(dry_run=not apply)
    mode = "APPLIED" if apply else "DRY-RUN"
    typer.secho(f"✅ {mode}: {links} links across {files} files → {report}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
