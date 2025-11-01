"""
Government Ration Rates — Naborly
Shows current ration rates and availability in the local area
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# Sample Data
# -----------------------------

# Current month's ration rates
RATION_RATES = {
    "Ward 12": [
        {"item": "Rice", "category": "APL", "rate_per_kg": 8.50, "monthly_limit_kg": 5, "availability": "In Stock"},
        {"item": "Rice", "category": "BPL", "rate_per_kg": 3.00, "monthly_limit_kg": 7, "availability": "In Stock"},
        {"item": "Wheat", "category": "APL", "rate_per_kg": 7.50, "monthly_limit_kg": 5, "availability": "Limited Stock"},
        {"item": "Wheat", "category": "BPL", "rate_per_kg": 2.50, "monthly_limit_kg": 7, "availability": "In Stock"},
        {"item": "Sugar", "category": "APL", "rate_per_kg": 30.00, "monthly_limit_kg": 2, "availability": "In Stock"},
        {"item": "Sugar", "category": "BPL", "rate_per_kg": 15.00, "monthly_limit_kg": 3, "availability": "Out of Stock"},
        {"item": "Kerosene", "category": "All", "rate_per_liter": 25.00, "monthly_limit_liters": 3, "availability": "Limited Stock"},
    ],
    "Surrounding Areas": [
        {"item": "Rice", "category": "APL", "rate_per_kg": 9.00, "monthly_limit_kg": 5, "availability": "In Stock"},
        {"item": "Rice", "category": "BPL", "rate_per_kg": 3.00, "monthly_limit_kg": 7, "availability": "Limited Stock"},
        {"item": "Wheat", "category": "APL", "rate_per_kg": 8.00, "monthly_limit_kg": 5, "availability": "In Stock"},
        {"item": "Wheat", "category": "BPL", "rate_per_kg": 2.50, "monthly_limit_kg": 7, "availability": "In Stock"},
        {"item": "Sugar", "category": "APL", "rate_per_kg": 31.00, "monthly_limit_kg": 2, "availability": "Out of Stock"},
        {"item": "Sugar", "category": "BPL", "rate_per_kg": 15.00, "monthly_limit_kg": 3, "availability": "Limited Stock"},
        {"item": "Kerosene", "category": "All", "rate_per_liter": 26.00, "monthly_limit_liters": 3, "availability": "In Stock"},
    ]
}

# Sample announcements
ANNOUNCEMENTS = [
    {
        "date": "2025-11-01",
        "title": "Sugar stock update",
        "content": "New sugar stock expected by Nov 5. BPL card holders can collect previous month's quota until Nov 10."
    },
    {
        "date": "2025-10-28",
        "title": "Rate revision notice",
        "content": "Slight increase in APL rates expected from next month due to transport cost adjustment."
    }
]

# Ration shop timings
SHOP_TIMINGS = {
    "Ward 12 Main Shop": "Mon-Sat: 9:00 AM - 5:00 PM",
    "Ward 12 Extension Counter": "Mon-Fri: 10:00 AM - 4:00 PM",
    "Holiday Notice": "Closed on Sundays and public holidays"
}

# -----------------------------
# Helper Functions
# -----------------------------

def style_availability(val):
    """Returns a colored badge based on availability"""
    colors = {
        "In Stock": "green",
        "Limited Stock": "orange",
        "Out of Stock": "red"
    }
    color = colors.get(val, "gray")
    return f"background-color: {color}; color: white; padding: 0.1rem 0.5rem; border-radius: 0.25rem"

# -----------------------------
# Page Layout
# -----------------------------

st.title("Government Ration Rates")
st.write("Current rates and availability for Ward 12 and surrounding areas.")

# Show latest update time
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Important announcements at the top
st.subheader("📢 Important Announcements")
for announcement in ANNOUNCEMENTS:
    st.info(f"**{announcement['title']}** ({announcement['date']})\n\n{announcement['content']}")

# Ration shop timings
st.subheader("⏰ Ration Shop Timings")
for shop, timing in SHOP_TIMINGS.items():
    st.write(f"**{shop}**: {timing}")

# Tabs for different areas
tab1, tab2 = st.tabs(["Ward 12", "Surrounding Areas"])

with tab1:
    st.subheader("Ward 12 Current Rates")
    # Convert data to DataFrame for better display
    df = pd.DataFrame(RATION_RATES["Ward 12"])
    # Style the availability column
    st.dataframe(
        df.style.applymap(
            lambda x: style_availability(x) if x in ["In Stock", "Limited Stock", "Out of Stock"] else '',
            subset=['availability']
        ),
        use_container_width=True
    )

with tab2:
    st.subheader("Rates in Surrounding Areas")
    df = pd.DataFrame(RATION_RATES["Surrounding Areas"])
    st.dataframe(
        df.style.applymap(
            lambda x: style_availability(x) if x in ["In Stock", "Limited Stock", "Out of Stock"] else '',
            subset=['availability']
        ),
        use_container_width=True
    )

# Notes and information
with st.expander("ℹ️ Information about Categories"):
    st.write("""
    - **APL** (Above Poverty Line): Standard rates apply
    - **BPL** (Below Poverty Line): Subsidized rates
    - **Monthly limits** are per ration card
    - Availability status is updated daily
    - Bring your ration card for collection
    """)

# Footer with helpline
st.markdown("---")
st.caption("For questions or concerns, contact the Ward 12 Ration Office: +1-555-0123 (Mon-Fri, 9 AM - 6 PM)")