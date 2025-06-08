import asyncio

import click
from rich.console import Console
from src.cli.ui.chat_engine import ChatEngine

console = Console()


@click.command()
@click.option("--provider", "-p", help="LLM provider (openai, ollama, gemini, etc.)")
@click.option("--model", "-m", help="Model to use")
@click.option("--system-prompt", "-s", help="System prompt")
@click.option("--session", help="Session name to use/create")
@click.option("--no-save", is_flag=True, help="Don't save session")
@click.argument("message", required=False)
def chat_command(provider, model, system_prompt, session, no_save, message):
    """Interactive chat with LLM"""
    console.print("[bold green]🤖 mcode chat[/bold green]")

    # Run async chat
    asyncio.run(_run_chat(provider, model, system_prompt, session, no_save, message))


async def _run_chat(provider, model, system_prompt, session, no_save, message):
    """Async chat runner"""
    chat_engine = ChatEngine(session_name=session, save_session=not no_save)

    # Setup provider
    success = chat_engine.setup_provider(
        provider_name=provider, model_name=model, system_prompt=system_prompt
    )

    if not success:
        return

    console.print()  # Empty line for spacing

    # Handle single message or interactive mode
    if message:
        # Add user message to session
        chat_engine.session_manager.add_message("user", message)

        response = await chat_engine.single_query(message)

        # Add assistant response to session
        if response:
            chat_engine.session_manager.add_message("assistant", response)

        # Save session if needed
        if not no_save and chat_engine.session_manager.get_current_session():
            current_session = chat_engine.session_manager.get_current_session()
            if current_session.messages and session:
                # Named session - save automatically
                chat_engine.session_manager.save_current_session()
                console.print(f"[dim]Session saved: {session}[/dim]")
    else:
        await chat_engine.interactive_chat()
