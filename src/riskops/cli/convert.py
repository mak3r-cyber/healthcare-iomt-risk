import typer

app = typer.Typer(help="Conversions CSV/JSON/XLSX (stub MVP).")


@app.command("csv2json")
def csv2json():
    """Stub conversion CSV -> JSON."""
    typer.echo("[convert] csv2json (stub).")
