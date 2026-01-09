import streamlit as st
import feedparser
from datetime import datetime

# --- SETTINGS & WEIGHTS ---
# This dictionary lets us control how much "space" each issue takes
DAILY_WEIGHTS = {
    "PDX Permits": "Medium", # Title + AI Summary
    "Beaverton News": "Surface", # Just Titles
    "Atlantic Canada": "Medium",
    "Blender Studio": "Deep"  # Full text/Details
}

# --- STYLING (The Finite Look) ---
st.markdown("""
    <style>
    .daily-card { border-left: 3px solid black; padding-left: 15px; margin-bottom: 20px; }
    .seasonal-box { background-color: #f9f9f9; padding: 10px; border: 1px solid #eee; }
    @media print { .no-print { display: none; } }
    </style>
    """, unsafe_content_html=True)

# --- LAYOUT ---
st.title("FINITE CUT")
st.caption(f"VOL. 01 | {datetime.now().strftime('%A, %b %d')}")

# 01 / DAILY BRIEF
st.header("01 / DAILY")
col1, col2 = st.columns([2, 1])

with col1:
    # We will build a function to handle these based on the WEIGHTS above
    st.subheader("Sentinel & Craft")
    st.write("*(RSS Feeds loading based on weights...)*")
    
with col2:
    st.subheader("Inspiration")
    # Placeholder for your Pinterest/Cyclic image
    st.image("https://picsum.photos/400/500", caption="Daily Reference")

# 02 / WEEKLY (Only shows more detail on your weekly deep dive day)
if datetime.now().strftime('%A') == "Sunday":
    st.header("02 / WEEKLY DEEP DIVE")
    st.write("New Restos & Music Review")

# 04 / SEASONAL (Persistent)
st.divider()
st.subheader("04 / SEASONAL PULSE")
st.info("Winter: Persimmons in season. Douglas Firs dormant. Check beaverton outdoor events.")