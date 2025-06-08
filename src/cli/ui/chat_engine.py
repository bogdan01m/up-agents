# Import providers for registration
import src.llms.llm_call.llm_providers  # noqa: F401
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from src.cli.session import SessionManager
from src.llms.llm_call.base_provider import ProviderType
from src.llms.llm_call.provider_factory import ProviderFactory

console = Console()


class ChatEngine:
    def __init__(self, session_name: str = None, save_session: bool = True):
        self.provider = None
        self.session_manager = SessionManager()
        self.session_name = session_name
        self.save_session = save_session
        self._setup_session()

    def _setup_session(self):
        """Setup session based on session_name"""
        if self.session_name:
            # Try to load existing session
            existing = self.session_manager.load_session(self.session_name)
            if existing:
                console.print(
                    f"[dim]Loaded session: {self.session_name} ({len(existing.messages)} messages)[/dim]"
                )
            else:
                # Create new named session
                self.session_manager.create_session(self.session_name)
                console.print(f"[dim]Created new session: {self.session_name}[/dim]")
        else:
            # Create temporary session
            is_temp = not self.save_session
            self.session_manager.create_session(temp=is_temp)
            if is_temp:
                console.print("[dim]Using temporary session (not saved)[/dim]")

    def setup_provider(
        self,
        provider_name: str | None = None,
        model_name: str | None = None,
        system_prompt: str | None = None,
    ):
        """Setup LLM provider based on parameters or environment"""

        # If no provider specified, try to detect from environment or ask user
        if not provider_name:
            provider_name = self._select_provider_interactive()

        try:
            provider_type = ProviderType(provider_name.lower())
        except ValueError:
            available = [p.value for p in ProviderFactory.get_available_providers()]
            console.print(f"[red]Unknown provider: {provider_name}[/red]")
            console.print(f"Available providers: {', '.join(available)}")
            return False

        try:
            # Try to create provider from environment first
            self.provider = ProviderFactory.create_provider_from_env(
                provider_type=provider_type,
                model_name=model_name,
                system_prompt=system_prompt,
            )

            console.print(f"[green]✓[/green] Using {provider_type.value}")
            console.print(f"[dim]Model:[/dim] {self.provider.model_name}")
            if self.provider.system_prompt:
                console.print(
                    f"[dim]System prompt:[/dim] {self.provider.system_prompt}"
                )

            return True

        except Exception as e:
            console.print(f"[red]Failed to setup provider {provider_name}: {e}[/red]")
            console.print(
                "[yellow]Make sure you have the required API keys in your .env file[/yellow]"
            )
            return False

    def _select_provider_interactive(self) -> str:
        """Interactively select a provider"""
        available_providers = ProviderFactory.get_available_providers()

        console.print("[bold]Available providers:[/bold]")
        for i, provider in enumerate(available_providers, 1):
            console.print(f"  {i}. {provider.value}")

        while True:
            try:
                # Use input() instead of prompt() to avoid asyncio issues
                choice = input("Select provider (number or name): ")

                # Try as number first
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(available_providers):
                        return available_providers[idx].value

                # Try as provider name
                choice_lower = choice.lower()
                for provider in available_providers:
                    if provider.value == choice_lower:
                        return provider.value

                console.print("[red]Invalid choice. Try again.[/red]")

            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Cancelled[/yellow]")
                exit(1)

    async def single_query(self, message: str) -> str:
        """Send a single message and get response"""
        if not self.provider:
            console.print("[red]Provider not setup[/red]")
            return ""

        try:
            console.print(f"\n[bold blue]You:[/bold blue] {message}")

            with Live("[dim]Thinking...[/dim]", console=console) as live:
                # Get real LLM response
                response = await self._get_llm_response(message)
                live.update("")

            console.print("[bold green]Assistant:[/bold green]")
            console.print(Markdown(response))

            return response

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return ""

    async def interactive_chat(self):
        """Start interactive chat session"""
        if not self.provider:
            console.print("[red]Provider not setup[/red]")
            return

        console.print(
            Panel(
                "[bold green]Interactive Chat Mode[/bold green]\n"
                "Type your messages and press Enter. Use 'exit', 'quit', or Ctrl+C to stop.",
                title="🤖 mcode",
                border_style="green",
            )
        )

        try:
            while True:
                try:
                    message = input("You: ")

                    if message.lower() in ["exit", "quit", "bye"]:
                        break

                    if message.strip():
                        # Add user message to session
                        self.session_manager.add_message("user", message)

                        response = await self.single_query(message)

                        # Add assistant response to session
                        if response:
                            self.session_manager.add_message("assistant", response)

                        console.print()  # Empty line for spacing

                except EOFError:
                    break

        except KeyboardInterrupt:
            console.print("\n[yellow]Chat ended[/yellow]")

        # Save session if needed
        if self.save_session and self.session_manager.get_current_session():
            current_session = self.session_manager.get_current_session()
            if current_session.messages:
                try:
                    if self.session_name:
                        # Named session - save automatically
                        self.session_manager.save_current_session()
                        console.print(f"[dim]Session saved: {self.session_name}[/dim]")
                    else:
                        # Temporary session - ask for name
                        save_choice = input("Save this chat session? (Y/n): ").lower()
                        if save_choice in ["", "y", "yes"]:
                            session_name = input("Enter session name: ").strip()
                            if session_name:
                                current_session.session_name = session_name
                                self.session_manager.save_current_session()
                                console.print(
                                    f"[dim]Session saved as: {session_name}[/dim]"
                                )
                            else:
                                console.print("[dim]Session not saved[/dim]")
                except (EOFError, KeyboardInterrupt):
                    pass

    async def _get_llm_response(self, message: str) -> str:
        """Get real LLM response using the provider"""
        try:
            # Get conversation history for context
            messages = self.session_manager.get_messages_for_llm()

            # Add current message
            current_messages = messages + [{"role": "user", "content": message}]

            # Use the provider's get_response method with full context
            if hasattr(self.provider, "get_response_with_history"):
                response = await self.provider.get_response_with_history(
                    current_messages
                )
            else:
                # Fallback to single message if provider doesn't support history
                response = await self.provider.get_response(message)

            return response
        except Exception as e:
            # Fallback to simulation if LLM call fails
            console.print(
                f"[yellow]Warning: LLM call failed ({e}), using simulation[/yellow]"
            )
            return f"I'm a simulated response because the real LLM call failed. You said: '{message}'"
