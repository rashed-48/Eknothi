# Legal sources

The agent may only state law, procedure or deadlines that come from files in this folder.

- One JSON file per source, e.g. `legal_aid_act_2000.json`, `labour_act_2006_wages.json`.
- Each file is a list of chunks in the format shown in `_example.json`.
- `case_type` is one of `unpaid_wages`, `land_notice`, `family`, or `general` (returned for every case type).
- Files starting with `_` are ignored.

Sources to collect:

| Case type | Source | Where |
|---|---|---|
| general | Legal Aid Services Act 2000 and its regulations (eligibility, how to apply) | bdlaws.minlaw.gov.bd, nlaso.gov.bd |
| unpaid_wages | Bangladesh Labour Act 2006: wage payment and claim sections | bdlaws.minlaw.gov.bd |
| land_notice | The procedure behind the notices you will demo | bdlaws.minlaw.gov.bd |
| family | Family court procedure (only if time allows) | bdlaws.minlaw.gov.bd |

Copy section text exactly and record the section number. The lawyer reviews these files.

## Fields

- `text`: exact section text as published. Amendment markers like `2[ত্রিশ]` are resolved to the amended words; the
  footnote itself goes in `notes`. Some bdlaws pages contain old font-conversion errors (e.g. `দরখাসত্দ` for
  `দরখাস্ত`); these are kept as published.
- `notes`: footnotes from the source — amendments, and SROs saying from when and in which districts a provision is in force.
- `keywords`: everyday words for retrieval only (people say বেতন, the Act says মজুরী). Not legal content.
- `verified`: `false` until the lawyer has checked the chunk against the source; then set `true`.

## Current files (copied 2026-10-29 from bdlaws.minlaw.gov.bd, all `verified: false`)

| File | Sections |
|---|---|
| `labour_act_2006_wages.json` | বাংলাদেশ শ্রম আইন, ২০০৬ — ধারা ৩০, ৩৩, ১২১, ১২৩, ১২৪ক, ১৩২, ২১৩ |
| `legal_aid_act_2000.json` | আইনগত সহায়তা প্রদান আইন, ২০০০ (as amended by Act 45 of 2026) — ধারা ২(খ), ১৬, ২১খ, তফসিল |

For the lawyer: the 2026 amendment created বাংলাদেশ আইনগত সহায়তা অধিদপ্তর and made pre-case mediation mandatory for the
disputes in the তফসিল, in force only in the districts named in the SRO footnotes (not Dhaka, Gazipur or Narayanganj
as of the copy date). Please confirm this is current, and give the regulation that sets the income limit.
