import os
from typing import Any, Dict, List

import openai
from granturismo.model import Packet


class AIRacingEngineer:
    """Simple AI Racing Engineer using OpenAI's ChatCompletion API."""

    def __init__(self, api_key: str | None = None) -> None:
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OpenAI API key is required")
        openai.api_key = api_key
        try:
            self.client = openai.OpenAI(api_key=api_key)
        except AttributeError:
            # fallback for older openai versions
            self.client = openai

    def _packet_info(self, packet: Packet) -> Dict[str, Any]:
        info = {}
        for name in dir(packet):
            if name.startswith("_"):
                continue
            value = getattr(packet, name)
            if not callable(value):
                info[name] = value
        return info

    def answer(self, question: str, packet: Packet) -> str:
        context = self._packet_info(packet)
        messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are an AI Racing Engineer. Use the provided telemetry data to "
                    "answer the user's questions as briefly as possible."
                ),
            },
            {
                "role": "system",
                "content": f"Telemetry: {context}",
            },
            {"role": "user", "content": question},
        ]
        chat = self.client.chat.completions.create(
            model="gpt-4o-mini-realtime-preview-2024-12-17",
            messages=messages,
        )
        return chat.choices[0].message.content
