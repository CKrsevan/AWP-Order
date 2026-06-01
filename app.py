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

    # ✅ FIX EMPTY FIELDS
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
        return data.get(key, "")

    # ---------- FIELDS ----------
    fields = [
        "Company Name",
        "Person making the application",
        "Applicants email",
        "Applicants phone number",
        "WSI Representative",
        "Detailed Location of Works",
        "Detailed Scope of Works",
        "Proposed Start Date",
        "Proposed End Date",
    ]

    df = pd.DataFrame([[f, get(f)] for f in fields], columns=["Field","Value"])

    st.subheader("Parsed Output")

    # ---------- DISPLAY ----------
    for i, row in df.iterrows():

        st.markdown(f"### {row['Field']}")

        # ✅ CUSTOM BUTTON (THIS NOW WORKS PROPERLY)
        if st.button("📋 Copy", key=f"copy_{i}"):
            st.session_state["copy_val"] = row["Value"]

        # show value normally
        st.write(row["Value"])

    # ✅ GLOBAL COPY BOX (REAL COPY)
    if "copy_val" in st.session_state:
        st.subheader("Copy Value")

        st.code(
            st.session_state["copy_val"], 
            language="text"
        )
``