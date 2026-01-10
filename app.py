import streamlit as st
import feedparser
from datetime import datetime
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Finite Cut", layout="wide")

# --- 2. CSS STYLING ---
# Using 'unsafe_allow_html' to inject custom fonts and borders
st.markdown("""
    <style>
    @media print {
        header, [data-testid="stSidebar"], .stButton, .stCheckbox { display: none !important; }
        .main .block-container { max-width: 100% !important; padding: 0 !important; }
    }
    .main-title { font-family: 'Courier New', monospace; font-weight: bold; font-size: 3.5rem; margin-bottom: 0px; }
    .sub-quote { font-family: 'Georgia', serif; font-style: italic; color: #444; font-size: 1.3rem; margin-top: -10px; margin-bottom: 30px; border-bottom: 1px solid #000; padding-bottom: 15px; }
    .section-header { font-family: 'Courier New', monospace; font-weight: bold; letter-spacing: 2px; border-bottom: 2px solid #000; margin-bottom: 15px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE HEADER ---
st.markdown('<div class="main-title">FINITE CUT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-quote">"It is better to be a victim of your own passions than of the whims of others."</div>', unsafe_allow_html=True)
st.caption(f"PDX • BEAVERTON • CANADA | {datetime.now().strftime('%A, %b %d, %Y')}")

# --- 4. SIDEBAR: 04 / SEASONAL ---
with st.sidebar:
    st.markdown('<div class="section-header">04 / SEASONAL</div>', unsafe_allow_html=True)
    st.subheader("Deep Winter")
    st.write("**Grocery:** Persimmons, Root Veg, Dungeness Crab.")
    st.write("**Flora:** Douglas Fir (Dormant), Witch Hazel (Blooming).")
    st.write("**Fauna:** Great Horned Owls nesting.")
    st.markdown("---")
    st.caption("Phase: Dormancy & Planning")

# --- 5. 01 / DAILY : THE SENTINEL ---
st.markdown('<div class="section-header">01 / DAILY : THE SENTINEL</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # PORTLAND FEED
    st.markdown("### 🌲 Portland & Beaverton")
    pdx_feed = feedparser.parse("https://www.portland.gov/bds/news/rss")
    for entry in pdx_feed.entries[:2]:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.write(re.sub('<[^<]+?>', '', entry.summary)[:250] + "...")
    
    st.markdown("---")
    
    # CANADA FEED
    st.markdown("### 🌊 Atlantic Canada")
    canada_feed = feedparser.parse("https://www.cbc.ca/cctoc/rss/news/canada/atlantic")
    for entry in canada_feed.entries[:2]:
        st.markdown(f"**{entry.title}**")
        st.write(re.sub('<[^<]+?>', '', entry.summary)[:200] + "...")

    st.markdown("---")
    
    # BLENDER FEED
    st.markdown("### 🧡 Blender Studio")
    blender_feed = feedparser.parse("https://studio.blender.org/blog/rss")
    if blender_feed.entries:
        st.markdown(f"**{blender_feed.entries[0].title}**")

with col2:
    st.subheader("Daily Inspiration")
    # PINTEREST FEED
    pin_feed = feedparser.parse("https://www.pinterest.com/laurenthomas8261/feed.rss")
    if pin_feed.entries:
        desc = pin_feed.entries[0].description
        img_urls = re.findall(r'src="([^"]+)"', desc)
        if img_urls:
            st.image(img_urls[0], use_container_width=True)
    else:
        st.image(f"https://picsum.photos/seed/{datetime.now().day}/400/600")

# --- 6. 02 / WEEKLY : DEEP DIVES ---
st.markdown('<div class="section-header">02 / WEEKLY : DEEP DIVES</div>', unsafe_allow_html=True)

w_col1, w_col2 = st.columns(2)
with w_col1:
    with st.expander("Music & Reviews"):
        st.write("Placeholder: Pitchfork/YouTube weekly summaries.")
with w_col2:
    with st.expander("Restaurant Leads"):
        st.write("Placeholder: Eater PDX and new permit alerts.")

# --- 7. THE ARCHIVE / PRINT ---
st.markdown("---")
if st.button("Format for Print"):
    st.success("Ready. Press Cmd+P to save as a 'Finite' physical copy.")