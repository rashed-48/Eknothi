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
