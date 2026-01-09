import streamlit as st
import feedparser
import os
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Finite Cut", layout="wide")

# --- 2. STYLE & CSS ---
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

# --- 3. THE HEADER ---
st.markdown('<div class="main-title">FINITE CUT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-quote">"It is better to be a victim of your own passions than of the whims of others."</div>', unsafe_allow_html=True)
st.caption(f"PDX • BEAVERTON • CANADA | {datetime.now().strftime('%A, %B %d, %Y')}")

# --- 4. DATA SOURCES ---
FEEDS = {
    "PDX Permits & News": "https://www.portland.gov/bds/news/rss",
    "Atlantic Canada (CBC)": "https://www.cbc.ca/cctoc/rss/news/canada/atlantic",
    "Blender Studio": "https://studio.blender.org/blog/rss",
    "Pitchfork Music": "https://pitchfork.com/feed/feed-reviews/rss"
}

# --- 5. SIDEBAR: SEASONAL ---
with st.sidebar:
    st.header("04 / SEASONAL")
    st.markdown("---")
    st.subheader("January Pulse")
    st.write("**Grocery:** Persimmons, Root Veg, Dungeness Crab.")
    st.write("**Flora:** Douglas Fir (Dormant), Witch Hazel (Blooming).")
    st.write("**Fauna:** Great Horned Owls nesting.")

# --- 6. THE DAILY BRIEFING ---
st.header("01 / DAILY")

def render_feed(name, url, limit=3):
    feed = feedparser.parse(url)
    if not feed.entries:
        st.write(f"No new updates for {name}")
        return
    for entry in feed.entries[:limit]:
        st.markdown(f"**{entry.title}**")
        st.caption(f"Source: {name}")
        if name in ["PDX Permits & News", "Atlantic Canada (CBC)"]:
            with st.expander("Read Overview"):
                st.write(entry.summary[:300] + "...")
        st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Sentinel News")
    render_feed("PDX Permits & News", FEEDS["PDX Permits & News"])
    render_feed("Atlantic Canada (CBC)", FEEDS["Atlantic Canada (CBC)"])
    render_feed("Blender Studio", FEEDS["Blender Studio"])

with col2:
    st.subheader("Cyclic Inspiration")
    # Tries to pull your Pinterest feed image, falls back to Picsum if empty
    pin_feed = feedparser.parse("https://www.pinterest.com/laurenthomas8261/feed.rss")
    if pin_feed.entries:
        # Get the first image from your Pinterest feed
        st.image(pin_feed.entries[0].enclosures[0].href, caption="From your Pinterest")
    else:
        day_of_year = datetime.now().timetuple().tm_yday
        st.image(f"https://picsum.photos/seed/{day_of_year}/400/600", caption="Daily Pinterest Reflection")

# --- 7. WEEKLY & PRINT ---
st.header("02 / WEEKLY")
with st.expander("Reveal Weekly Music"):
    render_feed("Pitchfork Music", FEEDS["Pitchfork Music"], limit=5)

st.markdown("---")
if st.button("Prepare Print Version"):
    st.write("Done! Use **Cmd + P** to print.")