import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="AWP Parser")

st.title("AWP Parser")

raw = st.text_area("Paste raw AWP text here", height=300)

# ---------- PROCESS ----------
if st.button("Process"):

    if not raw.strip():
        st.warning("Paste data first")
        st.stop()

    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    data = {}
    current_key = None

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = value.strip()
        else:
            if current_key:
                data[current_key] += " " + line.strip()

    st.session_state["data"] = data

# ---------- LOAD ----------
data = st.session_state.get("data", None)

if data:

    # ---------- MAPPING ----------
    mapping = {
        "Company Name": "Account",
        "Applicants email": "Email address",
        "Applicants phone number": "Phone",
        "Person making the application": "Requested by",
        "WSI Representative": "Who is your WSI representative?",
        "Detailed Location of Works": "Detailed location of works/activity",
        "Detailed Scope of Works": "Detailed scope of works/activity",
        "Proposed Start Date": "Proposed start date",
        "Proposed End Date": "Proposed end date",
    }

    def get(field):
        key = mapping.get(field, field)
        val = data.get(key, "")
        if isinstance(val, str) and val.lower() == "true":
            return "Yes"
        return val

    # ---------- SOURCES ----------
    area = data.get("Detailed location of works/activity", "")
    days = data.get("Days required", "")
    hours = data.get("Working Hours", "")

    def check(val, src):
        return "Yes" if val.lower() in src.lower() else ""

    # ---------- RESULTS ----------
    results = [
        ["Company Name", get("Company Name")],
        ["Applicants email", get("Applicants email")],
        ["Applicants phone number", get("Applicants phone number")],
        ["WSI Representative", get("WSI Representative")],
        ["Detailed Location of Works", get("Detailed Location of Works")],
        ["Detailed Scope of Works", get("Detailed Scope of Works")],
    ]

    # checkbox logic
    for loc in ["Landside", "Apron", "Cargo Precinct"]:
        results.append([loc, check(loc, area)])

    for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        results.append([d, check(d, days)])

    for h in ["Morning","Afternoon","Night"]:
        results.append([h, check(h, hours)])

    df = pd.DataFrame(results, columns=["Field","Value"])

    st.subheader("Parsed Output")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    .field-title {
        font-weight: 600;
        font-size: 16px;
        margin-top: 16px;
        margin-bottom: 6px;
    }

    pre {
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 13px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- DISPLAY ----------
    for i, row in df.iterrows():

        st.markdown(f"<div class='field-title'>{row['Field']}</div>", unsafe_allow_html=True)

        # ✅ BUILT-IN COPY BUTTON (WORKS IN CLOUD)
        st.code(row["Value"], language="text")

    # ---------- DOWNLOAD ----------
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "awp_output.csv",
        "text/csv"
    )
