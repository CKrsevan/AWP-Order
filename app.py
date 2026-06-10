
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import re

st.set_page_config(layout="wide", page_title="AWP Parser")

st.image("logo.png", width=150)
st.title("AWP Formatter")


if st.session_state.get("clear_trigger"):
    st.session_state["raw_text"] = ""
    st.session_state["clear_trigger"] = False




raw = st.text_area(
    "Paste raw AWP text here",
    height=250,
    key="raw_text"
)




col1, col2 = st.columns([1,1])

with col1:
    process_clicked = st.button("Process", key="process_button", use_container_width=True)

with col2:
    if st.button("Clear", key="clear_button", use_container_width=True):
        st.session_state["clear_trigger"] = True
        st.session_state["data"] = None
        st.rerun()




# ✅ Only ONE trigger

if process_clicked:

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



# ---------- PARSER ----------

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
        def clean(text):
            text = text.lower()
            text = text.replace("&amp;", "&")
            text = re.sub(r'[^a-z0-9\s]', '', text)
            return text.strip()

        src_parts = [clean(p) for p in src.split(",") if p.strip()]
        val_clean = clean(val)

        return "☑" if any(val_clean in p for p in src_parts) else "☐"

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
    shutdown_reason = find_value("reason for the shutdown")
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
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)

    field("Applicant","Requested by",100)
    field("Email","Email address",101)
    field("Phone","Phone",102)

    field("WSI Rep","Who is your WSI representative",103)

    # ---------- APPROVAL ----------
    st.markdown("<div class='section'>Approval</div>", unsafe_allow_html=True)

    field("ABC / ALC Approval","ABC",50)
    field("BAN Number","BAN",51)
    field("Reason Not Required","not applicable",52)

  # ---------- WORK ----------
    st.markdown("<div class='section'>Work</div>", unsafe_allow_html=True)

    field("Type of Work","Type of Work",200)
    field("Type of Work Other","Type of Work (Other)",201)
    field("Detailed Location","Detailed location",202)
    field("Detailed Scope","Detailed scope",203)
    field("Start Date","start date",204)
    field("End Date","end date",205)
    field("Impacts","Impacts",206)
    field("Mitigation","Mitigation",207)

    # ---------- SUPERVISION ----------
    st.markdown("<div class='section'>Supervision</div>", unsafe_allow_html=True)

    field("Supervisor Name","Supervisor name",120)
    field("Supervisor Phone","Supervisor phone",121)

    field("Emergency Contact Name","Site Emergency/After Hours Contact person name",122)
    field("Emergency Contact Phone","after hours contact person phone number",123)

    # ---------- PLANS ----------
    st.markdown("<div class='section'>Plans / Management</div>", unsafe_allow_html=True)

    field("Asset Info","asset information",300)
    field("Communication Plan","communication plan",301)

    # ---------- SERVICES ----------
    st.markdown("<div class='section'>Services</div>", unsafe_allow_html=True)

    field("Tools in Terminal","tools",320)
    field("Tapping Services","tapping",321)
    field("Tapping Details","details associated",322)

    # ---------- ACKNOWLEDGEMENTS ----------
    st.markdown("<div class='section'>Acknowledgements</div>", unsafe_allow_html=True)

    st.markdown(f"Working on Airfield: {ack('airfield')}")
    st.markdown(f"Accessing Airfield: {ack('accessing the airfield')}")
    st.markdown(f"Working Landside: {ack('landside')}")
    st.markdown(f"Working Terminal: {ack('terminal acknowledged')}")

    # ---------- WASTE MANAGEMENT ----------
    st.markdown("<div class='section'>Waste Management</div>", unsafe_allow_html=True)

    field("Waste Plan","waste management",302)

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
            st.markdown("<div class='label'>Other Area</div>", unsafe_allow_html=True)
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
            st.markdown("<div class='label'>Other Access</div>", unsafe_allow_html=True)
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
        col1, col2 = st.columns([6,1])

        with col1:
            st.markdown("<div class='label'>Other System</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_system}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_system, "Copy", "Done", key="other_system_copy")


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
    st.markdown("<div class='section'>Shutdown Required</div>", unsafe_allow_html=True)
    st.markdown(yesno(shutdown_main))

    # ---------- SHUTDOWN TYPES ----------
    st.markdown("<div class='section'>Shutdown Types</div>", unsafe_allow_html=True)

    for s in [
        "Electrical","Data","HVAC",
        "Water","Fire detection system","High Voltage","Other"
    ]:
        st.markdown(f"{check(s, combined_shutdown)} {s}")


    if check("Other", shutdown) == "☑" and other_reason:
        col1, col2 = st.columns([6,1])

        with col1:
            st.markdown("<div class='label'>Other Reason</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_reason}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_reason, "Copy", "Done", key="other_reason_copy")

    # ---------- REASON FOR SHUTDOWN ----------
    st.markdown("<div class='section'>Reason For Shutdown</div>", unsafe_allow_html=True)

    reason_list = [
        "Maintenance",
        "Repair",
        "Installation",
        "Testing",
        "Other"   # ✅ ADD THIS
    ]

    c1, c2 = st.columns(2)
    for i, r in enumerate(reason_list):
        (c1 if i % 2 == 0 else c2).markdown(f"{check(r, shutdown_reason)} {r}")

    # ✅ SHOW "OTHER" VALUE (same pattern as other sections)
    if check("Other", shutdown_reason) == "☑" and other_reason:
        col1, col2 = st.columns([6,1])

        with col1:
            st.markdown("<div class='label'>Other Reason</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_reason}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_reason, "Copy", "Done", key="other_reason_reason_copy")
        # ---------- SHUTDOWN DETAILS ----------
    st.markdown("<div class='section'>Shutdown Details</div>", unsafe_allow_html=True)

    field("Shutdown Start","start date of the shutdown",500)
    field("Shutdown End","end date of the shutdown",501)
    field("Shutdown Duration","Total duration of the Shutdown/Isolations",502)
