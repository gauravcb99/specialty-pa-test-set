# Specialty PA test set

Nine synthetic prior authorization requests for Skyrizi, infliximab and Zepbound, each with one right answer under a current Aetna, UnitedHealthcare or Cigna policy. Built to check an AI that turns a chart and a payer policy into a prior auth request, field by field.

All patients are synthetic. Criteria come from public payer policies; versions and links are in `cases.json`. Policy text isn't reproduced here.

## The cases

| | Clean (should go out as written) | Gap (a requirement is missing) | Trap (the request is wrong) |
|---|---|---|---|
| Skyrizi for Crohn's | S1, Aetna CPB 1009: no prior-therapy step | S2, UHC 2026D0116H: mesalamine isn't on the conventional therapy list | S3, Cigna IP0670: restart filed as a continuation; initial criteria apply |
| Infliximab for Crohn's | I1, UHC 2026D0004AR: Inflectra 400 mg = 40 units of Q5103 | I2, Aetna CPB 0341: no TB test on file | I3, UHC 2026D0004AR: Remicade is non-preferred on a Medical Necessity Plan |
| Zepbound for weight loss | Z1, Cigna IP0816: four months of program clears Cigna's three | Z2, Aetna 6947-C: Aetna needs six months | Z3, Cigna IP0816: start dose is 2.5 mg, not 5 mg |

S1 is a judgment call: the key prefers submitting with the no-combination attestation on the form, and pending for it is also accepted, because the prompt says to pend when an attestation is missing.

## Files

- `cases.json`: policies, charts, the request as drafted, answer keys, rationale and changelog (v0.1.2)
- `prompt.md`: the prompt, the same for every case
- `score.py`: scores outputs against the answer keys
- `tally.csv`: every run, its action, and whether it matches the original and current keys
- `results/memory_off/`: the reported results. `baseline_outputs.json` (each case once), `all_runs.json` (plus S1, S2 and I2 four more times each), `s1b_variant_runs.json` (S1 with "Current medications: none" added)
- `results/memory_on/`: earlier runs with ChatGPT memory on, kept for the record, including the v0.1 cases they used

```
python score.py cases.json results/memory_off/baseline_outputs.json results/memory_off/baseline_review.json
```

## How it was run

ChatGPT (GPT6 Extra), November 9, 2026. A new chat for every run, memory off, web search not enabled, only the attached policy. Each case once; S1, S2 and I2 five times each; the S1 variant five times. 26 runs.

## Results (memory off)

- Product, billing code, units and dose right in all 26 runs.
- Planted problems found in all six cases that have one, and in every S2 and I2 run.
- Action matched the key in 9 of 9 cases counting S1 as a judgment call; 8 of 9 under the original key.

Where answers moved, the chart had left something open:

| Case | Chart | Result |
|---|---|---|
| S1 | No prior biologic; no current medication list | Held 5 of 5 for a "no other biologic" confirmation |
| S1 variant | Adds "Current medications: none." | Submitted 3 of 5; the two holds asked about future use |
| I2 | Complications not stated, then "with rectal bleeding" | Diagnosis code split 3 and 3 (memory-on runs); after the fix, K50.111 in 5 of 5 |

## Changelog (all November 9, 2026, after reading outputs)

- I1, I3: case note now says the plan is a UnitedHealthcare Medical Necessity Plan.
- S3: chart now states complication status.
- Z2: answer-key rationale corrected; Aetna's quantity limit table lists "Tirzepatide (Brand Mounjaro)" in every row.
- I2: chart and drafted request now state rectal bleeding.
- S1: key now accepts submit or pend.
- Setup: everything rerun with ChatGPT memory off.
- Withdrawn after reruns: a reading that the model treated Skyrizi and infliximab differently, and a reading that policy tense drove the call.

## Limits

Nine cases. Consumer ChatGPT with no control over randomness or model version. Five runs on four cases, one on the rest. Doses came out to whole vials. Answer keys written by the author from the posted policies, with no second reviewer yet. The prompt doesn't define "not met" versus "unclear," or whether fields show the request as drafted or corrected.

## Next

Uneven weights (units, vials, waste, payer rounding), a current medication list in every chart, a second model.

Public documents only, checked November 2026. Policies change, so check the current version before relying on any criterion. Not medical or legal advice.

Gaurav Bhatti, pharmacist by training, Master of Health Informatics, University of Michigan.
