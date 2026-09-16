from __future__ import annotations

import json
import os
from urllib import request

from dotenv import load_dotenv

load_dotenv()


def _setting(name: str, default: str = "") -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value
    try:
        import streamlit as st

        secret_value = st.secrets.get(name, default)
        return str(secret_value).strip()
    except Exception:
        return default


class AIModel:
    """Kết nối API tương thích OpenAI, có câu trả lời dự phòng khi chưa cấu hình key."""

    def __init__(self) -> None:
        self.api_key = _setting("AI_API_KEY")
        self.api_url = _setting(
            "AI_API_URL", "https://api.openai.com/v1/chat/completions"
        )
        self.model_name = _setting("AI_MODEL", "gpt-4o-mini")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def reply(self, messages: list[dict[str, str]]) -> str:
        if not self.is_configured:
            return (
                "Mình đang ở chế độ mô phỏng. Bạn hãy tạo file .env và điền "
                "AI_API_KEY để kết nối AI thật nhé."
            )

        payload = json.dumps(
            {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "Bạn là trợ lý học tập thân thiện, trả lời ngắn gọn bằng tiếng Việt.",
                    },
                    *messages[-12:],
                ],
                "temperature": 0.7,
            }
        ).encode("utf-8")
        api_request = request.Request(
            self.api_url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with request.urlopen(api_request, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"].strip()
        except Exception as error:
            return f"StudySync chưa nhận được phản hồi từ AI ({type(error).__name__}). Kiểm tra API key và Secrets rồi thử lại."
