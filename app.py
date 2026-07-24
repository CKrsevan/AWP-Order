import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
import re
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment


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


col1, col2 = st.columns([1, 1])

with col1:
    process_clicked = st.button("Process", key="process_button", use_container_width=True)

with col2:
    if st.button("Clear", key="clear_button", use_container_width=True):
        st.session_state["clear_trigger"] = True
        st.session_state["data"] = None
        st.rerun()


# ---------- PROCESS ----------
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


# ---------- EXCEL EXPORT FUNCTION ----------
def create_excel_file(export_rows):
    wb = Workbook()
    ws = wb.active
    ws.title = "AWP Formatted Data"

    headers = ["Section", "Field", "Value"]
    ws.append(headers)

    header_fill = PatternFill("solid", fgColor="1F77B4")
    header_font = Font(color="FFFFFF", bold=True)

    section_fill = PatternFill("solid", fgColor="D9EAF7")
    section_font = Font(color="1F77B4", bold=True)

    thin_gray = Side(style="thin", color="D9D9D9")

    # Style header row
    for cell in wscell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=thin_gray)

    current_row = 2

    for row in export_rows:
        section = row.get("Section", "")
        field = row.get("Field", "")
        value = row.get("Value", "")

        ws.append([section, field, value])

        # Section heading row
        if field == "" and value == "":
            for cell in wscell.fill = section_fill
                cell.font = section_font
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                cell.border = Border(bottom=thin_gray)
        else:
            ws.cell(current_row, 2).font = Font(bold=True)
            ws.cell(current_row, 3).alignment = Alignment(wrap_text=True, vertical="top")

            for cell in wscell.border = Border(bottom=thin_gray)
                cell.alignment = Alignment(wrap_text=True, vertical="top")

        current_row += 1

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 55
    ws.column_dimensions["C"].width = 95

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output


# ---------- PARSER ----------
data = st.session_state.get("data")

