"""Tools that build up the case file (the "ek nothi")."""

import json

from app import case_file, llm
from app.prompts import DRAFT_PROMPT, DRAFT_SYSTEM
from app.tools.registry import ToolContext, tool

CASE_FIELDS = {
    "name": {"type": "string"},
    "phone": {"type": "string"},
    "district": {"type": "string"},
    "case_type": {"type": "string", "enum": ["unpaid_wages", "land_notice", "family", "other"]},
    "monthly_income_bdt": {"type": "number"},
    "employer": {"type": "string"},
    "opposing_party": {"type": "string"},
    "key_dates": {"type": "string", "description": "Important dates and what happened on them"},
    "deadline": {"type": "string"},
    "summary": {"type": "string", "description": "The person's problem in 2-4 sentences"},
    "help_wanted": {"type": "string"},
}


@tool(
    "Save facts about the person's case. Call whenever you learn something new; only send the fields you learned.",
    {"type": "object", "properties": CASE_FIELDS},
)
def update_case(ctx: ToolContext, **facts) -> dict:
    ctx.case["facts"].update({k: v for k, v in facts.items() if k in CASE_FIELDS and v not in (None, "")})
    return {"facts": ctx.case["facts"]}


@tool(
    "Draft the person's free legal aid application (or complaint) in Bangla from the saved case facts.",
    {
        "type": "object",
        "properties": {"kind": {"type": "string", "enum": ["legal_aid_application", "complaint"]}},
        "required": ["kind"],
    },
)
def draft_application(ctx: ToolContext, kind: str) -> dict:
    kind_bn = {"legal_aid_application": "আইনগত সহায়তার আবেদন", "complaint": "অভিযোগপত্র"}.get(kind, kind)
    draft = llm.complete(
        DRAFT_PROMPT.format(
            kind=kind_bn,
            district=ctx.case["facts"].get("district", "[........]"),
            facts=json.dumps(ctx.case["facts"], ensure_ascii=False, indent=2),
            documents=json.dumps(ctx.case["documents"], ensure_ascii=False, indent=2),
        ),
        system=DRAFT_SYSTEM,
    )
    ctx.case["draft"] = {"kind": kind, "text": draft}
    return {"draft": draft}


@tool(
    "Build the shareable case file PDF (ek nothi) and send it to the person.",
    {"type": "object", "properties": {}},
)
def build_case_file(ctx: ToolContext) -> dict:
    path = case_file.render(ctx.case)
    if path not in ctx.files:
        ctx.files.append(path)
    return {"built": True, "file": path.name, "note": "The file will be sent with your reply."}


@tool(
    "Hand the case to a human at the national legal aid helpline 16430. Use for urgent, serious or uncertain cases.",
    {
        "type": "object",
        "properties": {
            "reason": {"type": "string"},
            "urgent": {"type": "boolean", "description": "True if there is danger to someone's safety"},
        },
        "required": ["reason"],
    },
)
def escalate_to_human(ctx: ToolContext, reason: str, urgent: bool = False) -> dict:
    ctx.case["escalated"] = {"reason": reason, "urgent": urgent}
    build_case_file(ctx)
    contacts = ["16430 (জাতীয় আইনগত সহায়তা হেল্পলাইন)"]
    if urgent:
        contacts = ["999 (জরুরি সেবা)", "109 (নারী ও শিশু নির্যাতন প্রতিরোধ হেল্পলাইন)"] + contacts
    return {"escalated": True, "tell_user_to_contact": contacts, "case_file_ready": True}
