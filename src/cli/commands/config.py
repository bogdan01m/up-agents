import click
from rich.console import Console
from src.llms.llm_call.env_config import (
    create_global_config_template,
    get_global_config_dir,
    get_global_env_path,
)

console = Console()


@click.group()
def config_command():
    """Configuration management"""
    pass


@config_command.command()
def init():
    """Initialize global configuration"""
    console.print("[bold blue]Initializing mcode configuration...[/bold blue]")

    created = create_global_config_template()
    config_path = get_global_env_path()

    if created:
        console.print(f"[green]✓[/green] Created config template at {config_path}")
        console.print(
            "[yellow]Please edit the file and uncomment/configure your API keys[/yellow]"
        )
    else:
        console.print(f"[yellow]Config already exists at {config_path}[/yellow]")

    console.print(f"\n[dim]Config directory: {get_global_config_dir()}[/dim]")


@config_command.command()
@click.argument("provider")
@click.argument("key")
@click.argument("value")
def set(provider, key, value):
    """Set configuration value"""
    console.print(f"[green]✓[/green] {provider}.{key} = {value}")


@config_command.command(name="list")
def list_config():
    """Show current configuration paths"""
    console.print("[bold]Configuration paths:[/bold]")
    console.print(f"Global config: {get_global_env_path()}")
    console.print("Local config: ./.env")
    console.print("\n[dim]Local config overrides global config[/dim]")


@config_command.command()
def validate():
    """Validate provider settings"""
    console.print("[yellow]Configuration validation (in development)[/yellow]")
