import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def session_command():
    """Chat session management"""
    pass


@session_command.command()
@click.option("--limit", "-l", default=10, help="Number of sessions to show")
def list(limit):
    """List sessions"""
    table = Table(title=f"Last {limit} sessions")
    table.add_column("ID", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("Provider", style="yellow")
    table.add_column("Messages", style="blue")

    table.add_row("demo-123", "2024-01-15 14:30", "OpenAI GPT-4", "12")
    table.add_row("demo-124", "2024-01-15 15:45", "Ollama Llama2", "8")

    console.print(table)


@session_command.command()
@click.argument("session_id")
def resume(session_id):
    """Resume session"""
    console.print(f"[green]Resuming session {session_id} (in development)[/green]")


@session_command.command()
@click.argument("session_id")
@click.option(
    "--format",
    "-f",
    default="json",
    type=click.Choice(["json", "markdown", "jsonl", "csv"]),
)
@click.option("--output", "-o", help="Файл для экспорта")
def export(session_id, format, output):
    """Export session"""
    output_info = f" to {output}" if output else ""
    console.print(
        f"[blue]Exporting session {session_id} in {format} format{output_info} (in development)[/blue]"
    )
