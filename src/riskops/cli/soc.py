import typer

app = typer.Typer(help="Commandes SOC (inventaire, logs, alertes – stub MVP).")


@app.command("status")
def soc_status():
    """Stub état SOC."""
    typer.echo("[soc] Statut SOC (stub).")
