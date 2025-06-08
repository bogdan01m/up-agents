import uuid
from datetime import datetime
from typing import Any

from .chat_history import ChatHistory
from .storage import BaseStorage, JSONStorage


class SessionManager:
    """Manages chat sessions and their persistence"""

    def __init__(self, storage: BaseStorage | None = None):
        self.storage = storage or JSONStorage()
        self.current_session: ChatHistory | None = None

    def create_session(
        self, session_name: str | None = None, temp: bool = False
    ) -> ChatHistory:
        """Create new session"""
        if session_name is None:
            if temp:
                # Generate temporary session name with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                session_name = f"session_{timestamp}_{uuid.uuid4().hex[:8]}"
            else:
                session_name = "default"

        # Check if session already exists
        if self.storage.session_exists(session_name) and not temp:
            existing = self.storage.load_session(session_name)
            if existing:
                self.current_session = existing
                return existing

        # Create new session
        history = ChatHistory(session_name)
        self.current_session = history
        return history

    def load_session(self, session_name: str) -> ChatHistory | None:
        """Load existing session"""
        history = self.storage.load_session(session_name)
        if history:
            self.current_session = history
        return history

    def save_current_session(self, is_temp: bool = False) -> bool:
        """Save current session to storage"""
        if not self.current_session:
            return False

        try:
            self.storage.save_session(self.current_session, is_temp=is_temp)
            return True
        except Exception:
            return False

    def save_session(self, history: ChatHistory, is_temp: bool = False) -> bool:
        """Save specific session to storage"""
        try:
            self.storage.save_session(history, is_temp=is_temp)
            return True
        except Exception:
            return False

    def delete_session(self, session_name: str) -> bool:
        """Delete session from storage"""
        result = self.storage.delete_session(session_name)

        # If we deleted the current session, clear it
        if self.current_session and self.current_session.session_name == session_name:
            self.current_session = None

        return result

    def list_sessions(self, include_temp: bool = False) -> list[str]:
        """List all available sessions"""
        return self.storage.list_sessions(include_temp=include_temp)

    def get_session_info(self, session_name: str) -> dict[str, Any] | None:
        """Get session metadata"""
        return self.storage.get_session_info(session_name)

    def get_current_session(self) -> ChatHistory | None:
        """Get current active session"""
        return self.current_session

    def add_message(
        self, role: str, content: str, metadata: dict | None = None
    ) -> bool:
        """Add message to current session"""
        if not self.current_session:
            # Create temporary session if none exists
            self.create_session(temp=True)

        if self.current_session:
            self.current_session.add_message(role, content, metadata)
            return True
        return False

    def get_messages_for_llm(
        self, max_messages: int | None = None
    ) -> list[dict[str, str]]:
        """Get messages formatted for LLM"""
        if not self.current_session:
            return []

        messages = self.current_session.get_messages_for_llm()

        if max_messages and len(messages) > max_messages:
            # Keep system messages and last N messages
            system_messages = [msg for msg in messages if msg.get("role") == "system"]
            other_messages = [msg for msg in messages if msg.get("role") != "system"]

            if len(other_messages) > max_messages:
                other_messages = other_messages[-max_messages:]

            return system_messages + other_messages

        return messages

    def clear_current_session(self) -> bool:
        """Clear current session history"""
        if self.current_session:
            self.current_session.clear()
            return True
        return False

    def rename_session(self, old_name: str, new_name: str) -> bool:
        """Rename a session"""
        # Load old session
        old_session = self.storage.load_session(old_name)
        if not old_session:
            return False

        # Check if new name already exists
        if self.storage.session_exists(new_name):
            return False

        # Update session name and save with new name
        old_session.session_name = new_name
        old_session.updated_at = datetime.now()

        try:
            # Save with new name
            self.storage.save_session(old_session)
            # Delete old session
            self.storage.delete_session(old_name)

            # Update current session if it was the renamed one
            if self.current_session and self.current_session.session_name == old_name:
                self.current_session = old_session

            return True
        except Exception:
            return False

    def cleanup_temp_sessions(self, older_than_days: int = 7) -> int:
        """Clean up old temporary sessions"""
        if hasattr(self.storage, "cleanup_temp_sessions"):
            return self.storage.cleanup_temp_sessions(older_than_days)
        return 0

    def export_session(self, session_name: str, format: str = "json") -> str | None:
        """Export session in specified format"""
        history = self.storage.load_session(session_name)
        if not history:
            return None

        if format.lower() == "json":
            return history.to_json()
        elif format.lower() == "txt":
            lines = []
            lines.append(f"Session: {history.session_name}")
            lines.append(f"Created: {history.created_at}")
            lines.append(f"Updated: {history.updated_at}")
            lines.append("=" * 50)

            for msg in history.messages:
                lines.append(f"\n[{msg.timestamp}] {msg.role.title()}:")
                lines.append(msg.content)
                lines.append("-" * 30)

            return "\n".join(lines)

        return None
