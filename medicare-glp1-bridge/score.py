"""Scorer for the Medicare GLP-1 Bridge routing suite. Called by run_eval.py."""
from collections import Counter


def score(cases, outputs, meta=None):
    lines = []
    if meta:
        lines.append(f"Suite: {meta.get('suite')} | model: {meta.get('model')} | effort: {meta.get('effort')} "
                     f"| docs as: {meta.get('doc_mode')} | runs per case: {meta.get('runs_per_case')} | seed: {meta.get('seed')}")
        lines.append("")
    tot = Counter()
    lines.append(f"{'case':5} {'route':>7} {'action':>7} {'product':>8}  key -> model actions")
    for c in cases:
        k = c["answer_key"]
        runs = outputs.get(c["id"], [])
        routes = [k["route"]] + k.get("route_also_accepted", [])
        acts = [k["action"]] + k.get("action_also_accepted", [])
        n = len(runs)
        r_ok = sum(1 for o in runs if o.get("route") in routes)
        a_ok = sum(1 for o in runs if o.get("recommended_action") in acts)
        p_key = k.get("product_covered_on_route")
        p_ok = (sum(1 for o in runs if o.get("product_covered_on_route") == p_key)
                if p_key in ("yes", "no") else None)
        errs = sum(1 for o in runs if "_error" in o)
        acts_seen = Counter(o.get("recommended_action", "error") for o in runs)
        extra = ""
        if c["id"].startswith("G7"):
            init = sum(1 for o in runs if o.get("bmi_timepoint") == "initiation")
            extra = f" | BMI at initiation {init}/{n}"
        p_str = f"{p_ok}/{n}" if p_ok is not None else "-"
        lines.append(f"{c['id']:5} {r_ok:>3}/{n:<3} {a_ok:>3}/{n:<3} {p_str:>8}  {k['action']} -> "
                     + ", ".join(f"{a} x{m}" for a, m in acts_seen.most_common()) + extra
                     + (f" | errors {errs}" if errs else ""))
        tot["n"] += n; tot["route"] += r_ok; tot["action"] += a_ok
    lines.append("")
    lines.append(f"All runs: route right {tot['route']}/{tot['n']}, action matched key {tot['action']}/{tot['n']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import json, sys
    cases = json.load(open(sys.argv[1]))["cases"]
    outputs = json.load(open(sys.argv[2]))
    print(score(cases, outputs))
