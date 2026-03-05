"""
AI chatbot for the map: answers questions using ingested articles and think-tank data.
Aligns with the analytical perspective of WSJ, The Economist, Hudson Institute, AEI, The Dispatch.
Supports OpenAI (OPENAI_API_KEY) or Groq free tier (GROQ_API_KEY) automatically.
"""
from __future__ import annotations
import logging
import os
from typing import Any

log = logging.getLogger(__name__)

# --- API key resolution ---
# Priority: OPENAI_API_KEY > GROQ_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

# Resolve which key and base URL to use
if OPENAI_API_KEY:
    _ACTIVE_KEY = OPENAI_API_KEY
    _ACTIVE_BASE_URL = OPENAI_BASE_URL or None
    _DEFAULT_MODEL = "gpt-4o-mini"
elif GROQ_API_KEY:
    _ACTIVE_KEY = GROQ_API_KEY
    _ACTIVE_BASE_URL = "https://api.groq.com/openai/v1"
    _DEFAULT_MODEL = "llama-3.3-70b-versatile"
else:
    _ACTIVE_KEY = ""
    _ACTIVE_BASE_URL = None
    _DEFAULT_MODEL = "gpt-4o-mini"

CHAT_MODEL = os.getenv("CHAT_MODEL", os.getenv("SUMMARY_MODEL", _DEFAULT_MODEL)).strip()

# Preferred sources for context and alignment (include more of these in context).
PREFERRED_SOURCES = frozenset({
    "wsj", "economist", "economist_asia", "economist_mea", "economist_graphic_detail",
    "economist_podcast",
    "hudson", "aei", "dispatch",
    "x_hudson", "x_carnegie",
})

SYSTEM_PROMPT = """
You are PVD, a confident geopolitics, sports, economics, and history wizard answering questions about the world using the map's data.

IDENTITY AND VOICE
- You speak in a clear, self-assured voice, as if you are giving your own expert opinion.
- You are comfortable taking a stance and explaining "what it really means," not just listing facts.
- If asked who you are, say you are PVD, a map-based analyst focused on geopolitics, sports, economics, and history.

DATA CONSTRAINTS
- You MUST ground your answers in the "Recent reporting and data" provided in the prompt.
- When a Country reference is provided, use it to answer questions about specific countries (capital, population, government, etc.), including when there are no recent articles for that country; do not say "there is no information" for a country that appears in the Country reference.
- Do not invent events or facts that are not supported by the provided data.
- When you refer to a specific claim, connect it implicitly or explicitly to the sources in the context (e.g., "reporting from the Economist," "analysis from Hudson," "a Guardian report on X," etc.).

PERSPECTIVE AND STYLE
- Your worldview aligns with outlets like the Wall Street Journal, The Economist, the Hudson Institute, the American Enterprise Institute, and The Dispatch:
  - fact-based and evidence-driven,
  - supportive of free markets and strong institutions,
  - skeptical of government overreach and authoritarian regimes,
  - attentive to geopolitical, economic, and security risks.
- You synthesize the sources and then speak in your own integrated voice:
  - Do NOT just quote; explain what it adds up to.
  - Offer concise, strong takes when appropriate ("This is ultimately about…", "The core risk is…").
- You are allowed to say "in my view" or "I'd put it this way" but remember that your views must still be grounded in the provided reporting and analysis.

TASK BEHAVIOR
- Use only the provided "Recent reporting and data" (and Country reference when present) as factual input.
- If the user asks about a specific country, region, team, or topic, focus your answer tightly on that.
- For sports questions, blend context (league, history, geopolitics if relevant) with the data you have.
- For economics and history questions, connect present events to historical patterns and structural forces where the data supports it.
- Be concise but substantive: aim for a few strong paragraphs, not one sentence, and not a long essay.
- If the data is thin or missing on a specific sub-question, say so briefly, then pivot to what you CAN say confidently based on the available sources.

OUTPUT FORMAT
- Answer in plain text paragraphs (no markdown unless the caller explicitly asks for formatting).
- Do not show the raw "Recent reporting and data" block back to the user; instead, summarize and interpret it.
"""


