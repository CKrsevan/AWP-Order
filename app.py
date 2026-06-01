
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import re

st.set_page_config(layout="wide", page_title="AWP Parser")

st.image("logo.png", width=150)
st.title("AWP Formatter")

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

    def find_value(keyword):
        for k, v in data.items():
            if keyword.lower() in k.lower():
                return v
        return ""

    def find_other(keyword):
        for k, v in data.items():
            kl = k.lower()
            if "other" in kl and keyword.lower() in kl:
                return v
            if "if other" in kl and keyword.lower() in kl:
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

    def ack(keyword):
        val = find_value(keyword)
        if not val:
            return "No"
        val = val.lower()
        if "true" in val or "yes" in val:
            return "Yes"
        if "false" in val or "no" in val:
            return "No"
        return val

    # ---------- SOURCES ----------
    area = find_value("located in")
    access = find_value("access")
    days = find_value("days")
    hours = find_value("working hours")
    systems = find_value("systems will be affected")

    permits = find_value("What sub permits will be required throughout the duration of the works")

    shutdown = find_value("What type of Shutdown or Isolation is required")
    shutdown_main = find_value("require any shutdown")

    combined_shutdown = shutdown + " " + permits + " " + shutdown_main

    other_area = find_other("area")
    other_access = find_other("access")
    other_system = find_other("system")
    other_reason = find_other("reason")

    # ✅ ✅ ✅ IMPROVED STYLE ONLY

    st.markdown("""
    <style>

    /* Light mode */
    [data-theme="light"] .value {
        color: black;
        background: #f7f7f7;
    }

    /* Dark mode */
    [data-theme="dark"] .value {
        color: white;
        background: #333333;
    }

    /* Section styling (same for both) */
    .section {
        font-size:20px;
        font-weight:700;
        margin-top:30px;
        margin-bottom:10px;
        padding-bottom:6px;
        border-bottom:2px solid #e6e6e6;
        color:#1f77b4;
    }

    /* Labels */
    .label {
        font-weight:600;
        font-size:13px;
        margin-bottom:2px;
    }

    /* Default value box */
    .value {
        font-family:monospace;
        font-size:13px;
        padding:6px 8px;
        border-radius:6px;
        margin-bottom:8px;
        border:1px solid #444;
    }

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

    for i,(l,k) in enumerate([
        ("AWP Number","AWP Number"),
        ("Date Updated","Date Updated"),
        ("Updated By","Updated By"),
        ("Description","Work/Activity Description"),
        ("Approval Conditions","Approval Conditions"),
        ("Company Name","Account"),
        ("Company Description","Company Description"),
    ]):
        field(l,k,i)

    # ---------- CONTACT ----------
    st.markdown("<div class='section'>Application / Contact</div>", unsafe_allow_html=True)

    field("Person making the application","Requested by",100)
    field("Applicants email","Email address",101)
    field("Applicants phone number","Phone",102)
    field("WSI Representative","Who is your WSI representative",103)

    # ---------- APPROVAL ----------
    st.markdown("<div class='section'>Approval</div>", unsafe_allow_html=True)

    field("Do you have ABC and ALC approval?","ABC",50)
    field("ABC Ban Number and ALC Permit Number","BAN",51)
    field("Reason ABC and ALC Approval Not Required","not applicable",52)

    # ---------- WORK ----------
    st.markdown("<div class='section'>Work Details</div>", unsafe_allow_html=True)

    field("Type of Work","Type of Work",200)
    field("Type of Work (Other)","Type of Work (Other)",201)
    field("Detailed Location of Works","Detailed location",202)
    field("Detailed Scope of Works","Detailed scope",203)
    field("Proposed Start Date","start date",204)
    field("Proposed End Date","end date",205)
    field("Impacts on Airport Ops","Impacts",206)
    field("Mitigation Measures for Op impacts","Mitigation",207)

    # ---------- PLANS ----------
    st.markdown("<div class='section'>Plans / Management</div>", unsafe_allow_html=True)

    field("Do you require any asset information?","asset information",300)
    field("Provide details of your communication plan","communication plan",301)
    field("Waste Management Plan Details","waste management",302)

    # ---------- SUPERVISION ----------
    st.markdown("<div class='section'>Supervision</div>", unsafe_allow_html=True)

    field("Work hours site Supervisor name","Supervisor name",120)
    field("Work hours site Supervisor Number","Supervisor phone",121)
    field("Site Emergency/After Hours Contact Name","Site Emergency/After Hours Contact person name",122)
    field("Site Emergency/After Hours Contact Number","after hours contact person phone number",123)

    # ---------- SERVICES ----------
    st.markdown("<div class='section'>Services</div>", unsafe_allow_html=True)

    field("Will tools be carried in and out of the Airport Terminal sterile areas?","tools",320)
    field("Will the work include tapping into any existing services?","tapping",321)
    field("Details associated with tapping into the existing service","details associated",322)

    # ---------- ACKNOWLEDGEMENTS ----------
    st.markdown("<div class='section'>Acknowledgements</div>", unsafe_allow_html=True)

    st.markdown(f"Working on the Airfield Acknowledged: {ack('airfield')}")
    st.markdown(f"Accessing the Airfield Acknowledged: {ack('accessing the airfield')}")
    st.markdown(f"Working and Accessing Landside Areas Acknowledged: {ack('landside')}")
    st.markdown(f"Working in the Terminal Acknowledged: {ack('terminal acknowledged')}")

    # ---------- LOCATION ----------
    st.markdown("<div class='section'>Location</div>", unsafe_allow_html=True)

    locs = [
        "Terminal Departures","Terminal Arrivals","Terminal Basement",
        "Terminal Loading Dock","Terminal Bag Room","Gate Lounges",
        "Landside","Apron","Aircraft Bay","Cargo Precinct",
        "Public Carpark","AOCC/AOMF","Terminal Roof",
        "Ancillary Building","Site Wide","Other"
    ]

    c1,c2 = st.columns(2)
    for i,l in enumerate(locs):
        (c1 if i%2==0 else c2).markdown(f"{check(l, area)} {l}")

    if check("Other", area) == "☑" and other_area:
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown("<div class='label'>Other Location</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_area}</div>", unsafe_allow_html=True)
        with col2:
            st_copy_to_clipboard(other_area, "Copy", "Done", key="other_area_copy")

    # ---------- ACCESS ----------
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_list = [
        "Airside Vehicle Gate","Terminal Main Entry","Terminal Staff Entry",
        "Loading Dock","Other"
    ]

    c1,c2 = st.columns(2)
    for i,a in enumerate(access_list):
        (c1 if i%2==0 else c2).markdown(f"{check(a, access)} {a}")

    if check("Other", access) == "☑" and other_access:
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown("<div class='label'>Other Access Point</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_access}</div>", unsafe_allow_html=True)
        with col2:
            st_copy_to_clipboard(other_access, "Copy", "Done", key="other_access_copy")

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
        "Electrical LV","Electrical HV","HVAC",
        "Technology & Network","Security","Hydraulics",
        "Roads and Signage","Fire Systems","Vertical Transport","Other"
    ]

    for s in systems_list:
        st.markdown(f"{check(s, systems)} {s}")

    if check("Other", systems) == "☑" and other_system:
        st.markdown(f"Other System: {other_system}")

    # ---------- PERMITS ----------
    st.markdown("<div class='section'>Permits</div>", unsafe_allow_html=True)

    permits_list = [
        "Confined Space Sub Permit","Out of Hours Works","Crane Lift Sub Permit",
        "Gantry Access Sub Permit","Excavation and Penetration Sub Permit",
        "Hot Work Sub Permit","Isolation Sub Permit","Material Import Permit",
        "Operational Resource Closure/Shutdown Sub Permit","Road Occupancy",
        "Permit to Discharge Water","Vegetation Works",
        "Working at Height or Below Permit","Fire Isolation Permit"
    ]

    for p in permits_list:
        st.markdown(f"{check(p, permits)} {p}")

    # ---------- SHUTDOWN ----------
    st.markdown("<div class='section'>Shutdown</div>", unsafe_allow_html=True)

    st.markdown("Will the work require any shutdowns and/or isolations?")
    st.markdown(yesno(shutdown_main))

    st.markdown("<div class='section'>Shutdown Types</div>", unsafe_allow_html=True)

    for s in [
        "Electrical","Data","HVAC",
        "Water","Fire detection system","High Voltage","Other"
    ]:
        st.markdown(f"{check(s, combined_shutdown)} {s}")

    if check("Other", shutdown) == "☑" and other_reason:
        st.markdown(f"Other Reason: {other_reason}")

    st.markdown("<div class='section'>Shutdown Details</div>", unsafe_allow_html=True)

    field("Proposed Start date of the shutdown/isolations","start date of the shutdown",500)
    field("Proposed End date of the shutdown/isolations","end date of the shutdown",501)
    field("Total duration of the shutdown/isolations","Total duration of the Shutdown/Isolations",502)
