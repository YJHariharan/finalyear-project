import os
from typing import Optional, Dict, Any

import requests
import streamlit as st


def _get_api_key() -> Optional[str]:
    """Resolve API key from Streamlit secrets or environment."""
    key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
    if not key:
        key = os.getenv("OPENAI_API_KEY")
    return key


class OpenAIService:
    """Lightweight client for text generation using OpenAI's Chat Completions API.

    Reads API key from Streamlit secrets or environment. Uses requests to avoid
    adding heavy dependencies. Designed for simple, robust usage within Streamlit.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        model: Optional[str] = None,
        timeout_seconds: int = 30,
    ) -> None:
        self.api_key = api_key or _get_api_key()
        self.base_url = base_url.rstrip("/")
        # Allow overriding via secrets/env to avoid hard-coding
        self.model = (
            model
            or (st.secrets.get("OPENAI_MODEL") if hasattr(st, "secrets") else None)
            or os.getenv("OPENAI_MODEL")
            or "gpt-4o-mini"
        )
        self.timeout_seconds = timeout_seconds

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate_text(
        self,
        prompt: str,
        *,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        """Generate text from a prompt using Chat Completions.

        Returns an empty string if not configured or on non-200 responses.
        """
        if not self.api_key:
            # In-app feedback is handled by caller; avoid raising in Streamlit flow.
            return ""

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": float(temperature),
            "max_tokens": int(max_tokens),
        }

        try:
            resp = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException:
            return ""

        if resp.status_code != 200:
            return ""

        try:
            data = resp.json()
            return (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
        except Exception:
            return ""


def get_openai_service() -> OpenAIService:
    """Convenience factory to use across the app."""
    return OpenAIService()