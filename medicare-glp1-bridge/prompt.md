# Model prompt (same for every case)

Run each case in a fresh chat with memory off and web search off. Attach the two CMS documents listed in run_sheet.md. Paste the prompt with the case filled in. Save the reply word for word.

---

You are a pharmacist at a health system routing a new GLP-1 prescription for a Medicare patient. Use only the attached CMS documents and the chart below. Don't assume facts that aren't in the chart.

Decide where this prescription should go: the Medicare GLP-1 Bridge, the patient's Part D plan, or neither, and what should happen before anything is submitted.

Plan: {plan}

Chart:
{chart}

Prescription as drafted:
{rx}

Return only this JSON:

```json
{
  "route": "bridge | part_d_plan | not_eligible | unclear",
  "qualifying_basis": "",
  "bmi_used": null,
  "bmi_timepoint": "initiation | current | n/a",
  "part_d_indications_found": [],
  "product_covered_on_route": "yes | no | n/a",
  "missing_or_problems": [],
  "recommended_action": "submit_bridge_pa | send_to_part_d_plan | fix_request | pend_for_info | do_not_submit"
}
```

Field notes:
- route: "unclear" only if the chart doesn't contain what's needed to decide.
- recommended_action: "submit_bridge_pa" if the patient qualifies for the Bridge and the prescription is right as written; "send_to_part_d_plan" if a Part D-covered indication applies; "fix_request" if the patient qualifies but the product or prescription should change first; "pend_for_info" if the prescriber must supply information first; "do_not_submit" if the patient doesn't qualify for the Bridge.
