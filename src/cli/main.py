import click
from rich.console import Console
from src.llms.llm_call.env_config import load_dotenv_if_exists

from .commands.chat import chat_command
from .commands.config import config_command
from .commands.providers import providers_command
from .commands.session import session_command

console = Console()

# Load .env file at startup
load_dotenv_if_exists()


@click.group()
@click.version_option(version="0.1.0", prog_name="mcode")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(verbose):
    """Terminal agent system with support for various LLM providers"""
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")


cli.add_command(chat_command, name="chat")
cli.add_command(config_command, name="config")
cli.add_command(providers_command, name="providers")
cli.add_command(session_command, name="session")


def main():
    """Entry point для CLI приложения"""
    cli()


if __name__ == "__main__":
    main()
