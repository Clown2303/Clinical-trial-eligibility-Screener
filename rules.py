"""Deterministic clinical trial eligibility rules."""

OPERATORS = {">=", "<=", ">", "<", "==", "contains", "not_contains"}


def check_patient(patient, trial):
    results = []
    for criterion in trial["criteria"]:
        field = criterion["field"]
        operator = criterion["operator"]
        expected = criterion["value"]
        patient_value = patient.get(field)
        passed = None
        if operator not in OPERATORS:
            raise ValueError(f"Unsupported operator: {operator}")
        if patient_value is not None:
            if operator == "contains":
                passed = expected in patient_value
            elif operator == "not_contains":
                passed = expected not in patient_value
            elif operator == "==":
                passed = patient_value == expected
            elif operator == ">=":
                passed = patient_value >= expected
            elif operator == "<=":
                passed = patient_value <= expected
            elif operator == ">":
                passed = patient_value > expected
            elif operator == "<":
                passed = patient_value < expected
        results.append({
            "criterion_id": criterion["id"],
            "text": criterion["text"],
            "passed": passed,
            "patient_value": patient_value,
        })

    if any(item["passed"] is False for item in results):
        decision = "Not eligible"
    elif any(item["passed"] is None for item in results):
        decision = "Needs review"
    else:
        decision = "Eligible"
    return {"decision": decision, "results": results}


def evaluate_trial(trial, patient):
    """Backward-compatible alias for the original app integration."""
    result = check_patient(patient, trial)
    return {"decision": result["decision"], "checks": result["results"]}
