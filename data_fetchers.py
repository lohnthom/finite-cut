"""
Data fetching modules for A Finite Cut
Handles RSS feeds, APIs, and web scraping
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import os

# Try to import OpenAI, fall back gracefully if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class RSSFetcher:
    """Fetch and parse RSS feeds"""
    
    @staticmethod
    def fetch_feed(url: str, max_items: int = 10) -> List[Dict]:
        """
        Fetch RSS feed and return structured items
        
        Args:
            url: RSS feed URL
            max_items: Maximum number of items to return
            
        Returns:
            List of feed items with title, summary, link, date
        """
        try:
            feed = feedparser.parse(url)
            items = []
            
            for entry in feed.entries[:max_items]:
                # Parse date
                published = entry.get('published_parsed') or entry.get('updated_parsed')
                if published:
                    date_obj = datetime(*published[:6])
                    date_str = RSSFetcher._format_date(date_obj)
                else:
                    date_str = "Recent"
                
                items.append({
                    'title': entry.get('title', 'No title'),
                    'summary': entry.get('summary', entry.get('description', ''))[:200],
                    'url': entry.get('link', '#'),
                    'date': date_str,
                    'source': feed.feed.get('title', 'RSS Feed')
                })
            
            return items
        except Exception as e:
            print(f"Error fetching RSS feed {url}: {e}")
            return []
    
    @staticmethod
    def _format_date(date_obj: datetime) -> str:
        """Format date as human-readable relative time"""
        now = datetime.now()
        diff = now - date_obj
        
        if diff.days == 0:
            if diff.seconds < 3600:
                mins = diff.seconds // 60
                return f"{mins} min ago" if mins > 1 else "Just now"
            else:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return date_obj.strftime("%b %d")


class RedditFetcher:
    """Fetch Reddit posts from specific subreddits"""
    
    @staticmethod
    def fetch_subreddit(subreddit: str, max_items: int = 5, time_filter: str = 'week') -> List[Dict]:
        """
        Fetch top posts from a subreddit
        
        Args:
            subreddit: Subreddit name (without r/)
            max_items: Maximum number of posts
            time_filter: 'day', 'week', 'month', 'year'
            
        Returns:
            List of Reddit posts
        """
        try:
            url = f"https://www.reddit.com/r/{subreddit}/top.json"
            headers = {'User-Agent': 'FiniteCut/1.0'}
            params = {'limit': max_items, 't': time_filter}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = []
            
            for post in data['data']['children']:
                post_data = post['data']
                created = datetime.fromtimestamp(post_data['created_utc'])
                
                items.append({
                    'title': post_data['title'],
                    'summary': post_data.get('selftext', '')[:200] or f"{post_data['ups']} upvotes",
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'date': RSSFetcher._format_date(created),
                    'source': f"r/{subreddit}"
                })
            
            return items
        except Exception as e:
            print(f"Error fetching Reddit r/{subreddit}: {e}")
            return []


class AIOverviewGenerator:
    """Generate conversational overviews using OpenAI API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize with OpenAI API key
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_overview(self, items: List[Dict], section_name: str) -> str:
        """
        Generate conversational overview from feed items
        
        Args:
            items: List of feed items
            section_name: Name of the section (for context)
            
        Returns:
            Conversational overview text
        """
        if not OPENAI_AVAILABLE:
            return "AI overview generation requires the 'openai' package. Install with: pip install openai"
        
        if not self.client:
            return "AI overview generation requires OPENAI_API_KEY environment variable."
        
        if not items:
            return f"No news in {section_name} today."
        
        # Prepare feed items for GPT
        feed_text = "\n\n".join([
            f"**{item['source']}**: {item['title']}\n{item['summary']}"
            for item in items
        ])
        
        prompt = f"""You're creating a conversational morning briefing. Here are news items from the "{section_name}" section:

{feed_text}

Write a friendly, conversational 2-3 sentence overview that:
- Sounds like you're talking to a friend over coffee
- Highlights the most interesting/important items
- Uses casual language ("there's", "apparently", "looks like")
- Connects related items naturally
- Avoids listy language or bullet points

Just the overview, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cheap, perfect for this
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates friendly, conversational news briefings."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating AI overview: {e}")
            return f"Updates from {section_name}: " + ", ".join([item['title'] for item in items[:3]])


# Feed source configurations
FEED_SOURCES = {
    'world_news': [
        'https://feeds.bbci.co.uk/news/world/rss.xml',  # BBC World
        'https://feeds.reuters.com/reuters/topNews',     # Reuters
        'http://rss.cnn.com/rss/cnn_topstories.rss',    # CNN
    ],
    'us_politics': [
        'https://www.politico.com/rss/politics08.xml',   # Politico
        'https://www.npr.org/rss/rss.php?id=1001',       # NPR Politics
    ],
    'portland_local': [
        'https://www.portlandoregon.gov/rss.cfm',        # City of Portland (if available)
        'https://www.oregonlive.com/arc/outboundfeeds/rss/?outputType=xml',  # OregonLive
    ],
    'canada_news': [
        'https://www.cbc.ca/cmlink/rss-topstories',      # CBC Top Stories
        'https://www.cbc.ca/cmlink/rss-canada-toronto',   # CBC Toronto
    ],
    '3d_industry': [
        'https://www.blender.org/feed/',                 # Blender Blog
        'https://www.cgchannel.com/feed/',               # CGChannel
    ],
    'weather': [
        'https://alerts.weather.gov/cap/us.php?x=0',     # NOAA Alerts
    ],
}

# Reddit sources
REDDIT_SOURCES = {
    '3d_industry': ['blender', 'vfx', '3Dmodeling'],
}


def fetch_section_data(section_id: str, ai_generator: AIOverviewGenerator = None) -> Dict:
    """
    Fetch all data for a section and generate AI overview
    
    Args:
        section_id: Section identifier
        ai_generator: Optional AI overview generator
        
    Returns:
        Dictionary with items and ai_overview
    """
    items = []
    
    # Fetch RSS feeds
    if section_id in FEED_SOURCES:
        for feed_url in FEED_SOURCES[section_id]:
            items.extend(RSSFetcher.fetch_feed(feed_url, max_items=5))
    
    # Fetch Reddit posts
    if section_id in REDDIT_SOURCES:
        for subreddit in REDDIT_SOURCES[section_id]:
            items.extend(RedditFetcher.fetch_subreddit(subreddit, max_items=3))
    
    # Sort by recency (this is approximate with our date strings)
    # You might want to store actual datetime objects for better sorting
    
    # Generate AI overview
    if ai_generator and items:
        overview = ai_generator.generate_overview(items, section_id)
    else:
        overview = f"Found {len(items)} items in {section_id}."
    
    return {
        'items': items[:10],  # Limit to 10 items per section
        'ai_overview': overview
    }


# Example usage
if __name__ == "__main__":
    # Test RSS fetching
    print("Testing RSS fetch...")
    items = RSSFetcher.fetch_feed('https://feeds.bbci.co.uk/news/world/rss.xml', max_items=3)
    for item in items:
        print(f"\n{item['title']}\n{item['summary']}\n")
    
    # Test Reddit fetching
    print("\n\nTesting Reddit fetch...")
    reddit_items = RedditFetcher.fetch_subreddit('blender', max_items=3)
    for item in reddit_items:
        print(f"\n{item['title']}\n{item['url']}\n")
    
    # Test AI overview (requires OPENAI_API_KEY)
    print("\n\nTesting AI overview...")
    ai_gen = AIOverviewGenerator()
    if ai_gen.client:
        overview = ai_gen.generate_overview(items[:3], "World News")
        print(f"\nOverview: {overview}")
    else:
        print("Set OPENAI_API_KEY to test AI overview generation")