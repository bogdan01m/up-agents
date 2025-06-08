import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from src.cli.session import SessionManager

console = Console()


@click.group()
def session_command():
    """Chat session management"""
    pass


@session_command.command()
@click.option("--include-temp", is_flag=True, help="Include temporary sessions")
def list(include_temp):
    """List all sessions"""
    session_manager = SessionManager()
    sessions = session_manager.list_sessions(include_temp=include_temp)

    if not sessions:
        console.print("[dim]No sessions found[/dim]")
        return

    table = Table(title="Chat Sessions")
    table.add_column("Name", style="cyan")
    table.add_column("Messages", justify="right")
    table.add_column("Created", style="dim")
    table.add_column("Updated", style="dim")
    table.add_column("Type", style="yellow")

    for session_name in sessions:
        info = session_manager.get_session_info(session_name)
        if info:
            session_type = "temp" if info["is_temp"] else "saved"
            table.add_row(
                session_name,
                str(info["message_count"]),
                info["created_at"][:19] if info["created_at"] else "-",
                info["updated_at"][:19] if info["updated_at"] else "-",
                session_type,
            )

    console.print(table)


@session_command.command()
@click.argument("session_name")
@click.option(
    "--format",
    "-f",
    default="rich",
    type=click.Choice(["rich", "json", "text"]),
    help="Output format",
)
def show(session_name, format):
    """Show session content"""
    session_manager = SessionManager()
    history = session_manager.load_session(session_name)

    if not history:
        console.print(f"[red]Session '{session_name}' not found[/red]")
        return

    if format == "json":
        console.print(history.to_json())
    elif format == "text":
        export_text = session_manager.export_session(session_name, "txt")
        console.print(export_text)
    else:  # rich format
        console.print(Panel(f"[bold]Session: {session_name}[/bold]", style="blue"))
        console.print(f"[dim]Messages: {len(history.messages)}[/dim]")
        console.print(f"[dim]Created: {history.created_at}[/dim]")
        console.print(f"[dim]Updated: {history.updated_at}[/dim]")
        console.print()

        for i, message in enumerate(history.messages, 1):
            role_color = "blue" if message.role == "user" else "green"
            console.print(
                f"[bold {role_color}]{message.role.title()}:[/bold {role_color}]"
            )
            console.print(Markdown(message.content))
            if i < len(history.messages):
                console.print("─" * 50)


@session_command.command()
@click.argument("session_name")
@click.option("--force", "-f", is_flag=True, help="Don't ask for confirmation")
def delete(session_name, force):
    """Delete a session"""
    session_manager = SessionManager()

    if not session_manager.storage.session_exists(session_name):
        console.print(f"[red]Session '{session_name}' not found[/red]")
        return

    if not force:
        confirm = input(f"Delete session '{session_name}'? (y/N): ").lower()
        if confirm not in ["y", "yes"]:
            console.print("[yellow]Cancelled[/yellow]")
            return

    if session_manager.delete_session(session_name):
        console.print(f"[green]Session '{session_name}' deleted[/green]")
    else:
        console.print(f"[red]Failed to delete session '{session_name}'[/red]")


@session_command.command()
@click.argument("old_name")
@click.argument("new_name")
def rename(old_name, new_name):
    """Rename a session"""
    session_manager = SessionManager()

    if not session_manager.storage.session_exists(old_name):
        console.print(f"[red]Session '{old_name}' not found[/red]")
        return

    if session_manager.storage.session_exists(new_name):
        console.print(f"[red]Session '{new_name}' already exists[/red]")
        return

    if session_manager.rename_session(old_name, new_name):
        console.print(
            f"[green]Session renamed from '{old_name}' to '{new_name}'[/green]"
        )
    else:
        console.print("[red]Failed to rename session[/red]")


@session_command.command()
@click.argument("session_name")
@click.option(
    "--format",
    "-f",
    default="json",
    type=click.Choice(["json", "text"]),
    help="Export format",
)
@click.option("--output", "-o", help="Output file (default: stdout)")
def export(session_name, format, output):
    """Export session to file"""
    session_manager = SessionManager()

    export_data = session_manager.export_session(session_name, format)
    if not export_data:
        console.print(f"[red]Session '{session_name}' not found[/red]")
        return

    if output:
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(export_data)
            console.print(f"[green]Session exported to {output}[/green]")
        except Exception as e:
            console.print(f"[red]Failed to write file: {e}[/red]")
    else:
        console.print(export_data)


@session_command.command()
@click.option("--days", "-d", default=7, help="Delete temp sessions older than N days")
@click.option("--dry-run", is_flag=True, help="Show what would be deleted")
def cleanup(days, dry_run):
    """Clean up old temporary sessions"""
    session_manager = SessionManager()

    if dry_run:
        console.print(
            f"[dim]Would delete temporary sessions older than {days} days[/dim]"
        )
        return

    cleaned = session_manager.cleanup_temp_sessions(days)
    if cleaned > 0:
        console.print(f"[green]Cleaned up {cleaned} temporary sessions[/green]")
    else:
        console.print("[dim]No temporary sessions to clean up[/dim]")
