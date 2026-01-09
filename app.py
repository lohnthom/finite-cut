import streamlit as st
import feedparser
from datetime import datetime

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="Finite Cut", layout="wide")

# This fixes the 'unsafe_allow_html' typo and adds your custom style
st.markdown("""
    <style>
    @media print {
        header, [data-testid="stSidebar"], .stButton, .stCheckbox { display: none !important; }
        .main .block-container { max-width: 100% !important; padding: 0 !important; }
    }
    .main-title { font-family: 'Courier New', monospace; font-weight: bold; font-size: 3rem; margin-bottom: 0px; }
    .sub-quote { font-family: 'Georgia', serif; font-style: italic; color: #555; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px; }
    .feed-card { border-left: 2px solid #000; padding-left: 15px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE HEADER ---
st.markdown('<div class="main-title">FINITE CUT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-quote">"It is better to be a victim of your own passions than of the whims of others."</div>', unsafe_allow_html=True)
st.caption(f"PDX • BEAVERTON • CANADA | {datetime.now().strftime('%A, %B %d, %Y')}")

# --- 3. SIDEBAR: 04 / SEASONAL (Persistent) ---
with st.sidebar:
    st.header("04 / SEASONAL")
    st.markdown("---")
    st.subheader("January Pulse")
    st.write("**Grocery:** Persimmons, Root Veg, Dungeness Crab.")
    st.write("**Flora:** Douglas Fir (Dormant), Witch Hazel (Blooming).")
    st.write("**Fauna:** Great Horned Owls nesting.")

# --- 4. THE DAILY BRIEFING ---
st.header("01 / DAILY")

# The RSS logic
feeds = {
    "PDX Permits": "https://www.portland.gov/ppd/news/rss",
    "Canada Atlantic": "https://www.cbc.ca/webfeed/rss/rss-canada-novascotia",
    "Blender Studio": "https://studio.blender.org/blog/rss"
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Sentinel News")
    for name, url in feeds.items():
        with st.expander(f"REVEAL: {name}"):
            f = feedparser.parse(url)
            for entry in f.entries[:3]: # Limit to 3 items
                st.markdown(f"**{entry.title}**")
                st.caption(f"Source: {name}")
                st.write(entry.summary[:200] + "...")
                st.markdown("---")

with col2:
    st.subheader("Daily Inspiration")
    # This will pull a random high-quality image for your Pinterest feel
    st.image("https://picsum.photos/400/600", caption="Inspiration Cycle")

# --- 5. THE PRINT BUTTON ---
st.markdown("---")
if st.button("Prepare Print Version"):
    st.write("Done! Use **Cmd + P** to print this briefing.")