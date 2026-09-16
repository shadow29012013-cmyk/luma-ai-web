from __future__ import annotations

from database.chat_repository import ChatRepository
from model.ai_model import AIModel


class ChatBus:
    """Điều phối nghiệp vụ giữa giao diện, kho dữ liệu và model AI."""

    def __init__(self) -> None:
        self.repository = ChatRepository()
        self.ai_model = AIModel()

    def get_messages(self) -> list[dict[str, str]]:
        return self.repository.get_messages()

    def send_message(self, content: str) -> tuple[dict[str, str], dict[str, str]]:
        clean_content = content.strip()
        if not clean_content:
            raise ValueError("Tin nhắn không được để trống.")

        user_message = self.repository.add_message("user", clean_content)
        history = [
            {"role": item["role"], "content": item["content"]}
            for item in self.repository.get_messages()
        ]
        ai_message = self.repository.add_message("assistant", self.ai_model.reply(history))
        return user_message, ai_message

    def clear_chat(self) -> None:
        self.repository.clear_messages()
