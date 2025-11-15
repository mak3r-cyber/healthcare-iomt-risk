import typer

app = typer.Typer(help="Assistant d’évaluation des risques (wizard EBIOS RM Light – stub MVP).")


@app.command("start")
def assess_start():
    """Stub pour le wizard d’assessment."""
    typer.echo("[assess] Lancement du wizard (stub).")