def _client():
    """Return OpenAI-compatible client or None if not configured."""
    if not _ACTIVE_KEY:
        return None
    try:
        import openai
    except ImportError:
        return None
    kwargs: dict[str, Any] = {"api_key": _ACTIVE_KEY}
    if _ACTIVE_BASE_URL:
        kwargs["base_url"] = _ACTIVE_BASE_URL
    return openai.OpenAI(**kwargs)


def _prioritize_stories_for_chat(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Put preferred sources (WSJ, Economist, Hudson, AEI, Dispatch) first, then by date."""
    def key(s: dict[str, Any]) -> tuple[int, str]:
        src = (s.get("source") or "").strip().lower()
        preferred = 0 if src in PREFERRED_SOURCES else 1
        pub = (s.get("published_at") or "")[:20]
        return (preferred, pub)
    return sorted(stories, key=key)


def _build_context_from_stories(stories: list[dict[str, Any]], max_chars: int = 28000) -> str:
    """Turn a list of story dicts (source, title, summary, country, published_at) into a text block for the LLM."""
    lines: list[str] = []
    total = 0
    for s in stories:
        source = (s.get("source") or "").strip()
        title = (s.get("title") or "").strip()
        summary = (s.get("summary") or "").strip()[:800]
        country = (s.get("country") or "").strip()
        pub = (s.get("published_at") or "").strip()
        block = f"[{source}]"
        if country:
            block += f" ({country})"
        if pub:
            block += f" {pub}"
        block += f"\n  {title}\n  {summary}\n"
        if total + len(block) > max_chars:
            break
        lines.append(block)
        total += len(block)
    return "\n".join(lines) if lines else "(No recent articles in the database.)"


def _build_country_baseline_text(country_baseline: list[dict[str, Any]], max_chars: int = 18000) -> str:
    """Format baseline facts for every country so the bot can answer questions about any country."""
    lines: list[str] = []
    total = 0
    for row in country_baseline:
        name = (row.get("country_name") or "").strip()
        if not name:
            continue
        parts = [name]
        capital = (row.get("capital") or "").strip()
        if capital:
            parts.append(f"capital {capital}")
        pop = (row.get("population") or "").strip()
        if pop:
            parts.append(f"population {pop}")
        gov = (row.get("government_type") or "").strip()
        if gov:
            parts.append(f"government {gov[:60]}")
        gdp = (row.get("gdp_ppp") or "").strip()
        if gdp:
            parts.append(f"GDP (PPP) {gdp[:50]}")
        line = ": " + ", ".join(parts[1:]) if len(parts) > 1 else ""
        line = parts[0] + line + "\n"
        if total + len(line) > max_chars:
            break
        lines.append(line)
        total += len(line)
    if not lines:
        return ""
    return "Country reference (every country below has embedded facts; use this when the user asks about a country, including when there are no recent articles for it):\n" + "".join(lines)


def chat(
    user_message: str,
    stories: list[dict[str, Any]],
    map_key: str | None = None,
    country: str | None = None,
    country_baseline: list[dict[str, Any]] | None = None,
) -> str | None:
    """
    Reply to the user using the given stories as context. Returns the assistant reply or None if API unavailable.
    country_baseline: optional list of per-country facts (from get_all_countries_baseline) so every country has embedded info.
    """
    if not (user_message or "").strip():
        return None
    client = _client()
    if not client:
        return None
    prioritized = _prioritize_stories_for_chat(stories)
    context = _build_context_from_stories(prioritized)
    baseline_block = ""
    if country_baseline:
        baseline_block = _build_country_baseline_text(country_baseline)
    map_note = ""
    if map_key:
        map_note = f"\nCurrent map view: {map_key}."
    if country:
        map_note += f" User may be interested in: {country}."
    user_content = ""
    if baseline_block:
        user_content = baseline_block + "\n\n"
    user_content += f"Recent reporting and data from the map:\n\n{context}\n\n---\nUser question:{map_note}\n\n{user_message.strip()}"
    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=1200,
            temperature=0.4,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else None
    except Exception as e:
        log.warning("Chat API call failed: %s", e)
        return None
