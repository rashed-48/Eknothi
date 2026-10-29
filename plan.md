# EkNothi — Master Plan and Status

> **This file is the single source of truth for the project.**
> Read it fully before starting any work. Update it after every piece of work (see §0).
> Last updated: **2026-10-30**, switched host to Render free (Railway sign-ups closed) (Bangladesh time)

---

## 0. How to use this file

1. **Before work:** read §1–§4 for context, then §6 (status) and §8 (blockers) to see what to do next.
2. **After work:** in the same session, before stopping:
   - tick the finished items in §6 and move details from "Not yet implemented" to "Implemented";
   - add any new decision to §5 (decision log) with the reason;
   - update §8 (blockers / open questions);
   - add a dated entry to §10 (work log): what was done, what was verified, what is next;
   - update "Last updated" at the top;
   - commit `plan.md` together with the code change.
3. Never delete history from §5 or §10; mark superseded decisions instead.
4. All times are **Bangladesh time (BST, UTC+6)** unless written as ET.

---

## 1. Hackathon facts (what we are competing in)

**Event:** Meta Global AI Developer Hackathon, hosted by Meta and Cerebral Valley. Remote. $1M prize pool.
Event page: https://cerebralvalley.ai/e/meta-ai-developer-hackathon (participant details page needs login).

### 1.1 Key dates

