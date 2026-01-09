import streamlit as st
import feedparser
from datetime import datetime
import re

# 1. PAGE SETUP
st.set_page_config(page_title="Finite Cut", layout="wide")

# 2. STYLING (CRITICAL: 'unsafe_allow_html' is the only correct term)
st.markdown("""
    <style>
    .main-title { font-family: 'Courier New', monospace; font-weight: bold; font-size: 3rem; margin-bottom: 0px; }
    .sub-quote { font-family: 'Georgia', serif; font-style: italic; color: #555; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px; }
    .daily-card { border-left: 3px solid black; padding-left: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE HEADER ---
st.markdown('<div class="main-title">FINITE CUT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-quote">"It is better to be a victim of your own passions than of the whims of others."</div>', unsafe_allow_html=True)
st.caption(f"PDX • BEAVERTON • CANADA | {datetime.now().strftime('%A, %B %d, %Y')}")

# 4. COLUMNS
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("01 / NEWS")
    feed = feedparser.parse("https://www.portland.gov/bds/news/rss")
    for entry in feed.entries[:3]:
        st.markdown(f"**{entry.title}**")
        st.write(re.sub('<[^<]+?>', '', entry.summary)[:200] + "...")
        st.markdown("---")

with col2:
    st.subheader("02 / INSPIRATION")
    pin_feed = feedparser.parse("https://www.pinterest.com/laurenthomas8261/feed.rss")
    if pin_feed.entries:
        # Extract image from the description HTML
        desc = pin_feed.entries[0].description
        img_url = re.findall(r'src="([^"]+)"', desc)
        if img_url:
            st.image(img_url[0], use_container_width=True)
        else:
            st.info("Feed found, but no image link detected.")
    else:
        st.write("No pins found.")