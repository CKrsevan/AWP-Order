import streamlit as st
import pandas as pd
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(layout="wide", page_title="AWP Parser")

st.title("AWP Parser")

raw = st.text_area("Paste raw AWP text here", height=250)

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

    # ✅ MAPPING (IMPORTANT FIX)
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
        "Impacts on Airport Ops": "Impacts on Airport Operations",
        "Mitigation Measures for Op impacts": "Mitigation Measures for operational impacts",
        "Waste Management Plan Details": "Provide details of your waste management plan",
        "Description": "Work/Activity Description"  # ✅ YOUR REQUEST
    }

    def get(field):
        key = mapping.get(field, field)
        val = data.get(key, "")
        return "Yes" if isinstance(val, str) and val.lower() == "true" else val

    def check(val, src):
        return "☑" if val.lower() in src.lower() else "☐"

    # ---------- SOURCES ----------
    area = data.get("Detailed location of works/activity", "")
    days = data.get("Days required", "")
    hours = data.get("Working Hours", "")
    access = data.get("What Access point will be required for personnel and deliveries", "")
    systems = data.get("What systems will be affected by the works?", "")
    permits = data.get("What sub permits will be required throughout the duration of the works?", "")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    .section {
        font-size: 18px;
        font-weight: 700;
        margin-top: 20px;
    }

    .field-row {
        padding: 6px 0;
        border-bottom: 1px solid #333;
    }

    .field-title {
        font-weight: 600;
        font-size: 13px;
    }

    .value {
        font-family: monospace;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- FIELD DISPLAY FUNCTION ----------
    def show_field(name, key):

        value = get(name)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(f"<div class='field-title'>{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{value}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(
                value,
                before_copy_label="Copy",
                after_copy_label="Done",
                key=key
            )

    # ---------- GENERAL ----------
    st.markdown("<div class='section'>General Information</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "AWP Number","Date Updated","Updated By","Description",
        "Approval Conditions or Requirements","Company Name","Company Description"
    ]):
        show_field(f, f"gen_{i}")

    # ---------- CONTACT ----------
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "Person making the application","Applicants email","Applicants phone number",
        "WSI Representative","WSI Representative Name"
    ]):
        show_field(f, f"contact_{i}")

    # ---------- WORK ----------
    st.markdown("<div class='section'>Work Details</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "Type of Work","Detailed Location of Works","Detailed Scope of Works",
        "Proposed Start Date","Proposed End Date"
    ]):
        show_field(f, f"work_{i}")

# ---------- LOCATION (FIXED) ----------
st.markdown("<div class='section'>Location of Works</div>", unsafe_allow_html=True)

location_fields = [
    "Terminal Departures","Terminal Arrivals","Terminal Basement",
    "Terminal Loading Dock","Terminal Bag Room","Gate Lounges",
    "Landside","Apron","Aircraft Bay","Cargo Precinct",
    "Public Carpark","AOCC/AOMF","Terminal Roof",
    "Ancillary Building","Site Wide","Other Location"
]

col1, col2 = st.columns(2)

for i, loc in enumerate(location_fields):

    # ✅ ALWAYS use check()
    value = check(loc, area)

    text = f"{value} {loc}"

    if i % 2 == 0:
        col1.markdown(text)
    else:
        col2.markdown(text)

    # ---------- ACCESS ----------
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_fields = ["Airside Vehicle Gate","Terminal Main Entry","Terminal Staff Entry"]

    col1, col2 = st.columns(2)

    for i, a in enumerate(access_fields):
        text = f"{check(a, access)} {a}"

        if i % 2 == 0:
            col1.markdown(text)
        else:
            col2.markdown(text)

    # ---------- DAYS ----------
    st.markdown("<div class='section'>Days</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    for i, d in enumerate(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]):
        text = f"{check(d, days)} {d}"

        if i % 2 == 0:
            col1.markdown(text)
        else:
            col2.markdown(text)

    # ---------- HOURS ----------
    st.markdown("<div class='section'>Working Hours</div>", unsafe_allow_html=True)

    for h in ["Morning","Afternoon","Night"]:
        st.markdown(f"{check(h, hours)} {h}")

    # ---------- SYSTEMS ----------
    st.markdown("<div class='section'>Systems</div>", unsafe_allow_html=True)

    for s in ["Electrical LV","Electrical HV","HVAC","Security"]:
        st.markdown(f"{check(s, systems)} {s}")

    # ---------- PERMITS ----------
    st.markdown("<div class='section'>Permits</div>", unsafe_allow_html=True)

    for p in ["Confined Space Sub Permit","Hot Work Sub Permit"]:
        st.markdown(f"{check(p, permits)} {p}")