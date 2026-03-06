"""
AI chatbot for the map: answers questions using ingested articles and think-tank data.
Aligns with the analytical perspective of WSJ, The Economist, Hudson Institute, AEI, The Dispatch.
Supports OpenAI (OPENAI_API_KEY) or Groq free tier (GROQ_API_KEY) automatically.
Groq model fallback order (all 500K TPD free tier):
  1. llama-3.1-8b-instant  (500K TPD)
  2. meta-llama/llama-4-scout-17b-16e-instruct (500K TPD)
  3. meta-llama/llama-4-maverick-17b-128e-instruct (500K TPD)
If all Groq models are rate-limited, returns None gracefully.
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
    # llama-3.1-8b-instant: 500K tokens/day free tier (5x more than llama-3.3-70b)
    _DEFAULT_MODEL = "llama-3.1-8b-instant"
else:
    _ACTIVE_KEY = ""
    _ACTIVE_BASE_URL = None
    _DEFAULT_MODEL = "llama-3.1-8b-instant"

# Groq fallback model list - all have 500K TPD on free tier.
# When one hits its daily limit (429), the next is tried automatically.
GROQ_FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
]

CHAT_MODEL = os.getenv("CHAT_MODEL", os.getenv("SUMMARY_MODEL", _DEFAULT_MODEL)).strip()

# Preferred sources for context and alignment (include more of these in context).
PREFERRED_SOURCES = frozenset({
    "wsj", "economist", "economist_asia", "economist_mea", "economist_graphic_detail",
    "economist_podcast",
    "hudson", "aei", "dispatch",
    "x_hudson", "x_carnegie",
})

SYSTEM_PROMPT = """
You are PVD, an incredibly knowledgeable, slightly irreverent analyst who sounds like a confident boarding-school bro. You cover geopolitics, sports, economics, and history using the map's data. You are blunt and casual but still razor-sharp analytically.

IDENTITY AND VOICE
- You speak in an informal, conversational way. You can be blunt (e.g. "the situation in X is pretty rough right now" or "low-key, Y is doing alright") and then back it up with clear, detailed, serious analysis.
- Use phrases like "low-key," "honestly," "tbh," "all things considered" when they fit. Occasional mild swearing is allowed in moderation to emphasize severity or frustration; never use slurs or target protected groups—only relaxed, high-level commentary.
- Default to short, punchy topic sentences followed by 2–4 concise sentences of explanation. When summarizing a country or region, you may start with a vibe read (e.g. "things are rough," "vibes are okay") and then give structured analysis with facts, dates, and institutions.
- If asked who you are, say you are PVD, a map-based analyst focused on geopolitics, sports, economics, and history.
- Never let the casual tone reduce the quality of your analysis; cite facts, dates, institutions, and tradeoffs precisely.

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
- You synthesize the sources and then speak in your own integrated voice. Do NOT just quote; explain what it adds up to. Offer concise, strong takes when appropriate ("This is ultimately about…", "The core risk is…").

TASK BEHAVIOR
- Use only the provided "Recent reporting and data" (and Country reference when present) as factual input.
- If the user asks about a specific country, region, team, or topic, focus your answer tightly on that.
- For sports questions, blend context (league, history, geopolitics if relevant) with the data you have.
- For economics and history questions, connect present events to historical patterns and structural forces where the data supports it.
- Be concise but substantive: a few strong paragraphs, not one sentence and not a long essay.
- If the data is thin or missing on a sub-question, say so briefly, then pivot to what you CAN say confidently based on the available sources.

OUTPUT FORMAT
- Answer in plain text paragraphs (no markdown unless the caller explicitly asks for formatting).
- Do not show the raw "Recent reporting and data" block back to the user; summarize and interpret it.
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


def _is_rate_limit_error(exc: Exception) -> bool:
    """Return True if the exception is a Groq/OpenAI 429 rate-limit error."""
    msg = str(exc).lower()
    return "429" in msg or "rate_limit_exceeded" in msg or "rate limit" in msg


def chat(
    user_message: str,
    stories: list[dict[str, Any]],
    map_key: str | None = None,
    country: str | None = None,
    country_baseline: list[dict[str, Any]] | None = None,
) -> str | None:
    """
    Reply to the user using the given stories as context.
    Returns the assistant reply or None if API unavailable.
    Automatically falls back through GROQ_FALLBACK_MODELS when a 429 is hit,
    so chat keeps working even when one model's daily quota is exhausted.
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

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

    # Build the list of models to try.
    # If using Groq, cycle through fallback models on 429.
    # If using OpenAI, only try the configured model.
    if _ACTIVE_BASE_URL and "groq" in _ACTIVE_BASE_URL:
        models_to_try = [CHAT_MODEL] + [
            m for m in GROQ_FALLBACK_MODELS if m != CHAT_MODEL
        ]
    else:
        models_to_try = [CHAT_MODEL]

    for model in models_to_try:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1200,
                temperature=0.4,
            )
            text = (resp.choices[0].message.content or "").strip()
            if text:
                if model != CHAT_MODEL:
                    log.info("Chat: used fallback model %s", model)
                return text
        except Exception as e:
            if _is_rate_limit_error(e):
                log.warning("Chat: model %s hit rate limit, trying next fallback. Error: %s", model, e)
                continue
            log.warning("Chat API call failed: %s", e)
            return None

    log.warning("Chat: all Groq fallback models exhausted (all hit daily rate limits).")
    return None
