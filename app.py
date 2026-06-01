import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="AWP Parser")

st.title("AWP Full Parser")

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

    # ✅ FIELD MAPPING (FIXES EMPTY VALUES)
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
    }

    def get(field):
        key = mapping.get(field, field)
        val = data.get(key, "")
        if isinstance(val, str) and val.lower() == "true":
            return "Yes"
        return val

    def check(val, source):
        return "Yes" if val.lower() in source.lower() else ""

    # ---------- SOURCE DATA ----------
    area = data.get("Detailed location of works/activity", "")
    days = data.get("Days required", "")
    hours = data.get("Working Hours", "")
    systems = data.get("What systems will be affected by the works?", "")
    permits = data.get("What sub permits will be required throughout the duration of the works?", "")
    access = data.get("What Access point will be required for personnel and deliveries", "")
    shutdown = data.get("Will the work require any shutdowns and/or isolations?", "")

    # ---------- FULL FIELD LIST ----------
    fields = [
        "AWP Number","Date Updated","Updated By","Description",
        "Approval Conditions or Requirements","Company Name","Company Description",
        "Person making the application","Applicants email","Applicants phone number",
        "WSI Representative","WSI Representative Name",
        "Do you have ABC and ALC approval?",
        "ABC Ban Number and ALC Permit Number",
        "Reason ABC and ALC Approval Not Required",
        "Type of Work","Type of Work (Other)",
        "Detailed Location of Works","Detailed Scope of Works",
        "Proposed Start Date","Proposed End Date",
        "Impacts on Airport Ops","Mitigation Measures for Op impacts",
        "Do you require any asset information?",
        "Provide details of your communication plan",
        "Work hours site Supervisor name","Work hours site Supervisor Number",
        "Site Emergency/After Hours Contact Name",
        "Site Emergency/After Hours Contact Number",
        "Will tools be carried in and out of the Airport Terminal sterile areas?",
        "Will the work include tapping into any existing services?",
        "Details associated with tapping into the existing service",
        "Do you require WSI owned and managed equipment?",
        "Details for Required Equipment",
        "Waste Management Plan Details",
        "Will Equipment, Materials or Chemicals be stored onsite?",
        "Management plan for equipment, materials or chemicals on site",
        "Hoarding, Barricading or Signage Required",
        "Hoarding, Barricading or Signage Acknowledged",
        "Road Occupancy or Traffic Management Plans Required",
        "Road Occupancy and Traffic Management Plans Acknowledged",
        "Sub Permit Documentation Read and Understood",
        "Will Temporary Services be Required",
        "Provide Details of Temporary Services Required",
        "Will the work require lighting",
        "Lighting Acknowledged",
        "Special conditions or requirements associated with site Access",
    ]

    results = [[f, get(f)] for f in fields]

    # ---------- CHECKBOX GROUPS ----------

    # Locations
    for loc in [
        "Terminal Departures","Terminal Arrivals","Terminal Basement",
        "Terminal Loading Dock","Terminal Bag Room","Gate Lounges",
        "Landside","Apron","Aircraft Bay","Cargo Precinct",
        "Public Carpark","AOCC/AOMF","Terminal Roof",
        "Ancillary Building","Site Wide","Other Location"
    ]:
        results.append([loc, check(loc, area)])

    # Access
    for a in [
        "Airside Vehicle Gate","Terminal Main Entry",
        "Terminal Staff Entry","Loading Dock","Other Access Point"
    ]:
        results.append([a, check(a, access)])

    # Days
    for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        results.append([d, check(d, days)])

    # Hours
    for h in ["Morning","Afternoon","Night"]:
        results.append([h, check(h, hours)])

    # Systems
    for s in [
        "Electrical LV","Electrical HV","HVAC",
        "Technology & Network","Security","Hydraulics",
        "Roads and Signage","Fire Systems","Vertical Transport"
    ]:
        results.append([s, check(s, systems)])

    # Permits
    for p in [
        "Confined Space Sub Permit","Out of Hours Works",
        "Crane Lift Sub Permit","Gantry Access Sub Permit",
        "Permit to Enter Protected Areas or No-Go Areas",
        "Excavation & Penetration Sub Permit",
        "Hot Work Sub Permit",
        "Isolation Sub Permit",
        "Material Import Permit"
    ]:
        results.append([p, check(p, permits)])

    # Shutdown
    for s in [
        "Electrical","Data","HVAC",
        "Water (potable/recycled/sewer etc)",
        "Fire detection system","High Voltage","Other Shutdown/Isolation"
    ]:
        results.append([s, check(s, shutdown)])

    df = pd.DataFrame(results, columns=["Field", "Value"])

    st.subheader("Parsed Output")

    # ---------- DISPLAY (COPY WORKS HERE) ----------
    for i, row in df.iterrows():

        st.markdown(f"### {row['Field']}")

        # ✅ IMPORTANT: this has built-in copy button
        st.code(row["Value"], language="text")

    # ---------- DOWNLOAD ----------
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "awp_output.csv",
        "text/csv"
    )