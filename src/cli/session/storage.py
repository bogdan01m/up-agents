import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path

from .chat_history import ChatHistory


class BaseStorage(ABC):
    """Base storage interface"""

    @abstractmethod
    def save_session(self, history: ChatHistory) -> None:
        """Save session to storage"""
        pass

    @abstractmethod
    def load_session(self, session_name: str) -> ChatHistory | None:
        """Load session from storage"""
        pass

    @abstractmethod
    def delete_session(self, session_name: str) -> bool:
        """Delete session from storage"""
        pass

    @abstractmethod
    def list_sessions(self) -> list[str]:
        """List all session names"""
        pass

    @abstractmethod
    def session_exists(self, session_name: str) -> bool:
        """Check if session exists"""
        pass


class JSONStorage(BaseStorage):
    """JSON file storage implementation"""

    def __init__(self, base_dir: Path | None = None):
        if base_dir is None:
            base_dir = Path.home() / ".mcode" / "sessions"

        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir
        self.temp_dir = self.base_dir / "temp"

        # Create directories if they don't exist
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_path(self, session_name: str, is_temp: bool = False) -> Path:
        """Get path for session file"""
        if is_temp:
            return self.temp_dir / f"{session_name}.json"
        return self.sessions_dir / f"{session_name}.json"

    def save_session(self, history: ChatHistory, is_temp: bool = False) -> None:
        """Save session to JSON file"""
        session_path = self._get_session_path(history.session_name, is_temp)

        try:
            with open(session_path, "w", encoding="utf-8") as f:
                f.write(history.to_json())
        except Exception as e:
            raise RuntimeError(f"Failed to save session {history.session_name}: {e}")

    def load_session(self, session_name: str) -> ChatHistory | None:
        """Load session from JSON file"""
        # Try regular sessions first, then temp
        for is_temp in [False, True]:
            session_path = self._get_session_path(session_name, is_temp)
            if session_path.exists():
                try:
                    with open(session_path, encoding="utf-8") as f:
                        return ChatHistory.from_json(f.read())
                except Exception as e:
                    raise RuntimeError(f"Failed to load session {session_name}: {e}")

        return None

    def delete_session(self, session_name: str) -> bool:
        """Delete session file"""
        deleted = False

        # Try both regular and temp directories
        for is_temp in [False, True]:
            session_path = self._get_session_path(session_name, is_temp)
            if session_path.exists():
                try:
                    session_path.unlink()
                    deleted = True
                except Exception:
                    pass

        return deleted

    def list_sessions(self, include_temp: bool = False) -> list[str]:
        """List all session names"""
        sessions = []

        # Regular sessions
        for file_path in self.sessions_dir.glob("*.json"):
            if file_path.is_file():
                sessions.append(file_path.stem)

        # Temp sessions if requested
        if include_temp:
            for file_path in self.temp_dir.glob("*.json"):
                if file_path.is_file():
                    sessions.append(f"temp/{file_path.stem}")

        return sorted(sessions)

    def session_exists(self, session_name: str) -> bool:
        """Check if session exists"""
        for is_temp in [False, True]:
            session_path = self._get_session_path(session_name, is_temp)
            if session_path.exists():
                return True
        return False

    def cleanup_temp_sessions(self, older_than_days: int = 7) -> int:
        """Clean up temporary sessions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        cleaned = 0

        for file_path in self.temp_dir.glob("*.json"):
            if file_path.is_file():
                # Check file modification time
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        cleaned += 1
                    except Exception:
                        pass

        return cleaned

    def get_session_info(self, session_name: str) -> dict | None:
        """Get session metadata without loading full history"""
        for is_temp in [False, True]:
            session_path = self._get_session_path(session_name, is_temp)
            if session_path.exists():
                try:
                    with open(session_path, encoding="utf-8") as f:
                        data = json.load(f)

                    return {
                        "name": session_name,
                        "created_at": data.get("created_at"),
                        "updated_at": data.get("updated_at"),
                        "message_count": len(data.get("messages", [])),
                        "is_temp": is_temp,
                    }
                except Exception:
                    pass

        return None
