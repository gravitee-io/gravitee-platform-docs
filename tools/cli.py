from __future__ import annotations

from pathlib import Path

import typer

from .link_gov.index_build import build_indexes

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


if __name__ == "__main__":
    app()
