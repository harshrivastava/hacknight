"""
Local Complaint Box

- Users can submit complaints (category, description, optional contact info)
- Complaints are stored persistently in the app's SQLite DB (`naborly.db`) if present.
- If the DB is missing, complaints are stored in `complaints.json` as fallback.
- A table of recent complaints is shown for transparency.

Beginner-friendly and well-commented so you can customize later.
"""

import streamlit as st
import sqlite3
from pathlib import Path
import json
from datetime import datetime

# File paths
DB_PATH = Path(__file__).parent.parent / "naborly.db"
JSON_FALLBACK = Path(__file__).parent.parent / "complaints.json"

st.title("Local Complaint Box")
st.write("Submit civic complaints or service requests. Submissions are visible below for transparency.")

# Simple categories - feel free to expand
CATEGORIES = ["Sanitation", "Water", "Roads", "Electricity", "Safety", "Other"]

# Complaint form
with st.form("complaint_form"):
    st.subheader("Submit a complaint")
    category = st.selectbox("Category", CATEGORIES)
    description = st.text_area("Describe the issue (be as specific as possible)")
    contact = st.text_input("Contact info (phone/email) — optional")
    location = st.text_input("Location / Landmark (optional)")

    submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        if not description.strip():
            st.error("Please add a description for the complaint.")
        else:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Try to persist to SQLite first
            if DB_PATH.exists():
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cur = conn.cursor()
                    # Create table if not exists (safe to run every time)
                    cur.execute('''
                        CREATE TABLE IF NOT EXISTS complaints (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category TEXT,
                            description TEXT,
                            contact TEXT,
                            location TEXT,
                            status TEXT DEFAULT 'submitted',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    cur.execute(
                        "INSERT INTO complaints (category, description, contact, location, created_at) VALUES (?, ?, ?, ?, ?)",
                        (category, description, contact, location, created_at)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Complaint submitted and saved to the local database.")
                except Exception as e:
                    st.error(f"Could not save to database: {e}. Falling back to local JSON file.")
                    # fallback to JSON
                    fallback_entry = {
                        "category": category,
                        "description": description,
                        "contact": contact,
                        "location": location,
                        "status": "submitted",
                        "created_at": created_at
                    }
                    try:
                        data = []
                        if JSON_FALLBACK.exists():
                            data = json.loads(JSON_FALLBACK.read_text())
                        data.insert(0, fallback_entry)
                        JSON_FALLBACK.write_text(json.dumps(data, indent=2))
                        st.success("Complaint saved to complaints.json fallback file.")
                    except Exception as e2:
                        st.error(f"Failed to save complaint fallback: {e2}")
            else:
                # No DB: write to JSON file
                try:
                    data = []
                    if JSON_FALLBACK.exists():
                        data = json.loads(JSON_FALLBACK.read_text())
                    entry = {
                        "category": category,
                        "description": description,
                        "contact": contact,
                        "location": location,
                        "status": "submitted",
                        "created_at": created_at
                    }
                    data.insert(0, entry)
                    JSON_FALLBACK.write_text(json.dumps(data, indent=2))
                    st.success("Complaint saved to complaints.json")
                except Exception as e:
                    st.error(f"Failed to save complaint: {e}")

# Display recent complaints (read from DB if available, otherwise JSON)
st.markdown("---")
st.subheader("Recent complaints")

def load_complaints(limit=100):
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
                SELECT id, category, description, contact, location, status, created_at
                FROM complaints
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            st.warning(f"Could not read from DB: {e}. Falling back to JSON.")
    # fallback
    if JSON_FALLBACK.exists():
        try:
            return json.loads(JSON_FALLBACK.read_text())[:limit]
        except Exception:
            return []
    return []

complaints = load_complaints(limit=200)

if complaints:
    # Simple table view
    import pandas as pd
    df = pd.DataFrame(complaints)
    # Show newest first
    st.dataframe(df[['id','category','description','location','contact','status','created_at']].head(200))
else:
    st.info("No complaints submitted yet.")

# Optional CSV export button
if complaints:
    import pandas as pd
    df = pd.DataFrame(complaints)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download complaints CSV", data=csv, file_name="complaints.csv", mime='text/csv')

# Small note
st.caption("Note: Complaints submitted through this toy app are stored locally for demo purposes. To route them to municipal systems, you'd implement API integration or share with relevant authorities.")
