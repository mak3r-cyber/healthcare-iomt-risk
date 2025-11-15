import typer

app = typer.Typer(help="Génération de rapports PDF/Excel (stub MVP).")


@app.command("pdf")
def report_pdf():
    """Stub pour rapport PDF."""
    typer.echo("[report] Génération de rapport PDF (stub).")
