import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Clock, Calendar, Coffee, Sparkles } from 'lucide-react';

// Mock data structure
const mockBriefing = {
  date: "Monday, January 10, 2026",
  totalEstimatedTime: 35,
  sections: [
    {
      id: 'world-news',
      title: 'World News',
      frequency: 'Daily',
      estimatedTime: 7,
      aiOverview: "Major diplomatic developments today: the UN climate summit in Geneva wrapped up with a new carbon reduction framework that's actually getting cautious optimism from scientists. US politics: House Republicans are gridlocked over budget negotiations again, shutdown possible by end of month. In tech regulation news, the EU just hit three major AI companies with antitrust investigations. Middle East tensions are de-escalating slightly after ceasefire talks showed progress.",
      feedItems: [
        {
          source: 'Reuters',
          title: 'UN Climate Summit Delivers Unexpected Carbon Framework',
          summary: 'New binding targets for 2030, developing nations get $200B fund',
          url: '#',
          date: 'Today'
        },
        {
          source: 'Associated Press',
          title: 'House Budget Talks Stall, Shutdown Looms',
          summary: 'Republican factions divided on spending cuts, deadline Jan 31',
          url: '#',
          date: '3 hours ago'
        },
        {
          source: 'BBC',
          title: 'EU Launches Antitrust Probes into AI Companies',
          summary: 'Google, Microsoft, OpenAI face investigations over market dominance',
          url: '#',
          date: 'Today'
        },
        {
          source: 'Al Jazeera',
          title: 'Middle East Ceasefire Talks Show Progress',
          summary: 'Mediators report breakthrough on key sticking points',
          url: '#',
          date: '5 hours ago'
        }
      ]
    },
    {
      id: 'portland-local',
      title: 'Portland / Beaverton',
      frequency: 'Daily',
      estimatedTime: 6,
      aiOverview: "Good morning! Portland's planning commission is meeting Wednesday to discuss a new mixed-use development in the Pearl District - 200 units plus ground-floor retail. There's a permit filed for a night market in Director Park this spring (April 15-May 15), which looks promising. Public works is draining a wetland area near Powell Butte for restoration work starting next month. In Beaverton: City council approved funding for a new MAX station at Walker Road. On the boring-but-interesting front: three new building permits on Division Street for mid-rise residential.",
      feedItems: [
        {
          source: 'Portland Planning Commission',
          title: 'Pearl District Mixed-Use Development - Public Hearing',
          summary: '200-unit residential building with ground-floor retail, 15th & Lovejoy',
          url: '#',
          date: 'Jan 12 meeting'
        },
        {
          source: 'City Permits',
          title: 'Special Event Permit: Director Park Night Market',
          summary: 'Weekly night market, Thursdays 5-9pm, April-May',
          url: '#',
          date: 'Filed Jan 8'
        },
        {
          source: 'Beaverton City Council',
          title: 'Walker Road MAX Station Approved',
          summary: '$45M funding approved, construction starts fall 2026',
          url: '#',
          date: 'Yesterday'
        },
        {
          source: 'Portland Parks & Rec',
          title: 'Powell Butte Wetland Restoration Project',
          summary: 'Temporary drainage for invasive species removal and native planting',
          url: '#',
          date: 'Starts Feb 1'
        }
      ]
    },
    {
      id: 'places-i-care',
      title: 'Places I Care About',
      frequency: 'Daily',
      estimatedTime: 5,
      aiOverview: "Atlantic Canada is dealing with a major winter storm - Halifax got 40cm of snow overnight, schools closed. There's some political drama in Nova Scotia over fishing quotas. Toronto news: new affordable housing development approved in Scarborough, 800 units. Also, the Raptors are on a surprising winning streak (5 games!) and Toronto FC just signed a big-name striker from Europe.",
      feedItems: [
        {
          source: 'CBC Halifax',
          title: 'Major Winter Storm Hits Atlantic Provinces',
          summary: '40cm snow in Halifax, travel disruptions across region',
          url: '#',
          date: 'Today'
        },
        {
          source: 'The Chronicle Herald',
          title: 'Nova Scotia Fishing Quota Dispute Escalates',
          summary: 'Federal limits clash with provincial industry demands',
          url: '#',
          date: 'Yesterday'
        },
        {
          source: 'Toronto Star',
          title: 'Scarborough Affordable Housing Project Approved',
          summary: '800-unit development, mix of rental and ownership',
          url: '#',
          date: 'Today'
        },
        {
          source: 'The Athletic',
          title: 'Raptors Extend Win Streak to 5 Games',
          summary: 'Playoff hopes renewed after strong January performance',
          url: '#',
          date: 'Last night'
        }
      ]
    },
    {
      id: '3d-industry',
      title: '3D Industry',
      frequency: '3x per week',
      estimatedTime: 5,
      aiOverview: "Blender 4.3 beta dropped some wild geometry nodes updates - there's a new 'curve to mesh' node that's apparently way faster. Industry news: Unreal Engine 6 was teased at GDC with some mind-blowing real-time ray tracing demos. Adobe just acquired a procedural texture startup, probably integrating into Substance. The Blender subreddit is buzzing about someone who made a procedural city generator that actually looks usable.",
      feedItems: [
        {
          source: 'Blender.org Blog',
          title: 'Blender 4.3 Beta - Geometry Nodes Performance',
          summary: 'New curve to mesh node, 3x faster in benchmarks',
          url: '#',
          date: '2 days ago'
        },
        {
          source: 'CGChannel',
          title: 'Unreal Engine 6 Preview at GDC',
          summary: 'Real-time path tracing, improved Nanite workflows',
          url: '#',
          date: 'Yesterday'
        },
        {
          source: 'TechCrunch',
          title: 'Adobe Acquires Procedural Texture Startup Textura',
          summary: '$120M deal, likely Substance integration',
          url: '#',
          date: 'Today'
        },
        {
          source: 'r/blender',
          title: 'Procedural City Generator [Free Download]',
          summary: 'Geometry nodes setup for realistic cities, customizable',
          url: '#',
          date: '1 day ago'
        }
      ]
    },
    {
      id: 'seasonal-nature',
      title: 'Seasonal & Wild Weather',
      frequency: '3x per week',
      estimatedTime: 4,
      aiOverview: "Weather drama: there's a gnarly atmospheric river hitting Northern California right now - some areas expecting 15+ inches of rain through Wednesday. Iceland's got another volcanic fissure that opened yesterday, spectacular lava fountains but no threat to populated areas. Seasonally in Portland: red-tailed hawks are starting courtship displays (watch for aerial acrobatics). Indian plum should start budding in the next two weeks - first native shrub to bloom. Coho salmon are still running in local streams.",
      feedItems: [
        {
          source: 'NOAA',
          title: 'Atmospheric River Targets Northern California',
          summary: 'Major flooding threat, 10-15" rain through Jan 12',
          url: '#',
          date: 'Today'
        },
        {
          source: 'Iceland Met Office',
          title: 'New Volcanic Fissure - Reykjanes Peninsula',
          summary: 'Lava fountains, no populated areas threatened',
          url: '#',
          date: 'Yesterday'
        },
        {
          source: 'Portland Audubon',
          title: 'Red-Tailed Hawk Courtship Season',
          summary: 'Watch for aerial displays mid-January through February',
          url: '#',
          date: 'This week'
        },
        {
          source: 'Oregon Wild',
          title: 'Coho Salmon Winter Run Continues',
          summary: 'Peak spawning through January in local streams',
          url: '#',
          date: 'Jan 1'
        }
      ]
    },
    {
      id: 'movies',
      title: 'Movies',
      frequency: '2x per week',
      estimatedTime: 4,
      aiOverview: "The Criterion Channel just added a retrospective on 90s Hong Kong action cinema - lots of John Woo and Jackie Chan deep cuts. There's a new A24 film getting incredible buzz at Sundance called 'The Greenhouse' - slow-burn psychological thing. And if you haven't seen it, there's a 4K restoration of 'The Third Man' playing at Cinema 21 this week.",
      feedItems: [
        {
          source: 'Criterion Channel',
          title: '90s Hong Kong Action Cinema Collection',
          summary: '24 films added, John Woo and Jackie Chan retrospectives',
          url: '#',
          date: 'Added Jan 1'
        },
        {
          source: 'IndieWire',
          title: '"The Greenhouse" Stuns at Sundance',
          summary: 'A24 psychological thriller, Rave reviews',
          url: '#',
          date: 'Yesterday'
        },
        {
          source: 'Cinema 21',
          title: 'The Third Man - 4K Restoration',
          summary: 'Special engagement Jan 10-16',
          url: '#',
          date: 'This week'
        }
      ]
    },
    {
      id: 'restaurants',
      title: 'Restaurants',
      frequency: '1x per week',
      estimatedTime: 2,
      aiOverview: "New Vietnamese spot called 'Bà Nội' just opened on Hawthorne - family recipes, the spring rolls are apparently incredible. Getting lots of love on Portland Food Instagram.",
      feedItems: [
        {
          source: 'Eater Portland',
          title: 'Bà Nội Opens on Hawthorne',
          summary: 'Family-run Vietnamese, traditional recipes, spring rolls a highlight',
          url: '#',
          date: 'Jan 8'
        }
      ]
    },
    {
      id: 'seasonal',
      title: 'Seasonal Nature',
      frequency: '1x per week',
      estimatedTime: 3,
      aiOverview: "Mid-January in Portland: red-tailed hawks are starting courtship displays (watch for aerial acrobatics). Indian plum should start budding in the next two weeks - first native shrub to bloom. If you're hiking, keep an eye out for winter wrens - they're tiny but loud. Coho salmon are still running in local streams.",
      feedItems: [
        {
          source: 'Audubon Society',
          title: 'Red-Tailed Hawk Courtship Season',
          summary: 'Watch for aerial displays mid-January through February',
          url: '#',
          date: 'This week'
        },
        {
          source: 'Portland Urban Forestry',
          title: 'Indian Plum Early Blooming',
          summary: 'First native shrub to bloom, watch for buds late January',
          url: '#',
          date: 'Jan 5'
        },
        {
          source: 'Oregon Wild',
          title: 'Coho Salmon Winter Run',
          summary: 'Peak spawning continues through January',
          url: '#',
          date: 'Jan 1'
        }
      ]
    }
  ]
};

