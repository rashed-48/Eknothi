"""Tools backed by hand-checked data in data/: legal sources, eligibility rules, office directory.

None of these call a model. Answers about law come from here, not from the model's memory.
"""

import json
import re
from functools import lru_cache

from app.config import settings
from app.tools.registry import ToolContext, tool

CASE_TYPES = ["unpaid_wages", "land_notice", "family"]

_SPLIT = re.compile(r"[\s,.;:!?()\[\]{}\"'।॥\-–—/]+")


def _tokens(text: str) -> set[str]:
    return {t for t in _SPLIT.split(text.lower()) if len(t) > 1}


@lru_cache
def legal_chunks() -> list[dict]:
    chunks = []
    for path in sorted((settings.data_dir / "legal").glob("*.json")):
        if path.name.startswith("_"):  # _example.json and other templates
            continue
        chunks.extend(json.loads(path.read_text(encoding="utf-8")))
    return chunks


@lru_cache
def _json(name: str) -> dict:
    return json.loads((settings.data_dir / name).read_text(encoding="utf-8"))


@tool(
    "Search Bangladesh legal aid rules, laws and procedures. Use before saying anything about law, rights, "
    "procedure or deadlines, and cite the returned source and section.",
    {
        "type": "object",
        "properties": {
            "case_type": {"type": "string", "enum": CASE_TYPES},
            "query": {"type": "string", "description": "What you need to know, in Bangla or English"},
        },
        "required": ["case_type", "query"],
    },
)
def retrieve_law(ctx: ToolContext, case_type: str, query: str, k: int = 4) -> dict:
    q = _tokens(query)
    scored = []
    for c in legal_chunks():
        if c.get("case_type") not in (case_type, "general"):
            continue
        score = len(q & _tokens(c["text"] + " " + c.get("title", "")))
        if score:
            scored.append((score, c))
    scored.sort(key=lambda s: s[0], reverse=True)
    results = [
        {k_: c.get(k_) for k_ in ("id", "source", "section", "title", "text", "url")}
        for _, c in scored[:k]
    ]
    known = {s["id"] for s in ctx.case["sources"]}
    ctx.case["sources"] += [r for r in results if r["id"] not in known]
    if not results:
        return {
            "results": [],
            "note": "No verified source found. Do not answer from memory; say you are not sure and refer to 16430.",
        }
    return {"results": results}


@tool(
    "Check whether the person likely qualifies for free government legal aid, using the official criteria.",
    {
        "type": "object",
        "properties": {
            "monthly_income_bdt": {"type": "number", "description": "Household monthly income in taka, if known"},
            "categories": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Category keys from the eligibility rules that apply to the person",
            },
        },
    },
)
def check_eligibility(ctx: ToolContext, monthly_income_bdt: float | None = None,
                      categories: list[str] | None = None) -> dict:
    rules = _json("eligibility.json")
    known = rules["categories"]
    matched = [c for c in (categories or []) if c in known]
    reasons = [known[c]["label_bn"] for c in matched]

    eligible = True if matched else None
    limit = rules.get("income_limit_bdt")
    if eligible is None and limit and monthly_income_bdt is not None:
        income = monthly_income_bdt * (12 if rules.get("income_period") == "year" else 1)
        eligible = income <= limit
        reasons.append(f"income {income:.0f} vs limit {limit}")

    result = {
        "eligible": eligible,  # None = cannot decide from the rules loaded
        "reasons": reasons,
        "rules_verified": rules.get("verified", False),
        "rules_source": rules.get("source"),
        "documents_to_bring": rules.get("documents_to_bring", []),
        "available_categories": {k: v["label_bn"] for k, v in known.items()},
    }
    ctx.case["eligibility"] = {k: result[k] for k in ("eligible", "reasons", "rules_verified")}
    return result


@tool(
    "Find the district legal aid office the person should go to, and the national helpline.",
    {
        "type": "object",
        "properties": {"district": {"type": "string", "description": "District name in Bangla or English"}},
        "required": ["district"],
    },
)
def find_office(ctx: ToolContext, district: str) -> dict:
    directory = _json("offices.json")
    needle = district.strip().lower()
    office = next(
        (o for key, o in directory["districts"].items()
         if needle == key or needle in [a.lower() for a in o.get("aliases", [])]),
        None,
    )
    ctx.case["office"] = office
    return {
        "office": office,
        "helpline": directory["helpline"],
        "note": None if office else "District not in directory yet; give the 16430 helpline.",
    }
