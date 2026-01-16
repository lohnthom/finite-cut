import streamlit as st
from datetime import datetime
import sys
import os

# Import our data fetchers
# Save the data_fetchers code as 'data_fetchers.py' in the same directory
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
    st.warning("data_fetchers.py not found. Using mock data. Create data_fetchers.py to enable real data.")

# Page config
st.set_page_config(
    page_title="A Finite Cut",
    page_icon="📰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(to right, #EFF6FF, #F5F3FF);
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    .ai-overview {
        background: linear-gradient(to right, #F5F3FF, #FAF5FF);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #9333EA;
        margin-bottom: 1rem;
    }
    .feed-item {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 0.5rem;
    }
    .source-tag {
        color: #6B7280;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .time-badge {
        background: #DBEAFE;
        color: #1E40AF;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Section configuration
SECTION_CONFIG = [
    {
        "id": "world_news",
        "title": "World News",
        "frequency": "Daily",
        "time": 7,
    },
    {
        "id": "us_politics",
        "title": "US Politics",
        "frequency": "Daily",
        "time": 5,
    },
    {
        "id": "portland_local",
        "title": "Portland / Beaverton",
        "frequency": "Daily",
        "time": 6,
    },
    {
        "id": "canada_news",
        "title": "Places I Care About",
        "frequency": "Daily",
        "time": 5,
    },
    {
        "id": "3d_industry",
        "title": "3D Industry",
        "frequency": "3x per week",
        "time": 5,
    },
    {
        "id": "weather",
        "title": "Seasonal & Wild Weather",
        "frequency": "3x per week",
        "time": 4,
    },
]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_section_data(section_id: str):
    """Load data for a section with caching"""
    if not DATA_AVAILABLE:
        return get_mock_data(section_id)
    
    # Initialize AI generator (only if API key is set)
    api_key = os.environ.get('OPENAI_API_KEY')
    ai_gen = AIOverviewGenerator(api_key) if api_key else None
    
    # Fetch real data
    data = fetch_section_data(section_id, ai_gen)
    return data

def get_mock_data(section_id: str):
    """Fallback mock data"""
    mock_data = {
        "world_news": {
            "ai_overview": "Major diplomatic developments today: the UN climate summit wrapped up with a new framework. US politics: House Republicans are gridlocked over budget negotiations. The EU hit three AI companies with antitrust investigations.",
            "items": [
                {
                    "source": "Reuters",
                    "title": "UN Climate Summit Delivers New Framework",
                    "summary": "New binding targets for 2030",
                    "date": "Today",
                    "url": "#"
                }
            ]
        }
    }
    return mock_data.get(section_id, {"ai_overview": "No data available", "items": []})

# Initialize session state
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = {}
if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = {}

# Calculate total time
total_time = sum(section['time'] for section in SECTION_CONFIG)

# Header
st.markdown(f"""
<div class="main-header">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">A Finite Cut</h1>
    <p style="font-style: italic; color: #6B7280; margin-bottom: 1rem;">
        "It is better to be a victim of your own passions than of the whims of others."
    </p>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <p style="color: #4B5563; margin: 0;">{datetime.now().strftime('%A, %B %d, %Y')}</p>
        <div>
            <span style="font-size: 2rem; font-weight: bold; color: #1F2937;">{total_time}</span>
            <span style="color: #6B7280;"> minutes</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Info banner
if DATA_AVAILABLE:
    st.info("**How it works:** Each section starts with an AI overview. Click 'View sources' to see the articles. Data refreshes every hour.")
else:
    st.info("**Demo Mode:** Install dependencies (`pip install feedparser openai requests`) and set OPENAI_API_KEY to enable live data fetching.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    if st.button("🔄 Refresh All Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Data Sources")
    st.markdown(f"**Status:** {'✅ Live Data' if DATA_AVAILABLE else '⚠️ Mock Data'}")
    
    if DATA_AVAILABLE:
        st.markdown(f"**RSS Feeds:** {sum(len(feeds) for feeds in FEED_SOURCES.values())}")
        st.markdown(f"**AI Overviews:** {'✅ Enabled' if os.environ.get('OPENAI_API_KEY') else '❌ Disabled'}")

# Render sections
for section_config in SECTION_CONFIG:
    section_id = section_config['id']
    
    # Load section data
    with st.spinner(f"Loading {section_config['title']}..."):
        section_data = load_section_data(section_id)
    
    with st.container():
        # Section header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {section_config['title']}")
        with col2:
            st.markdown(
                f"<span class='time-badge'>{section_config['frequency']} • {section_config['time']} min</span>", 
                unsafe_allow_html=True
            )
        
        # AI Overview
        overview = section_data.get('ai_overview', 'No overview available')
        st.markdown(f"""
        <div class="ai-overview">
            <div style="display: flex; align-items: start; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">✨</span>
                <p style="margin: 0; line-height: 1.6; color: #374151;">{overview}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle for sources
        items = section_data.get('items', [])
        if st.button(
            f"{'Hide' if st.session_state.expanded_sections.get(section_id, False) else 'View'} sources ({len(items)})", 
            key=f"toggle_{section_id}"
        ):
            st.session_state.expanded_sections[section_id] = not st.session_state.expanded_sections.get(section_id, False)
        
        # Show sources if expanded
        if st.session_state.expanded_sections.get(section_id, False):
            for idx, item in enumerate(items):
                item_key = f"{section_id}_{idx}"
                
                st.markdown(f"""
                <div class="feed-item">
                    <div class="source-tag">{item.get('source', 'Unknown')}</div>
                    <h4 style="margin: 0.5rem 0; color: #1F2937;">{item.get('title', 'No title')}</h4>
                    <p style="margin: 0.5rem 0; color: #4B5563;">{item.get('summary', '')}</p>
                    <span style="font-size: 0.75rem; color: #9CA3AF;">{item.get('date', 'Recent')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(
                    f"{'Hide' if st.session_state.expanded_items.get(item_key, False) else 'Read'} full article", 
                    key=f"item_{item_key}"
                ):
                    st.session_state.expanded_items[item_key] = not st.session_state.expanded_items.get(item_key, False)
                
                if st.session_state.expanded_items.get(item_key, False):
                    st.markdown(f"""
                    > **Full article content would appear here.** In future updates, this will show the complete article text.
                    
                    [View original source →]({item.get('url', '#')})
                    """)
        
        st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>You've reached the end of today's briefing. Come back tomorrow for fresh content.</p>", unsafe_allow_html=True)