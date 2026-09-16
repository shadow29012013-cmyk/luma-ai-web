from __future__ import annotations

import json
import os
from urllib import request
from urllib.error import HTTPError, URLError

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
        return bool(self.api_key) and self.api_key not in {
            "PASTE_A_NEW_KEY_HERE",
            "your_api_key_here",
        }

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
        except HTTPError as error:
            try:
                detail = error.read().decode("utf-8", errors="replace")
                provider_message = json.loads(detail).get("error", {}).get("message", detail)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                provider_message = "Nhà cung cấp không trả về chi tiết lỗi."
            return f"StudySync chưa nhận được phản hồi từ AI (HTTP {error.code}). {provider_message}"
        except URLError as error:
            return f"StudySync không kết nối được tới AI: {error.reason}."
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
            return f"StudySync nhận dữ liệu AI không đúng định dạng ({type(error).__name__})."
