import logging
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app import agent, store, whatsapp
from app.config import ROOT, settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("eknothi")

app = FastAPI(title="EkNothi")

RESET_WORDS = {"reset", "restart", "নতুন", "শুরু"}
UNSUPPORTED = "এখন আমি লেখা, ভয়েস নোট আর নথির ছবি বুঝতে পারি। অনুগ্রহ করে এর যেকোনো একটি পাঠান।"


@app.get("/health")
def health():
    return {"ok": True}


# ---------- WhatsApp ----------

@app.get("/webhook/whatsapp")
def verify(request: Request):
    q = request.query_params
    if q.get("hub.mode") == "subscribe" and q.get("hub.verify_token") == settings.wa_verify_token:
        return PlainTextResponse(q.get("hub.challenge", ""))
    raise HTTPException(status_code=403)


@app.post("/webhook/whatsapp")
async def incoming(request: Request, background: BackgroundTasks):
    body = await request.body()
    if not whatsapp.signature_ok(body, request.headers.get("X-Hub-Signature-256")):
        raise HTTPException(status_code=403)
    for msg in whatsapp.parse(await request.json()):
        if store.mark_seen(msg.message_id):
            background.add_task(handle_whatsapp, msg)
    return {"ok": True}  # answer fast; WhatsApp retries slow webhooks


def handle_whatsapp(msg: whatsapp.Incoming) -> None:
    try:
        if msg.kind == "other":
            whatsapp.send_text(msg.sender, UNSUPPORTED)
            return
        if msg.kind == "text" and msg.text.strip().lower() in RESET_WORDS:
            store.reset(msg.sender)
            whatsapp.send_text(msg.sender, "নতুন করে শুরু হলো। আপনার সমস্যাটি বলুন।")
            return

        kwargs = {}
        if msg.media_id:
            data, mime = whatsapp.download_media(msg.media_id)
            if msg.kind == "audio":
                kwargs.update(audio=data, audio_name="voice.ogg")
            else:
                kwargs.update(image=data, image_mime=mime)

        reply = agent.run(msg.sender, msg.text, **kwargs)
        whatsapp.send_text(msg.sender, reply.text)
        for path in reply.files:
            whatsapp.send_document(msg.sender, path, caption="আপনার এক নথি (মামলা-নথি)")
    except Exception:
        log.exception("failed to handle WhatsApp message %s", msg.message_id)
        try:
            whatsapp.send_text(msg.sender, agent.FALLBACK_REPLY)
        except Exception:
            log.exception("failed to send fallback reply")


# ---------- Web chat (same agent; the link judges can try) ----------

@app.post("/api/chat")
def chat(
    user_id: str = Form(...),
    text: str = Form(""),
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None),
):
    if text.strip().lower() in RESET_WORDS:
        store.reset(user_id)
        return {"reply": "নতুন করে শুরু হলো। আপনার সমস্যাটি বলুন।", "files": []}
    kwargs = {}
    if image:
        kwargs.update(image=image.file.read(), image_mime=image.content_type or "image/jpeg")
    if audio:
        kwargs.update(audio=audio.file.read(), audio_name=audio.filename or "voice.webm")
    reply = agent.run(f"web:{user_id}", text, **kwargs)
    return {"reply": reply.text, "files": [f"/files/{p.name}" for p in reply.files]}


# Case files are named by an unguessable token, not the user's number.
app.mount("/files", StaticFiles(directory=settings.files_dir), name="files")
app.mount("/", StaticFiles(directory=Path(ROOT / "web"), html=True), name="web")
