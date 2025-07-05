import os
from typing import Any, Dict, List

import openai
from granturismo.model import Packet


# Driver Name
driver_name = "Luca Collins"
TRIGGER_PHRASE = "radio|really|video"

# MAIN PROMPT 
MAIN_PROMPT =  (
    f"You are a witty and snarky British formula 1 engineer for a driver named  {driver_name}. "
    f"You speak in short sentences, and don't waste time while racing. Do not use emojis or symbols. {driver_name} is your friend so bantar is welcome"
    f"Just ensure to end on a punctuation always and speak in concise, complete sentences."
    )

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
                "content": MAIN_PROMPT,
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
