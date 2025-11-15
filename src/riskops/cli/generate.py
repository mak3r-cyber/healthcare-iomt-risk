"""Generate commands for RiskOps CLI.

Commands for generating risk matrices, reports, and visualizations.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from riskops.converters.csv_to_xlsx import convert_csv_to_xlsx

app = typer.Typer(help="Generate risk matrices, heatmaps, and dashboards")
console = Console()


@app.command("matrix")
def generate_matrix(
    csv_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Path to CSV risk matrix file",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output path for Excel file (default: <csv_dir>/reports/risk_matrix.xlsx)",
    ),
    verbose: bool = typer.Option(
        True,
        "--verbose/--quiet",
        "-v/-q",
        help="Show detailed progress messages",
    ),
) -> None:
    """
    Generate an Excel risk matrix from a CSV file.

    Creates a professional Excel workbook with three sheets:
    - Risk Matrix: Color-coded risk table
    - Heatmap: Probability × Impact visualization
    - Dashboard: Risk statistics and top risks

    Security features:
    - CSV injection protection
    - File size validation (max 10MB)
    - Risk score validation (Probability & Impact 1-5)

    Example:
        riskops generate matrix 02-Matrices/risk_matrix.csv
        riskops generate matrix risks.csv --output custom_report.xlsx
    """
    try:
        if verbose:
            console.print("\n[bold blue]Generating Excel risk matrix...[/]")
            console.print(f"Input:  {csv_file}")

        # Convert CSV to Excel using security-hardened converter
        output_path = convert_csv_to_xlsx(csv_path=csv_file, output_path=output, verbose=verbose)

        if verbose:
            console.print("\n[bold green]✓ Success![/]")
            console.print(f"Output: {output_path}")
        else:
            console.print(f"Generated: {output_path}")

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


@app.command("heatmap")
def generate_heatmap(
    csv_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to CSV risk matrix file",
    ),
) -> None:
    """
    Generate a standalone risk heatmap (Probability × Impact).

    This command generates only the heatmap visualization.
    For a complete report, use 'generate matrix' instead.

    Example:
        riskops generate heatmap 02-Matrices/risk_matrix.csv
    """
    console.print("[yellow]Note:[/] Heatmap generation is included in 'generate matrix'")
    console.print("Generating full matrix with heatmap...")

    # For now, just call generate_matrix
    # TODO: In future, implement standalone heatmap generation
    generate_matrix(csv_file=csv_file, output=None, verbose=True)


@app.command("dashboard")
def generate_dashboard(
    csv_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to CSV risk matrix file",
    ),
) -> None:
    """
    Generate a risk dashboard with statistics.

    This command generates only the dashboard with risk statistics.
    For a complete report, use 'generate matrix' instead.

    Example:
        riskops generate dashboard 02-Matrices/risk_matrix.csv
    """
    console.print("[yellow]Note:[/] Dashboard generation is included in 'generate matrix'")
    console.print("Generating full matrix with dashboard...")

    # For now, just call generate_matrix
    # TODO: In future, implement standalone dashboard generation
    generate_matrix(csv_file=csv_file, output=None, verbose=True)


if __name__ == "__main__":
    app()
