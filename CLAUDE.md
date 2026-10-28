# EkNothi — instructions for Claude

**Read [plan.md](plan.md) in full before doing anything.** It holds the idea, hackathon rules, decisions, status,
blockers and work log. The submission deadline is **Wed Nov 4, 2026, 9:00 PM ET (Thu Nov 5, 8:00 AM Bangladesh)**.

## After every piece of work
Update `plan.md` in the same session, before stopping (see its §0):
- tick finished items in §6 and move them to "Implemented" with details;
- add new decisions to §5 with the reason;
- update §8 blockers;
- add a dated entry to §10 work log (done / verified / next);
- update "Last updated";
- commit `plan.md` together with the code change.

## Rules for this codebase
- All model calls go through `app/llm.py`. No other module imports a provider SDK.
- Law, eligibility rules and office details come only from `data/`. Never put legal facts, section numbers,
  deadlines, income limits or addresses into prompts or code from memory. Unverified data stays `verified: false`.
- Replies to users are in simple Bangla; the bot gives legal information, not legal advice.
- Keep scope to three case types: unpaid_wages, land_notice, family.
- Run `pytest` after changes. Tests must not need a model or network.
- The repo is public: never commit `.env`, `var/`, real people's documents or eval results with personal data.
- Commit often (commit history shows the work was done during the hackathon).
