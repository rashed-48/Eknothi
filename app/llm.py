"""The only module that knows which model provider is in use.

Every model call in EkNothi goes through here. Switching from a stand-in
endpoint to the Meta Model API or Muse Spark Open on Baseten is a .env change.
If the Meta Model API turns out not to be OpenAI-compatible, adapt this file only.
"""

import base64
from functools import lru_cache

from openai import OpenAI

from app.config import settings


@lru_cache
def _client(base_url: str, api_key: str) -> OpenAI:
    if not base_url or not api_key:
        raise RuntimeError("Model endpoint not configured. Set LLM_BASE_URL and LLM_API_KEY in .env")
    return OpenAI(base_url=base_url, api_key=api_key)


def chat(messages: list[dict], tools: list[dict] | None = None, **kwargs):
    """Agent call. Returns the assistant message (may contain tool_calls)."""
    args = {"model": settings.llm_model, "messages": messages, **kwargs}
    if tools:
        args["tools"] = tools
    resp = _client(settings.llm_base_url, settings.llm_api_key).chat.completions.create(**args)
    return resp.choices[0].message


def complete(prompt: str, system: str | None = None, **kwargs) -> str:
    """Plain text generation with no tools, used for drafting."""
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    return chat(messages, **kwargs).content or ""


def read_image(image: bytes, mime: str, prompt: str) -> str:
    """Vision call: Muse Spark (multimodal) in production."""
    data_url = f"data:{mime};base64,{base64.b64encode(image).decode()}"
    resp = _client(settings.vision_base_url, settings.vision_api_key).chat.completions.create(
        model=settings.vision_model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }],
    )
    return resp.choices[0].message.content or ""


def transcribe(audio: bytes, filename: str, language: str = "bn") -> str:
    """Speech to text: Muse Voice Transcribe in production."""
    if not settings.asr_model:
        raise RuntimeError("ASR_MODEL not configured in .env")
    resp = _client(settings.asr_base_url, settings.asr_api_key).audio.transcriptions.create(
        model=settings.asr_model, file=(filename, audio), language=language
    )
    return resp.text
