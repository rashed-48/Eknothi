"""Turn attachments (document photos, voice notes) into text before the agent sees them."""

import json
import re

from app import llm
from app.prompts import DOCUMENT_PROMPT


def read_document(image: bytes, mime: str) -> dict:
    raw = llm.read_image(image, mime, DOCUMENT_PROMPT)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        return json.loads(match.group(0)) if match else {"raw": raw}
    except json.JSONDecodeError:
        return {"raw": raw}


def transcribe(audio: bytes, filename: str) -> str:
    return llm.transcribe(audio, filename, language="bn")
