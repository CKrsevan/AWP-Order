import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import re

st.set_page_config(layout="wide", page_title="AWP Parser")

st.title("AWP Parser")

raw = st.text_area("Paste raw AWP text here", height=250)

# ---------- PARSER ----------
if st.button("Process"):
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    data = {}
    key = None

    for line in lines:
        if ":" in line:
            k, v = line.split(":", 1)
            key = k.strip()
            data[key] = v.strip()
        elif key:
            data[key] += " " + line.strip()

    st.session_state["data"] = data

data = st.session_state.get("data")

if data:

    # ---------- HELPERS ----------
    def find_value(keyword):
        for k, v in data.items():
            if keyword.lower() in k.lower():
                return v
        return ""

    def check(val, src):
        src = src.lower()
        src = re.sub(r'[^a-z0-9,\s]', '', src)
        parts = [p.strip() for p in src.split(",") if p.strip()]
        return "☑" if any(val.lower() in p for p in parts) else "☐"

    def yesno(val):
        val = val.lower()
        if "yes" in val:
            return "☑ Yes    ☐ No"
        if "no" in val:
            return "☐ Yes    ☑ No"
        return "☐ Yes    ☐ No"

    # ---------- SOURCES ----------
    area = find_value("located in")
    access = find_value("access point")
    days = find_value("days")
    hours = find_value("working hours")
    systems = find_value("systems will be affected")

    permits = find_value("sub permits will be required")
    shutdown = find_value("shutdown")
    shutdown_main = find_value("require any shutdowns")

    combined_shutdown = shutdown + " " + permits + " " + shutdown_main

    # ✅ OTHER VALUES
    other_location = find_value("other location")
    other_access = find_value("other access")
    description_other = find_value("description other")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    .section { font-size:18px; font-weight:700; margin-top:20px; }
    .label { font-weight:600; font-size:13px; }
    .value { font-family:monospace; font-size:13px; }
    </style>
    """, unsafe_allow_html=True)

    def field(label, keyword, i):
        val = find_value(keyword)
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown(f"<div class='label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{val}</div>", unsafe_allow_html=True)
        with col2:
            st_copy_to_clipboard(val, "Copy", "Done", key=f"{label}_{i}")

    # ---------- GENERAL ----------
    st.markdown("<div class='section'>General</div>", unsafe_allow_html=True)

    general_fields = [
        ("AWP Number","AWP Number"),
        ("Date Updated","Date Updated"),
        ("Updated By","Updated By"),
        ("Description","Work/Activity Description"),
        ("Approval Conditions","Approval Conditions"),
        ("Company Name","Account"),
        ("Company Description","Company Description"),
    ]

    for i,(l,k) in enumerate(general_fields):
        field(l,k,i)

    # ---------- SHUTDOWN FLAG ----------
    st.markdown("<div class='section'>Shutdown / Isolation / Permit Required</div>", unsafe_allow_html=True)
    st.markdown(yesno(shutdown_main))

    # ---------- CONTACT ----------
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)

    for i,(l,k) in enumerate([
        ("Applicant","Requested by"),
        ("Email","Email address"),
        ("Phone","Phone"),
        ("WSI Rep","WSI representative"),
        ("WSI Rep Name","WSI Representative Name"),
    ]):
        field(l,k,i+100)

    # ---------- WORK ----------
    st.markdown("<div class='section'>Work</div>", unsafe_allow_html=True)

    for i,(l,k) in enumerate([
        ("Type of Work","Type of Work"),
        ("Type of Work Other","Type of Work (Other)"),
        ("Detailed Location","Detailed location"),
        ("Detailed Scope","Detailed scope"),
        ("Start Date","start date"),
        ("End Date","end date"),
    ]):
        field(l,k,i+200)

    # ---------- LOCATION ----------
    st.markdown("<div class='section'>Location</div>", unsafe_allow_html=True)

    locs = [
        "Terminal Departures","Terminal Arrivals","Terminal Basement",
        "Terminal Loading Dock","Terminal Bag Room","Gate Lounges",
        "Landside","Apron","Aircraft Bay","Cargo Precinct",
        "Public Carpark","AOCC/AOMF","Terminal Roof",
        "Ancillary Building","Site Wide","Other Location"
    ]

    c1,c2 = st.columns(2)
    for i,l in enumerate(locs):
        (c1 if i%2==0 else c2).markdown(f"{check(l, area)} {l}")

    # ✅ SHOW OTHER LOCATION VALUE
    if "other location" in area.lower() or other_location:
        st.markdown(f"**Other Location:** {other_location}")

    # ---------- ACCESS ----------
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_list = [
        "Airside Vehicle Gate","Terminal Main Entry",
        "Terminal Staff Entry","Loading Dock","Other Access Point"
    ]

    c1,c2 = st.columns(2)
    for i,a in enumerate(access_list):
        (c1 if i%2==0 else c2).markdown(f"{check(a, access)} {a}")

    if "other" in access.lower() or other_access:
        st.markdown(f"**Other Access:** {other_access}")

    # ---------- DAYS ----------
    st.markdown("<div class='section'>Days</div>", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    for i,d in enumerate(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]):
        (c1 if i%2==0 else c2).markdown(f"{check(d, days)} {d}")

    # ---------- HOURS ----------
    st.markdown("<div class='section'>Hours</div>", unsafe_allow_html=True)

    for h in ["Morning","Afternoon","Night"]:
        st.markdown(f"{check(h, hours)} {h}")

    # ---------- SYSTEMS ----------
    st.markdown("<div class='section'>Systems</div>", unsafe_allow_html=True)

    for s in [
        "Electrical LV","Electrical HV","HVAC","Technology & Network",
        "Security","Hydraulics","Roads and Signage","Fire Systems","Vertical Transport"
    ]:
        st.markdown(f"{check(s, systems)} {s}")

    # ---------- PERMITS ----------
    st.markdown("<div class='section'>Permits</div>", unsafe_allow_html=True)

    for p in [
        "Confined Space","Out of Hours","Crane Lift","Gantry Access",
        "Protected Areas","Excavation","Hot Work","Isolation","Material Import"
    ]:
        st.markdown(f"{check(p, permits)} {p}")

    # ---------- SHUTDOWN TYPES ----------
    st.markdown("<div class='section'>Shutdowns</div>", unsafe_allow_html=True)

    for s in [
        "Electrical","Data","HVAC","Water",
        "Fire detection system","High Voltage","Other"
    ]:
        st.markdown(f"{check(s, combined_shutdown)} {s}")

    # ---------- EXTRA ----------
    st.markdown("<div class='section'>Shutdown Details</div>", unsafe_allow_html=True)

    for i,(l,k) in enumerate([
        ("Shutdown Start","start date of the shutdown"),
        ("Shutdown End","end date of the shutdown"),
        ("Shutdown Duration","duration")
    ]):
        field(l,k,i+500)

    # ✅ OTHER DESCRIPTION
    if description_other:
        st.markdown(f"**Other Description:** {description_other}")