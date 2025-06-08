import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class ChatMessage:
    """Single chat message"""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChatMessage":
        """Create from dictionary"""
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class ChatHistory:
    """Chat session history management"""

    def __init__(self, session_name: str):
        self.session_name = session_name
        self.messages: list[ChatMessage] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.metadata = {}

    def add_message(
        self, role: str, content: str, metadata: dict | None = None
    ) -> None:
        """Add new message to history"""
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages_for_llm(self) -> list[dict[str, str]]:
        """Get messages in format expected by LLM providers"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]

    def get_last_n_messages(self, n: int) -> list[ChatMessage]:
        """Get last N messages"""
        return self.messages[-n:] if n > 0 else self.messages

    def clear(self) -> None:
        """Clear all messages"""
        self.messages.clear()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "session_name": self.session_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
            "messages": [msg.to_dict() for msg in self.messages],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChatHistory":
        """Create from dictionary"""
        history = cls(data["session_name"])
        history.created_at = datetime.fromisoformat(data["created_at"])
        history.updated_at = datetime.fromisoformat(data["updated_at"])
        history.metadata = data.get("metadata", {})

        for msg_data in data.get("messages", []):
            history.messages.append(ChatMessage.from_dict(msg_data))

        return history

    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "ChatHistory":
        """Create from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
