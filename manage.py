#!/usr/bin/env python3
"""Unified CLI for ste-writing-style."""

import os
import sys
from pathlib import Path

# Resolve root relative to this file for cross-worktree portability
BASE_DIR = Path(__file__).resolve().parent

# Auto-re-exec inside project .venv if available and running outside virtualenv
venv_python = BASE_DIR / ".venv" / "bin" / "python"
if sys.prefix == sys.base_prefix and venv_python.exists():
    os.execv(str(venv_python), [str(venv_python)] + sys.argv)

from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from ste_writing_style.core import (
    audit_file,
    generate_template_dictionary,
    load_project_dictionary,
    save_dictionary,
)


# Resolve root relative to this file for cross-worktree portability
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

console = Console()

app = typer.Typer(
    name="ste-writing-style",
    help="Unified management CLI for ste-writing-style",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.callback()
def main_callback() -> None:
    """Simplified Technical English (ASD-STE100) CLI Operations."""
    pass


@app.command("info")
def info() -> None:
    """Display project configuration and environment status."""
    console.print("[bold blue]ste-writing-style[/bold blue] Environment Status")
    console.print(f"Base Directory: [cyan]{BASE_DIR}[/cyan]")

    dict_path = BASE_DIR / ".ste-dictionary.yaml"
    if dict_path.exists():
        d = load_project_dictionary(dict_path)
        console.print(f"Dictionary Project: [green]{d.project}[/green]")
        console.print(f"Technical Names: [green]{len(d.technical_names)}[/green]")
        console.print(f"Technical Verbs: [green]{len(d.technical_verbs)}[/green]")
        console.print(
            f"Forbidden Words: [green]{len(d.forbidden_project_words)}[/green]"
        )
    else:
        console.print(
            "Dictionary: [yellow]No .ste-dictionary.yaml found (using defaults)[/yellow]"
        )


@app.command("audit")
def audit(
    target: Annotated[
        Path, typer.Argument(help="Path to Markdown or text document to audit")
    ],
    dictionary: Annotated[
        Path | None,
        typer.Option("--dictionary", "-d", help="Custom .ste-dictionary.yaml path"),
    ] = None,
) -> None:
    """Audit a documentation file for ASD-STE100 compliance."""
    resolved_target = (
        (BASE_DIR / target).resolve() if not target.is_absolute() else target
    )
    if not resolved_target.exists():
        console.print(
            f"[bold red]Error:[/bold red] Target file '{resolved_target}' does not exist."
        )
        raise typer.Exit(code=1)

    resolved_dict = (
        (BASE_DIR / dictionary).resolve()
        if dictionary and not dictionary.is_absolute()
        else dictionary
    )
    report = audit_file(resolved_target, resolved_dict)

    console.print(f"\n[bold]Auditing:[/bold] {resolved_target.name}")
    console.print(f"Total Sentences: {report.total_sentences}")
    console.print(f"Compliant Sentences: {report.compliant_sentences}")
    console.print(
        f"Compliance Score: [bold green]{report.compliance_score}%[/bold green]\n"
    )

    if not report.violations:
        console.print(
            "[bold green]No STE violations found. Document complies with ASD-STE100 rules![/bold green]\n"
        )
        return

    table = Table(title=f"STE Audit Violations ({len(report.violations)} issues)")
    table.add_column("Line", justify="right", style="cyan", no_wrap=True)
    table.add_column("Rule", style="magenta")
    table.add_column("Issue", style="red")
    table.add_column("Suggestion", style="green")

    for v in report.violations:
        table.add_row(str(v.line_number), v.rule, v.issue, v.suggestion)

    console.print(table)


@app.command("dict-gen")
def dict_gen(
    output: Annotated[
        Path, typer.Option("--output", "-o", help="Target output file")
    ] = Path(".ste-dictionary.yaml"),
    project_name: Annotated[
        str, typer.Option("--project", "-p", help="Project name")
    ] = "Project",
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Overwrite existing dictionary")
    ] = False,
) -> None:
    """Generate a starter .ste-dictionary.yaml schema."""
    resolved_output = (
        (BASE_DIR / output).resolve() if not output.is_absolute() else output
    )
    if resolved_output.exists() and not force:
        console.print(
            f"[bold yellow]Notice:[/bold yellow] Dictionary already exists at '{resolved_output}'. Use --force to overwrite."
        )
        raise typer.Exit(code=0)

    model = generate_template_dictionary(project_name)
    save_dictionary(model, resolved_output)
    console.print(
        f"[bold green]Created[/bold green] starter dictionary at [cyan]{resolved_output}[/cyan]"
    )


if __name__ == "__main__":
    app()
