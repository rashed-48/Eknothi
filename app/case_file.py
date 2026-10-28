"""Render the case file (ek nothi) as HTML, then PDF via headless Chromium.

Chromium shapes Bangla conjuncts correctly; most pure-Python PDF libraries do not.
If Playwright is not installed, the HTML file is returned instead.
"""

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings

log = logging.getLogger(__name__)

BANGLADESH_TZ = timezone(timedelta(hours=6))
FONT_PATH = Path(__file__).parent / "fonts" / "NotoSansBengali.ttf"  # SIL OFL, see fonts/OFL.txt

_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(["html"]),
)

FACT_LABELS = {
    "name": "নাম",
    "phone": "ফোন",
    "district": "জেলা",
    "case_type": "সমস্যার ধরন",
    "monthly_income_bdt": "মাসিক আয় (টাকা)",
    "employer": "নিয়োগকর্তা",
    "opposing_party": "প্রতিপক্ষ",
    "key_dates": "গুরুত্বপূর্ণ তারিখ",
    "deadline": "শেষ তারিখ",
    "summary": "সমস্যার বিবরণ",
    "help_wanted": "যে সহায়তা চান",
}

CASE_TYPE_LABELS = {
    "unpaid_wages": "বকেয়া মজুরি",
    "land_notice": "জমি সংক্রান্ত নোটিশ",
    "family": "পারিবারিক মামলা",
    "other": "অন্যান্য",
}


def render_html(case: dict) -> str:
    facts = dict(case["facts"])
    if "case_type" in facts:
        facts["case_type"] = CASE_TYPE_LABELS.get(facts["case_type"], facts["case_type"])
    return _env.get_template("case_file.html").render(
        case=case,
        # Fixed order (name first), whatever order the model saved the facts in.
        facts=[(FACT_LABELS.get(k, k), v)
               for k, v in sorted(facts.items(), key=lambda kv: list(FACT_LABELS).index(kv[0])
                                  if kv[0] in FACT_LABELS else len(FACT_LABELS))],
        generated_at=datetime.now(BANGLADESH_TZ).strftime("%d/%m/%Y %H:%M"),
        font_uri=FONT_PATH.resolve().as_uri(),
    )


def render(case: dict) -> Path:
    html_path = settings.files_dir / f"{case['file_token']}.html"
    html_path.write_text(render_html(case), encoding="utf-8")
    pdf_path = html_path.with_suffix(".pdf")
    return pdf_path if _to_pdf(html_path, pdf_path) else html_path


def _to_pdf(src: Path, dst: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Local files only: the bundled font makes the PDF identical online or offline, and fast.
            page.route("**/*", lambda route: route.continue_() if route.request.url.startswith("file:")
                       else route.abort())
            page.goto(src.resolve().as_uri(), wait_until="load")
            page.pdf(path=str(dst), format="A4", print_background=True,
                     margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
            browser.close()
        return True
    except Exception:
        log.exception("PDF rendering failed, falling back to HTML")
        return False
