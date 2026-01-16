import streamlit as st
from datetime import datetime
import os

# Import our data fetchers
try:
    from data_fetchers import (
        RSSFetcher, 
        RedditFetcher, 
        AIOverviewGenerator,
        fetch_section_data,
        FEED_SOURCES
    )
    DATA_AVAILABLE = True
except ImportError:
    DATA_AVAILABLE = False
    st.warning("data_fetchers.py not found. Using mock data.")

# Page config
st.set_page_config(
    page_title="A Finite Cut",
    page_icon="📰",
    layout="wide"
)

# Section configuration
SECTION_CONFIG = [
    {"id": "world_news", "title": "World News", "frequency": "Daily", "time": 7},
    {"id": "us_politics", "title": "US Politics", "frequency": "Daily", "time": 5},
    {"id": "portland_local", "title": "Portland / Beaverton", "frequency": "Daily", "time": 6},
    {"id": "canada_news", "title": "Places I Care About", "frequency": "Daily", "time": 5},
    {"id": "3d_industry", "title": "3D Industry", "frequency": "3x per week", "time": 5},
    {"id": "weather", "title": "Seasonal & Wild Weather", "frequency": "3x per week", "time": 4},
]

@st.cache_data(ttl=3600)
def load_section_data(section_id: str):
    """Load data for a section with caching"""
    if not DATA_AVAILABLE:
        return get_mock_data(section_id)
    
    api_key = os.environ.get('OPENAI_API_KEY')
    ai_gen = AIOverviewGenerator(api_key) if api_key else None
    data = fetch_section_data(section_id, ai_gen)
    return data

def get_mock_data(section_id: str):
    """Fallback mock data"""
    mock_data = {
        "world_news": {
            "ai_overview": "Major diplomatic developments today.",
            "items": [{"source": "Reuters", "title": "UN Climate Summit", "summary": "New targets", "date": "Today", "url": "#"}]
        }
    }
    return mock_data.get(section_id, {"ai_overview": "No data available", "items": []})

# Initialize session state
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = {}
if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = {}

# Header
st.title("A Finite Cut")
st.caption("_It is better to be a victim of your own passions than of the whims of others._")

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"**{datetime.now().strftime('%A, %B %d, %Y')}**")
with col2:
    total_time = sum(section['time'] for section in SECTION_CONFIG)
    st.metric("Est. Time", f"{total_time} min")

st.divider()

# Info banner
if DATA_AVAILABLE:
    st.info("💡 Each section starts with an AI overview. Click 'View sources' to see articles. Data refreshes hourly.")
else:
    st.info("📦 Demo Mode: Install dependencies and set OPENAI_API_KEY to enable live data.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    if st.button("🔄 Refresh All Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    st.subheader("Data Sources")
    st.write(f"**Status:** {'✅ Live' if DATA_AVAILABLE else '⚠️ Mock'}")
    
    if DATA_AVAILABLE:
        st.write(f"**RSS Feeds:** {sum(len(feeds) for feeds in FEED_SOURCES.values())}")
        st.write(f"**AI Overviews:** {'✅ On' if os.environ.get('OPENAI_API_KEY') else '❌ Off'}")

# Render sections
for section_config in SECTION_CONFIG:
    section_id = section_config['id']
    
    with st.spinner(f"Loading {section_config['title']}..."):
        section_data = load_section_data(section_id)
    
    # Section header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader(section_config['title'])
    with col2:
        st.caption(f"{section_config['frequency']} • {section_config['time']} min")
    
    # AI Overview in a nice container
    with st.container(border=True):
        st.write(f"✨ {section_data.get('ai_overview', 'No overview available')}")
    
    # Toggle for sources
    items = section_data.get('items', [])
    if st.button(
        f"{'▼ Hide' if st.session_state.expanded_sections.get(section_id) else '▶ View'} sources ({len(items)})", 
        key=f"toggle_{section_id}"
    ):
        st.session_state.expanded_sections[section_id] = not st.session_state.expanded_sections.get(section_id, False)
    
    # Show sources if expanded
    if st.session_state.expanded_sections.get(section_id, False):
        for idx, item in enumerate(items):
            item_key = f"{section_id}_{idx}"
            
            with st.container(border=True):
                st.caption(item.get('source', 'Unknown'))
                st.markdown(f"**{item.get('title', 'No title')}**")
                st.write(item.get('summary', ''))
                st.caption(item.get('date', 'Recent'))
                
                if st.button(
                    f"{'Hide' if st.session_state.expanded_items.get(item_key) else 'Read'} full article", 
                    key=f"item_{item_key}"
                ):
                    st.session_state.expanded_items[item_key] = not st.session_state.expanded_items.get(item_key, False)
                
                if st.session_state.expanded_items.get(item_key, False):
                    st.info("Full article content would appear here.")
                    st.markdown(f"[View original source →]({item.get('url', '#')})")
    
    st.divider()

# Footer
st.caption("You've reached the end of today's briefing. Come back tomorrow for fresh content.")