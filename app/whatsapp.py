"""WhatsApp Cloud API: parse webhooks, download media, send replies."""

import hashlib
import hmac
from dataclasses import dataclass
from pathlib import Path

import httpx

from app.config import settings

MAX_TEXT = 4000  # WhatsApp limit is 4096


def _graph(path: str) -> str:
    return f"https://graph.facebook.com/{settings.graph_version}/{path}"


def _auth() -> dict:
    return {"Authorization": f"Bearer {settings.wa_token}"}


@dataclass
class Incoming:
    message_id: str
    sender: str  # the user's WhatsApp number
    kind: str  # text | image | audio | document | other
    text: str = ""
    media_id: str | None = None
    mime: str | None = None


def signature_ok(body: bytes, header: str | None) -> bool:
    if not settings.wa_app_secret:
        return True  # not configured (local testing)
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(settings.wa_app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.removeprefix("sha256="))


def parse(payload: dict) -> list[Incoming]:
    out = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            # Only new incoming messages; echoes of our own sends or history syncs must never get a reply.
            if change.get("field") != "messages":
                continue
            for m in change.get("value", {}).get("messages", []):
                kind = m.get("type")
                msg = Incoming(message_id=m["id"], sender=m["from"], kind=kind)
                if kind == "text":
                    msg.text = m["text"]["body"]
                elif kind in ("image", "audio", "document"):
                    media = m[kind]
                    msg.media_id, msg.mime = media["id"], media.get("mime_type")
                    msg.text = media.get("caption", "")
                else:
                    msg.kind = "other"
                out.append(msg)
    return out


def download_media(media_id: str) -> tuple[bytes, str]:
    with httpx.Client(timeout=30) as client:
        meta = client.get(_graph(media_id), headers=_auth()).raise_for_status().json()
        data = client.get(meta["url"], headers=_auth()).raise_for_status().content
    return data, meta.get("mime_type", "application/octet-stream")


def send_text(to: str, text: str) -> None:
    chunks = [text[i:i + MAX_TEXT] for i in range(0, len(text), MAX_TEXT)] or [""]
    with httpx.Client(timeout=30) as client:
        for chunk in chunks:
            client.post(
                _graph(f"{settings.wa_phone_number_id}/messages"),
                headers=_auth(),
                json={"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": chunk}},
            ).raise_for_status()


def send_document(to: str, path: Path, caption: str = "") -> None:
    mime = "application/pdf" if path.suffix == ".pdf" else "text/html"
    with httpx.Client(timeout=60) as client:
        upload = client.post(
            _graph(f"{settings.wa_phone_number_id}/media"),
            headers=_auth(),
            data={"messaging_product": "whatsapp", "type": mime},
            files={"file": (path.name, path.read_bytes(), mime)},
        ).raise_for_status().json()
        client.post(
            _graph(f"{settings.wa_phone_number_id}/messages"),
            headers=_auth(),
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "document",
                "document": {"id": upload["id"], "filename": f"ek-nothi{path.suffix}", "caption": caption},
            },
        ).raise_for_status()
