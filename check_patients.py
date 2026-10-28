"""Check that every patient's correct_answers match the criteria in trials.json.
Usage: python check_patients.py [patients_file]   (default: patients.json)"""
import json, sys

OPS = {">=": lambda v, t: v >= t, "<=": lambda v, t: v <= t, ">": lambda v, t: v > t,
       "<": lambda v, t: v < t, "==": lambda v, t: v == t,
       "contains": lambda v, t: t in v, "not_contains": lambda v, t: t not in v}

def decide(trial, p):
    res = [None if p.get(c["field"]) is None else OPS[c["operator"]](p[c["field"]], c["value"])
           for c in trial["criteria"]]
    if False in res: return "Not eligible"
    if None in res: return "Needs review"
    return "Eligible"

trials = json.load(open("trials.json"))
patients = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "patients.json"))
bad = 0
for p in patients:
    for t in trials:
        want, got = p["correct_answers"].get(t["trial_id"]), decide(t, p)
        if want != got:
            bad += 1
            print(f"MISMATCH {p['id']} {t['trial_id']}: file says {want!r}, criteria give {got!r}")
print(f"{len(patients)} patients checked:", "all correct" if bad == 0 else f"{bad} mismatches")
