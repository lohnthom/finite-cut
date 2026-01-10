import streamlit as st
from datetime import datetime

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

# Mock data
mock_briefing = {
    "date": datetime.now().strftime("%A, %B %d, %Y"),
    "total_time": 35,
    "sections": [
        {
            "id": "world-news",
            "title": "World News",
            "frequency": "Daily",
            "time": 7,
            "ai_overview": "Major diplomatic developments today: the UN climate summit in Geneva wrapped up with a new carbon reduction framework that's actually getting cautious optimism from scientists. US politics: House Republicans are gridlocked over budget negotiations again, shutdown possible by end of month. In tech regulation news, the EU just hit three major AI companies with antitrust investigations. Middle East tensions are de-escalating slightly after ceasefire talks showed progress.",
            "items": [
                {
                    "source": "Reuters",
                    "title": "UN Climate Summit Delivers Unexpected Carbon Framework",
                    "summary": "New binding targets for 2030, developing nations get $200B fund",
                    "date": "Today"
                },
                {
                    "source": "Associated Press",
                    "title": "House Budget Talks Stall, Shutdown Looms",
                    "summary": "Republican factions divided on spending cuts, deadline Jan 31",
                    "date": "3 hours ago"
                },
                {
                    "source": "BBC",
                    "title": "EU Launches Antitrust Probes into AI Companies",
                    "summary": "Google, Microsoft, OpenAI face investigations over market dominance",
                    "date": "Today"
                }
            ]
        },
        {
            "id": "portland-local",
            "title": "Portland / Beaverton",
            "frequency": "Daily",
            "time": 6,
            "ai_overview": "Good morning! Portland's planning commission is meeting Wednesday to discuss a new mixed-use development in the Pearl District - 200 units plus ground-floor retail. There's a permit filed for a night market in Director Park this spring (April 15-May 15), which looks promising. In Beaverton: City council approved funding for a new MAX station at Walker Road. On the boring-but-interesting front: three new building permits on Division Street for mid-rise residential.",
            "items": [
                {
                    "source": "Portland Planning Commission",
                    "title": "Pearl District Mixed-Use Development - Public Hearing",
                    "summary": "200-unit residential building with ground-floor retail, 15th & Lovejoy",
                    "date": "Jan 12 meeting"
                },
                {
                    "source": "City Permits",
                    "title": "Special Event Permit: Director Park Night Market",
                    "summary": "Weekly night market, Thursdays 5-9pm, April-May",
                    "date": "Filed Jan 8"
                },
                {
                    "source": "Beaverton City Council",
                    "title": "Walker Road MAX Station Approved",
                    "summary": "$45M funding approved, construction starts fall 2026",
                    "date": "Yesterday"
                }
            ]
        },
        {
            "id": "places-care",
            "title": "Places I Care About",
            "frequency": "Daily",
            "time": 5,
            "ai_overview": "Atlantic Canada is dealing with a major winter storm - Halifax got 40cm of snow overnight, schools closed. There's some political drama in Nova Scotia over fishing quotas. Toronto news: new affordable housing development approved in Scarborough, 800 units. Also, the Raptors are on a surprising winning streak (5 games!) and Toronto FC just signed a big-name striker from Europe.",
            "items": [
                {
                    "source": "CBC Halifax",
                    "title": "Major Winter Storm Hits Atlantic Provinces",
                    "summary": "40cm snow in Halifax, travel disruptions across region",
                    "date": "Today"
                },
                {
                    "source": "Toronto Star",
                    "title": "Scarborough Affordable Housing Project Approved",
                    "summary": "800-unit development, mix of rental and ownership",
                    "date": "Today"
                }
            ]
        },
        {
            "id": "3d-industry",
            "title": "3D Industry",
            "frequency": "3x per week",
            "time": 5,
            "ai_overview": "Blender 4.3 beta dropped some wild geometry nodes updates - there's a new 'curve to mesh' node that's apparently way faster. Industry news: Unreal Engine 6 was teased at GDC with some mind-blowing real-time ray tracing demos. Adobe just acquired a procedural texture startup, probably integrating into Substance. The Blender subreddit is buzzing about someone who made a procedural city generator that actually looks usable.",
            "items": [
                {
                    "source": "Blender.org Blog",
                    "title": "Blender 4.3 Beta - Geometry Nodes Performance",
                    "summary": "New curve to mesh node, 3x faster in benchmarks",
                    "date": "2 days ago"
                },
                {
                    "source": "CGChannel",
                    "title": "Unreal Engine 6 Preview at GDC",
                    "summary": "Real-time path tracing, improved Nanite workflows",
                    "date": "Yesterday"
                }
            ]
        },
        {
            "id": "seasonal",
            "title": "Seasonal & Wild Weather",
            "frequency": "3x per week",
            "time": 4,
            "ai_overview": "Weather drama: there's a gnarly atmospheric river hitting Northern California right now - some areas expecting 15+ inches of rain through Wednesday. Iceland's got another volcanic fissure that opened yesterday, spectacular lava fountains but no threat to populated areas. Seasonally in Portland: red-tailed hawks are starting courtship displays (watch for aerial acrobatics). Indian plum should start budding in the next two weeks.",
            "items": [
                {
                    "source": "NOAA",
                    "title": "Atmospheric River Targets Northern California",
                    "summary": "Major flooding threat, 10-15\" rain through Jan 12",
                    "date": "Today"
                },
                {
                    "source": "Iceland Met Office",
                    "title": "New Volcanic Fissure - Reykjanes Peninsula",
                    "summary": "Lava fountains, no populated areas threatened",
                    "date": "Yesterday"
                }
            ]
        },
        {
            "id": "movies",
            "title": "Movies",
            "frequency": "2x per week",
            "time": 4,
            "ai_overview": "The Criterion Channel just added a retrospective on 90s Hong Kong action cinema - lots of John Woo and Jackie Chan deep cuts. There's a new A24 film getting incredible buzz at Sundance called 'The Greenhouse' - slow-burn psychological thing. And if you haven't seen it, there's a 4K restoration of 'The Third Man' playing at Cinema 21 this week.",
            "items": [
                {
                    "source": "Criterion Channel",
                    "title": "90s Hong Kong Action Cinema Collection",
                    "summary": "24 films added, John Woo and Jackie Chan retrospectives",
                    "date": "Added Jan 1"
                },
                {
                    "source": "Cinema 21",
                    "title": "The Third Man - 4K Restoration",
                    "summary": "Special engagement Jan 10-16",
                    "date": "This week"
                }
            ]
        },
        {
            "id": "restaurants",
            "title": "Restaurants",
            "frequency": "1x per week",
            "time": 2,
            "ai_overview": "New Vietnamese spot called 'Bà Nội' just opened on Hawthorne - family recipes, the spring rolls are apparently incredible. Getting lots of love on Portland Food Instagram.",
            "items": [
                {
                    "source": "Eater Portland",
                    "title": "Bà Nội Opens on Hawthorne",
                    "summary": "Family-run Vietnamese, traditional recipes, spring rolls a highlight",
                    "date": "Jan 8"
                }
            ]
        }
    ]
}

