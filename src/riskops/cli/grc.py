import typer

app = typer.Typer(help="Commandes avancées GRC (RiskOps GRC module – stub MVP).")


@app.command("summary")
def grc_summary():
    """Stub résumé GRC."""
    typer.echo("[grc] Résumé GRC (stub).")
