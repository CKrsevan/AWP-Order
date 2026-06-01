import streamlit as st
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
        "Description": "Work/Activity Description"
    }

    def get(field):
        key = mapping.get(field, field)
        val = data.get(key, "")
        return "Yes" if isinstance(val, str) and val.lower() == "true" else val

    # ✅ FINAL CHECK FUNCTION (FIXED PROPERLY)
    def check(val, src):
        src = src.lower()

        # normalize separators
        for ch in [";", "/", "-", "(", ")", "\n"]:
            src = src.replace(ch, ",")

        parts = [p.strip() for p in src.split(",") if p.strip()]

        return "☑" if any(val.lower() in p for p in parts) else "☐"

    # ---------- SOURCES ----------
    area = (
        data.get("What area(s) is the work/activity located in", "")
        or data.get("Detailed location of works/activity", "")
    )

    days = data.get("Days required", "")
    hours = data.get("Working Hours", "")
    access = data.get("What Access point will be required for personnel and deliveries", "")
    systems = data.get("What systems will be affected by the works?", "")
    permits = data.get("What sub permits will be required throughout the duration of the works?", "")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    .section { font-size:18px; font-weight:700; margin-top:20px; }
    .label { font-weight:600; font-size:13px; }
    .value { font-family:monospace; font-size:13px; }
    </style>
    """, unsafe_allow_html=True)

    # ---------- FIELD DISPLAY ----------
    def show_field(name, i):
        val = get(name)

        col1, col2 = st.columns([6,1])

        with col1:
            st.markdown(f"<div class='label'>{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{val}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(
                val,
                before_copy_label="Copy",
                after_copy_label="Done",
                key=f"{name}_{i}"
            )

    # ---------- GENERAL ----------
    st.markdown("<div class='section'>General Information</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "AWP Number","Date Updated","Updated By","Description",
        "Company Name","Company Description"
    ]):
        show_field(f, i)

    # ---------- CONTACT ----------
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "Person making the application","Applicants email","Applicants phone number",
        "WSI Representative"
    ]):
        show_field(f, i + 100)

    # ---------- WORK ----------
    st.markdown("<div class='section'>Work Details</div>", unsafe_allow_html=True)
    for i, f in enumerate([
        "Detailed Location of Works","Detailed Scope of Works",
        "Proposed Start Date","Proposed End Date"
    ]):
        show_field(f, i + 200)

    # ---------- LOCATION ----------
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
        text = f"{check(loc, area)} {loc}"
        if i % 2 == 0:
            col1.markdown(text)
        else:
            col2.markdown(text)

    # ---------- ACCESS ----------
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_fields = [
        "Airside Vehicle Gate","Terminal Main Entry",
        "Terminal Staff Entry","Loading Dock"
    ]

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