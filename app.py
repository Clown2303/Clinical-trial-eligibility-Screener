"""Simple Streamlit UI for the clinical-trial eligibility demo."""
import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent


@st.cache_data
def load_data(filename):
    with (ROOT / filename).open(encoding="utf-8") as data_file:
        return json.load(data_file)


def fake_check_patient(patient, trial):
    """Temporary demo result. Replace with rules.check_patient when integrated."""
    return "Eligible"


st.set_page_config(page_title="Trial Eligibility Screener", page_icon="🩺", layout="centered")
st.title("Clinical Trial Eligibility Screener")
st.caption("Demo using synthetic trial and patient data.")

trials = load_data("trials.json")
patients = load_data("patients.json")

trial_col, patient_col = st.columns(2)
with trial_col:
    trial = st.selectbox(
        "Pick a trial",
        trials,
        format_func=lambda item: f"{item['trial_id']} · {item['name']}",
    )
with patient_col:
    patient = st.selectbox("Pick a patient", patients, format_func=lambda item: item["id"])

if st.button("Check", type="primary", use_container_width=True):
    st.session_state.screening = {
        "patient_id": patient["id"],
        "trial_id": trial["trial_id"],
        "decision": fake_check_patient(patient, trial),
    }

screening = st.session_state.get("screening")
if screening and (screening["patient_id"], screening["trial_id"]) == (
    patient["id"], trial["trial_id"]
):
    st.divider()
    st.subheader("Screening result")
    st.success(f"Decision: **{screening['decision']}**")

    st.markdown("#### Trial rules")
    for criterion in trial.get("criteria", []):
        value = patient.get(criterion.get("field"))
        value_text = "Missing" if value is None else str(value)
        st.markdown(f"❓ **{criterion.get('text', criterion.get('id', 'Criterion'))}** · Patient value: `{value_text}`")

    st.markdown("#### Explanation")
    st.write("This is a placeholder result from the demo check function. Connect the rules and explanation modules when they are ready.")
