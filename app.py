import streamlit as st
import feedparser
from datetime import datetime
import re

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Finite Cut", layout="wide")

# --- STYLING (The Finite Look) ---
st.markdown("""
<style>
    @media print {
        header, [data-testid="stSidebar"], .stButton, .stCheckbox { display: none !important; }
        .main .block-container { max-width: 100% !important; padding: 0 !important; }
    }
    .main-title { font-family: 'Courier New', monospace; font-weight: bold; font-size: 3rem; margin-bottom: 0px; }
    .sub-quote { font-family: 'Georgia', serif; font-style: italic; color: #555; font-size: 1.1rem; margin-top: -10px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE HEADER ---
st.markdown('<div class="main-title">FINITE CUT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-quote">"It is better to be a victim of your own passions than of the whims of others."</div>', unsafe_allow_html=True)
st.caption(f"PDX • BEAVERTON • CANADA | {datetime.now().strftime('%A, %b %d, %Y')}")

# --- 4. DATA SOURCES ---
FEEDS = {
    "PDX Permits & News": "https://www.portland.gov/bds/news/rss",
    "Atlantic Canada (CBC)": "https://www.cbc.ca/cctoc/rss/news/canada/atlantic",
    "Blender Studio": "https://studio.blender.org/blog/rss",
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
    for entry in feed.entries[:limit]:
        st.markdown(f"**{entry.title}**")
        st.caption(f"Source: {name}")
        with st.expander("Read Overview"):
            # Clean up HTML tags from summaries
            summary = re.sub('<[^<]+?>', '', entry.summary)
            st.write(summary[:300] + "...")
        st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Brief Cut")
    for name, url in FEEDS.items():
        render_feed(name, url)

with col2:
    st.subheader("Cyclic Inspiration")
    # This reaches out to your specific Pinterest feed
    pin_feed = feedparser.parse("https://www.pinterest.com/laurenthomas8261/feed.rss")
    
    if pin_feed.entries:
        # Pinterest buries the image in the 'description' field
        # We use a 'regex' to find the URL ending in .jpg or .png
        import re
        desc = pin_feed.entries[0].description
        img_urls = re.findall(r'src="([^"]+)"', desc)
        
        if img_urls:
            # We take the first image URL found in the description
            st.image(img_urls[0], use_container_width=True, caption="Latest from Pinterest")
        else:
            st.warning("Found the feed, but couldn't 'dig out' the image.")
    else:
        # Fallback if Pinterest is being slow or the feed is empty
        st.image(f"https://picsum.photos/seed/{datetime.now().day}/400/600", caption="Daily Reflection")