# Initialize session state for expanded sections
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = {}
if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = {}

# Header
st.markdown(f"""
<div class="main-header">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">A Finite Cut</h1>
    <p style="font-style: italic; color: #6B7280; margin-bottom: 1rem;">
        "It is better to be a victim of your own passions than of the whims of others."
    </p>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <p style="color: #4B5563; margin: 0;">{mock_briefing['date']}</p>
        <div>
            <span style="font-size: 2rem; font-weight: bold; color: #1F2937;">{mock_briefing['total_time']}</span>
            <span style="color: #6B7280;"> minutes</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Info banner
st.info("**How it works:** Each section starts with an AI overview. Click 'View sources' to see the articles that informed it. Click 'Read full article' to dive deeper.")

# Render sections
for section in mock_briefing['sections']:
    section_id = section['id']
    
    with st.container():
        # Section header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {section['title']}")
        with col2:
            st.markdown(f"<span class='time-badge'>{section['frequency']} • {section['time']} min</span>", unsafe_allow_html=True)
        
        # AI Overview
        st.markdown(f"""
        <div class="ai-overview">
            <div style="display: flex; align-items: start; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">✨</span>
                <p style="margin: 0; line-height: 1.6; color: #374151;">{section['ai_overview']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Toggle for sources
        if st.button(f"{'Hide' if st.session_state.expanded_sections.get(section_id, False) else 'View'} sources ({len(section['items'])})", key=f"toggle_{section_id}"):
            st.session_state.expanded_sections[section_id] = not st.session_state.expanded_sections.get(section_id, False)
        
        # Show sources if expanded
        if st.session_state.expanded_sections.get(section_id, False):
            for idx, item in enumerate(section['items']):
                item_key = f"{section_id}_{idx}"
                
                st.markdown(f"""
                <div class="feed-item">
                    <div class="source-tag">{item['source']}</div>
                    <h4 style="margin: 0.5rem 0; color: #1F2937;">{item['title']}</h4>
                    <p style="margin: 0.5rem 0; color: #4B5563;">{item['summary']}</p>
                    <span style="font-size: 0.75rem; color: #9CA3AF;">{item['date']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"{'Hide' if st.session_state.expanded_items.get(item_key, False) else 'Read'} full article", key=f"item_{item_key}"):
                    st.session_state.expanded_items[item_key] = not st.session_state.expanded_items.get(item_key, False)
                
                if st.session_state.expanded_items.get(item_key, False):
                    st.markdown("""
                    > **Full article content would appear here.** In the real app, this would be the scraped/fetched article text or a link to the source.
                    
                    [View original source →](#)
                    """)
        
        st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>You've reached the end of today's briefing. Come back tomorrow for fresh content.</p>", unsafe_allow_html=True)