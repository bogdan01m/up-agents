import click

# Импортируем провайдеры для регистрации
import src.llms.llm_call.llm_providers  # noqa: F401
from rich.console import Console
from rich.table import Table
from src.llms.llm_call.provider_factory import ProviderFactory

console = Console()


@click.group()
def providers_command():
    """LLM providers management"""
    pass


@providers_command.command()
def list():
    """Show available providers"""
    table = Table(title="Available LLM Providers")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")

    available_providers = ProviderFactory.get_available_providers()

    for provider in available_providers:
        table.add_row(provider.value, "✓ Available")

    console.print(table)


@providers_command.command()
@click.argument("provider")
def test(provider):
    """Test connection to provider"""
    console.print(f"[yellow]Testing {provider} (in development)[/yellow]")


@providers_command.command()
@click.argument("provider")
def info(provider):
    """Provider information"""
    console.print(f"[blue]Information about {provider} (in development)[/blue]")
