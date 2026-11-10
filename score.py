"""Score model outputs against the answer keys in cases.json.

Usage: python score.py cases.json run1/outputs.json [run1/review.json]
Field checks are automatic. review.json holds the human read of each output
(was the key problem found, false alarms, problems in the test set itself).
"""
import json, re, sys

def codes(xs):
    return {m for x in xs for m in re.findall(r"[A-Z]\d{2}\.?\w*", x)}

def score(case, out, rev):
    k = case["answer_key"]
    actions = [k["action"]] + k.get("action_also_accepted", [])
    statuses = [k["criteria_status"]] + k.get("status_also_accepted", [])
    pend_like = k["action"] in ("pend_for_info", "fix_request")
    status = out["overall_criteria_status"]
    hc = out["hcpcs_code"]
    if k["benefit"] == "pharmacy":
        code_ok = hc.startswith("N/A")
    else:
        found = set(re.findall(r"[A-Z]\d{4}", hc))
        # On a fix_request, keeping the drafted code and naming the fix elsewhere is accepted
        code_ok = bool(found & set(k["hcpcs_accepted"])) or (
            found == {k.get("hcpcs_as_drafted")} and out["recommended_action"] == "fix_request")
    r = {
        "action": out["recommended_action"] in actions,
        "status_exact": status in statuses,
        # 'unclear' counted as not_met when the right move is still to stop and fix or pend
        "status_lenient": status in statuses or (pend_like and status in ("not_met", "unclear")),
        "code": code_ok,
        "units": out["units_per_dose"] == k["units_per_dose"],
        "dx": bool(codes(out["diagnosis_codes"]) & set(k["dx_accepted"])),
    }
    if rev:
        r["key_problem_found"] = rev["key_problem_found"]
        r["false_alarms"] = len(rev["false_alarms"])
        r["test_set_issues"] = len(rev["test_set_issues"])
    return r

def main(cases_path, outputs_path, review_path=None):
    cases = {c["id"]: c for c in json.load(open(cases_path))["cases"]}
    outs = json.load(open(outputs_path))["outputs"]
    revs = json.load(open(review_path))["cases"] if review_path else {}
    rows = {cid: score(cases[cid], outs[cid], revs.get(cid)) for cid in cases}
    cols = list(next(iter(rows.values())).keys())
    print("case  " + "  ".join(cols))
    for cid, r in rows.items():
        print(f"{cid:<5} " + "  ".join(str(r[c]) for c in cols))
    print()
    for c in ("action", "status_exact", "status_lenient", "code", "units", "dx"):
        print(f"{c:<15} {sum(r[c] for r in rows.values())}/{len(rows)}")
    if revs:
        found = [r["key_problem_found"] for r in rows.values() if r["key_problem_found"] is not None]
        print(f"{'key problems':<15} {sum(found)}/{len(found)} found")
        print(f"{'false alarms':<15} {sum(r['false_alarms'] for r in rows.values())}")
        print(f"{'test set fixes':<15} {sum(r['test_set_issues'] for r in rows.values())}")
    return rows

if __name__ == "__main__":
    main(*sys.argv[1:])
