# Model prompt (same for every case)

Run each case in a fresh chat. Attach the payer policy document (PDF, or the full page text for Aetna CPBs) and paste the prompt below with the case's chart and drafted request filled in. Record the model name and date, and save the reply word for word.

---

You are preparing a prior authorization request for a specialty drug on behalf of the prescriber's office. Use only the attached payer policy and the chart below. Don't assume facts that aren't in the chart.

Plan context: {case_note}

Chart:
{chart}

Request as drafted by the office:
{request_as_drafted}

Fill in the JSON below. Return only the JSON.

```json
{
  "product": "",
  "hcpcs_code": "",
  "dose": "",
  "frequency": "",
  "units_per_dose": null,
  "quantity_per_fill": "",
  "diagnosis_codes": [],
  "criteria_review": [
    {"criterion": "", "met": "yes | no | unclear", "chart_evidence": ""}
  ],
  "overall_criteria_status": "met | not_met | unclear",
  "missing_or_problems": [],
  "recommended_action": "submit | pend_for_info | fix_request"
}
```

Field notes:
- hcpcs_code and units_per_dose apply to drugs billed under the medical benefit. Write "N/A (pharmacy benefit)" and null otherwise.
- recommended_action: "submit" if criteria are met and the request is correct as written; "pend_for_info" if documentation or an attestation is missing; "fix_request" if the product, code or dose should change before submitting.
