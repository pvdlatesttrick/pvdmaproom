"""
Canonical topic labels, definitions, and priority for map views.
When a story matches multiple topics, it is assigned to the first in TOPIC_PRIORITY.
"""

TOPIC_LABELS = ["economics", "geopolitics", "conflicts", "sports"]

TOPIC_DEFINITIONS = {
    "economics": "Macroeconomy, inflation, trade flows, markets, industry, business deals, economic policy that primarily affects money, jobs, trade, or growth.",
    "geopolitics": "Diplomacy, alliances, great-power competition, elections, foreign policy, international institutions, sanctions as tools of statecraft.",
    "conflicts": "Wars, military operations, armed clashes, terrorism, ceasefires, troop movements, frontlines.",
    "sports": "Professional or national sports, leagues, competitions, tournaments, transfers, game results.",
}

# If a story matches multiple topics, pick the first in this list.
TOPIC_PRIORITY = ["conflicts", "geopolitics", "economics", "sports"]
