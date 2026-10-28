"""Polished Streamlit UI for the synthetic clinical-trial eligibility demo."""
import html
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


st.set_page_config(page_title="Trial Eligibility Screener", page_icon="🩺", layout="wide")
dark_mode = st.sidebar.toggle("Dark mode", value=False)
dark_theme_css = """
<style>
:root {
  --ink: #e4eef2;
  --muted: #a8bdc7;
  --teal: #58c6c1;
  --teal-dark: #30aaa8;
  --line: #2b4654;
  --paper: #142a36;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stSidebar"], [data-testid="stBottom"] {
  background-color: #0b1520 !important;
  color: #e4eef2 !important;
}
[data-testid="stAppViewContainer"] {
  background: radial-gradient(ellipse at 50% -18%, #153a43 0, transparent 48%), #0b1520 !important;
}
[data-testid="stSidebar"] { border-right: 1px solid #223a47; }
[data-testid="stHeader"] { background: transparent !important; }
h1, h2, h3, p, label, [data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"] {
  color: #e4eef2 !important;
}
.section-label, [data-testid="stSelectbox"] label { color: #b0c5ce !important; }
.hero { background: linear-gradient(120deg, #0a2435 0%, #10404d 58%, #086b75 100%); }
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background: #142a36 !important; border-color: #35515e !important; color: #e4eef2 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] * { color: #e4eef2 !important; }
[data-baseweb="popover"], [role="listbox"], [role="option"] {
  background: #142a36 !important; color: #e4eef2 !important;
}
[role="option"]:hover { background: #20414e !important; }
div.stButton > button { color: #06232b !important; background: linear-gradient(100deg, #58c6c1, #38aaa9) !important; }
.result-card, .criterion-row { background: #142a36 !important; border-color: #2b4654 !important; }
.result-title, .criterion-text, .subhead { color: #e4eef2 !important; }
.result-kicker, .criterion-value, .footnote { color: #a8bdc7 !important; }
.explanation { color: #d5e5e9 !important; background: #17343e !important; border-left-color: #58c6c1 !important; }
.criterion-icon { color: #58c6c1 !important; }
</style>
""" if dark_mode else ""
st.markdown(
    """
    <style>
    :root {
      --ink: #142b3b;
      --muted: #5d7180;
      --teal: #087f8c;
      --teal-dark: #06636e;
      --line: #dce7e8;
      --paper: #ffffff;
    }
    [data-testid="stAppViewContainer"] {
      background: radial-gradient(ellipse at 50% -18%, #d9f0ed 0, transparent 48%), #f4f8f8;
      color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1040px; padding-top: 3.2rem; padding-bottom: 4rem; }
    h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { color: var(--ink); }
    .hero {
      padding: 2rem 2.2rem 1.9rem;
      border: 1px solid rgba(255,255,255,.22);
      border-radius: 24px;
      color: white;
      background: linear-gradient(120deg, #102f43 0%, #155565 58%, #087f8c 100%);
      box-shadow: 0 18px 44px rgba(18, 53, 68, .16);
      margin-bottom: 1.6rem;
      animation: enter 650ms cubic-bezier(.2,.75,.25,1) both;
    }
    .hero .eyebrow { color: #a9e2dc; font-size: .76rem; letter-spacing: .13em; font-weight: 750; text-transform: uppercase; margin: 0 0 .8rem; }
    .hero h1 { color: white; font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.06; letter-spacing: -.035em; margin: 0; }
    .hero .lede { color: #d5e7e9; font-size: 1.02rem; margin: .8rem 0 0; }
    .section-label { color: #486171; font-size: .78rem; font-weight: 750; letter-spacing: .1em; text-transform: uppercase; margin: .3rem 0 .55rem; }
    [data-testid="stSelectbox"] label { color: #405a69; font-size: .9rem; font-weight: 650; }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
      background: var(--paper); border: 1px solid var(--line); border-radius: 12px; min-height: 3.1rem;
      box-shadow: 0 3px 12px rgba(25, 55, 65, .035);
    }
    [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover { border-color: #84bdc0; }
    div.stButton > button {
      border: 0; border-radius: 12px; min-height: 3.2rem; font-weight: 700; letter-spacing: .01em;
      color: white; background: linear-gradient(100deg, #087f8c, #0a9295);
      box-shadow: 0 8px 20px rgba(8, 127, 140, .2); transition: transform 160ms ease, box-shadow 160ms ease;
    }
    div.stButton > button:hover { color: white; transform: translateY(-2px); box-shadow: 0 12px 24px rgba(8, 127, 140, .28); border: 0; }
    .result-card {
      background: var(--paper); border: 1px solid var(--line); border-radius: 20px;
      padding: 1.3rem 1.5rem; margin: 1.2rem 0 1.5rem;
      box-shadow: 0 12px 32px rgba(25, 55, 65, .07);
      animation: enter 500ms ease-out both;
    }
    .result-top { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
    .result-kicker { color: var(--muted); font-size: .78rem; font-weight: 750; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 .35rem; }
    .result-title { color: var(--ink); font-size: 1.35rem; font-weight: 750; margin: 0; }
    .badge { border-radius: 999px; padding: .48rem .85rem; font-size: .86rem; font-weight: 750; white-space: nowrap; }
    .badge-eligible { color: #17634a; background: #e2f4e9; border: 1px solid #c4e8d2; }
    .badge-review { color: #8b5812; background: #fff2d8; border: 1px solid #f3dfb2; }
    .badge-ineligible { color: #9b3f48; background: #fbe9e9; border: 1px solid #f0cece; }
    .subhead { color: #19394b; font-size: 1.08rem; font-weight: 750; margin: 1.7rem 0 .7rem; }
    .criterion-row {
      display: grid; grid-template-columns: 2rem minmax(0, 1fr) minmax(130px, .7fr); align-items: center; gap: .8rem;
      background: rgba(255,255,255,.9); border: 1px solid var(--line); border-radius: 12px;
      padding: .8rem 1rem; margin: .5rem 0; box-shadow: 0 3px 10px rgba(25,55,65,.025);
      animation: enter 450ms ease-out both;
    }
    .criterion-icon { color: #087f8c; font-size: 1.55rem; line-height: 1; text-align: center; }
    .criterion-text { color: #203c4b; font-weight: 650; }
    .criterion-value { color: #536b78; font-size: .87rem; text-align: right; overflow-wrap: anywhere; }
    .explanation {
      color: #405b69; background: #eaf4f3; border-left: 3px solid #48a5a2;
      border-radius: 0 12px 12px 0; padding: .95rem 1rem; line-height: 1.6;
    }
    .footnote { color: #71838e; font-size: .8rem; text-align: center; margin-top: 2rem; }
    @keyframes enter { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes reveal { from { opacity: .28; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
    @supports (animation-timeline: view()) {
      .criterion-row { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% entry 85%; }
    }
    @media (max-width: 650px) {
      .block-container { padding-top: 1.25rem; }
      .hero { padding: 1.5rem; border-radius: 18px; }
      .criterion-row { grid-template-columns: 1.8rem minmax(0, 1fr); }
      .criterion-value { grid-column: 2; text-align: left; }
      .result-card { padding: 1.1rem; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
    }
    </style>
    """ + dark_theme_css,
    unsafe_allow_html=True,
)

