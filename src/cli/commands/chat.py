import asyncio

import click
from rich.console import Console
from src.cli.ui.chat_engine import ChatEngine

console = Console()


@click.command()
@click.option("--provider", "-p", help="LLM provider (openai, ollama, gemini, etc.)")
@click.option("--model", "-m", help="Model to use")
@click.option("--system-prompt", "-s", help="System prompt")
@click.option("--no-history", is_flag=True, help="Don't save chat history")
@click.argument("message", required=False)
def chat_command(provider, model, system_prompt, no_history, message):
    """Interactive chat with LLM"""
    console.print("[bold green]🤖 up-agents chat[/bold green]")

    # Run async chat
    asyncio.run(_run_chat(provider, model, system_prompt, no_history, message))


async def _run_chat(provider, model, system_prompt, no_history, message):
    """Async chat runner"""
    chat_engine = ChatEngine()

    # Setup provider
    success = chat_engine.setup_provider(
        provider_name=provider, model_name=model, system_prompt=system_prompt
    )

    if not success:
        return

    console.print()  # Empty line for spacing

    # Handle single message or interactive mode
    if message:
        await chat_engine.single_query(message)
    else:
        await chat_engine.interactive_chat(save_history=not no_history)