if data:

    export_rows = []

    def add_section(section_name):
        export_rows.append({
            "Section": section_name,
            "Field": "",
            "Value": ""
        })

    def add_export(section, field, value):
        export_rows.append({
            "Section": section,
            "Field": field,
            "Value": value
        })

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

    def find_shutdown_other():
        for k, v in data.items():
            kl = k.lower()
            if "other" in kl and ("shutdown" in kl or "isolation" in kl):
                return v
        return ""

    def check(val, src):
        val_clean = re.sub(r'[^a-z0-9\s]', '', val.lower())
        src_clean = re.sub(r'[^a-z0-9\s]', '', src.lower())

        return "☑" if val_clean in src_clean else "☐"

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
    temp_services = find_value("Temporary Services")
    permits = find_value("What sub permits will be required throughout the duration of the works")
    shutdown = find_value("What type of Shutdown or Isolation is required")
    shutdown_main = find_value("require any shutdown")
    shutdown_reason = find_value("reason for the shutdown")
    combined_shutdown = shutdown + " " + shutdown_main
    shutdown_other = find_shutdown_other()
    other_area = find_other("area")
    other_access = find_other("access")
    combined_access = access + " " + other_access
    other_system = find_other("system")
    other_reason = find_other("reason")

    # ---------- STYLE ----------
    st.markdown("""
    <style>

    [data-theme="light"] .value {
        color: black;
        background: #f7f7f7;
    }

    [data-theme="dark"] .value {
        color: white;
        background: #333333;
    }

    .section {
        font-size:20px;
        font-weight:700;
        margin-top:30px;
        margin-bottom:10px;
        padding-bottom:6px;
        border-bottom:2px solid #e6e6e6;
        color:#1f77b4;
    }

    .label {
        font-weight:600;
        font-size:13px;
        margin-bottom:2px;
    }

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

    def field(label, keyword, i, section_name):
        val = find_value(keyword)
        add_export(section_name, label, val)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(f"<div class='label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{val}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(val, "Copy", "Done", key=f"{label}_{i}")

    # ---------- GENERAL ----------
    section = "General"
    add_section(section)
    st.markdown("<div class='section'>General</div>", unsafe_allow_html=True)

    for i, (l, k) in enumerate([
        ("Description", "Work/Activity Description"),
        ("Approval Conditions", "Approval Conditions"),
        ("Company Name", "Account"),
    ]):
        field(l, k, i, section)

    # ---------- CONTACT ----------
    section = "Contact"
    add_section(section)
    st.markdown("<div class='section'>Contact</div>", unsafe_allow_html=True)

    field("Person making the application", "Requested by", 100, section)
    field("Applicants Email", "Email address", 101, section)
    field("Applicants Phone", "Phone", 102, section)
    field("WSI Rep", "Who is your WSI representative", 103, section)

    # ---------- APPROVAL ----------
    section = "Approval"
    add_section(section)
    st.markdown("<div class='section'>Approval</div>", unsafe_allow_html=True)

    field("ABC / ALC Approval", "ABC", 50, section)
    field("ABC BAN Number / ALC Permit Number", "BAN", 51, section)
    field("Reason Not Required", "not applicable", 52, section)

    # ---------- WORK ----------
    section = "Work"
    add_section(section)
    st.markdown("<div class='section'>Work</div>", unsafe_allow_html=True)

    field("Type of Work", "Type of Work", 200, section)

    other_work = find_other("type of work")
    add_export(section, "Type of Work Other", other_work)

    col1, col2 = st.columns([6, 1])

    with col1:
        st.markdown("<div class='label'>Type of Work Other</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='value'>{other_work}</div>", unsafe_allow_html=True)

    with col2:
        st_copy_to_clipboard(other_work, "Copy", "Done", key="type_of_work_other")

    field("Detailed Location of Works", "Detailed location", 202, section)
    field("Detailed Scope of Works", "Detailed scope", 203, section)
    field("Start Date", "start date", 204, section)
    field("End Date", "end date", 205, section)
    field("Impacts on Airport Ops", "Impacts", 206, section)
    field("Mitigation Measures for Op impacts", "Mitigation", 207, section)

    # ---------- PLANS ----------
    section = "Plans / Management"
    add_section(section)
    st.markdown("<div class='section'>Plans / Management</div>", unsafe_allow_html=True)

    field("Do you require and asset information?", "asset information", 300, section)
    field("Communication Plan", "communication plan", 301, section)

    # ---------- SUPERVISION ----------
    section = "Supervision"
    add_section(section)
    st.markdown("<div class='section'>Supervision</div>", unsafe_allow_html=True)

    field("Supervisor Name", "Supervisor name", 120, section)
    field("Supervisor Phone", "Supervisor phone", 121, section)
    field("Emergency Contact Name", "Site Emergency/After Hours Contact person name", 122, section)
    field("Emergency Contact Phone", "after hours contact person phone number", 123, section)

    # ---------- SERVICES ----------
    section = "Services"
    add_section(section)
    st.markdown("<div class='section'>Services</div>", unsafe_allow_html=True)

    field("Tools in Terminal sterile areas", "tools", 320, section)
    field("Tapping Services", "tapping", 321, section)
    field("Tapping Details", "details associated", 322, section)

    # ---------- ACKNOWLEDGEMENTS ----------
    section = "Acknowledgements"
    add_section(section)
    st.markdown("<div class='section'>Acknowledgements</div>", unsafe_allow_html=True)

    acknowledgements = [
        ("Working on Airfield", ack("airfield")),
        ("Accessing Airfield", ack("accessing the airfield")),
        ("Working Landside", ack("landside")),
        ("Working Terminal", ack("requirements around working in the Terminal")),
    ]

    for label, value in acknowledgements:
        st.markdown(f"{label}: {value}")
        add_export(section, label, value)

    # ---------- WASTE MANAGEMENT ----------
    section = "Waste Management"
    add_section(section)
    st.markdown("<div class='section'>Waste Management</div>", unsafe_allow_html=True)

    field("Waste Management Plan", "waste management", 302, section)

    storage_val = find_value("stored on-site")
    storage_result = yesno(storage_val)

    st.markdown(f"Equipment / Materials / Chemicals Stored On-Site: {storage_result}")
    add_export(section, "Equipment / Materials / Chemicals Stored On-Site", storage_result)

    field(
        "Management plan for equipment, materials or chemical storage on site",
        "management plan for equipment, materials or chemical storage",
        303,
        section
    )

    # ---------- SITE CONTROLS ----------
    section = "Site Controls"
    add_section(section)
    st.markdown("<div class='section'>Site Controls</div>", unsafe_allow_html=True)

    hoarding_val = find_value("Hoarding, Barricading")
    hoarding_result = yesno(hoarding_val)

    st.markdown(f"Hoarding / Barricading / Signage Required: {hoarding_result}")
    add_export(section, "Hoarding / Barricading / Signage Required", hoarding_result)

    hoarding_ack = ack("requirements around Hoarding, Barricading and Signage")

    st.markdown(f"Hoarding / Barricading / Signage Acknowledged: {hoarding_ack}")
    add_export(section, "Hoarding / Barricading / Signage Acknowledged", hoarding_ack)

    road_val = find_value("Road Occupancy or Traffic Management")
    road_result = yesno(road_val)

    st.markdown(f"Road Occupancy / Traffic Management Required: {road_result}")
    add_export(section, "Road Occupancy / Traffic Management Required", road_result)

    # ---------- TEMPORARY SERVICES ----------
    section = "Temporary Services"
    add_section(section)
    st.markdown("<div class='section'>Temporary Services</div>", unsafe_allow_html=True)

    temp_services_result = yesno(temp_services)

    st.markdown(f"Temporary Services Required: {temp_services_result}")
    add_export(section, "Temporary Services Required", temp_services_result)

    field(
        "Special Access Conditions (Personnel / Vehicles / Equipment)",
        "special conditions",
        340,
        section
    )

    # ---------- LOCATION ----------
    section = "Location"
    add_section(section)
    st.markdown("<div class='section'>Location</div>", unsafe_allow_html=True)

    locs = [
        "Terminal Departures", "Terminal Arrivals", "Terminal Basement",
        "Terminal Loading Dock", "Terminal Bag Room", "Gate Lounges",
        "Landside", "Apron", "Aircraft Bay", "Cargo Precinct",
        "Public Carpark", "AOCC/AOMF", "Terminal Roof",
        "Ancillary Building", "Site-Wide", "Other"
    ]

    c1, c2 = st.columns(2)

    for i, l in enumerate(locs):
        result = check(l, area)
        display_text = f"{result} {l}"
        (c1 if i % 2 == 0 else c2).markdown(display_text)
        add_export(section, l, result)

    if check("Other", area) == "☑" and other_area:
        add_export(section, "Other Area", other_area)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown("<div class='label'>Other Area</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_area}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_area, "Copy", "Done", key="other_area_copy")

    # ---------- ACCESS ----------
    section = "Access"
    add_section(section)
    st.markdown("<div class='section'>Access</div>", unsafe_allow_html=True)

    access_list = [
        "Airside Vehicle Gate",
        "Terminal Main Entry",
        "Terminal Staff Entry",
        "Loading Dock",
        "Other"
    ]

    c1, c2 = st.columns(2)

    for i, a in enumerate(access_list):
        result = check(a, combined_access)
        display_text = f"{result} {a}"
        (c1 if i % 2 == 0 else c2).markdown(display_text)
        add_export(section, a, result)

    if check("Other", access) == "☑" and other_access:
        add_export(section, "Other Access", other_access)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown("<div class='label'>Other Access</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_access}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_access, "Copy", "Done", key="other_access_copy")

    # ---------- DAYS ----------
    section = "Days"
    add_section(section)
    st.markdown("<div class='section'>Days</div>", unsafe_allow_html=True)

    days_list = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    c1, c2 = st.columns(2)

    for i, d in enumerate(days_list):
        result = check(d, days)
        display_text = f"{result} {d}"
        (c1 if i % 2 == 0 else c2).markdown(display_text)
        add_export(section, d, result)

    # ---------- HOURS ----------
    section = "Hours"
    add_section(section)
    st.markdown("<div class='section'>Hours</div>", unsafe_allow_html=True)

    for h in ["Morning", "Afternoon", "Night"]:
        result = check(h, hours)
        st.markdown(f"{result} {h}")
        add_export(section, h, result)

    # ---------- SYSTEMS ----------
    section = "Systems Impacted"
    add_section(section)
    st.markdown("<div class='section'>Systems Impacted</div>", unsafe_allow_html=True)

    systems_list = [
        "Electrical LV",
        "Electrical HV",
        "HVAC",
        "Technology & Network",
        "Security",
        "Hydraulics",
        "Roads and Signage",
        "Fire Systems",
        "Vertical Transport",
        "Other"
    ]

    not_applicable = "☑" if any(x in systems.lower() for x in ["na", "n/a", "not applicable"]) else "☐"

    st.markdown(f"{not_applicable} Not Applicable")
    add_export(section, "Not Applicable", not_applicable)

    for s in systems_list:
        result = check(s, systems)
        st.markdown(f"{result} {s}")
        add_export(section, s, result)

    if check("Other", systems) == "☑" and other_system:
        add_export(section, "Other System", other_system)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown("<div class='label'>Other System</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_system}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_system, "Copy", "Done", key="other_system_copy")

    # ---------- PERMITS ----------
    section = "Permits"
    add_section(section)
    st.markdown("<div class='section'>Permits</div>", unsafe_allow_html=True)

    permits_list = [
        "Confined Space Sub Permit",
        "Out of Hours Works",
        "Crane Lift Sub Permit",
        "Gantry Access Sub Permit",
        "Excavation and Penetration Sub Permit",
        "Hot Works Sub Permit",
        "Isolation Sub Permit",
        "Material Import Permit",
        "Operational Resource Closure/Shutdown Sub Permit",
        "Road Occupancy",
        "Permit to Discharge Water",
        "Vegetation Works",
        "Working at Height or Below Permit",
        "Fire Isolation Permit",
        "Permit to Enter Protected Areas or No-Go Areas"
    ]

    permits_na = "☑" if "no" in shutdown_main.lower() else "☐"

    st.markdown(f"{permits_na} Not Applicable")
    add_export(section, "Not Applicable", permits_na)

    for p in permits_list:
        result = check(p, permits)
        st.markdown(f"{result} {p}")
        add_export(section, p, result)

    # ---------- SHUTDOWN ----------
    section = "Shutdown Required"
    add_section(section)
    st.markdown("<div class='section'>Shutdown Required</div>", unsafe_allow_html=True)

    shutdown_required_result = yesno(shutdown_main)

    st.markdown(shutdown_required_result)
    add_export(section, "Shutdown Required", shutdown_required_result)

    # ---------- SHUTDOWN TYPES ----------
    section = "Shutdown Types"
    add_section(section)
    st.markdown("<div class='section'>Shutdown Types</div>", unsafe_allow_html=True)

    shutdown_types = [
        "Electrical",
        "Data",
        "HVAC",
        "Water",
        "Fire detection system",
        "High Voltage",
        "Other"
    ]

    for s in shutdown_types:
        result = check(s, combined_shutdown)
        st.markdown(f"{result} {s}")
        add_export(section, s, result)

    if check("Other", shutdown) == "☑" and shutdown_other:
        add_export(section, "Other Shutdown Type", shutdown_other)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown("<div class='label'>Other Shutdown Type</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{shutdown_other}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(shutdown_other, "Copy", "Done", key="other_shutdown_copy")

    # ---------- REASON FOR SHUTDOWN ----------
    section = "Reason For Shutdown"
    add_section(section)
    st.markdown("<div class='section'>Reason For Shutdown</div>", unsafe_allow_html=True)

    reason_list = [
        "Maintenance",
        "Repair",
        "Installation",
        "Testing",
        "Other"
    ]

    c1, c2 = st.columns(2)

    for i, r in enumerate(reason_list):
        result = check(r, shutdown_reason)
        display_text = f"{result} {r}"
        (c1 if i % 2 == 0 else c2).markdown(display_text)
        add_export(section, r, result)

    if check("Other", shutdown_reason) == "☑" and other_reason:
        add_export(section, "Other Reason", other_reason)

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown("<div class='label'>Other Reason</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='value'>{other_reason}</div>", unsafe_allow_html=True)

        with col2:
            st_copy_to_clipboard(other_reason, "Copy", "Done", key="other_reason_reason_copy")

    # ---------- SHUTDOWN DETAILS ----------
    section = "Shutdown Details"
    add_section(section)
    st.markdown("<div class='section'>Shutdown Details</div>", unsafe_allow_html=True)

    field("Shutdown Start", "start date of the shutdown", 500, section)
    field("Shutdown End", "end date of the shutdown", 501, section)
    field("Shutdown Duration", "Total duration of the Shutdown/Isolations", 502, section)

    # ---------- DOWNLOAD EXCEL ----------
    excel_file = create_excel_file(export_rows)

    st.markdown("---")

    st.download_button(
        label="Download Reformatted Data as Excel",
        data=excel_file,
        file_name="AWP_Reformatted_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )