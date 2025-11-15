import typer
from rich.console import Console

from . import assess, convert, generate, grc, pentest, report, soc, validate

app = typer.Typer(
    name="riskops",
    help="RiskOps Health / IoMT – GRC + SOC + Pentest CLI",
    invoke_without_command=True,
)

console = Console()

# Sous-commandes
app.add_typer(validate.app, name="validate")
app.add_typer(generate.app, name="generate")
app.add_typer(report.app, name="report")
app.add_typer(assess.app, name="assess")
app.add_typer(convert.app, name="convert")
app.add_typer(grc.app, name="grc")
app.add_typer(soc.app, name="soc")
app.add_typer(pentest.app, name="pentest")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        help="Afficher la version de RiskOps et quitter",
    ),
):
    """Point d’entrée global de la CLI RiskOps."""
    from riskops import __version__

    if version:
        console.print(f"[bold green]riskops[/] version {__version__}")
        raise typer.Exit(0)

    # Si aucune sous-commande n'est appelée, afficher l'aide
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(0)
