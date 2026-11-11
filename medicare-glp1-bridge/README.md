# Medicare GLP-1 Bridge routing set

Nine synthetic Medicare charts, each with one right answer under CMS's Medicare GLP-1 Bridge rules: send the prescription to the Bridge, send it to the patient's Part D plan, or stop before submitting. Plus G1b, a variant of G1 with two lines added to the prescription. All patients are synthetic.

## Files

- `cases.json`: charts, prescriptions as drafted, answer keys, rationale, the CMS rules used, and a changelog
- `prompt.md`: the prompt, the same for every case
- `score.py`: scores outputs against the answer keys (`python score.py cases.json results/all_runs.json`)
- `results/run1_replies.txt`, `results/reruns_replies.txt`: every reply, word for word
- `results/all_runs.json`: parsed replies; `results/score.txt`: the score table

## How it was run

ChatGPT (GPT6 High), November 10, 2026. A new chat for every run, memory off, web search off. Two CMS documents attached: the Bridge prescriber fact sheet (https://www.cms.gov/files/document/glp-1-prescribers-c-1.pdf) and the Bridge prior authorization form (https://www.cms.gov/files/document/glp-1-bridge.pdf). Each case once; G1 and G8 five times each; G1b five times. 22 runs.

## Results

- Route right in 22 of 22 runs, including every trap: single-dose pen, mild vs moderate sleep apnea, BMI at initiation, vials, GLP-1 through Part D in 2026, biopsy-staged MASH, and the two-drug blood pressure rule. The open-purpose case (G5) was pended with both routes named.
- G1, a clean Bridge case, was held 5 of 5 for an E66 obesity code and "SEND TO BRIDGE FOR WEIGHT MANAGEMENT" on the prescription. With both lines added (G1b), it was submitted 5 of 5. CMS recommends both and says they're "not required for a claim to be processed"; the answer key didn't include them, and results are reported against the key as written.
- G8 was kept off the Bridge 5 of 5; the action was pend 3, send to Part D 1, don't submit 1.
- Action matched the key in 13 of 22 runs.

## Limits

Nine cases, one model, consumer ChatGPT. One run on seven cases. Answer keys written by the author from CMS documents, with no second reviewer. The Wegovy charts say "1 month supply," which was imprecise (CMS covers 28- or 30-day fills).

Public documents only, checked November 2026. CMS rules can change. Not medical or legal advice.

Gaurav Bhatti, pharmacist by training, Master of Health Informatics, University of Michigan.
