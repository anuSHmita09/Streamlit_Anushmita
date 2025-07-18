import streamlit as st
import pandas as pd
import datetime
import io

# -- App Config --
st.set_page_config(page_title="Mental Wellness Entry Logger", layout="wide")
EXCEL_FILE = "mental_wellness_entries.xlsx"

st.title("🧠 Mental Wellness Entry Logger")
st.markdown("> Track your daily wellness activities to promote healthy mind habits!")

# -- Load entries from session_state, or initialize --
if "df_entries" not in st.session_state:
    st.session_state.df_entries = pd.DataFrame(
        columns=["Name", "Wellness Activity", "Me-time Activity", "Screen-free Time", "Status", "Date"]
    )

df_entries = st.session_state.df_entries

# -- Form for new entry --
with st.sidebar.form("add_entry", clear_on_submit=True):
    st.header("Add a New Entry")

    name = st.text_input("Student Name")
    activity = st.text_input("Wellness Activity (e.g. walked, meditated)")
    metime = st.text_input("Me-time Activity (e.g. reading, yoga)")
    screenfree = st.number_input("Screen-free Time (minutes)", min_value=1, max_value=1440, step=5)

    # Calculate Status
    status = "Healthy" if screenfree >= 240 else "Needs More Me-Time"
    st.markdown(f"**Status:** {'🟢' if status == 'Healthy' else '🟠'} {status}")

    submitted = st.form_submit_button("Add Entry")

    # --- Input Validation and Saving ---
    if submitted:
        if not (name and activity and metime):
            st.error("All fields must be filled.")
        elif not any(c.isalpha() for c in name):
            st.error("Name must contain letters.")
        elif not any(c.isalpha() for c in activity):
            st.error("Wellness Activity must contain letters.")
        elif not any(c.isalpha() for c in metime):
            st.error("Me-time Activity must contain letters.")
        else:
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            new_row = {
                "Name": name.strip(),
                "Wellness Activity": activity.strip(),
                "Me-time Activity": metime.strip(),
                "Screen-free Time": int(screenfree),
                "Status": status,
                "Date": today_str,
            }
            st.session_state.df_entries = pd.concat([st.session_state.df_entries, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Entry added.")

# -- Entries Table and Download/Delete Options --
st.subheader("📝 Entries Log")

if st.session_state.df_entries.empty:
    st.info("No entries yet. Start by adding one!")
else:
    st.dataframe(st.session_state.df_entries, use_container_width=True, hide_index=True)

    # Bulk delete
    with st.expander("🗑️ Manage Entries"):
        indices = st.multiselect(
            "Select rows to delete",
            options=st.session_state.df_entries.index.tolist(),
            format_func=lambda x: f"{st.session_state.df_entries.iloc[x]['Name']} ({st.session_state.df_entries.iloc[x]['Date']})"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Delete Selected"):
                if indices:
                    st.session_state.df_entries = st.session_state.df_entries.drop(indices).reset_index(drop=True)
                    st.success("Selected entries deleted.")
                else:
                    st.warning("Select at least one entry.")

        with col2:
            if st.button("Clear All Entries"):
                st.session_state.df_entries = pd.DataFrame(
                    columns=st.session_state.df_entries.columns)
                st.success("All entries cleared.")

    # Download as Excel file
    buffer = io.BytesIO()
    st.session_state.df_entries.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Download Excel",
        data=buffer.getvalue(),
        file_name="mental_wellness_entries.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -- Self-Care Reminder Button --
if st.button("💡 Self-Care Reminder"):
    st.info("Take a mindful break and do something relaxing! 🌱")

st.markdown("---")
st.caption("A simple wellness logger by [YourGitHubUsername] — share, fork, and improve!")
