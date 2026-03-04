"""World news RSS source adapters."""

from __future__ import annotations

import logging
from typing import Any

import feedparser

log = logging.getLogger(__name__)

WORLD_FEEDS: list[dict[str, str]] = [
    {"source": "bbc", "feed_url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"source": "bbc_asia", "feed_url": "https://feeds.bbci.co.uk/news/world/asia/rss.xml"},
    {"source": "bbc_africa", "feed_url": "https://feeds.bbci.co.uk/news/world/africa/rss.xml"},
    {"source": "bbc_middle_east", "feed_url": "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml"},
    {"source": "economist", "feed_url": "https://www.economist.com/the-world-this-week/rss.xml"},
    {"source": "economist_asia", "feed_url": "https://www.economist.com/asia/rss.xml"},
    {"source": "economist_mea", "feed_url": "https://www.economist.com/middle-east-and-africa/rss.xml"},
    {"source": "economist_graphic_detail", "feed_url": "https://www.economist.com/graphic-detail/rss.xml"},
    {"source": "guardian_world", "feed_url": "https://www.theguardian.com/world/rss"},
    {"source": "guardian_international", "feed_url": "https://www.theguardian.com/international/rss"},
    {"source": "dispatch", "feed_url": "https://thedispatch.com/feed/"},
    {"source": "politico", "feed_url": "https://www.politico.eu/feed/"},
    # USA
    {
        "source": "gov_us_dod_releases",
        "feed_url": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=9&Site=945&max=30",
    },
    {
        "source": "gov_us_dod_contracts",
        "feed_url": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=400&Site=945&max=30",
    },
    # UK
    {"source": "gov_uk_announcements", "feed_url": "https://www.gov.uk/search/news-and-communications.atom"},
    # EU
    {"source": "gov_eu_commission", "feed_url": "https://ec.europa.eu/commission/presscorner/api/rss"},
    # Canada
    {"source": "gov_canada_news", "feed_url": "https://api.io.canada.ca/io-server/gc/news/en/v2?sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=National"},
    {"source": "gov_canada_pm", "feed_url": "https://pm.gc.ca/en/news.rss"},
    {"source": "gov_canada_global_affairs", "feed_url": "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=50&format=atom&atomtitle=GlobalAffairs"},
    # Americas – South America & Latin America
    {"source": "gov_brazil_planalto", "feed_url": "https://www.gov.br/planalto/en/follow-the-government/speeches-statements/last-speeches-and-statements/RSS"},
    {"source": "gov_argentina_presidencia", "feed_url": "https://www.argentina.gob.ar/noticias/rss"},
    {"source": "gov_chile_presidencia", "feed_url": "https://www.gob.cl/en/news/feed/"},
    {"source": "gov_colombia_presidencia", "feed_url": "https://idm.presidencia.gov.co/prensa/Paginas/rss.aspx"},
    {"source": "gov_mexico_presidencia", "feed_url": "https://www.gob.mx/rss/presidencia"},
    {"source": "gov_peru_pcm", "feed_url": "https://www.gob.pe/rss"},
    # Asia
    {"source": "gov_japan_kantei", "feed_url": "https://japan.kantei.go.jp/rss/news.rdf"},
    {"source": "gov_japan_mof", "feed_url": "https://www.mof.go.jp/english/rss/index.rdf"},
    {"source": "gov_india_mea", "feed_url": "https://www.mea.gov.in/rss.xml"},
    {"source": "gov_singapore_mfa", "feed_url": "https://www.mfa.gov.sg/newsroom/press-statements-transcripts-and-photos/rss.xml"},
    {"source": "gov_south_korea_yonhap", "feed_url": "https://en.yna.co.kr/RSS/national.xml"},
    {"source": "gov_indonesia_kemlu", "feed_url": "https://kemlu.go.id/portal/en/rss"},
    {"source": "gov_malaysia_pmo", "feed_url": "https://www.pmo.gov.my/rss.xml"},
    {"source": "gov_philippines_dfa", "feed_url": "https://www.dfa.gov.ph/rss"},
    {"source": "gov_thailand_mfa", "feed_url": "https://www.mfa.go.th/en/rss.xml"},
    {"source": "gov_vietnam_mofa", "feed_url": "https://www.mofa.gov.vn/en/rss"},
    # Eurasia & Russia
    {"source": "gov_russia_kremlin", "feed_url": "https://www.kremlin.ru/rss/news"},
    {"source": "gov_kazakhstan_pm", "feed_url": "https://primeminister.kz/en/rss"},
    {"source": "gov_uzbekistan_mfa", "feed_url": "https://mfa.uz/en/press/rss"},
    # Africa
    {"source": "gov_south_africa", "feed_url": "https://www.gov.za/rss/news"},
    {"source": "gov_nigeria_fmino", "feed_url": "https://fmino.gov.ng/feed/"},
    {"source": "gov_kenya_president", "feed_url": "https://www.president.go.ke/rss"},
    {"source": "gov_egypt_sis", "feed_url": "https://www.sis.gov.eg/Story/Feed.aspx"},
    {"source": "gov_ethiopia_pmo", "feed_url": "https://www.pmo.gov.et/feed/"},
    {"source": "gov_ghana_presidency", "feed_url": "https://presidency.gov.gh/rss"},
    {"source": "gov_tanzania_presidency", "feed_url": "https://www.president.go.tz/rss"},
    {"source": "gov_morocco_map", "feed_url": "https://www.diplomatie.ma/en/rss.xml"},
    {"source": "gov_senegal_presidency", "feed_url": "https://www.presidence.sn/en/rss"},
    {"source": "gov_au_commission", "feed_url": "https://au.int/en/rss/pressreleases"},
    # Oceania & Australia
    {"source": "gov_australia_pm", "feed_url": "https://www.pm.gov.au/media/feed"},
    {"source": "gov_australia_rba", "feed_url": "https://www.rba.gov.au/rss/rss-cb-media-releases.xml"},
    {"source": "gov_new_zealand_beehive", "feed_url": "https://www.beehive.govt.nz/rss.xml"},
    {"source": "amnesty", "feed_url": "https://www.amnesty.org/en/latest/news/feed/"},
    {"source": "hrw", "feed_url": "https://www.hrw.org/rss/news"},
    {"source": "aljazeera", "feed_url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"source": "rudaw_english", "feed_url": "https://www.rudaw.net/english/rss"},
    {"source": "middle_east_eye", "feed_url": "https://www.middleeasteye.net/rss"},
    {"source": "dw_world", "feed_url": "https://rss.dw.com/rdf/rss-en-world"},
    {"source": "abc_news", "feed_url": "https://feeds.abcnews.com/abcnews/internationalheadlines"},
    {"source": "cnn", "feed_url": "https://rss.cnn.com/rss/edition_world.rss"},
    {"source": "nbc", "feed_url": "https://link.nbcnews.com/rss.xml"},
    {"source": "sky_news", "feed_url": "https://feeds.skynews.com/feeds/rss/world.xml"},
    {"source": "irrawaddy_myanmar", "feed_url": "https://www.irrawaddy.com/feed"},
    {"source": "reuters", "feed_url": "https://reutersbest.com/feed/"},
    {"source": "wsj", "feed_url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml"},
    {"source": "washingtonpost", "feed_url": "https://feeds.washingtonpost.com/rss/world"},
    {"source": "nyt", "feed_url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"},
    {"source": "axios", "feed_url": "https://www.axios.com/feeds/feed.rss"},
    # Think tanks – politics / geopolitics (Geopolitics map)
    {"source": "carnegie", "feed_url": "https://carnegieendowment.org/rss.xml"},
    {"source": "aei", "feed_url": "https://www.aei.org/feed/"},
    {"source": "hudson", "feed_url": "https://www.hudson.org/feed"},
    # Substack – Jamestown Foundation, Ukraine–Russia war analysts, similar
    {"source": "substack_jamestown", "feed_url": "https://jamestown.substack.com/feed"},
    {"source": "substack_rochan", "feed_url": "https://rochanconsulting.substack.com/feed"},
    {"source": "substack_counteroffensive", "feed_url": "https://counteroffensive.substack.com/feed"},
    {"source": "substack_warwickpowell", "feed_url": "https://warwickpowell.substack.com/feed"},
    {"source": "substack_professorbonk", "feed_url": "https://professorbonk.substack.com/feed"},
    # Sports (Sports map)
    {"source": "espn_news", "feed_url": "https://www.espn.com/espn/rss/news"},
    {"source": "espn_nfl", "feed_url": "https://www.espn.com/espn/rss/nfl/news"},
    {"source": "espn_nba", "feed_url": "https://www.espn.com/espn/rss/nba/news"},
    {"source": "espn_mlb", "feed_url": "https://www.espn.com/espn/rss/mlb/news"},
    {"source": "espn_nhl", "feed_url": "https://www.espn.com/espn/rss/nhl/news"},
    {"source": "espn_soccer", "feed_url": "https://www.espn.com/espn/rss/soccer/news"},
    {"source": "espn_ncf", "feed_url": "https://www.espn.com/espn/rss/ncf/news"},
    {"source": "espn_ncb", "feed_url": "https://www.espn.com/espn/rss/ncb/news"},
    {"source": "espn_ncaa", "feed_url": "https://www.espn.com/espn/rss/ncaa/news"},
    {"source": "espn_tennis", "feed_url": "https://www.espn.com/espn/rss/tennis/news"},
    # Additional sports (Sports map)
    {"source": "on3", "feed_url": "https://www.on3.com/feed/"},
    {"source": "nbcsports", "feed_url": "https://www.nbcsports.com/feed/"},
    {"source": "the_athletic", "feed_url": "https://theathletic.com/rss-feed/"},
]
MAX_STORIES_PER_FEED = 200


def _normalize_rss_entry(source: str, entry: Any) -> dict[str, Any]:
    """Convert an RSS entry into the app's normalized story shape."""
    published = (
        str(entry.get("published", "")).strip()
        or str(entry.get("updated", "")).strip()
        or str(entry.get("pubDate", "")).strip()
    )
    summary = (
        str(entry.get("summary", "")).strip()
        or str(entry.get("description", "")).strip()
    )
    return {
        "source": source,
        "title": str(entry.get("title", "")).strip(),
        "url": str(entry.get("link", "")).strip(),
        "summary": summary,
        "published_at": published,
    }


def fetch_world_feed(source: str, feed_url: str) -> list[dict[str, Any]]:
    """Fetch one RSS feed and normalize all entries."""
    parsed = feedparser.parse(feed_url)
    stories: list[dict[str, Any]] = []
    for entry in parsed.entries[:MAX_STORIES_PER_FEED]:
        stories.append(_normalize_rss_entry(source, entry))
    return stories


def fetch_all_world_sources() -> list[dict[str, Any]]:
    """Fetch all configured world news RSS feeds. Skips feeds that fail to load."""
    stories: list[dict[str, Any]] = []
    for cfg in WORLD_FEEDS:
        try:
            stories.extend(fetch_world_feed(cfg["source"], cfg["feed_url"]))
        except Exception as e:
            log.warning("Skipping feed %s (%s): %s", cfg["source"], cfg["feed_url"], e)
    return stories

