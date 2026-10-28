"""check_patient(): decide if ONE patient fits ONE trial.

Works directly on the friend's data format (criteria + operator, patients
with lists like diagnoses/medications/conditions).
The AI teammate can rewrite the inside, but must keep:
  - the function name and arguments: check_patient(patient, trial)
  - the output: {"decision", "criteria_results", "explanation"}
  - decision is exactly "Eligible", "Not eligible" or "Needs review"
"""

# Each operator is a tiny function: v = patient's value, t = trial's target value
OPS = {
    ">=": lambda v, t: v >= t,
    "<=": lambda v, t: v <= t,
    ">": lambda v, t: v > t,
    "<": lambda v, t: v < t,
    "==": lambda v, t: v == t,
    "contains": lambda v, t: t in v,          # list contains the item
    "not_contains": lambda v, t: t not in v,  # list does NOT contain the item
}


def check_patient(patient, trial):
    results = []
    for c in trial["criteria"]:
        value = patient.get(c["field"])
        # None = data missing, so we can't judge this rule
        passed = None if value is None else OPS[c["operator"]](value, c["value"])
        results.append({
            "id": c["id"],
            "criterion": c["text"],
            "value": value,
            "passed": passed,
        })

    failed = [r for r in results if r["passed"] is False]
    missing = [r for r in results if r["passed"] is None]

    # A clear failure beats missing data; missing data beats eligible.
    if failed:
        decision = "Not eligible"
        explanation = "Failed: " + "; ".join(
            f"{r['criterion']} (patient: {r['value']})" for r in failed)
    elif missing:
        decision = "Needs review"
        explanation = "Missing data for: " + "; ".join(r["criterion"] for r in missing)
    else:
        decision = "Eligible"
        explanation = "All criteria met."
    return {"decision": decision, "criteria_results": results, "explanation": explanation}
