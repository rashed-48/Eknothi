"""The agent loop: user turn in -> tool calls -> Bangla reply (+ files) out.

Attachments are converted to text first (media.py), so the model reasons over
plain text and the case file keeps a record of every document received.
Only user/assistant text is kept in history; facts live in the case file.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

from app import llm, media, store, tools
from app.prompts import SYSTEM_PROMPT

log = logging.getLogger(__name__)

MAX_STEPS = 8
FALLBACK_REPLY = (
    "দুঃখিত, এই মুহূর্তে উত্তর দিতে সমস্যা হচ্ছে। জরুরি হলে জাতীয় আইনগত সহায়তা হেল্পলাইন ১৬৪৩০-এ ফোন করুন।"
)


@dataclass
class Reply:
    text: str
    files: list[Path] = field(default_factory=list)


def _case_context(case: dict) -> str:
    view = {k: case[k] for k in ("case_id", "facts", "eligibility", "office", "escalated")}
    view["documents"] = [d.get("doc_type") or "document" for d in case["documents"]]
    view["has_draft"] = case["draft"] is not None
    return "Current case file (JSON):\n" + json.dumps(view, ensure_ascii=False)


def _attachment_text(case: dict, image: bytes | None, image_mime: str,
                     audio: bytes | None, audio_name: str) -> list[str]:
    parts = []
    if audio:
        try:
            transcript = media.transcribe(audio, audio_name)
            case["transcripts"].append(transcript)
            parts.append(f"[ভয়েস নোট]: {transcript}")
        except Exception:
            log.exception("transcription failed")
            parts.append("[ভয়েস নোট পাঠানো হয়েছে, কিন্তু শোনা যায়নি। ব্যবহারকারীকে লিখে জানাতে বলুন।]")
    if image:
        try:
            doc = media.read_document(image, image_mime)
            case["documents"].append(doc)
            parts.append("[নথির ছবি পাঠানো হয়েছে। নথি থেকে পাওয়া তথ্য]: " + json.dumps(doc, ensure_ascii=False))
        except Exception:
            log.exception("document reading failed")
            parts.append("[নথির ছবি পাঠানো হয়েছে, কিন্তু পড়া যায়নি। আরও পরিষ্কার ছবি চাইতে বলুন।]")
    return parts


def run(user_id: str, text: str = "", *, image: bytes | None = None, image_mime: str = "image/jpeg",
        audio: bytes | None = None, audio_name: str = "voice.ogg") -> Reply:
    history, case = store.load(user_id)
    ctx = tools.ToolContext(user_id=user_id, case=case)

    user_content = "\n".join(_attachment_text(case, image, image_mime, audio, audio_name) + ([text] if text else []))
    history.append({"role": "user", "content": user_content or "(empty message)"})

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": _case_context(case)},
        *history[-store.MAX_HISTORY:],
    ]

    reply_text = FALLBACK_REPLY
    try:
        for _ in range(MAX_STEPS):
            msg = llm.chat(messages, tools=tools.schemas())
            if not msg.tool_calls:
                reply_text = msg.content or FALLBACK_REPLY
                break
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ],
            })
            for tc in msg.tool_calls:
                result = tools.execute(tc.function.name, tc.function.arguments, ctx)
                log.info("tool %s(%s) -> %s", tc.function.name, tc.function.arguments, str(result)[:300])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False, default=str),
                })
    except Exception:
        log.exception("agent turn failed for %s", user_id)

    history.append({"role": "assistant", "content": reply_text})
    store.save(user_id, history, case)
    return Reply(text=reply_text, files=ctx.files)
