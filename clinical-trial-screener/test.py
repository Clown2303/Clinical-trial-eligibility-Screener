"""Run check_patient on every patient x trial and compare with the answers
stored inside each patient (correct_answers).

Usage: python test.py [patients.json] [trials.json]
"""
import json
import sys
from collections import defaultdict

from screener import check_patient  # AI teammate: keep this import name

patients_file = sys.argv[1] if len(sys.argv) > 1 else "patients.json"
trials_file = sys.argv[2] if len(sys.argv) > 2 else "trials.json"

with open(patients_file, encoding="utf-8") as f:
    patients = json.load(f)
with open(trials_file, encoding="utf-8") as f:
    trials = json.load(f)

total = correct = 0
per_trial = defaultdict(lambda: [0, 0])   # trial_id -> [correct, total]
mismatches = []

for p in patients:
    for t in trials:
        tid = t["trial_id"]
        expected = p.get("correct_answers", {}).get(tid)
        if expected is None:
            print(f"WARNING: {p['id']} has no answer for {tid}, skipped")
            continue
        result = check_patient(p, t)
        got = result["decision"]
        total += 1
        per_trial[tid][1] += 1
        if got == expected:
            correct += 1
            per_trial[tid][0] += 1
        else:
            mismatches.append((p["id"], tid, expected, got, result.get("explanation", "")))

names = {t["trial_id"]: t["name"] for t in trials}
print(f"\nOVERALL ACCURACY: {correct}/{total} = {100 * correct / total:.1f}%")
print("\nPER TRIAL:")
for tid in sorted(per_trial):
    c, n = per_trial[tid]
    print(f"  {tid} ({names[tid]}): {c}/{n} = {100 * c / n:.1f}%")

print(f"\nMISMATCHES ({len(mismatches)}):")
if not mismatches:
    print("  none")
for pid, tid, exp, got, why in mismatches:
    print(f"  patient={pid} trial={tid} expected={exp!r} got={got!r}\n    AI said: {why}")
