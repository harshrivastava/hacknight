"""
Naborly — Home page with modern UI and interactions
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.ui import load_css, custom_card, status_badge, add_logo, add_js_interactivity, show_alert

# -----------------------------
# Setup and Configuration
# -----------------------------

# Page config
st.set_page_config(
    page_title="Naborly — Ward 12, ABC City",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent / "styles" / "main.css"
load_css(css_file)

# Add JavaScript functionality
add_js_interactivity()

# -----------------------------
# Dummy / static data (edit here)
# -----------------------------
REGION_NAME = "Ward 12, ABC City"

# Points for the map: shops, leaders, key points (latitude, longitude)
LOCATIONS = [
    {"name": "Green Grocers", "type": "Shop", "lat": 37.7749, "lon": -122.4194},
    {"name": "Asha Clinic", "type": "Service", "lat": 37.7756, "lon": -122.4183},
    {"name": "Community Hall", "type": "Key Point", "lat": 37.7768, "lon": -122.4170},
    {"name": "Local Leader - Mr. Roy", "type": "Leader", "lat": 37.7750, "lon": -122.4160},
    {"name": "Bakery Corner", "type": "Shop", "lat": 37.7740, "lon": -122.4205},
    {"name": "Ration Shop", "type": "Government", "lat": 37.7745, "lon": -122.4180},
]

# Local news / bulletins
NEWS = [
    {"title": "Road repair on Main St", "date": "2025-11-01", "content": "Main St will have partial closures from Nov 3 to Nov 5 for resurfacing.", "tags": ["Transport", "Alert"]},
    {"title": "Health camp this weekend", "date": "2025-10-28", "content": "Free health checkup at Community Hall on Sunday 10am-2pm.", "tags": ["Health"]},
    {"title": "Festive cleanup drive", "date": "2025-10-20", "content": "Volunteer cleanup drive; meet at 8am near Bakery Corner.", "tags": ["Community"]},
]

# Directory of shops / services / leaders
DIRECTORY = [
    {"name": "Green Grocers", "type": "Shop", "contact": "+1-555-0101", "notes": "Groceries & vegetables"},
    {"name": "Asha Clinic", "type": "Service", "contact": "+1-555-0202", "notes": "General physician"},
    {"name": "Mr. Roy", "type": "Local Leader", "contact": "+1-555-0303", "notes": "Ward representative"},
]

# Utility schedules (fake)
UTILITIES = {
    "water_supply": [
        {"area": "North Block", "schedule": "Mon, Wed, Fri: 6am - 9am"},
        {"area": "South Block", "schedule": "Tue, Thu: 5pm - 8pm"},
    ],
    "garbage_collection": [
        {"area": "All Areas", "schedule": "Tue & Fri - 7am"},
    ],
}

# Notifications / alerts
NOTIFICATIONS = [
    {"level": "info", "text": "Novel community meeting on Nov 6 at 6pm, Community Hall."},
    {"level": "warning", "text": "Expect short water outage on Nov 3 morning due to maintenance."},
]

# -----------------------------
# Helper functions
# -----------------------------

def locations_to_dataframe(locations):
    """Convert list of location dicts to a pandas DataFrame for st.map"""
    df = pd.DataFrame(locations)
    # st.map expects latitude column 'lat' and longitude column 'lon'
    return df

def format_news_item(item):
    return f"**{item['title']}** — {item['date']}\n\n{item['content']}"

# -----------------------------
# UI Layout
# -----------------------------

# Add logo to sidebar
add_logo()

# Top header with notifications
st.title(f"Welcome to {REGION_NAME} 🏘️")

# Notification area with animation
for note in NOTIFICATIONS:
    custom_card(f'''
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.25rem">{"ℹ️" if note["level"] == "info" else "⚠️"}</span>
            <p style="margin: 0">{note["text"]}</p>
        </div>
    ''')

# Sidebar quick info
with st.sidebar:
    st.header("About this area")
    st.write(f"Welcome to {REGION_NAME}!")
    st.markdown("---")
    st.subheader("Map filters")
    types = [loc["type"] for loc in LOCATIONS]
    types = sorted(list(set(types)))
    chosen = st.multiselect("Show types", options=types, default=types)

# Main content: layout columns
col1, col2 = st.columns([2, 1])

# Left column: Map and Directory
with col1:
    st.subheader("📍 Local Map")
    # Map filters in a card
    with st.expander("Map Filters", expanded=True):
        types = sorted(list(set(loc["type"] for loc in LOCATIONS)))
        chosen = st.multiselect("Show locations", options=types, default=types)
    
    # Show map
    df_map = locations_to_dataframe([l for l in LOCATIONS if l["type"] in chosen])
    if not df_map.empty:
        st.map(df_map[["lat", "lon"]])
        
        # Show location details in a scrollable card
        custom_card('''
            <div style="max-height: 200px; overflow-y: auto;">
                <table style="width: 100%">
                    <tr style="background: #f8f9fa">
                        <th style="padding: 0.5rem">Name</th>
                        <th style="padding: 0.5rem">Type</th>
                    </tr>
                    ''' + 
                    ''.join(f'''
                        <tr>
                            <td style="padding: 0.5rem">{loc["name"]}</td>
                            <td style="padding: 0.5rem">{loc["type"]}</td>
                        </tr>
                    ''' for loc in LOCATIONS if loc["type"] in chosen) +
                '''
                </table>
            </div>
        ''')

# Right column: News, Utilities
with col2:
    st.subheader("Local News & Bulletins")
    for item in NEWS:
        st.markdown(format_news_item(item))
        st.markdown("---")

    st.subheader("Utility Tracker")
    for utype, entries in UTILITIES.items():
        st.write(f"**{utype.replace('_',' ').title()}**")
        for e in entries:
            st.write(f"- {e['area']}: {e['schedule']}")

# Footer
st.markdown("---")
st.caption("Browse other sections using the pages menu in the sidebar!")