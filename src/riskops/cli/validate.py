"""Validate commands for RiskOps CLI.

Commands for validating risk data, links, and compliance documentation.
"""

from pathlib import Path

import pandas as pd
import typer
from rich.console import Console
from rich.table import Table

from riskops.core.constants import REQUIRED_RISK_COLUMNS
from riskops.utils.security import validate_file_size, validate_risk_scores
from riskops.validators.link_validator import validate_documentation_links

app = typer.Typer(help="Validate risk data, links, and documentation")
console = Console()


@app.command("links")
def validate_links(
    file_or_dir: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to markdown file or directory containing markdown files",
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Show detailed validation output",
    ),
) -> None:
    """
    Validate HTTP/HTTPS links in markdown documentation.

    Security features:
    - Path traversal protection
    - HTTP timeout (10 seconds)
    - SSL certificate verification
    - Rate limiting to prevent DoS

    Example:
        riskops validate links docs/compliance/iso27002-iomt-mapping.md
        riskops validate links docs/compliance/
    """
    try:
        if file_or_dir.is_file():
            # Validate single file
            if verbose:
                console.print(f"\n[bold blue]Validating links in:[/] {file_or_dir}")

            all_valid = validate_documentation_links(str(file_or_dir), verbose=verbose)

            if all_valid:
                console.print("\n[bold green]✓ All links are valid![/]")
            else:
                console.print("\n[bold red]✗ Some links are invalid[/]")
                raise typer.Exit(code=1)

        elif file_or_dir.is_dir():
            # Validate all markdown files in directory
            md_files = list(file_or_dir.rglob("*.md"))

            if not md_files:
                console.print(f"[yellow]Warning:[/] No markdown files found in {file_or_dir}")
                raise typer.Exit(code=0)

            console.print(f"\n[bold blue]Found {len(md_files)} markdown files[/]")

            results = []
            for md_file in md_files:
                if verbose:
                    console.print(f"\nValidating: {md_file.relative_to(file_or_dir)}")

                all_valid = validate_documentation_links(str(md_file), verbose=False)
                results.append((md_file.name, all_valid))

            # Display summary table
            table = Table(title="Link Validation Summary")
            table.add_column("File", style="cyan")
            table.add_column("Status", style="bold")

            for filename, is_valid in results:
                status = "[green]✓ Valid[/]" if is_valid else "[red]✗ Invalid[/]"
                table.add_row(filename, status)

            console.print(table)

            # Exit code based on results
            all_files_valid = all(is_valid for _, is_valid in results)
            if all_files_valid:
                console.print("\n[bold green]✓ All files validated successfully![/]")
            else:
                console.print("\n[bold red]✗ Some files have invalid links[/]")
                raise typer.Exit(code=1)

    except typer.Exit:
        raise  # Re-raise typer.Exit without handling
    except (ValueError, FileNotFoundError) as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {e}")
        raise typer.Exit(code=1)


@app.command("csv")
def validate_csv(
    csv_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to CSV risk matrix file",
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Show detailed validation output",
    ),
) -> None:
    """
    Validate a CSV risk matrix file.

    Checks:
    - File size (max 10MB)
    - Required columns present
    - Probability values (1-5)
    - Impact values (1-5)
    - Risk calculation (P × I)

    Example:
        riskops validate csv 02-Matrices/risk_matrix.csv
    """
    try:
        if verbose:
            console.print("\n[bold blue]Validating CSV risk matrix...[/]")
            console.print(f"File: {csv_file}")

        # Security: Validate file size
        validate_file_size(csv_file)
        if verbose:
            file_size_mb = csv_file.stat().st_size / 1024 / 1024
            console.print(f"[green]✓[/] File size: {file_size_mb:.2f}MB (valid)")

        # Load CSV
        df = pd.read_csv(csv_file)
        if verbose:
            console.print(f"[green]✓[/] Loaded {len(df)} rows")

        # Check required columns
        missing_cols = [col for col in REQUIRED_RISK_COLUMNS if col not in df.columns]
        if missing_cols:
            console.print(f"[bold red]✗ Missing columns:[/] {', '.join(missing_cols)}")
            raise typer.Exit(code=1)

        if verbose:
            console.print("[green]✓[/] All required columns present")

        # Validate data types for numeric columns
        try:
            df["Probability"] = pd.to_numeric(df["Probability"], errors="raise")
            df["Impact"] = pd.to_numeric(df["Impact"], errors="raise")
            df["Risk"] = pd.to_numeric(df["Risk"], errors="raise")
        except ValueError as e:
            console.print(f"[bold red]✗ Invalid numeric values:[/] {e}")
            raise typer.Exit(code=1)

        # Validate risk scores
        validate_risk_scores(df)
        if verbose:
            console.print("[green]✓[/] Probability & Impact values valid (1-5)")
            console.print("[green]✓[/] Risk calculations valid (P × I)")

        # Display statistics
        if verbose:
            console.print("\n[bold]Risk Statistics:[/]")
            console.print(f"  Critical (≥15): {len(df[df['Risk'] >= 15])}")
            console.print(f"  High (13-14):   {len(df[(df['Risk'] >= 13) & (df['Risk'] <= 14)])}")
            console.print(f"  Medium (7-12):  {len(df[(df['Risk'] >= 7) & (df['Risk'] <= 12)])}")
            console.print(f"  Low (≤6):       {len(df[df['Risk'] <= 6])}")

        console.print("\n[bold green]✓ CSV validation passed![/]")

    except typer.Exit:
        raise  # Re-raise typer.Exit without handling
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {e}")
        raise typer.Exit(code=1)


@app.command("risk")
def validate_risk_json(
    json_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to JSON risk assessment file",
    ),
) -> None:
    """
    Validate a JSON risk assessment file against schema.

    This command will validate JSON risk data against the RiskOps schema.

    Example:
        riskops validate risk samples/healthcare/risk_sample.json
    """
    console.print("[yellow]Note:[/] JSON schema validation not yet implemented")
    console.print("Coming in v0.3 - Threat Intelligence Integration")
    console.print(f"\nFile: {json_file}")

    # TODO: Implement JSON schema validation using Pydantic models
    # from riskops.core.models import RiskAssessment
    # assessment = RiskAssessment.parse_file(json_file)


@app.command("all")
def validate_all(
    directory: Path = typer.Option(
        Path("."),
        "--dir",
        "-d",
        help="Project directory to validate",
    ),
) -> None:
    """
    Validate entire project (CSV files, links, documentation).

    Runs all validation checks on the project directory.

    Example:
        riskops validate all
        riskops validate all --dir /path/to/project
    """
    console.print("\n[bold blue]Running comprehensive validation...[/]")
    console.print(f"Directory: {directory}")

    # Find and validate all CSV files
    csv_files = list(directory.rglob("*.csv"))
    if csv_files:
        console.print(f"\n[bold]Found {len(csv_files)} CSV files[/]")
        # TODO: Validate each CSV file

    # Find and validate all markdown files
    md_files = list(directory.rglob("*.md"))
    if md_files:
        console.print(f"\n[bold]Found {len(md_files)} markdown files[/]")
        # TODO: Validate links in each markdown file

    console.print("\n[yellow]Note:[/] Comprehensive validation not fully implemented")
    console.print("Use individual validation commands for now:")
    console.print("  - riskops validate csv <file>")
    console.print("  - riskops validate links <file>")


if __name__ == "__main__":
    app()