const SectionCard = ({ section }) => {
  const [overviewExpanded, setOverviewExpanded] = useState(false);
  const [feedExpanded, setFeedExpanded] = useState({});
  
  const toggleFeedItem = (index) => {
    setFeedExpanded(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-4 overflow-hidden">
      <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
        <div className="flex justify-between items-start mb-2">
          <h2 className="text-xl font-semibold text-gray-800">{section.title}</h2>
          <div className="flex gap-3 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              {section.frequency}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {section.estimatedTime} min
            </span>
          </div>
        </div>
      </div>

      {/* AI Overview Layer */}
      <div className="p-4 bg-gradient-to-r from-violet-50 to-purple-50 border-b border-gray-200">
        <div className="flex items-start gap-2 mb-2">
          <Sparkles className="w-5 h-5 text-purple-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <p className="text-gray-700 leading-relaxed">
              {section.aiOverview}
            </p>
          </div>
        </div>
        <button
          onClick={() => setOverviewExpanded(!overviewExpanded)}
          className="mt-3 text-sm font-medium text-purple-700 hover:text-purple-900 flex items-center gap-1"
        >
          {overviewExpanded ? (
            <>
              <ChevronDown className="w-4 h-4" />
              Hide sources
            </>
          ) : (
            <>
              <ChevronRight className="w-4 h-4" />
              View sources ({section.feedItems.length})
            </>
          )}
        </button>
      </div>

      {/* Feed Items Layer */}
      {overviewExpanded && (
        <div className="p-4 bg-gray-50">
          {section.feedItems.map((item, index) => (
            <div key={index} className="mb-3 last:mb-0">
              <div className="bg-white rounded border border-gray-200 p-3">
                <div className="flex justify-between items-start mb-1">
                  <div className="flex-1">
                    <div className="text-xs text-gray-500 mb-1">{item.source}</div>
                    <h3 className="font-medium text-gray-800 mb-1">{item.title}</h3>
                    <p className="text-sm text-gray-600">{item.summary}</p>
                  </div>
                  <span className="text-xs text-gray-400 ml-3 whitespace-nowrap">{item.date}</span>
                </div>
                <button
                  onClick={() => toggleFeedItem(index)}
                  className="mt-2 text-xs font-medium text-blue-600 hover:text-blue-800 flex items-center gap-1"
                >
                  {feedExpanded[index] ? (
                    <>
                      <ChevronDown className="w-3 h-3" />
                      Hide full article
                    </>
                  ) : (
                    <>
                      <ChevronRight className="w-3 h-3" />
                      Read full article
                    </>
                  )}
                </button>
                
                {/* Full Article Layer */}
                {feedExpanded[index] && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-sm text-gray-700 mb-3">
                      [Full article content would appear here. In the real app, this would be the scraped/fetched article text or a link to the source.]
                    </p>
                    <a
                      href={item.url}
                      className="text-sm text-blue-600 hover:text-blue-800 underline"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View original source &rarr;
                    </a>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default function PersonalIntelDashboard() {
  const [activeSections, setActiveSections] = useState(
    mockBriefing.sections.map(s => s.id)
  );

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-1">A Finite Cut</h1>
              <p className="text-sm italic text-gray-500 mb-2">"It is better to be a victim of your own passions than of the whims of others."</p>
              <p className="text-gray-600">{mockBriefing.date}</p>
            </div>
            <div className="text-right">
              <div className="flex items-center gap-2 text-gray-600">
                <Coffee className="w-5 h-5" />
                <span className="text-2xl font-semibold">{mockBriefing.totalEstimatedTime}</span>
                <span className="text-sm">minutes</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">Estimated reading time</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>How it works:</strong> Each section starts with an AI overview. Click "View sources" to see the articles that informed it. Click "Read full article" to dive deeper.
          </p>
        </div>

        {mockBriefing.sections
          .filter(section => activeSections.includes(section.id))
          .map(section => (
            <SectionCard key={section.id} section={section} />
          ))}
      </div>

      {/* Footer */}
      <div className="max-w-5xl mx-auto px-6 py-8 text-center text-sm text-gray-500">
        <p>You've reached the end of today's briefing. Come back tomorrow for fresh content.</p>
      </div>
    </div>
  );
}