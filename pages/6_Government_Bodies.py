"""
Government Bodies Directory

- Directory of government and administrative bodies relevant to the locality.
- Provides quick contact details, office hours, locations, and links.
- Dummy data for now but structured for easy migration to DB.
"""

import streamlit as st
from pathlib import Path

st.title("Government & Administrative Bodies")
st.write("Quick access to government offices and services in the ward.")

# Dummy data structure — expand as needed
BODIES = [
    {"name": "Ward Office (Panchayat)", "department": "Local Administration", "contact": "+91-12345-00001", "hours": "Mon-Fri 10:00-17:00", "location": "Community Hall Complex", "website": ""},
    {"name": "Electricity Department (Local)", "department": "Electricity", "contact": "+91-12345-00002", "hours": "Mon-Fri 09:30-17:30", "location": "Billing Office, Main Road", "website": ""},
    {"name": "Water Billing Office", "department": "Water", "contact": "+91-12345-00003", "hours": "Mon-Fri 09:00-16:00", "location": "Ration Shop Complex", "website": ""},
    {"name": "Anganwadi Center - Block A", "department": "Child Welfare", "contact": "+91-12345-00004", "hours": "Mon-Fri 08:30-13:30", "location": "Block A", "website": ""},
    {"name": "Public Health Center (PHC)", "department": "Health", "contact": "+91-12345-00005", "hours": "Mon-Sat 09:00-14:00", "location": "Near Main Road", "website": ""}
]

st.subheader("Directory")

# Search/filter
q = st.text_input("Search by name, department, or location")
dept_filter = st.selectbox("Filter by department", options=["All"] + sorted(list({b['department'] for b in BODIES})))

def filter_bodies(items):
    res = items
    if dept_filter and dept_filter != "All":
        res = [i for i in res if i.get('department') == dept_filter]
    if q:
        ql = q.lower()
        res = [i for i in res if ql in i.get('name','').lower() or ql in i.get('department','').lower() or ql in i.get('location','').lower()]
    return res

results = filter_bodies(BODIES)

if results:
    for r in results:
        website = r.get('website','')
        website_html = f"<div style='margin-top:8px;'><a href='{website}' target='_blank'>Website</a></div>" if website else ''
        st.markdown(f"""
        <div style='background:#f7f7ff;padding:12px;border-radius:8px;margin-bottom:8px;'>
            <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                    <div style='font-weight:700'>{r['name']}</div>
                    <div style='font-size:13px;color:#555'>{r['department']} • {r['location']}</div>
                </div>
                <div style='text-align:right'>
                    <div style='font-weight:600'>{r['contact']}</div>
                </div>
            </div>
            <div style='margin-top:8px;color:#333'>Office hours: {r.get('hours','')}</div>
            {website_html}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No government bodies found for your query.")

st.caption('Data is dummy and for demonstration. Replace with real contacts or a database lookup as needed.')
# Duplicate block removed (already defined above)