| What | ET | Bangladesh |
|---|---|---|
| Building period | Oct 27 – Nov 4 | |
| Fireworks workshop | Fri Oct 30, 12:00 PM | Fri Oct 30, 10:00 PM |
| Discord office hours (#office-hours, weekdays, text only) | 10–11 AM | 8–9 PM until Oct 30; 9–10 PM from Nov 2 (US clocks change Nov 1) |
| Last full day for help | Tue Nov 3 | Tue Nov 3 – Wed Nov 4 morning |
| Meta credit claim deadline | Wed Nov 4, 9:00 PM | Thu Nov 5, 8:00 AM |
| **SUBMISSION DEADLINE** | **Wed Nov 4, 9:00 PM** | **Thu Nov 5, 8:00 AM** — target: submit by **Wed Nov 4 evening** |
| Judging | Nov 5 – Nov 8 | |
| Closing ceremony, top 10 announced, community vote opens | Mon Nov 9, 12:00 PM | Mon Nov 9, 11:00 PM |
| X engagement counted until | Nov 8 EOD | |
| Community vote winner | Nov 16 | |

### 1.2 Rules that can disqualify us

- **Repository must be public.**
- **New work only:** everything shown must be built during the event. The concept came from Legal Tech Hackathon 2026; say this clearly, and that all code was written during this hackathon (README already says so; repeat in video and submission).
- **Demo must only show what we built during the hackathon**, and judges must be able to tell what is new.
- **Must use Meta models** (Stage 1 pass/fail): Muse Spark series, Muse Wonder, Muse Image, Muse Voice Transcribe, SAM 3.1 via Meta Model API; open weights Muse Glimmer / Muse Spark Open; Muse Code coding agent.
- Only use code, data and assets we have rights to.
- **Banned / anti-projects** (avoid looking like these): medical or mental-health advice, **basic RAG apps**, simple image analyzers, simple education chatbots, job screeners, nutrition coaches, personality analyzers, sports coaches, anything political or about war.
  → EkNothi must be presented as an **agent that takes actions** (reads documents, checks eligibility, finds the office, drafts, builds a case file, escalates), with retrieval as one tool only. It gives **legal information, not legal advice**.
- Team max 4; solo allowed. One submission per team, by the Representative.

### 1.3 Submission requirements (CV platform)

- Public repo link
- **3-minute demo video** (YouTube unlisted is fine) showing only hackathon-built work — a primary judging artifact
- Live product link (our web chat)
- All team members listed
- Optional: X post link (Most Viral prize)
- Check repo and video links in a private browser window before submitting.

### 1.4 Judging

1. **Stage 1 (pass/fail):** fits a theme and really uses Meta models.
2. **Stage 2 (0–10 each):** Impact 30% · Use of Meta AI tooling 25% · Demo 25% · Technical depth & execution 20%.
3. **Stage 3:** top 5 per track ranked live from demo videos.

### 1.5 Prizes we target

| Prize | Amount | How we compete |
|---|---|---|
| Indie Developer track | $150K / 100K / 75K / 50K / 25K | Main entry |
| Best Build on Meta Open Weights | $10K | Agent runs on **Muse Spark Open** via Baseten/Modal |
| Best Agentic Use-Case | $5K | Multi-step agent with tools and handoff |
| Most Viral (X) | $20K | Post demo on X after submitting, submit post link |
| Community Vote | $10K | Share gallery link in Bangladeshi tech/legal groups after Nov 9 |

### 1.6 Credits and resources

- **Meta Model API:** $150 credits via claim form (each person individually). Needs a **credit card** on the Billing page; a temporary pre-auth hold appears. **Set a spend limit** on Billing. Claim by Nov 4, 9 PM ET.
- **Baseten:** $100 + 2M TPM (up to 2,000 participants, reviewed). Model name for the hackathon: **`meta-models/muse-spark-open-1026`** (not the one in their docs).
- **Modal:** $100 (first 1,000).
- **Fireworks:** shortlisted teams only.
- Discord channels: #announcements, #questions (CV team), #office-hours (Meta team), #team-search, Baseten channel.

---

## 2. The idea

**EkNothi (এক নথি, "one file")** — a legal aid agent for Bangladesh that works inside WhatsApp (plus a web chat with the same agent).

### 2.1 Problem
- Over 4 million cases pending in Bangladesh's lower courts.
- People with land disputes, unpaid wages, family problems or police notices cannot afford a lawyer; many cannot read the documents they receive.
- Free government legal aid exists (NLASO — since the 2026 amendment **বাংলাদেশ আইনগত সহায়তা অধিদপ্তর**; district legal aid offices; helpline **16430**), but people don't know they qualify, which office to go to, or what to bring. They pay middlemen, miss deadlines, give up, and must retell their story every time.

### 2.2 Users
Low-income people in Bangladesh who use WhatsApp, may have low literacy, and speak Bangla. Demo persona: **a garment worker in Gazipur with three months of unpaid wages.**

### 2.3 What the agent does
A user sends a **Bangla voice note** or a **photo** of a notice, land deed or court paper. The agent:
1. Reads the document and understands the spoken problem.
2. Explains in simple Bangla what is happening, their rights and any deadline — with cited sources.
3. Checks whether they qualify for free legal aid and tells them exactly where to go and what to bring.
4. Drafts their legal aid application or complaint.
5. Builds one structured **case file (the "ek nothi") PDF** they can share with the legal aid office or a lawyer.
6. Hands serious, urgent or uncertain cases to a human (16430; 999 and 109 for violence) with the case file ready.

### 2.4 Why Meta's models
- Legal problems are private. **Open weights (Muse Spark Open)** let a government or NGO legal aid office run the agent on its own servers, so case data never leaves the country.
- Meta's multimodal models read photographed documents and handle Bangla voice.

### 2.5 Safety design
- Law, procedure and deadlines come **only** from hand-checked sources in `data/legal/`, cited as `[উৎস: source, section]`. No source → "not sure, call 16430". Never invent sections, deadlines, fees or addresses.
- Never claims to be a lawyer; framed as legal information.
- Violence / danger / child at risk / self-harm → 999 and 109 first, urgent escalation, no further analysis.
- Eligibility rules and office directory are data files reviewed by a practising lawyer; until verified, results are labelled "preliminary".

### 2.6 Scope (deliberately narrow)
Three case types: **unpaid wages**, **land notices**, **family cases**. Drop family if time runs short. Everything else → 16430. Office directory: 2–3 districts only (Dhaka, Gazipur, Narayanganj).

### 2.7 Demo goal
A working WhatsApp bot + web chat, tested on **15–20 realistic scenarios**, answers **reviewed by a practising lawyer**.

### 2.8 Winning strategy
1. A real working WhatsApp demo beats slides: photo of a notice → Bangla explanation → case file in the chat.
2. "Checked by a practising lawyer" is the strongest credibility line — line up the lawyer early.
3. Tell **one person's story** in the video.
4. Keep scope narrow; polish over breadth.
5. Combine several Meta models (Spark Open for the agent, Spark vision for documents, Voice Transcribe for voice, optionally SAM 3.1 to crop messy document photos) to score on "Use of Meta AI tooling".

### 2.9 Demo video script (3 minutes)
- **0:00–0:20** Rahima, a garment worker in Gazipur, 3 months unpaid, can't afford a lawyer.
- **0:20–1:50** Real phone screen recording: voice note + photo → Bangla explanation with deadline and source → eligibility → office and documents to bring → drafted application → case file PDF arrives.
- **1:50–2:30** Architecture: which Meta model does what; Muse Spark Open on Baseten; cited sources; 16430 handoff; what was built during the hackathon.
- **2:30–3:00** Results: "N/20 scenarios correct, reviewed by Advocate X". Close with 4M+ pending cases.

---

## 3. Architecture

```
WhatsApp (Cloud API test number)      Web chat (web/index.html)
            │  text · voice note · document photo  │
            └───────────────┬───────────────────────┘
                            ▼
                 app/main.py  (FastAPI)
                            ▼
 app/media.py ── voice ─► llm.transcribe  (Muse Voice Transcribe)
              └─ photo ─► llm.read_image  (Muse Spark vision) → structured JSON
                            ▼
 app/agent.py  tool-calling loop (Muse Spark Open), max 8 steps
     ├─ update_case        save facts                         (no model)
     ├─ retrieve_law       data/legal/*.json, cited           (no model)
     ├─ check_eligibility  data/eligibility.json              (no model)
     ├─ find_office        data/offices.json                  (no model)
     ├─ draft_application  llm.complete with DRAFT_PROMPT
     ├─ build_case_file    app/case_file.py → HTML → PDF (Chromium)
     └─ escalate_to_human  16430 / 999 / 109 + case file
                            ▼
 app/store.py  SQLite: per-user history (last 20 msgs) + case JSON; webhook dedupe
                            ▼
 Bangla reply + case file document back to the user
```

**Model mapping (target):**

| Role | Model | Provider | `.env` keys |
|---|---|---|---|
| Agent (reasoning, tools, drafting) | Muse Spark Open `meta-models/muse-spark-open-1026` | Baseten (or Modal) | `LLM_*` |
| Document reading | Muse Spark (multimodal) | Meta Model API | `VISION_*` |
| Voice notes | Muse Voice Transcribe | Meta Model API | `ASR_*` |
| Optional: crop document from messy photo | SAM 3.1 | Meta Model API | (not yet) |
| Optional: Bangla voice replies | Meta MMS-TTS (open, supports Bengali) | self-hosted | (not yet) |

**Stand-in until the Muse key arrives:** `openai/gpt-oss-120b` on Groq (`LLM_BASE_URL=https://api.groq.com/openai/v1`). Groq no longer serves Llama chat models, so this is not a Meta model — it must be fully removed before submission.

---

## 4. Repository and how to run

- Local path: `E:\eknothi`
- GitHub: https://github.com/rashed-48/Eknothi (public, `origin`, branch `main`)
- Stack: Python 3.11, FastAPI, OpenAI SDK (as a generic client), SQLite, Jinja2, Playwright (PDF), httpx.

```
app/
  config.py        settings from .env (LLM_*, VISION_*, ASR_*, WHATSAPP_*)
  llm.py           ONLY module that talks to model providers
  prompts.py       system prompt, document-reading prompt, drafting prompts
  agent.py         tool-calling loop; attachments → text first
  media.py         read_document (JSON extraction), transcribe
  store.py         SQLite store, new_case() schema, dedupe
  case_file.py     Jinja2 HTML → PDF via Playwright Chromium (HTML fallback)
  whatsapp.py      webhook parsing, signature check, media download, send text/document
  main.py          routes: /health, /webhook/whatsapp (GET verify, POST), /api/chat, /files, / (web)
  tools/           registry.py (decorator + schemas + execute), legal.py, case.py
  templates/case_file.html
  fonts/           NotoSansBengali.ttf (SIL OFL) — bundled so PDFs render offline
data/
  eligibility.json offices.json legal/README.md legal/_example.json
  legal/labour_act_2006_wages.json legal/legal_aid_act_2000.json  (exact text from bdlaws, verified:false)
scenarios/         wages_01, land_01, family_01 (.yaml)
eval/run_eval.py   runs scenarios → eval/results_*.csv with lawyer columns
web/index.html     web chat (text, photo, voice)
tests/test_tools.py 15 tests, no model or network needed
```

**Run:**
```
cd E:\eknothi
.venv\Scripts\activate
copy .env.example .env        # then fill in keys
uvicorn app.main:app --reload # http://localhost:8000
pytest                        # tests
python -m eval.run_eval       # scenarios → CSV for lawyer
```
PDF: Playwright is in requirements; also run `python -m playwright install chromium` once.
WhatsApp: webhook URL `https://<deployed host>/webhook/whatsapp` (local tunnels don't work on this machine, see §5).
Docker: `docker build -t eknothi .` then `docker run --env-file .env -p 8000:8000 -v eknothi-data:/data eknothi`. Deploy steps in README.
Chat commands: "reset" / "নতুন" / "শুরু" start a new case.

**Case JSON schema** (`store.new_case()`): `case_id`, `file_token` (unguessable file name), `created_at`, `facts{name, phone, district, case_type, monthly_income_bdt, employer, opposing_party, key_dates, deadline, summary, help_wanted}`, `documents[]`, `transcripts[]`, `sources[]`, `eligibility`, `office`, `draft{kind,text}`, `escalated{reason,urgent}`.

---

## 5. Decision log

| Date | Decision | Why |
|---|---|---|
| 10-29 | Indie Developer track, theme "Build for Your World" | Individual/student builder; local real-world problem |
| 10-29 | WhatsApp only (no Messenger) | Messenger needs a Page + app review; one channel done well |
| 10-29 | WhatsApp Cloud API **test number** | Works with up to 5 recipient numbers without business verification |
| 10-29 | Also build a **web chat** using the same agent | Judges can't message the test number; it is the "live product" link |
| 10-29 | Python + FastAPI | Simplest for webhooks and AI work |
| 10-29 | All model calls behind `app/llm.py`, OpenAI-compatible client, configured by `.env` | Muse key not yet available; switch providers without code changes |
| 10-29 | Separate `LLM_*`, `VISION_*`, `ASR_*` settings | Agent on Baseten (open weights prize) while vision/voice use Meta Model API |
| 10-29 | Attachments converted to text **before** the agent loop | Deterministic; case file keeps every document; model reasons over text |
| 10-29 | Only user/assistant text kept in history; facts live in the case JSON | Avoids broken tool-call pairs when trimming history |
| 10-29 | Law, eligibility and offices come from data files, not the model | Safety; avoids hallucinated law; lawyer can review the files |
| 10-29 | Simple keyword retrieval, no vector DB | Small corpus; avoids looking like "basic RAG" |
| 10-29 | PDF via headless Chromium (Playwright), HTML fallback | Most Python PDF libraries break Bangla conjuncts |
| 10-29 | Case files named by random token, served at `/files/` | Don't expose phone numbers in URLs |
| 10-29 | Data files ship with `verified: false` and null gaps | Never invent legal facts; bot says "preliminary" until verified |
| 10-29 | 15–20 scenarios (not 30+) | Quality of lawyer review over quantity in 6 days |
| 10-29 | MIT license, public repo | Rules require a public repo |
| 10-29 | Stand-in model: `openai/gpt-oss-120b` on Groq (supersedes "a Llama stand-in") | The Groq account offers no Llama chat models (only Prompt Guard); gpt-oss-120b is the best tool-calling model there; stand-in only |
| 10-29 | Rules that must always hold are enforced in code, not only in the prompt: WhatsApp formatting + helpline digits (`agent.whatsapp_format`), draft date, no markdown in drafts, case file built inside `draft_application` | The stand-in ignored these prompt rules in the first conversation |
| 10-29 | Phone numbers always in English digits (16430, 999, 109) | Bangla digits are not tap-to-call in WhatsApp; eval `must_mention` checks "16430" |
| 10-29 | `llm.chat` retries Groq `output_parse_failed` / `tool_use_failed` (2 retries) and 429s (`max_retries=5`) | Sampled output sometimes fails the host's parser/schema check; a retry fixes it. Provider quirk stays inside `llm.py` |
| 10-29 | Legal chunks: exact bdlaws text; amendment markers `2[ত্রিশ]` resolved to the amended words; footnotes (amendments, SRO in-force districts) kept in `notes`; bdlaws font-conversion typos kept as published | "Copy exactly" while staying readable; in-force info is needed per district |
| 10-29 | `keywords` field on legal chunks, scored by `retrieve_law` | Users say বেতন, the Act says মজুরী; plain keyword overlap missed every wages question |
| 10-29 | Bundle Noto Sans Bengali (`app/fonts/`); PDF render blocks all network requests | Deterministic PDF offline/on any server; tests stay network-free (2.4 s instead of 12 s) |
| 10-29 | After drafting the bot sends a one-line summary, not the full draft; code strips ``` fences | Full draft pasted in a code block was unreadable on a phone; the draft is in the case file |
| 10-29 | Phone numbers of real people (e.g. WhatsApp recipient numbers) never go into the repo | Repo is public |
| 10-30 | Host on **Railway** from GitHub with the Dockerfile (+ volume at `/data`), deployed early instead of using a local tunnel | Tunnels failed on this machine: ISP/network resets `api.trycloudflare.com`; ngrok 3.39 flagged by Defender as PUA (not overridden); Claude Code auto mode blocks starting inbound tunnels. A deployed URL is needed anyway for the live product link; Railway doesn't sleep (Render free does, ~50 s cold start) and has volumes |
| 10-30 | Base image `python:3.11-slim-bookworm` | Playwright 1.49 `--with-deps` fails on Debian 13 (renamed font packages) |
| 10-30 | `railway.json` sets health check `/health` and restart policy | Fewer manual dashboard steps |
| 10-30 | **Supersedes Railway:** host on **Render free** via `render.yaml` blueprint (Docker, Singapore, `/health`) — user's choice | Railway sign-ups disabled after its Oct 21 incident. Render free: no card, but sleeps after 15 min (~50 s cold start) and no disk (data resets on restart). Consider Render Starter + disk for judging (Nov 5–8). `railway.json` kept for any later move |
| 10-29 | `check_eligibility.categories` is an enum built from `eligibility.json` | Model invented category keys (`unpaid_wages`, `monthly_income`) that never matched |

---

## 6. Status

### 6.1 Implemented (commit `ce9dc91`, 2026-10-29)

- [x] **Project skeleton** at `E:\eknothi`, git initialised on `main`, venv `.venv` with requirements installed.
- [x] **`app/llm.py`** — `chat()`, `complete()`, `read_image()` (base64 data URL), `transcribe()` (language `bn`); clear error if endpoint not configured.
- [x] **`app/agent.py`** — loop of up to 8 tool steps; injects case summary as a system message; Bangla fallback reply on any failure; returns text + files.
- [x] **`app/media.py`** — document photo → JSON (`doc_type, issuing_authority, case_number, parties, dates, what_it_asks, summary_bn, unreadable_or_uncertain`); voice → text.
- [x] **Tools** (`app/tools/`): `update_case`, `retrieve_law`, `check_eligibility`, `find_office`, `draft_application`, `build_case_file`, `escalate_to_human`; registry with JSON schemas; bad arguments return errors instead of crashing.
- [x] **System prompt** (`app/prompts.py`): Bangla, scope, safety override, citation rule, workflow.
- [x] **`app/store.py`** — SQLite conversations + case JSON; `reset()`; `mark_seen()` for WhatsApp retry dedupe.
- [x] **`app/whatsapp.py`** — webhook parsing (text/image/audio/document), HMAC signature check (if `WHATSAPP_APP_SECRET` set), media download, send text (chunked at 4000), upload + send document.
- [x] **`app/main.py`** — routes; WhatsApp work runs in background so webhook answers fast; reset words.
- [x] **Case file template** (`app/templates/case_file.html`) — Bangla, Noto Sans Bengali; facts, documents, transcripts, eligibility, office, draft, sources, escalation banner, "not legal advice" footer.
- [x] **Web chat** (`web/index.html`) — WhatsApp-like UI, text + photo + voice recording, case file link.
- [x] **Data placeholders** — `eligibility.json` (10 candidate categories, null income limit, documents list, `verified:false`), `offices.json` (16430 + Dhaka/Gazipur/Narayanganj with null address/phone/hours), `data/legal/` format and source list.
- [x] **Scenarios** — `wages_01`, `land_01`, `family_01` (violence → must escalate).
- [x] **Eval runner** — automatic checks (case type, escalation, must-mention) + blank lawyer verdict columns; CSV in UTF-8 with BOM for Excel.
- [x] **README** — idea, architecture, model table, hackathon new-work statement, run instructions.

**Verified:** 11 tests pass; server starts; `/health` 200; web page loads; webhook verification rejects wrong token; `/api/chat` without a model returns the Bangla fallback (no crash).

#### First real conversation (2026-10-29, stand-in `openai/gpt-oss-120b` on Groq)
- [x] `.env` filled (Groq). Fixed: key had been pasted inside `<...>`; `llama-3.3-70b-versatile` not available → gpt-oss-120b.
- [x] Garment-worker story (wages_01 + "yes, write the application") run through `agent.run` and through `POST /api/chat`.
- [x] Tools called in the right order: `update_case`, `retrieve_law` (empty → says "not sure, call 16430"), `check_eligibility` (`worker_low_income`, preliminary), `find_office` (Gazipur), `draft_application` → case file built and attached (HTML; Playwright not installed yet).
- [x] Fixes from the run: eligibility category enum; Groq parse/tool-validation retries; `whatsapp_format` (`**`→`*`, no `#`, helplines in English digits); fallback reply uses 16430; draft gets today's date (BD time), no markdown, no invented hardships; `draft_application` builds the case file; prompt: no unsourced procedure claims (with wrong/right example), 999/109 only for danger, no repeated tool calls.
- [x] 3 new tests (eligibility enum, draft → case file without markdown, `whatsapp_format`) — 14 pass.
- **Still wrong:** the model sometimes states procedure without a source (e.g. "must file in the labour court"). Needs legal data (D) + eval scenarios (G) to catch it; re-check on Muse.

#### Legal data, PDF, web chat (2026-10-29)
- [x] `data/legal/labour_act_2006_wages.json` — শ্রম আইন ২০০৬ ধারা ৩০, ৩৩, ১২১, ১২৩, ১২৪ক, ১৩২, ২১৩ (7 chunks).
- [x] `data/legal/legal_aid_act_2000.json` — আইনগত সহায়তা প্রদান আইন ২০০০ as amended 2026: ধারা ২(খ), ১৬, ২১খ, তফসিল (4 chunks).
- [x] All copied from bdlaws.minlaw.gov.bd with URLs, `verified: false`; README documents fields and lawyer questions.
- [x] `retrieve_law` scores `keywords`, returns `notes` and `verified`. Prompt: check notes against the person's district.
- [x] PDF: Playwright + Chromium installed; bundled font; network blocked during render; conjuncts checked visually; facts in fixed order; BD time stamp.
- [x] Web chat renders `*bold*` (DOM nodes, HTML stays escaped).
- [x] Re-ran wages story: cites ধারা ১৩২ "12 months" correctly; with prompt fixes no invented gratuity/999/ধারা ৩৩; PDF attached.

**Not verified yet:** WhatsApp end to end, voice and photo input with a real model.

### 6.2 Not yet implemented — in order

#### A. Setup and accounts (user)
- [x] Create GitHub repo https://github.com/rashed-48/Eknothi (public) and push `main` — done 10-29.
- [ ] Submit the Meta credit claim form; add card on Billing; set $150 spend limit.
- [ ] Request Baseten credits (and Modal as backup).
- [ ] Contact the lawyer; agree review of ~20 answers on Nov 2–3; ask permission to name them.
- [x] Get a stand-in API key; fill `.env` — Groq, done 10-29.
- [ ] Join Discord, post in #intros.

#### B. First real conversation (stand-in model)
- [x] Fill `.env` (`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`; a model that supports tool calling).
- [x] Chat through the agent and `/api/chat`; tools are called (see §6.1 "First real conversation").
- [x] Tune system prompt / add code guards (first pass).
- [ ] Try it yourself in the browser at http://localhost:8000.
- [x] Web chat renders WhatsApp `*bold*` as bold — done 10-29.
- **Done (10-29):** the wages story gets eligibility, office and a draft through tool calls.

#### C. WhatsApp end to end
- [x] Meta developer app `EkNothi` → WhatsApp use case → test number +1 555-634-4621; user's phone added as recipient — 10-30.
- [x] `.env`: `WHATSAPP_TOKEN` (temporary, 24 h), `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_APP_SECRET`, `WHATSAPP_VERIFY_TOKEN` — token checked against Graph API (200, quality GREEN).
- [x] Webhook verify (right token → challenge, wrong → 403) and signature check (unsigned POST → 403) tested locally and in the container.
- [x] Webhook `https://eknothi.onrender.com/webhook/whatsapp` verified; only `messages` subscribed — 10-30.
- [ ] Test text, voice note (OGG/Opus — may need ffmpeg conversion for the ASR model), image, case file document.
- [x] Permanent System User token `eknothi-bot` (never expires; whatsapp_business_messaging + management) in `.env` and Render — 10-30.
- [x] App subscribed to the WABA (`POST /{waba}/subscribed_apps`, run by user) — without it Meta never forwards messages — 10-30.
- **Done when:** a phone sends a voice note + photo and receives a Bangla reply and the PDF.

#### D. Legal data (user, with lawyer)
- [x] `data/legal/legal_aid_act_2000.json` — Act (as amended 2026) ধারা ২(খ), ১৬, ২১খ, তফসিল. **Regulations (income limit) still missing** — not on bdlaws.
- [x] `data/legal/labour_act_2006_wages.json` — ধারা ৩০, ৩৩, ১২১, ১২৩, ১২৪ক, ১৩২, ২১৩.
- [ ] `data/legal/land_notice.json` — procedure behind the notices used in the demo.
- [ ] `data/legal/family.json` — only if time allows. Note: তফসিল item 1 (পারিবারিক আদালত আইন ২০২৩ ধারা ৫) and 8 (যৌতুক) need mandatory pre-case mediation in 10 districts — a strong, sourced answer for family cases.
- [ ] Fill `eligibility.json` (income limit + period, real category list, documents) → `verified: true`, `verified_by`.
- [ ] Fill `offices.json` addresses/phones/hours for 3 districts from nlaso.gov.bd → `verified: true`.
- Sources: bdlaws.minlaw.gov.bd, nlaso.gov.bd. Copy text exactly with section numbers.

#### E. Case file PDF
- [x] Install Playwright + Chromium; render a case with Bangla text; conjuncts look right — 10-29.
- [x] Bundle Noto Sans Bengali locally; block network during render — 10-29.

#### F. Switch to Meta models (when key arrives)
- [ ] Read Muse quickstart + model list; check OpenAI compatibility (if not, adapt only `app/llm.py`).
- [ ] Test Muse Voice Transcribe on 5 real Bangla voice notes.
- [ ] Test Muse Spark vision on 5 real notice/deed photos.
- [ ] Agent on Muse Spark Open via Baseten (`meta-models/muse-spark-open-1026`).
- [ ] Remove the stand-in model entirely; every model call goes to Meta.
- [ ] Optional: SAM 3.1 to crop documents before reading.
- [ ] Optional: Bangla voice replies (MMS-TTS) — only if time allows.

#### G. Scenarios and evaluation
- [ ] Write 15–20 scenarios (~6 per case type, 2–3 that must escalate), with anonymised document photos in `scenarios/images/`.
- [ ] Run `python -m eval.run_eval`; fix failures.
- [ ] Send CSV to lawyer; apply fixes; re-run; record final numbers here.

#### H. Deployment
- [x] `Dockerfile` (bookworm, Chromium headless shell, `/data` volume, `$PORT`), `.dockerignore`, `railway.json` — 10-30.
- [x] Built and ran the image locally: `/health`, web page, webhook verify/signature, PDF rendered in container (Bangla OK, BD time), one `/api/chat` turn through Groq.
- [x] `render.yaml` blueprint (free, Singapore, Docker, health check, secrets prompted with `sync: false`) — 10-30.
- [ ] ~~User: Railway project~~ — Railway sign-ups closed (10-30).
- [x] Deployed on Render: https://eknothi.onrender.com — `/health`, web chat, webhook verify/signature and one chat turn checked from outside — 10-30.
- [ ] Point WhatsApp webhook to the deployed URL. (`PUBLIC_BASE_URL` is not used by the code; no need to set it.)
- [ ] Test the full flow on a phone 3 times.

#### I. Submission package
- [ ] README: demo GIF, final model table, eval results, lawyer credit, "built during hackathon" section.
- [ ] Record and upload 3-minute video (script §2.9); check link in private window.
- [ ] Submit on CV platform by **Wed Nov 4 evening BD time** (repo, video, live link, team).
- [ ] Post on X; submit the post link. Share for community vote after Nov 9.

---

## 7. Timeline (Bangladesh time)

| Day | Plan |
|---|---|
| **Thu Oct 29** | ✅ Skeleton. Repo on GitHub, credits, lawyer contact, stand-in model, first conversation (A, B) |
| **Fri Oct 30** | WhatsApp end to end (C); start legal data (D); Fireworks workshop 10 PM |
| **Sat Oct 31** | Legal data + eligibility + offices (D); PDF (E); switch to Muse if key arrived (F) |
| **Sun Nov 1** | Finish Meta switch (F); polish conversation; deploy (H) |
| **Mon Nov 2** | Write and run 15–20 scenarios; send to lawyer (G) |
| **Tue Nov 3** | Apply lawyer fixes; README; phone tests; ask last questions in office hours |
| **Wed Nov 4** | Record video; **submit by evening**; post on X (I) |

---

## 8. Blockers and open questions

| Item | Status | Owner |
|---|---|---|
| Muse / Meta Model API key | **Waiting** (credits arrive in batches; ask in #questions if not by Oct 30) | User |
| Lawyer for review | Unknown — confirm contacted | User |
| Baseten / Modal credits | Unknown — confirm requested | User |
| Does Muse Voice Transcribe handle Bangla well? | Untested | — |
| Does Muse Spark read Bangla legal documents well? | Untested | — |
| Is the Meta Model API OpenAI-compatible? | Unknown — check quickstart | — |
| Official legal aid income limit and categories | Unknown — from regulations, lawyer verifies | User + lawyer |
| Stand-in model states procedure without a source | Seen in first conversation; prompt alone doesn't stop it. Legal data (D) + eval (G); re-check on Muse | — |
| Groq free tier rate limits | Each turn waits on several 429 retries (~30–60 s). Fine for dev; not for demo | — |
| Lawyer: does ধারা ৩৩ (grievance to employer in 30 days) apply to unpaid wages, or only ধারা ১৩২? | The model applied ৩৩ to wages in one run | Lawyer |
| Lawyer: is the 2026 mandatory mediation (ধারা ২১খ, তফসিল) list of districts current? Dhaka/Gazipur/Narayanganj not in it as copied | Copied from bdlaws footnotes 10-29 | Lawyer |
| Legal aid income-limit regulation (প্রবিধানমালা) — not on bdlaws; check nlaso.gov.bd / অধিদপ্তর site | Missing; `eligibility.json` income limit still null | User + lawyer |
| Is 16430 still the helpline under the new অধিদপ্তর? | Unchecked | User |
| Bot says "I'll tell you the address" but office address/phone are null | Fill `offices.json` (D) | User |
| Render free sleeps after 15 min and has no disk | First WhatsApp message / web visit after idle waits ~50 s (Meta may retry; dedupe handles it); case files and history reset on restart. Decide on Starter + disk before judging | User |
| ~~Temporary WhatsApp token expires~~ | Done: permanent System User token (10-30) | — |
| Public `/api/chat` spends our model key; anyone with the link can use it | Acceptable for the demo; add a simple rate limit if abused | — |
| Bot sometimes gives advice-like wording ("settlement first is better") or unsourced consequences ("hard to claim if late" — ধারা ১৩২(২) proviso allows late filing with sufficient cause) | Seen 10-30; add eval scenarios (G) | — |
| Eligibility: any matched category → `eligible: true` regardless of income | Check with lawyer whether e.g. "স্বল্প আয়ের শ্রমিক" needs an income test | User + lawyer |

---

## 9. Risks and fallbacks

| Risk | Fallback |
|---|---|
| Weak Bangla speech recognition | Ask user to type; keep voice as a bonus |
| Poor document reading on bad photos | Ask for a clearer photo; confirm extracted fields with the user; SAM 3.1 crop |
| No Bangla text-to-speech among Meta's listed models | Text replies only, or MMS-TTS |
| Muse key arrives late | Keep building on stand-in; switch is a `.env` change; must switch before Nov 4 |
| Model skips tools / hallucinates law | Stricter prompt, fewer tools per step, eval scenarios catch it |
| WhatsApp setup delays | Web chat demo still works; record WhatsApp later |
| Looks like "basic RAG" | Emphasise agent actions, case file and handoff in video and README |
| Lawyer unavailable | Ask Legal Tech Hackathon network early; at minimum get eligibility rules verified |

---

## 10. Work log

### 2026-10-29
- Researched hackathon rules, judging, prizes, credits, deadlines; evaluated the idea (fits theme, not on anti-project list; must be framed as an agent and as legal information).
- Built the full project skeleton (see §6.1) — commit `ce9dc91`.
- Verified: 11 tests pass; server starts; web page loads; fallback works without a model.
- Attempted to create the GitHub repo — blocked by permissions; user to create `rashed-48/eknothi` manually.
- Added this `plan.md` and `CLAUDE.md`.
- User created https://github.com/rashed-48/Eknothi; added as `origin` and pushed `main`.
- **Next:** fill `.env` with a stand-in model; first real conversation (§6.2 B); WhatsApp setup (§6.2 C).
- **First real conversation (§6.2 B done).** `.env` on Groq; fixed key pasted in `<...>`; no Llama chat models on Groq → `openai/gpt-oss-120b`.
  Ran the wages story three times + once over `POST /api/chat`. Run 1: crash on draft (Groq parse error), invented eligibility categories, `**` and Bangla-digit helplines. Run 2: worked end to end but invented a 3-month deadline, garbled 999, wrong draft date, invented facts in draft, no case file. Run 3 (after fixes): correct date, clean draft, case file attached, 16430 only; one remaining unsourced claim (labour court).
  Verified: 14 tests pass; `/api/chat` turn 1 answers "not sure about the deadline, call 16430".
  **Next:** user — Meta credit claim + spend limit, Baseten request, lawyer, WhatsApp test number (§6.2 A, C). Claude — legal data from official sources with `verified: false` (D), Playwright PDF check (E), web chat bold rendering.
- **Legal data, PDF, web chat.** User started WhatsApp setup (own phone to be added as recipient; number kept out of repo).
  Copied 11 chunks from bdlaws (Labour Act 2006 wages sections; Legal Aid Act 2000 as amended by Act 45 of 2026). Found: NLASO is now বাংলাদেশ আইনগত সহায়তা অধিদপ্তর; applications can be filed online (ধারা ১৬); mandatory pre-case mediation for family/dowry/partition/pre-emption disputes in 10 + 30 districts via SRO 276 and 288 of 2026 (not our 3 districts). Labour Act ধারা ১৩২: wage claims within 12 months — the earlier invented "3 months" was wrong.
  Added `keywords` (বেতন vs মজুরী) to retrieval; bundled font, offline PDF; web chat bold; Playwright in requirements.
  Verified: 15 tests pass in 2.4 s, no network; PDF conjuncts checked; web bold escapes HTML; wages story run twice more — final run cites ধারা ১৩২ correctly with no invented claims.
  **Next:** user — WhatsApp values into `.env`, Meta credits, Baseten, lawyer. Claude — WhatsApp end to end once `.env` has the values (C); `offices.json` and eligibility income limit from official sites (D); land notice data once the demo notice is chosen; more scenarios (G).

### 2026-10-30
- **WhatsApp credentials + deployment setup.** User created the Meta app, added their phone as recipient; token, phone number ID, app secret, verify token in `.env` (token verified with Graph API). Local server on 8001 passed webhook verify + signature checks.
  Tunnel attempts failed: ngrok 3.3.1 too old → updated to 3.39.13 → blocked by Windows Defender as PUA (left to the user, not overridden); cloudflared quick tunnel → `api.trycloudflare.com` connection reset by the network; Claude Code auto mode also blocks starting inbound tunnels. Decided to deploy now (§5).
  Added `Dockerfile`, `.dockerignore`, `railway.json`, README deploy section. Built image (1.33 GB) after pinning bookworm; ran container: health, web, webhook verify/signature, PDF with Bangla, one chat turn — all OK.
  Verified: 15 tests pass.
  **Next:** user — Railway project + variables + volume + domain; then Meta webhook to `https://<domain>/webhook/whatsapp`, subscribe `messages`; permanent System User token. Claude — end-to-end phone test (text, voice, photo, PDF) once the webhook is set.
- **Railway sign-ups disabled** ("Sign ups are currently disabled", after their Oct 21 incident). User chose **Render free**. Added `render.yaml`; README deploy section now Render. 15 tests pass.
  **Next:** user — Render Blueprint deploy, then Meta webhook to `https://<service>.onrender.com/webhook/whatsapp`; Claude — phone end-to-end test.
- **Render live** at https://eknothi.onrender.com (health, web chat, webhook checked from outside). First WhatsApp "hello" got no reply. Diagnosed read-only via Graph API: (1) temporary token had expired → user made a permanent System User token, put in `.env` + Render; (2) the WABA forwarded only to Meta's "WA DevX Webhook Events" app, not EkNothi → user ran `POST /1110112525252982/subscribed_apps` (Claude's attempt was blocked by auto mode; changing account settings is the user's call). Confirmed EkNothi now subscribed.
  **Next:** phone test — text, voice note, photo, PDF.
- User verified the webhook and subscribed many fields. Only `messages` is needed; `whatsapp.parse` now ignores every other field (echoes/history could otherwise get replies). Test added — 16 pass. Advised unsubscribing the rest (each event wakes the free server).
