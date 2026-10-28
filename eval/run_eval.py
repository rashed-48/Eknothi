"""Run every scenario through the agent and write a sheet for the lawyer to review.

    python -m eval.run_eval              # all scenarios
    python -m eval.run_eval wages_01     # one scenario
"""

import csv
import json
import mimetypes
import sys
import uuid
from datetime import datetime

import yaml

from app import agent, store
from app.config import ROOT

SCENARIOS = ROOT / "scenarios"
OUT = ROOT / "eval" / f"results_{datetime.now():%Y%m%d_%H%M}.csv"

DIGITS_BN = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def run_scenario(s: dict) -> dict:
    user_id = f"eval:{s['id']}:{uuid.uuid4().hex[:6]}"
    transcript = []
    for turn in s["turns"]:
        kwargs = {}
        if turn.get("image"):
            path = ROOT / turn["image"]
            kwargs.update(image=path.read_bytes(), image_mime=mimetypes.guess_type(path)[0] or "image/jpeg")
        if turn.get("audio"):
            path = ROOT / turn["audio"]
            kwargs.update(audio=path.read_bytes(), audio_name=path.name)
        reply = agent.run(user_id, turn.get("text", ""), **kwargs)
        transcript += [f"USER: {turn.get('text', '')}", f"BOT: {reply.text}"]

    _, case = store.load(user_id)
    expected = s.get("expected", {})
    all_replies = "\n".join(transcript).translate(DIGITS_BN)
    missing = [m for m in expected.get("must_mention", []) if m not in all_replies]
    escalated = bool(case["escalated"])

    return {
        "id": s["id"],
        "description": s.get("description", ""),
        "expected_case_type": expected.get("case_type"),
        "got_case_type": case["facts"].get("case_type"),
        "expected_escalate": expected.get("should_escalate"),
        "got_escalate": escalated,
        "missing_mentions": ", ".join(missing),
        "eligibility": json.dumps(case["eligibility"], ensure_ascii=False),
        "sources_cited": len(case["sources"]),
        "auto_pass": (
            case["facts"].get("case_type") == expected.get("case_type")
            and escalated == bool(expected.get("should_escalate"))
            and not missing
        ),
        "transcript": "\n".join(transcript),
        "lawyer_verdict": "",  # correct / partly correct / wrong
        "lawyer_notes": "",
    }


def main(only: list[str]) -> None:
    files = sorted(SCENARIOS.glob("*.yaml"))
    scenarios = [yaml.safe_load(f.read_text(encoding="utf-8")) for f in files]
    if only:
        scenarios = [s for s in scenarios if s["id"] in only]
    rows = []
    for s in scenarios:
        print(f"running {s['id']} ...", flush=True)
        rows.append(run_scenario(s))
        print(f"  auto_pass={rows[-1]['auto_pass']}")
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig so Excel shows Bangla
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    passed = sum(r["auto_pass"] for r in rows)
    print(f"\n{passed}/{len(rows)} passed automatic checks. Sheet for lawyer review: {OUT}")


if __name__ == "__main__":
    main(sys.argv[1:])
