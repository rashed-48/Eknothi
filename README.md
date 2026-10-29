# EkNothi (এক নথি, "one file")

A legal aid agent for Bangladesh that works inside WhatsApp. People send a Bangla voice note or a photo of a
notice, land deed or court paper. EkNothi explains it in simple Bangla, checks whether they qualify for free
government legal aid, tells them where to go and what to bring, drafts their application, and builds one case
file they can hand to the legal aid office so they never have to tell their story again.

> Built for the **Meta Global AI Developer Hackathon** (Oct 26 – Nov 4, 2026), Indie Developer track,
> theme *Build for Your World*.
> The concept came from Legal Tech Hackathon 2026 (Bangladesh). **All code in this repository was written
> during the Meta hackathon, starting Oct 29, 2026**; see the commit history.

EkNothi gives legal *information*, not legal advice. It cites its sources, never claims to be a lawyer, and
hands serious or uncertain cases to the national legal aid helpline **16430** with the case file ready.

## Why it matters

Bangladesh has over 4 million cases pending in its lower courts. Most people facing unpaid wages, land
notices or family disputes cannot afford a lawyer, and many cannot read the documents they receive. Free
legal aid exists, but people don't know they qualify, which office to visit or what to bring.

## How it works

```
WhatsApp / web chat
      │  text · voice note · document photo
      ▼
 media.py ── voice note ──► Muse Voice Transcribe ──► Bangla text
          └─ photo ───────► Muse Spark (vision) ─────► structured document facts
      ▼
 agent.py  (Muse Spark Open, tool-calling loop)
      ├─ update_case        save facts to the case file
      ├─ retrieve_law       hand-checked legal sources, cited  (no model)
      ├─ check_eligibility  official legal aid criteria         (no model)
      ├─ find_office        district legal aid offices          (no model)
      ├─ draft_application  Bangla application from saved facts
      ├─ build_case_file    the "ek nothi" PDF
      └─ escalate_to_human  16430 / 999 / 109 handoff
      ▼
 Bangla reply + case file PDF back in the chat
```

| Meta model | Used for |
|---|---|
| Muse Spark Open (served on Baseten) | The agent: reasoning, tool calls, drafting. Open weights, so a legal aid office can run it on its own servers and case data never leaves the country. |
| Muse Spark (Meta Model API) | Reading photographed Bangla documents |
| Muse Voice Transcribe (Meta Model API) | Bangla voice notes |

All model access goes through [app/llm.py](app/llm.py); providers are configured in `.env`.

## Scope

Three case types: **unpaid wages**, **land notices**, **family cases**. Anything else is referred to 16430.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python -m playwright install chromium   # for PDF case files
cp .env.example .env            # fill in model + WhatsApp settings
uvicorn app.main:app --reload
```

Open http://localhost:8000 for the web chat. Run tests with `pytest`.

### WhatsApp

1. developers.facebook.com → create an app (Business) → add **WhatsApp** → **API Setup**.
2. Copy the test phone number ID and access token into `.env`; add your own number as a recipient.
3. Put the server on a public HTTPS address (deploy it, see below, or use a tunnel such as `ngrok http 8000`) and
   set the webhook to `https://<host>/webhook/whatsapp` with your `WHATSAPP_VERIFY_TOKEN`; subscribe to `messages`.
4. Send "hi" to the test number. Send "reset" or "নতুন" to start a new case.

## Deploy (Render)

The [Dockerfile](Dockerfile) bundles Chromium for the PDF case files; [render.yaml](render.yaml) describes the service.

1. render.com → **New → Blueprint** → this repo.
2. Fill in the values Render asks for (the same as your `.env`) → **Apply**.
3. When the deploy is live, open `https://<service>.onrender.com/health`; the web chat is at the root.
4. Set the WhatsApp webhook to `https://<service>.onrender.com/webhook/whatsapp`.

The free plan sleeps after 15 minutes idle and has no disk; a paid plan with a disk mounted at `/data` keeps
conversations and case files. Any Docker host works the same way ([railway.json](railway.json) is included):
set the `.env` variables, mount a volume at `/data`, expose `$PORT`.

## Evaluation

Scenarios live in [scenarios/](scenarios/). `python -m eval.run_eval` runs them all and writes a CSV with
automatic checks plus blank columns for a practising lawyer's verdict.

## Project layout

```
app/        FastAPI server, agent loop, tools, WhatsApp client, case file renderer
data/       legal sources, eligibility rules, office directory (hand-checked, lawyer-reviewed)
scenarios/  test cases
eval/       evaluation runner
web/        web chat (same agent as WhatsApp)
tests/      tests that need no model
```

## Status

- [x] Agent loop, tools, WhatsApp webhook, web chat, case file, eval runner
- [ ] Legal sources loaded into `data/legal/`
- [ ] Eligibility rules and office directory verified by a lawyer
- [ ] Switched to Muse Spark Open / Meta Model API
- [ ] 15–20 scenarios reviewed by a practising lawyer

## License

MIT
