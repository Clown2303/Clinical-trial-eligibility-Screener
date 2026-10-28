"""Plain-English explanations from LM Studio, with an offline fallback."""

import json
import os
from pathlib import Path


def _strip_think(text):
    while "<think>" in text and "</think>" in text:
        start = text.index("<think>")
        end = text.index("</think>", start) + len("</think>")
        text = text[:start] + text[end:]
    return text.replace("<think>", "").replace("</think>", "").strip()


def _offline_explanation(result):
    failed = [item["text"] for item in result["results"] if item["passed"] is False]
    unknown = [item["text"] for item in result["results"] if item["passed"] is None]
    if result["decision"] == "Not eligible":
        return f"The patient is not eligible because {failed[0].lower()}. Other checked criteria do not change this decision."
    if result["decision"] == "Needs review":
        return f"The patient needs review because {unknown[0].lower()} is unknown. The remaining checked criteria did not fail."
    return "The patient is eligible because all checked criteria passed. No checked criterion failed or was unknown."


def explain(patient, trial, result):
    """Use only the deterministic result when composing the explanation."""
    try:
        from openai import OpenAI
        client = OpenAI(base_url=os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1"), api_key="lm-studio")
        response = client.chat.completions.create(
            model=os.getenv("LM_STUDIO_MODEL", "local-model"),
            temperature=0,
            max_tokens=180,
            messages=[
                {"role": "system", "content": "Write exactly 2 or 3 concise sentences. Use only the supplied decision and checked results. Never infer or invent patient facts."},
                {"role": "user", "content": json.dumps({"decision": result["decision"], "results": result["results"]})},
            ],
        )
        return _strip_think(response.choices[0].message.content)
    except Exception:
        return _offline_explanation(result)


if __name__ == "__main__":
    root = Path(__file__).parent
    trials = json.loads((root / "trials.json").read_text())
    patients = json.loads((root / "patients.json").read_text())
    from rules import check_patient
    trial, patient = trials[0], patients[0]
    result = check_patient(patient, trial)
    print(result)
    print(explain(patient, trial, result))