st.markdown(
    '<section class="hero"><p class="eyebrow">Clinical research · Screening demo</p>'
    '<h1>Trial Eligibility Screener</h1>'
    '<p class="lede">A clear first look at trial criteria using synthetic patient data.</p></section>',
    unsafe_allow_html=True,
)
trials = load_data("trials.json")
patients = load_data("patients.json")

st.markdown('<div class="section-label">Choose a study and patient</div>', unsafe_allow_html=True)
trial_col, patient_col = st.columns(2)
with trial_col:
    trial = st.selectbox(
        "Trial",
        trials,
        format_func=lambda item: f"{item['trial_id']} · {item['name']}",
    )
with patient_col:
    patient = st.selectbox("Patient", patients, format_func=lambda item: item["id"])

if st.button("Check eligibility", type="primary", use_container_width=True):
    st.session_state.screening = {
        "patient_id": patient["id"],
        "trial_id": trial["trial_id"],
        "decision": fake_check_patient(patient, trial),
    }

screening = st.session_state.get("screening")
if screening and (screening["patient_id"], screening["trial_id"]) == (
    patient["id"], trial["trial_id"]
):
    decision = screening["decision"]
    badge_class = {
        "Eligible": "badge-eligible",
        "Not eligible": "badge-ineligible",
        "Needs review": "badge-review",
    }.get(decision, "badge-review")
    safe_decision = html.escape(str(decision))
    st.markdown(
        '<section class="result-card"><div class="result-top">'
        '<div><p class="result-kicker">Screening result</p><p class="result-title">'
        f'{html.escape(trial["name"])}</p></div>'
        f'<span class="badge {badge_class}">{safe_decision}</span></div></section>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="subhead">Criterion checklist</div>', unsafe_allow_html=True)
    for criterion in trial.get("criteria", []):
        value = patient.get(criterion.get("field"))
        value_text = "Missing" if value is None else str(value)
        criterion_text = html.escape(str(criterion.get("text", criterion.get("id", "Criterion"))))
        value_text = html.escape(value_text)
        st.markdown(
            '<div class="criterion-row"><span class="criterion-icon">•</span>'
            f'<span class="criterion-text">{criterion_text}</span>'
            f'<span class="criterion-value">Patient value: {value_text}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="subhead">Explanation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="explanation">This is a demo placeholder. The temporary check returns '
        '“Eligible” for every patient; connect the rules and explanation modules before using '
        'screening results.</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footnote">Synthetic data only · For demonstration, not clinical decision-making</div>',
    unsafe_allow_html=True,
)
