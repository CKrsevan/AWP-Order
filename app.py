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

    # ---------- FIELD MAPPING ----------
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
        "Waste Management Plan Details": "Provide details of your waste management plan"
    }

    def get(field):
        key = mapping.get(field, field)
        val = data.get(key, "")
        if isinstance(val, str) and val.lower() == "true":
            return "Yes"
        return val

    def check(val, src):
        return "Yes" if val.lower() in src.lower() else ""

    # ---------- SOURCES ----------
    area = data.get("Detailed location of works/activity", "")
    days = data.get("Days required", "")
    hours = data.get("Working Hours", "")
    access = data.get("What Access point will be required for personnel and deliveries", "")
    systems = data.get("What systems will be affected by the works?", "")
    permits = data.get("What sub permits will be required throughout the duration of the works?", "")
    shutdown = data.get("Will the work require any shutdowns and/or isolations?", "")

    # ---------- GROUPS ----------
    sections = {
        "General Information": [
            "AWP Number","Date Updated","Updated By","Description",
            "Approval Conditions or Requirements","Company Name","Company Description"
        ],
        "Contact Details": [
            "Person making the application","Applicants email","Applicants phone number",
            "WSI Representative","WSI Representative Name"
        ],
        "Work Details": [
            "Type of Work","Type of Work (Other)",
            "Detailed Location of Works","Detailed Scope of Works",
            "Proposed Start Date","Proposed End Date",
            "Impacts on Airport Ops","Mitigation Measures for Op impacts"
        ],
        "Location": [
            "Terminal Departures","Terminal Arrivals","Terminal Basement",
            "Terminal Loading Dock","Terminal Bag Room","Gate Lounges",
            "Landside","Apron","Aircraft Bay","Cargo Precinct"
        ],
        "Access & Schedule": [
            "Airside Vehicle Gate","Terminal Main Entry","Terminal Staff Entry",
            "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",
            "Morning","Afternoon","Night"
        ],
        "Systems & Permits": [
            "Electrical LV","Electrical HV","HVAC",
            "Technology & Network","Security","Hydraulics",
            "Confined Space Sub Permit","Hot Work Sub Permit"
        ],
        "Shutdowns": [
            "Electrical","Data","HVAC","Water (potable/recycled/sewer etc)",
            "Fire detection system","High Voltage"
        ]
    }

    # ---------- STYLING ----------
    st.markdown("""
    <style>
    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .field-row {
        padding: 6px;
        border-bottom: 1px solid #333;
        margin-bottom: 6px;
    }

    .field-title {
        font-weight: 600;
        font-size: 13px;
    }

    .value-text {
        font-family: monospace;
        font-size: 13px;
        margin-top: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- DISPLAY ----------
    for section, fields in sections.items():

        st.markdown(f"<div class='section-title'>{section}</div>", unsafe_allow_html=True)

        for f in fields:

            value = get(f)

            # checkbox logic
            if f in area:
                value = check(f, area)
            if f in days:
                value = check(f, days)
            if f in hours:
                value = check(f, hours)
            if f in access:
                value = check(f, access)
            if f in systems:
                value = check(f, systems)
            if f in permits:
                value = check(f, permits)
            if f in shutdown:
                value = check(f, shutdown)

            st.markdown("<div class='field-row'>", unsafe_allow_html=True)

            col1, col2 = st.columns([6, 1])

            with col1:
                st.markdown(f"<div class='field-title'>{f}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='value-text'>{value}</div>", unsafe_allow_html=True)

            with col2:
                st_copy_to_clipboard(
                    value,
                    before_copy_label="Copy",
                    after_copy_label="Done",
                    key=f"{section}_{f}"
                )

            st.markdown("</div>", unsafe_allow_html=True)