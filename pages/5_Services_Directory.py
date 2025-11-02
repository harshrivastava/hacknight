"""
Services Directory

- Lists local service providers (electrician, plumber, tuition, etc.) and local vendors (vegetables, fruits, essentials)
- Allows filtering by category and quick contact
- Uses dummy data stored in the file; easily connect to a DB later
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.title("Services Directory")
st.write("Find local service providers and vendors in your area.")

# File fallback for persisted listings (optional)
SERVICES_JSON = Path(__file__).parent.parent / "services_listings.json"

# Dummy data for providers (you can edit or replace with DB calls)
DEFAULT_PROVIDERS = [
    {"category": "Electrician", "name": "Ramesh Electricals", "contact": "+91-98765-00001", "area": "North Block", "description": "Home wiring, repairs, emergency service"},
    {"category": "Plumber", "name": "Shyam Plumbing", "contact": "+91-98765-00002", "area": "South Block", "description": "Tap repair, leak fixing, bathroom fittings"},
    {"category": "Tuition", "name": "ABC Tutors", "contact": "+91-98765-00003", "area": "Near Community Hall", "description": "Maths and Science tuition for Grades 6-10"},
    {"category": "Housemaid", "name": "Lakshmi Services", "contact": "+91-98765-00004", "area": "Ward 12", "description": "Trusted home staff for daily/weekly help"},
]

DEFAULT_VENDORS = [
    {"type": "Vegetables", "name": "Green Grocers", "contact": "+91-90000-11111", "area": "Market Street", "notes": "Fresh daily produce"},
    {"type": "Fruits", "name": "Fruit World", "contact": "+91-90000-22222", "area": "Main Road", "notes": "Seasonal fruits and juices"},
]

# Load persisted listings if available
if SERVICES_JSON.exists():
    try:
        saved = json.loads(SERVICES_JSON.read_text())
        providers = saved.get('providers', DEFAULT_PROVIDERS)
        vendors = saved.get('vendors', DEFAULT_VENDORS)
    except Exception:
        providers = DEFAULT_PROVIDERS
        vendors = DEFAULT_VENDORS
else:
    providers = DEFAULT_PROVIDERS
    vendors = DEFAULT_VENDORS

# Sidebar filters
st.sidebar.header("Find a service")
categories = sorted(list({p['category'] for p in providers}))
chosen_cat = st.sidebar.selectbox("Category", options=["All"] + categories)
search = st.sidebar.text_input("Search name or area")

# Provider listing
st.subheader("Service Providers")

def filter_list(items):
    res = items
    if chosen_cat and chosen_cat != "All":
        res = [i for i in res if i.get('category') == chosen_cat]
    if search:
        q = search.lower()
        res = [i for i in res if q in i.get('name','').lower() or q in i.get('area','').lower() or q in i.get('description','').lower()]
    return res

filtered = filter_list(providers)

if filtered:
    for p in filtered:
        st.markdown(f"""
        <div style='background:#fafafa;padding:12px;border-radius:8px;margin-bottom:8px;'>
            <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                    <div style='font-weight:600'>{p['name']}</div>
                    <div style='font-size:13px;color:#555'>{p['category']} • {p['area']}</div>
                </div>
                <div style='text-align:right'>
                    <div style='font-weight:600'>{p['contact']}</div>
                </div>
            </div>
            <div style='margin-top:8px;color:#333'>{p.get('description','')}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No providers found for the chosen filters.")

# Vendors section
st.subheader("Local Vendors (Vegetables, Fruits, Essentials)")

if vendors:
    for v in vendors:
        st.markdown(f"""
        <div style='background:#fff7e6;padding:12px;border-radius:8px;margin-bottom:8px;'>
            <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                    <div style='font-weight:600'>{v['name']}</div>
                    <div style='font-size:13px;color:#555'>{v['type']} • {v['area']}</div>
                </div>
                <div style='text-align:right'>
                    <div style='font-weight:600'>{v['contact']}</div>
                </div>
            </div>
            <div style='margin-top:8px;color:#333'>{v.get('notes','')}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No vendors available yet.")

# Add new listing (simple UI stored to JSON)
st.markdown("---")
st.subheader("Add a listing (providers & vendors)")
with st.form('add_listing'):
    kind = st.selectbox('Listing type', ['Provider','Vendor'])
    name = st.text_input('Name')
    contact = st.text_input('Contact')
    area = st.text_input('Area served')
    category_or_type = st.text_input('Category (e.g. Electrician) or Type (Vegetables)')
    description = st.text_area('Short description or notes')
    if st.form_submit_button('Add listing'):
        entry = {}
        if kind == 'Provider':
            entry = {"category": category_or_type or 'General', "name": name, "contact": contact, "area": area, "description": description}
            providers.insert(0, entry)
        else:
            entry = {"type": category_or_type or 'General', "name": name, "contact": contact, "area": area, "notes": description}
            vendors.insert(0, entry)
        # Persist to JSON file (simple)
        try:
            tosave = {"providers": providers, "vendors": vendors}
            SERVICES_JSON.write_text(json.dumps(tosave, indent=2, ensure_ascii=False))
            st.success('Listing added and saved locally')
        except Exception as e:
            st.error(f'Could not save listing: {e}')

st.caption('Listings are stored locally in services_listings.json; you can switch to SQLite by writing similar insert/select logic.')
