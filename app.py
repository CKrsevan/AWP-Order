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

    # ---------- FLEXIBLE FIND ----------
    def find_value(keyword):
        for k, v in data.items():
            if keyword.lower() in k.lower():
                return v
        return ""

    # ---------- CLEAN MATCH ----------
    def check(val, src):
        src = src.lower()
        src = re.sub(r'[^a-z0-9,\s]', '', src)
        parts = [p.strip() for p in src.split(",") if p.strip()]
        return "☑" if any(val.lower() in p for p in parts) else "☐"

    # ---------- SOURCES ----------
    area = find_value("located in")
    access = find_value("access point")
    days = find_value("days")
    hours = find_value("working hours")
    systems = find_value("systems will be affected")
    permits = find_value("sub permits")
    shutdown = find_value("shutdown")

    # ---------- STYLE ----------
    st.markdown("""
    <style>
    .section { font-size:18px; font-weight:700; margin-top:20px; }
    .label { font-weight:600; font-size:13px; }
    .value { font-family:monospace; font-size:13px; }
    </style>
    """, unsafe_allow_html=True)

    # ---------- FIELD DISPLAY ----------
    def field(label, keyword, i):
        val = find_value(keyword)
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown(f"<div class='label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{val}</div>", unsafe_allow_html=True)
        with col2:
            st_copy_to_clipboard(val, before_copy_label="Copy", after_copy_label="Done", key=f"{label}_{i}")

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

    # ---------- CONTACT ----------
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)

    contact_fields = [
        ("Applicant","Requested by"),
        ("Email","Email address"),
        ("Phone","Phone"),
        ("WSI Rep","WSI representative"),
        ("WSI Rep Name","WSI Representative Name"),
    ]

    for i,(l,k) in enumerate(contact_fields):
        field(l,k,i+100)

    # ---------- WORK ----------
    st.markdown("<div class='section'>Work</div>", unsafe_allow_html=True)

    work_fields = [
        ("Type of Work","Type of Work"),
        ("Type of Work Other","Type of Work (Other)"),
        ("Detailed Location","Detailed location"),
        ("Detailed Scope","Detailed scope"),
        ("Start Date","start date"),
        ("End Date","end date"),
        ("Impacts","Impacts"),
        ("Mitigation","Mitigation"),
    ]

    for i,(l,k) in enumerate(work_fields):
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
        txt = f"{check(l, area)} {l}"
        (c1 if i%2==0 else c2).markdown(txt)

    # ---------- ACCESS ----------
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_list = [
        "Airside Vehicle Gate","Terminal Main Entry",
        "Terminal Staff Entry","Loading Dock","Other Access Point"
    ]

    c1,c2 = st.columns(2)
    for i,a in enumerate(access_list):
        (c1 if i%2==0 else c2).markdown(f"{check(a, access)} {a}")

    # ---------- DAYS ----------
    st.markdown("<div class='section'>Days</div>", unsafe_allow_html=True)

    days_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    c1,c2 = st.columns(2)
    for i,d in enumerate(days_list):
        (c1 if i%2==0 else c2).markdown(f"{check(d, days)} {d}")

    # ---------- HOURS ----------
    st.markdown("<div class='section'>Hours</div>", unsafe_allow_html=True)

    for h in ["Morning","Afternoon","Night"]:
        st.markdown(f"{check(h, hours)} {h}")

    # ---------- SYSTEMS ----------
    st.markdown("<div class='section'>Systems</div>", unsafe_allow_html=True)

    systems_list = [
        "Electrical LV","Electrical HV","HVAC","Technology & Network",
        "Security","Hydraulics","Roads and Signage","Fire Systems","Vertical Transport"
    ]

    for s in systems_list:
        st.markdown(f"{check(s, systems)} {s}")

    # ---------- PERMITS ----------
    st.markdown("<div class='section'>Permits</div>", unsafe_allow_html=True)

    permits_list = [
        "Confined Space","Out of Hours","Crane Lift","Gantry Access",
        "Protected Areas","Excavation","Hot Work","Isolation","Material Import",
        "Road Occupancy","Controlled Activity","Discharge Water",
        "Vegetation","Working at Height","Fire Isolation"
    ]

    for p in permits_list:
        st.markdown(f"{check(p, permits)} {p}")

    # ---------- SHUTDOWNS ----------
    st.markdown("<div class='section'>Shutdowns</div>", unsafe_allow_html=True)

    shutdown_list = [
        "Electrical","Data","HVAC","Water",
        "Fire detection system","High Voltage","Other"
    ]

    for s in shutdown_list:
        st.markdown(f"{check(s, shutdown)} {s}")

    # ---------- EXTRA ----------
    st.markdown("<div class='section'>Shutdown Details</div>", unsafe_allow_html=True)

    extra_fields = [
        ("Shutdown Type","Maintenance"),
        ("Shutdown Reason","Other Reason"),
        ("Shutdown Start","start date of the shutdown"),
        ("Shutdown End","end date of the shutdown"),
        ("Shutdown Duration","duration")
    ]

    for i,(l,k) in enumerate(extra_fields):
        field(l,k,i+500)