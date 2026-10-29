"""Tests for everything that does not need a model: data tools, store, case file rendering."""

import os
import tempfile

os.environ["EKNOTHI_VAR_DIR"] = tempfile.mkdtemp()

from app import case_file, store  # noqa: E402
from app.tools import ToolContext, execute, schemas  # noqa: E402


def ctx() -> ToolContext:
    return ToolContext(user_id="test", case=store.new_case())


def test_all_tools_have_schemas():
    names = {s["function"]["name"] for s in schemas()}
    assert names == {
        "retrieve_law", "check_eligibility", "find_office",
        "update_case", "draft_application", "build_case_file", "escalate_to_human",
    }


def test_retrieve_law_without_sources_refuses_to_guess():
    result = execute("retrieve_law", '{"case_type": "land_notice", "query": "রেলগাড়ি"}', ctx())
    assert result["results"] == []
    assert "16430" in result["note"]


def test_retrieve_law_matches_everyday_words():
    # The Act says মজুরী; people say বেতন. Keywords bridge the two.
    c = ctx()
    result = execute("retrieve_law", '{"case_type": "unpaid_wages", "query": "বেতন পাইনি মামলা কতদিন"}', c)
    ids = [r["id"] for r in result["results"]]
    assert "labour-132" in ids
    assert all(r["verified"] is False for r in result["results"])
    assert {s["id"] for s in c.case["sources"]} == set(ids)


def test_eligibility_by_category():
    c = ctx()
    result = execute("check_eligibility", '{"categories": ["worker_low_income"]}', c)
    assert result["eligible"] is True
    assert result["rules_verified"] is False
    assert c.case["eligibility"]["eligible"] is True


def test_eligibility_unknown_without_income_limit():
    result = execute("check_eligibility", '{"monthly_income_bdt": 12000}', ctx())
    assert result["eligible"] is None


def test_find_office_by_bangla_name():
    c = ctx()
    result = execute("find_office", '{"district": "গাজীপুর"}', c)
    assert result["office"]["office"].endswith("গাজীপুর")
    assert result["helpline"]["number"] == "16430"


def test_find_office_unknown_district_falls_back_to_helpline():
    result = execute("find_office", '{"district": "Bandarban"}', ctx())
    assert result["office"] is None
    assert result["helpline"]["number"] == "16430"


def test_update_case_ignores_unknown_fields():
    c = ctx()
    execute("update_case", '{"name": "রহিমা", "district": "Gazipur", "hacker": "x"}', c)
    assert c.case["facts"] == {"name": "রহিমা", "district": "Gazipur"}


def test_bad_arguments_return_error():
    assert "error" in execute("find_office", "not json", ctx())
    assert "error" in execute("no_such_tool", "{}", ctx())


def test_escalation_builds_case_file():
    c = ctx()
    result = execute("escalate_to_human", '{"reason": "violence", "urgent": true}', c)
    assert result["escalated"] is True
    assert any("999" in x for x in result["tell_user_to_contact"])
    assert len(c.files) == 1 and c.files[0].exists()


def test_store_roundtrip_and_dedupe():
    case = store.new_case()
    case["facts"]["name"] = "করিম"
    store.save("u1", [{"role": "user", "content": "hi"}], case)
    history, loaded = store.load("u1")
    assert loaded["facts"]["name"] == "করিম" and history[0]["content"] == "hi"
    assert store.mark_seen("m1") is True
    assert store.mark_seen("m1") is False


def test_case_file_html_contains_bangla_facts():
    case = store.new_case()
    case["facts"] = {"name": "রহিমা", "case_type": "unpaid_wages"}
    html = case_file.render_html(case)
    assert "রহিমা" in html and "বকেয়া মজুরি" in html and case["case_id"] in html


def test_eligibility_categories_are_limited_to_known_keys():
    schema = next(s for s in schemas() if s["function"]["name"] == "check_eligibility")
    enum = schema["function"]["parameters"]["properties"]["categories"]["items"]["enum"]
    assert "worker_low_income" in enum and "unpaid_wages" not in enum


def test_draft_builds_case_file_without_markdown(monkeypatch):
    from app import llm
    monkeypatch.setattr(llm, "complete", lambda prompt, system=None: "**বিষয়:** আবেদন")
    c = ctx()
    result = execute("draft_application", '{"kind": "legal_aid_application"}', c)
    assert result["case_file_ready"] and len(c.files) == 1
    assert c.case["draft"]["text"] == "বিষয়: আবেদন"


def test_whatsapp_format():
    from app.agent import whatsapp_format
    text = "## শিরোনাম\n**জরুরি:** ১৬৪৩০ বা ৯৯৯, কিন্তু ১৬৪৩০৫ নয়\n```text\nখসড়া\n```"
    assert whatsapp_format(text) == "শিরোনাম\n*জরুরি:* 16430 বা 999, কিন্তু ১৬৪৩০৫ নয়\n\nখসড়া"


def test_whatsapp_parse_only_replies_to_incoming_messages():
    from app.whatsapp import parse
    incoming = {"id": "wamid.1", "from": "8801000000000", "type": "text", "text": {"body": "হ্যালো"}}
    payload = {"entry": [{"changes": [
        {"field": "messages", "value": {"messages": [incoming]}},
        {"field": "messages", "value": {"statuses": [{"id": "wamid.0", "status": "delivered"}]}},
        {"field": "message_echoes", "value": {"messages": [dict(incoming, id="wamid.2")]}},
        {"field": "history", "value": {"messages": [dict(incoming, id="wamid.3")]}},
    ]}]}
    msgs = parse(payload)
    assert [(m.message_id, m.text) for m in msgs] == [("wamid.1", "হ্যালো")]
