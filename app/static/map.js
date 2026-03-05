const SOURCE_META = {
  bbc: { name: "BBC", logo: "https://cdn.simpleicons.org/bbc/FFFFFF" },
  bbc_asia: { name: "BBC Asia", logo: "https://cdn.simpleicons.org/bbc/FFFFFF" },
  bbc_africa: { name: "BBC Africa", logo: "https://cdn.simpleicons.org/bbc/FFFFFF" },
  bbc_middle_east: { name: "BBC Middle East", logo: "https://cdn.simpleicons.org/bbc/FFFFFF" },
  economist: { name: "The Economist", logo: "/static/logos/economist.png", logoFallback: "https://cdn.simpleicons.org/theeconomist/E3120B" },
  economist_asia: { name: "The Economist Asia", logo: "/static/logos/economist.png", logoFallback: "https://cdn.simpleicons.org/theeconomist/E3120B" },
  economist_mea: { name: "The Economist MEA", logo: "/static/logos/economist.png", logoFallback: "https://cdn.simpleicons.org/theeconomist/E3120B" },
  economist_graphic_detail: { name: "The Economist Graphic detail", logo: "/static/logos/economist.png", logoFallback: "https://cdn.simpleicons.org/theeconomist/E3120B" },
  economist_podcast: { name: "The Economist Podcast (The Intelligence)", logo: "/static/logos/economist.png", logoFallback: "https://cdn.simpleicons.org/theeconomist/E3120B" },
  guardian_world: { name: "The Guardian", logo: "https://cdn.simpleicons.org/theguardian/FFFFFF" },
  guardian_international: { name: "The Guardian International", logo: "https://cdn.simpleicons.org/theguardian/FFFFFF" },
  dispatch: { name: "The Dispatch", logo: "https://logo.clearbit.com/thedispatch.com" },
  politico: { name: "Politico", logo: "https://cdn.simpleicons.org/politico/FFFFFF" },
  gov_us_dod_releases: { name: "US DoD Releases", logo: "https://logo.clearbit.com/defense.gov" },
  gov_us_dod_contracts: { name: "US DoD Contracts", logo: "https://logo.clearbit.com/defense.gov" },
  gov_eu_commission: { name: "EU Commission Press", logo: "https://logo.clearbit.com/europa.eu" },
  gov_uk_announcements: { name: "UK Gov", logo: "https://logo.clearbit.com/gov.uk" },
  gov_canada_news: { name: "Canada News", logo: "https://logo.clearbit.com/canada.ca" },
  gov_canada_pm: { name: "Canada PM", logo: "https://logo.clearbit.com/pm.gc.ca" },
  gov_canada_global_affairs: { name: "Canada Global Affairs", logo: "https://logo.clearbit.com/international.gc.ca" },
  gov_brazil_planalto: { name: "Brazil Presidency", logo: "https://logo.clearbit.com/gov.br" },
  gov_argentina_presidencia: { name: "Argentina Govt", logo: "https://logo.clearbit.com/argentina.gob.ar" },
  gov_chile_presidencia: { name: "Chile Govt", logo: "https://logo.clearbit.com/gob.cl" },
  gov_colombia_presidencia: { name: "Colombia Presidency", logo: "https://logo.clearbit.com/presidencia.gov.co" },
  gov_mexico_presidencia: { name: "Mexico Govt", logo: "https://logo.clearbit.com/gob.mx" },
  gov_peru_pcm: { name: "Peru Govt", logo: "https://logo.clearbit.com/gob.pe" },
  gov_japan_kantei: { name: "Japan PM Office", logo: "https://logo.clearbit.com/kantei.go.jp" },
  gov_japan_mof: { name: "Japan Finance", logo: "https://logo.clearbit.com/mof.go.jp" },
  gov_india_mea: { name: "India MEA", logo: "https://logo.clearbit.com/mea.gov.in" },
  gov_singapore_mfa: { name: "Singapore MFA", logo: "https://logo.clearbit.com/mfa.gov.sg" },
  gov_south_korea_yonhap: { name: "South Korea (Yonhap)", logo: "https://logo.clearbit.com/yna.co.kr" },
  gov_indonesia_kemlu: { name: "Indonesia MFA", logo: "https://logo.clearbit.com/kemlu.go.id" },
  gov_malaysia_pmo: { name: "Malaysia PMO", logo: "https://logo.clearbit.com/pmo.gov.my" },
  gov_philippines_dfa: { name: "Philippines DFA", logo: "https://logo.clearbit.com/dfa.gov.ph" },
  gov_thailand_mfa: { name: "Thailand MFA", logo: "https://logo.clearbit.com/mfa.go.th" },
  gov_vietnam_mofa: { name: "Vietnam MFA", logo: "https://logo.clearbit.com/mofa.gov.vn" },
  gov_russia_kremlin: { name: "Russia Kremlin", logo: "https://logo.clearbit.com/kremlin.ru" },
  gov_kazakhstan_pm: { name: "Kazakhstan PM", logo: "https://logo.clearbit.com/primeminister.kz" },
  gov_uzbekistan_mfa: { name: "Uzbekistan MFA", logo: "https://logo.clearbit.com/mfa.uz" },
  gov_south_africa: { name: "South Africa Govt", logo: "https://logo.clearbit.com/gov.za" },
  gov_nigeria_fmino: { name: "Nigeria Govt", logo: "https://logo.clearbit.com/fmino.gov.ng" },
  gov_kenya_president: { name: "Kenya Presidency", logo: "https://logo.clearbit.com/president.go.ke" },
  gov_egypt_sis: { name: "Egypt SIS", logo: "https://logo.clearbit.com/sis.gov.eg" },
  gov_ethiopia_pmo: { name: "Ethiopia PMO", logo: "https://logo.clearbit.com/pmo.gov.et" },
  gov_ghana_presidency: { name: "Ghana Presidency", logo: "https://logo.clearbit.com/presidency.gov.gh" },
  gov_tanzania_presidency: { name: "Tanzania Presidency", logo: "https://logo.clearbit.com/president.go.tz" },
  gov_morocco_map: { name: "Morocco MFA", logo: "https://logo.clearbit.com/diplomatie.ma" },
  gov_senegal_presidency: { name: "Senegal Presidency", logo: "https://logo.clearbit.com/presidence.sn" },
  gov_au_commission: { name: "African Union", logo: "https://logo.clearbit.com/au.int" },
  gov_australia_pm: { name: "Australia PM", logo: "https://logo.clearbit.com/pm.gov.au" },
  gov_australia_rba: { name: "Australia RBA", logo: "https://logo.clearbit.com/rba.gov.au" },
  gov_new_zealand_beehive: { name: "NZ Govt", logo: "https://logo.clearbit.com/beehive.govt.nz" },
  amnesty: { name: "Amnesty International", logo: "https://logo.clearbit.com/amnesty.org" },
  hrw: { name: "Human Rights Watch", logo: "https://logo.clearbit.com/hrw.org" },
  aljazeera: { name: "Al Jazeera", logo: "https://cdn.simpleicons.org/aljazeera/CEA90D" },
  rudaw_english: { name: "Rudaw English", logo: "https://logo.clearbit.com/rudaw.net" },
  middle_east_eye: { name: "Middle East Eye", logo: "https://logo.clearbit.com/middleeasteye.net" },
  dw_world: { name: "DW World", logo: "https://cdn.simpleicons.org/deutschewelle/FFFFFF" },
  abc_news: { name: "ABC News", logo: "https://cdn.simpleicons.org/abcnews/FFFFFF" },
  cnn: { name: "CNN", logo: "https://cdn.simpleicons.org/cnn/CC0000" },
  nbc: { name: "NBC News", logo: "https://cdn.simpleicons.org/nbc/F37021" },
  sky_news: { name: "Sky News", logo: "https://cdn.simpleicons.org/sky/0072C6" },
  irrawaddy_myanmar: { name: "The Irrawaddy (Myanmar)", logo: "https://logo.clearbit.com/irrawaddy.com" },
  reuters: { name: "Reuters", logo: "https://cdn.simpleicons.org/reuters/FF8000" },
  wsj: { name: "Wall Street Journal", logo: "https://cdn.simpleicons.org/thewallstreetjournal/FFFFFF" },
  washingtonpost: { name: "Washington Post", logo: "/static/logos/washingtonpost.png", logoFallback: "https://cdn.simpleicons.org/washingtonpost/FFFFFF" },
  nyt: { name: "New York Times", logo: "/static/logos/nyt.png", logoFallback: "https://cdn.simpleicons.org/nytimes/000000" },
  axios: { name: "Axios", logo: "https://cdn.simpleicons.org/axios/FFFFFF" },
  espn_news: { name: "ESPN", logo: "https://cdn.simpleicons.org/espn/FF0033" },
  espn_nfl: { name: "ESPN NFL", logo: "https://cdn.simpleicons.org/nfl/013369" },
  espn_nba: { name: "ESPN NBA", logo: "https://cdn.simpleicons.org/nba/174B8A" },
  espn_mlb: { name: "ESPN MLB", logo: "https://cdn.simpleicons.org/mlb/041E42" },
  espn_nhl: { name: "ESPN NHL", logo: "https://cdn.simpleicons.org/nhl/000000" },
  espn_soccer: { name: "ESPN Soccer", logo: "https://cdn.simpleicons.org/espn/FF0033" },
  espn_ncf: { name: "ESPN College Football", logo: "https://cdn.simpleicons.org/ncaa/CC0000" },
  espn_ncb: { name: "ESPN College Basketball", logo: "https://cdn.simpleicons.org/ncaa/CC0000" },
  espn_ncaa: { name: "ESPN NCAA", logo: "https://cdn.simpleicons.org/ncaa/CC0000" },
  espn_tennis: { name: "ESPN Tennis", logo: "https://cdn.simpleicons.org/espn/FF0033" },
  on3: { name: "On3", logo: "https://logo.clearbit.com/on3.com" },
  nbcsports: { name: "NBC Sports", logo: "https://cdn.simpleicons.org/nbcsports/FFFFFF" },
  the_athletic: { name: "The Athletic", logo: "https://logo.clearbit.com/theathletic.com" },
  bbc_sport: { name: "BBC Sport", logo: "https://cdn.simpleicons.org/bbc/FFFFFF" },
  sky_sports_football: { name: "Sky Sports Football", logo: "https://cdn.simpleicons.org/sky/0072C6" },
  guardian_football: { name: "The Guardian Football", logo: "https://cdn.simpleicons.org/theguardian/FFFFFF" }
};
SOURCE_META.x_reutersworld = { name: "X @ReutersWorld", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_bbcbreaking = { name: "X @BBCBreaking", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_ap = { name: "X @AP", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_un = { name: "X @UN", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_africacenter = { name: "X @AfricaCDC", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_thetimes = { name: "X @thetimes", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_politico = { name: "X @politico", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_janesintel = { name: "X @JanesINTEL", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_rand = { name: "X @RANDCorporation", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_amnesty = { name: "X @amnesty", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_isw = { name: "X @ISW", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_liveuamap = { name: "X @Liveuamap", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_carnegie = { name: "X @Carnegie", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_hudson = { name: "X @Hudson", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_barakravid = { name: "Barak Ravid (Axios)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_clarissaward = { name: "Clarissa Ward (CNN)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_richardengel = { name: "Richard Engel (NBC)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_lynsaddler = { name: "X @lynsaddler (BBC)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_nickpatonwalsh = { name: "Nick Paton Walsh (CNN)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_borzsandor = { name: "Borzsándor (Reuters)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_ianbremmer = { name: "Ian Bremmer", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_rudaw = { name: "Rudaw (X)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_middleeasteye = { name: "Middle East Eye (X)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.x_kurdistan24 = { name: "Kurdistan 24 (X)", logo: "https://cdn.simpleicons.org/x/FFFFFF" };
SOURCE_META.carnegie = { name: "Carnegie Endowment", logo: "https://logo.clearbit.com/carnegieendowment.org" };
SOURCE_META.aei = { name: "American Enterprise Institute", logo: "https://logo.clearbit.com/aei.org" };
SOURCE_META.hudson = { name: "Hudson Institute", logo: "https://logo.clearbit.com/hudson.org" };
SOURCE_META.substack_jamestown = { name: "Jamestown Foundation", logo: "https://logo.clearbit.com/jamestown.org" };
SOURCE_META.substack_rochan = { name: "Ukraine Conflict Monitor", logo: "https://logo.clearbit.com/rochanconsulting.com" };
SOURCE_META.substack_counteroffensive = { name: "The Counteroffensive", logo: "https://logo.clearbit.com/counteroffensive.substack.com" };
SOURCE_META.substack_warwickpowell = { name: "Warwick Powell (Substack)", logo: "https://cdn.simpleicons.org/substack/FF6719" };
SOURCE_META.substack_professorbonk = { name: "Professor Bonk (Substack)", logo: "https://cdn.simpleicons.org/substack/FF6719" };
SOURCE_META.wikipedia_historical = { name: "Wikipedia (historical)", logo: "https://cdn.simpleicons.org/wikipedia/FFFFFF" };

// Logo-only map pins: per-source Leaflet icons (no generic teardrop). Keys match story.source.
const ICON_SIZE = [30, 30];
const ICON_ANCHOR = [15, 30];
const POPUP_ANCHOR = [0, -26];
const sourceIcons = {};
Object.keys(SOURCE_META).forEach((key) => {
  const meta = SOURCE_META[key];
  const logoUrl = meta.logo || meta.logoFallback || "/static/icons/default-news.svg";
  sourceIcons[key] = L.icon({
    iconUrl: logoUrl,
    iconSize: ICON_SIZE,
    iconAnchor: ICON_ANCHOR,
    popupAnchor: POPUP_ANCHOR,
  });
});
const defaultSourceIcon = L.icon({
  iconUrl: "/static/icons/default-news.svg",
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -24],
});

const GHOST_WAR_ICON_SVG = "data:image/svg+xml," + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="%23444" d="M12 2c-4 0-7 3-7 7v2c-2 0-4 2-4 4v6h4v-2h2v2h2v-2h2v2h2v-2h4v-6c0-2-2-4-4-4V9c0-4-3-7-7-7z"/><circle cx="9" cy="10" r="1.5" fill="%23fff"/><circle cx="15" cy="10" r="1.5" fill="%23fff"/></svg>'
);
const TOPIC_META = {
  conflict: { label: "Conflict", icon: "⚔️" },
  ghost_war: { label: "Ghost war", icon: "<img src=\"" + GHOST_WAR_ICON_SVG + "\" class=\"topic-icon-img\" alt=\"Ghost war\" width=\"14\" height=\"14\"/>", iconEmoji: "👻" },
  politics: { label: "Politics", icon: "🏛️" },
  business: { label: "Business", icon: "💼" },
  economy: { label: "Economy", icon: "📈" },
  tech: { label: "Tech", icon: "💻" },
  health: { label: "Health", icon: "🩺" },
  climate: { label: "Climate", icon: "🌍" },
  disaster: { label: "Disaster", icon: "🌪️" },
  crime: { label: "Crime", icon: "🚨" },
  other: { label: "General", icon: "📰" }
};
const MAP_DEFS = {
  economics: { mapId: "map-economics", title: "Economics Map" },
  geopolitics: { mapId: "map-geopolitics", title: "Geopolitics Map" },
  conflicts: { mapId: "map-conflicts", title: "Conflicts Map" },
  sports: { mapId: "map-sports", title: "Sports Map" }
};

const TOPIC_LABELS = ["economics", "geopolitics", "conflicts", "sports"];
const TOPIC_DEFINITIONS = {
  economics: "Macroeconomy, inflation, trade flows, markets, industry, business deals, economic policy that primarily affects money, jobs, trade, or growth.",
  geopolitics: "Diplomacy, alliances, great-power competition, elections, foreign policy, international institutions, sanctions as tools of statecraft.",
  conflicts: "Wars, military operations, armed clashes, terrorism, ceasefires, troop movements, frontlines.",
  sports: "Professional or national sports, leagues, competitions, tournaments, transfers, game results."
};
const TOPIC_PRIORITY = ["conflicts", "geopolitics", "economics", "sports"];
const SPORTS_LEAGUE_META = {
  nba: { name: "NBA", logo: "https://cdn.simpleicons.org/nba/174B8A" },
  nfl: { name: "NFL", logo: "https://cdn.simpleicons.org/nfl/013369" },
  nhl: { name: "NHL", logo: "https://cdn.simpleicons.org/nhl/000000" },
  mlb: { name: "MLB", logo: "https://cdn.simpleicons.org/mlb/041E42" },
  mls: { name: "MLS", logo: "https://logo.clearbit.com/mlssoccer.com" },
  ncaa_football: { name: "College Football", logo: "https://logo.clearbit.com/ncaa.com" },
  ncaa_basketball: { name: "College Basketball", logo: "https://logo.clearbit.com/ncaa.com" },
  ncaa_baseball: { name: "College Baseball", logo: "https://logo.clearbit.com/ncaa.com" },
  ncaa_tennis: { name: "College Tennis", logo: "https://logo.clearbit.com/ncaa.com" },
  ncaa_lacrosse: { name: "College Lacrosse", logo: "https://logo.clearbit.com/ncaa.com" },
  ncaa_soccer: { name: "College Soccer", logo: "https://logo.clearbit.com/ncaa.com" },
  euroleague: { name: "EuroLeague Basketball", logo: "https://logo.clearbit.com/euroleague.net" },
  fiba: { name: "FIBA", logo: "https://logo.clearbit.com/fiba.basketball" },
  uefa_champions_league: { name: "UEFA Champions League", logo: "https://logo.clearbit.com/uefa.com" },
  premier_league: { name: "Premier League", logo: "https://logo.clearbit.com/premierleague.com" },
  la_liga: { name: "La Liga", logo: "https://logo.clearbit.com/laliga.com" },
  bundesliga: { name: "Bundesliga", logo: "https://logo.clearbit.com/bundesliga.com" },
  serie_a: { name: "Serie A", logo: "https://logo.clearbit.com/legaseriea.it" },
  ligue_1: { name: "Ligue 1", logo: "https://logo.clearbit.com/ligue1.com" },
  liga_pr: { name: "Liga de Puerto Rico (BSN)", logo: "https://logo.clearbit.com/bsnpr.com" },
  cba: { name: "Chinese Basketball Association", logo: "https://logo.clearbit.com/cbaleague.com" },
  khl: { name: "KHL", logo: "https://logo.clearbit.com/khl.ru" },
  shl: { name: "SHL (Sweden)", logo: "https://logo.clearbit.com/shl.se" },
  ahl: { name: "AHL", logo: "https://logo.clearbit.com/theahl.com" },
  liiga: { name: "Liiga (Finland)", logo: "https://logo.clearbit.com/liiga.fi" },
  czech_extraliga: { name: "Czech Extraliga", logo: "https://logo.clearbit.com/hokej.cz" },
  sports: { name: "Sports", logo: "https://cdn.simpleicons.org/espn/FF0033" }
};

const TEAM_META = {
  "auburn-tigers-football": { name: "Auburn Tigers Football", logo: "/static/team-icons/auburn-tigers.png", sport: "football" },
  "auburn-tigers-basketball": { name: "Auburn Tigers Basketball", logo: "/static/team-icons/auburn-tigers.png", sport: "basketball" },
  "los-angeles-lakers": { name: "Los Angeles Lakers", logo: "/static/team-icons/la-lakers.png", sport: "basketball" },
  "boston-celtics": { name: "Boston Celtics", logo: "/static/team-icons/boston-celtics.png", sport: "basketball" },
  "new-york-yankees": { name: "New York Yankees", logo: "/static/team-icons/new-york-yankees.png", sport: "baseball" },
  "new-york-mets": { name: "New York Mets", logo: "/static/team-icons/new-york-mets.png", sport: "baseball" },
  "dallas-cowboys": { name: "Dallas Cowboys", logo: "/static/team-icons/dallas-cowboys.png", sport: "football" },
  "green-bay-packers": { name: "Green Bay Packers", logo: "/static/team-icons/green-bay-packers.png", sport: "football" },
  "chicago-bears": { name: "Chicago Bears", logo: "/static/team-icons/chicago-bears.png", sport: "football" },
  "boston-bruins": { name: "Boston Bruins", logo: "/static/team-icons/boston-bruins.png", sport: "hockey" },
  "toronto-maple-leafs": { name: "Toronto Maple Leafs", logo: "/static/team-icons/toronto-maple-leafs.png", sport: "hockey" },
  "manchester-united": { name: "Manchester United", logo: "/static/team-icons/manchester-united.png", sport: "soccer" },
  "real-madrid": { name: "Real Madrid", logo: "/static/team-icons/real-madrid.png", sport: "soccer" },
};
const SPORT_FALLBACK_META = {
  basketball: { name: "Basketball", logo: "/static/team-icons/generic-basketball.svg" },
  baseball: { name: "Baseball", logo: "/static/team-icons/generic-baseball.svg" },
  football: { name: "Football", logo: "/static/team-icons/generic-football.svg" },
  hockey: { name: "Hockey", logo: "/static/team-icons/generic-hockey.svg" },
  soccer: { name: "Soccer", logo: "/static/team-icons/generic-soccer.svg" },
};

const sportsLeagueIcons = {};
Object.keys(SPORTS_LEAGUE_META).forEach((key) => {
  const logoUrl = SPORTS_LEAGUE_META[key].logo || "/static/icons/default-news.svg";
  sportsLeagueIcons[key] = L.icon({
    iconUrl: logoUrl,
    iconSize: ICON_SIZE,
    iconAnchor: ICON_ANCHOR,
    popupAnchor: POPUP_ANCHOR,
  });
});
let activeMapKey = "economics";

function getActiveMapKey() {
  return typeof window.activeMapKey !== "undefined" ? window.activeMapKey : activeMapKey;
}

function setActiveMapKey(mapKey) {
  activeMapKey = mapKey;
  window.activeMapKey = mapKey;
}

/** Selected year for historical view; null = current/latest. Negative = BC (e.g. -1000 = 1000 BC). */
let selectedYear = null;
let worldCountryGeoJson = null;
const mapContexts = {};
/** Topic -> marker layer; populated after initMapContexts. Used by addStoryToMap. */
let layersByMapKey = {}; let allVisibleStories = []; let allCountryMajorEvents = {};

function truncate(text, maxLen = 240) {
  if (!text) return "";
  return text.length > maxLen ? `${text.slice(0, maxLen - 1)}…` : text;
}

function sourceMeta(sourceKey) {
  const key = String(sourceKey || "").toLowerCase();
  return SOURCE_META[key] || {
    name: key || "Unknown",
    logo: "https://logo.clearbit.com/news.google.com"
  };
}

function isEconomicsStory(story) {
  if ((story.source || "").toLowerCase() === "wikipedia_historical") return true;
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  return /(econom|finance|market|commodity|oil|gas|gold|copper|trade|tariff|inflation|interest rate|gdp|currency|bond|stocks?)/.test(text);
}

function isGeopoliticsStory(story) {
  const src = String(story.source || "").toLowerCase();
  if (src === "wikipedia_historical") return true;
  if (["carnegie", "aei", "hudson", "x_carnegie", "x_hudson", "substack_jamestown", "rudaw_english", "middle_east_eye", "x_rudaw", "x_middleeasteye", "x_kurdistan24"].includes(src)) return true;
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  return /(diplom|summit|treaty|election|parliament|president|prime minister|foreign minister|sanctions|united nations|asean|nato|geopolitic|border)/.test(text);
}

function isConflictStory(story) {
  const src = String(story.source || "").toLowerCase();
  if (src === "wikipedia_historical") return true;
  if (src === "x_isw" || src === "x_liveuamap") return true;
  if (["substack_rochan", "substack_counteroffensive", "substack_warwickpowell", "substack_professorbonk"].includes(src)) return true;
  if (["x_barakravid", "x_clarissaward", "x_richardengel", "x_lynsaddler", "x_nickpatonwalsh", "x_borzsandor", "x_ianbremmer", "x_rudaw", "x_middleeasteye", "x_kurdistan24"].includes(src)) return true;
  if (["rudaw_english", "middle_east_eye"].includes(src)) return true;
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  return /(war|conflict|civil war|separat|insurg|militia|cartel|organized crime|armed group|junta|ceasefire|offensive|airstrike|rebel)/.test(text);
}

const SPORTS_SOURCE_KEYS = new Set(["espn_news", "espn_nfl", "espn_nba", "espn_mlb", "espn_nhl", "espn_soccer", "espn_ncf", "espn_ncb", "espn_ncaa", "espn_tennis", "on3", "nbcsports", "the_athletic", "bbc_sport", "sky_sports_football"]);
function isSportsStory(story) {
  const src = String(story.source || "").toLowerCase();
  if (src === "wikipedia_historical") return true;
  return SPORTS_SOURCE_KEYS.has(src);
}

/** Canonical topic: use only story.topic (set at ingest). No client-side re-classification. */
function getStoryTopic(story) {
  return (story && (story.topic || "geopolitics")) || "geopolitics";
}

function getLeagueForStory(story) {
  const src = String(story.source || "").toLowerCase();
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  if (src === "espn_nfl") return "nfl";
  if (src === "espn_nba") return "nba";
  if (src === "espn_mlb") return "mlb";
  if (src === "espn_nhl") return "nhl";
  if (src === "espn_soccer") {
    if (/\b(champions league|uefa|premier league|la liga|bundesliga|serie a|ligue 1)\b/.test(text)) return "uefa_champions_league";
    return "mls";
  }
  if (src === "espn_ncf") return "ncaa_football";
  if (src === "espn_ncb") return "ncaa_basketball";
  if (src === "espn_ncaa") {
    if (/\b(football|ncf|sec|big ten)\b/.test(text)) return "ncaa_football";
    if (/\b(basketball|ncb|march madness)\b/.test(text)) return "ncaa_basketball";
    if (/\b(baseball|college world series)\b/.test(text)) return "ncaa_baseball";
    if (/\b(tennis|lacrosse|soccer)\b/.test(text)) return text.includes("tennis") ? "ncaa_tennis" : (text.includes("lacrosse") ? "ncaa_lacrosse" : "ncaa_soccer");
    return "ncaa_basketball";
  }
  if (src === "espn_tennis") return "ncaa_tennis";
  if (/\bkhl\b|kontinental hockey/.test(text)) return "khl";
  if (/\bshl\b|swedish hockey/.test(text)) return "shl";
  if (/\bahl\b|american hockey league/.test(text)) return "ahl";
  if (/\bliiga\b|finnish (hockey|liiga)/.test(text)) return "liiga";
  if (/\bczech (hockey|extraliga)|extraliga\b/.test(text)) return "czech_extraliga";
  if (/\beuroleague|eurobasket|euroleague basketball/.test(text)) return "euroleague";
  if (/\bfiba\b/.test(text)) return "fiba";
  if (/\bchampions league|uefa\b/.test(text)) return "uefa_champions_league";
  if (/\bpremier league\b/.test(text)) return "premier_league";
  if (/\bla liga\b/.test(text)) return "la_liga";
  if (/\bbundesliga\b/.test(text)) return "bundesliga";
  if (/\bserie a\b/.test(text)) return "serie_a";
  if (/\bligue 1\b/.test(text)) return "ligue_1";
  if (/\bbsn\b|puerto rico.*basketball|baloncesto.*puerto rico/.test(text)) return "liga_pr";
  if (/\bcba\b|chinese basketball association/.test(text)) return "cba";
  if (/\bnba\b/.test(text)) return "nba";
  if (/\bnfl\b/.test(text)) return "nfl";
  if (/\bnhl\b/.test(text)) return "nhl";
  if (/\bmlb\b/.test(text)) return "mlb";
  if (/\bmls\b/.test(text)) return "mls";
  return "sports";
}

function inferTeamAndSport(story) {
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  if (/auburn/.test(text)) {
    if (/basketball|sec tournament|ncaa tournament|march madness/.test(text)) {
      return { teamKey: "auburn-tigers-basketball", sport: "basketball" };
    }
    return { teamKey: "auburn-tigers-football", sport: "football" };
  }
  if (/lakers/.test(text)) return { teamKey: "los-angeles-lakers", sport: "basketball" };
  if (/celtics/.test(text)) return { teamKey: "boston-celtics", sport: "basketball" };
  if (/yankees/.test(text)) return { teamKey: "new-york-yankees", sport: "baseball" };
  if (/mets\b/.test(text)) return { teamKey: "new-york-mets", sport: "baseball" };
  if (/cowboys/.test(text)) return { teamKey: "dallas-cowboys", sport: "football" };
  if (/packers/.test(text)) return { teamKey: "green-bay-packers", sport: "football" };
  if (/bears\b/.test(text) && /chicago|nfl/.test(text)) return { teamKey: "chicago-bears", sport: "football" };
  if (/bruins/.test(text)) return { teamKey: "boston-bruins", sport: "hockey" };
  if (/maple leafs|leafs\b/.test(text)) return { teamKey: "toronto-maple-leafs", sport: "hockey" };
  if (/manchester united|man united|man u\b/.test(text)) return { teamKey: "manchester-united", sport: "soccer" };
  if (/real madrid/.test(text)) return { teamKey: "real-madrid", sport: "soccer" };

  const league = getLeagueForStory(story);
  if (["nba", "euroleague", "fiba", "ncaa_basketball"].includes(league)) {
    return { teamKey: null, sport: "basketball" };
  }
  if (["mlb", "ncaa_baseball"].includes(league)) {
    return { teamKey: null, sport: "baseball" };
  }
  if (["nfl", "ncaa_football"].includes(league)) {
    return { teamKey: null, sport: "football" };
  }
  if (["nhl", "khl", "ahl", "shl", "liiga", "czech_extraliga"].includes(league)) {
    return { teamKey: null, sport: "hockey" };
  }
  if (["mls", "uefa_champions_league", "premier_league", "la_liga", "bundesliga", "serie_a", "ligue_1"].includes(league)) {
    return { teamKey: null, sport: "soccer" };
  }
  return { teamKey: null, sport: null };
}

function teamOrSportPinHtml(story) {
  const { teamKey, sport } = inferTeamAndSport(story);
  const fallbackLogo = sport && SPORT_FALLBACK_META[sport] ? SPORT_FALLBACK_META[sport].logo : "/static/team-icons/generic-basketball.svg";

  if (teamKey && TEAM_META[teamKey]) {
    const meta = TEAM_META[teamKey];
    const logo = meta.logo;
    const name = meta.name;
    return `
      <div class="pin-logo" style="background:#111827;">
        <img src="${logo}" alt="${name} logo" data-fallback="${fallbackLogo}" onerror="var f=this.getAttribute('data-fallback');if(f){this.onerror=null;this.src=f;}" />
      </div>
    `;
  }

  if (sport && SPORT_FALLBACK_META[sport]) {
    const meta = SPORT_FALLBACK_META[sport];
    const logo = meta.logo;
    return `
      <div class="pin-logo" style="background:#111827;">
        <img src="${logo}" alt="${meta.name} icon" />
      </div>
    `;
  }

  const leagueKey = getLeagueForStory(story);
  return sportsLeaguePinHtml(leagueKey);
}

function teamOrSportMarkerIcon(story) {
  return L.divIcon({
    className: "custom-pin",
    html: teamOrSportPinHtml(story),
    iconSize: [20, 24],
    iconAnchor: [10, 23],
    popupAnchor: [0, -20],
  });
}

function isGhostWarStory(story) {
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  if (/(ghost war|proxy war|proxy conflict)/.test(text)) return true;
  if (/\b(backing|funding|funds|arming|supporting|backs|supports)\s+(rebels?|militias?|militant|insurgents?|factions?|armed groups?|proxies)/.test(text)) return true;
  if (/\b(backing|funding|arming|support(?:ing|s)?)\s+(the\s+)?(m23|wagner|hezbollah|houthis?|kurds?|taliban|pmf|popular mobilization)/.test(text)) return true;
  if (/\b(rwanda|uganda)\s+.*(m23|congo|drc|drcongo|goma)/.test(text) || /\b(m23|m23 rebels?)\s+.*(rwanda|congo|drc)/.test(text)) return true;
  if (/\b(turkey|turkish)\s+.*(syria|syrian|rebel|faction|proxy)/.test(text) || /\b(syria|syrian)\s+.*(turkey|turkish|backed|proxy)/.test(text)) return true;
  if (/\b(usa|united states|american)\s+.*(kurds?|kurdish).*(iran|iraq|syria)/.test(text) || /\b(kurds?|kurdish)\s+.*(iran|iraq|turkey).*(fund|back|support)/.test(text)) return true;
  if (/\b(china|chinese)\s+.*(myanmar|burma|wa state|mndaa|ethnic armed|rebel)/.test(text) || /\b(myanmar|burma)\s+.*(china|chinese).*(back|fund|support|arm)/.test(text)) return true;
  if (/\b(iran|iranian)\s+.*(hezbollah|houthis?|militia|proxy|syria|yemen)/.test(text) || /\b(saudi|uae|emirates)\s+.*(yemen|houthis?|libya|proxy)/.test(text)) return true;
  if (/\b(iran|north western iran|northwestern iran)\s+.*(israel|strike|attack|covert|proxy|backing)/.test(text) || /\b(israel|israeli)\s+.*(iran|proxy|strike|covert)/.test(text)) return true;
  if (/\b(external support|covert support|proxy force|foreign.backed|backed by)\s+(rebels?|militias?|insurgents?|faction)/.test(text)) return true;
  if (/\b(arms?\s+to|weapons?\s+to|military aid to)\s+(rebels?|militias?|insurgents?|opposition)/.test(text)) return true;
  return false;
}

function classifyStoryTopic(story) {
  if (isGhostWarStory(story)) return "ghost_war";
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  const checks = [
    ["conflict", /(war|conflict|offensive|missile|troops|military|strike|ceasefire|battle|attack)\b/],
    ["disaster", /(earthquake|flood|wildfire|hurricane|typhoon|cyclone|storm|eruption|disaster)\b/],
    ["politics", /(election|parliament|president|prime minister|government|policy|minister|senate|diplomat)\b/],
    ["economy", /(inflation|gdp|recession|interest rate|central bank|trade|tariff)\b/],
    ["business", /(company|market|stock|investor|deal|merger|earnings|bank|startup)\b/],
    ["tech", /(ai|artificial intelligence|chip|software|technology|cyber|data center)\b/],
    ["health", /(health|disease|virus|hospital|vaccine|who|outbreak)\b/],
    ["climate", /(climate|emission|carbon|warming|weather|environment)\b/],
    ["crime", /(police|court|judge|arrest|crime|trial|prosecutor|corruption)\b/]
  ];
  for (const [topic, re] of checks) {
    if (re.test(text)) return topic;
  }
  return "other";
}

function normalizeCountryKey(name) {
  return String(name || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .replace(/[^a-z0-9 ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function majorEventSignal(story) {
  const text = `${story.title || ""} ${story.summary || ""}`.toLowerCase();
  const rules = [
    { label: "Ghost war / proxy support", re: /(ghost war|proxy war|backing rebels?|funding militia|arming insurgents?|external support for|m23.*rwanda|rwanda.*m23|turkey.*syria.*rebel|china.*myanmar.*rebel|support for (m23|hezbollah|houthis?|kurds?))/ },
    { label: "Civil war and armed clashes", re: /(civil war|rebels?|insurgenc|junta|ethnic armed|military offensive)/ },
    { label: "Student protests and civil unrest", re: /(student protest|demonstration|protest|riot|crackdown)/ },
    { label: "Separatist or insurgent activity", re: /(separatist|secession|guerrilla|militia attack)/ },
    { label: "Geopolitical tensions", re: /(border clash|maritime dispute|naval standoff|sanctions|diplomatic row)/ },
    { label: "Humanitarian and displacement crisis", re: /(refugee|displaced|humanitarian|famine|aid access|cholera)/ },
    { label: "Election and power struggle", re: /(election|coup|parliament vote|constitutional crisis)/ },
    { label: "Disaster emergency response", re: /(earthquake|flood|wildfire|cyclone|typhoon|disaster)/ },
  ];
  for (const rule of rules) {
    if (rule.re.test(text)) return rule.label;
  }
  const topic = classifyStoryTopic(story);
  const topicLabel = (TOPIC_META[topic] || TOPIC_META.other).label;
  return `${topicLabel} developments`;
}

function buildCountryMajorEvents(stories) {
  const byCountry = {};
  stories.forEach((story) => {
    const country = story.country || "";
    const key = normalizeCountryKey(country);
    if (!key) return;
    const signal = majorEventSignal(story);
    if (!byCountry[key]) byCountry[key] = { country, signals: {}, sample: story };
    byCountry[key].signals[signal] = (byCountry[key].signals[signal] || 0) + 1;
    // Keep newest as sample fallback.
    if ((story.published_at || "") > (byCountry[key].sample?.published_at || "")) {
      byCountry[key].sample = story;
    }
  });

  const out = {};
  Object.keys(byCountry).forEach((key) => {
    const entry = byCountry[key];
    const sortedSignals = Object.entries(entry.signals).sort((a, b) => b[1] - a[1]);
    const topSignal = sortedSignals[0]?.[0] || "Major developments";
    const country = entry.country || "this country";
    const sample = entry.sample || {};
    out[key] = {
      linked_title: `${topSignal} in ${country}`,
      brief_summary: truncate(sample.summary || sample.title || "", 170),
      source_headline: sample.title || "",
    };
  });
  return out;
}

function sourceIconHtml(sourceKey, topicKey = "other") {
  const meta = sourceMeta(sourceKey);
  const topic = TOPIC_META[topicKey] || TOPIC_META.other;
  const bgBySource = {
    bbc: "#000000",
    bbc_asia: "#000000",
    bbc_africa: "#000000",
    bbc_middle_east: "#000000",
    economist: "#EB001B",
    economist_asia: "#EB001B",
    economist_mea: "#EB001B",
    economist_graphic_detail: "#EB001B",
    guardian_world: "#052962",
    guardian_international: "#052962",
    dispatch: "#1f2937",
    politico: "#A41E21",
    gov_us_dod_releases: "#111827",
    gov_us_dod_contracts: "#111827",
    gov_eu_commission: "#003399",
    gov_uk_announcements: "#003078",
    gov_canada_news: "#CC0000",
    gov_canada_pm: "#CC0000",
    gov_canada_global_affairs: "#CC0000",
    gov_brazil_planalto: "#009C3B",
    gov_argentina_presidencia: "#75AADB",
    gov_chile_presidencia: "#0039A6",
    gov_colombia_presidencia: "#FCD116",
    gov_mexico_presidencia: "#006847",
    gov_peru_pcm: "#D91023",
    gov_japan_kantei: "#BC002D",
    gov_japan_mof: "#BC002D",
    gov_india_mea: "#FF9933",
    gov_singapore_mfa: "#ED1C24",
    gov_south_korea_yonhap: "#003478",
    gov_indonesia_kemlu: "#CE1126",
    gov_malaysia_pmo: "#010066",
    gov_philippines_dfa: "#0038A8",
    gov_thailand_mfa: "#A51931",
    gov_vietnam_mofa: "#DA251D",
    gov_russia_kremlin: "#0039A6",
    gov_kazakhstan_pm: "#00AFCA",
    gov_uzbekistan_mfa: "#0099B5",
    gov_south_africa: "#007749",
    gov_nigeria_fmino: "#008751",
    gov_kenya_president: "#006600",
    gov_egypt_sis: "#C8102E",
    gov_ethiopia_pmo: "#078930",
    gov_ghana_presidency: "#CE1126",
    gov_tanzania_presidency: "#00A3DD",
    gov_morocco_map: "#C1272D",
    gov_senegal_presidency: "#00853F",
    gov_au_commission: "#007D3D",
    gov_australia_pm: "#012169",
    gov_australia_rba: "#012169",
    gov_new_zealand_beehive: "#00247D",
    amnesty: "#111827",
    hrw: "#111827",
    aljazeera: "#0F172A",
    abc_news: "#E41E22",
    rudaw_english: "#C41E3A",
    middle_east_eye: "#1a1a1a",
    dw_world: "#005B95",
    cnn: "#CC0000",
    nbc: "#F37021",
    sky_news: "#0072C6",
    irrawaddy_myanmar: "#1f2937",
    reuters: "#111827",
    wsj: "#111827",
    washingtonpost: "#111827",
    nyt: "#111827",
    axios: "#111827",
    x_reutersworld: "#000000",
    x_bbcbreaking: "#000000",
    x_ap: "#000000",
    x_un: "#000000",
    x_africacenter: "#000000",
    x_thetimes: "#000000",
    x_politico: "#000000",
    x_janesintel: "#000000",
    x_rand: "#000000",
    x_amnesty: "#000000",
    x_isw: "#000000",
    x_liveuamap: "#000000",
    x_carnegie: "#000000",
    x_hudson: "#000000",
    x_barakravid: "#000000",
    x_clarissaward: "#000000",
    x_richardengel: "#000000",
    x_lynsaddler: "#000000",
    x_nickpatonwalsh: "#000000",
    x_borzsandor: "#000000",
    x_ianbremmer: "#000000",
    x_rudaw: "#000000",
    x_middleeasteye: "#000000",
    x_kurdistan24: "#000000",
    carnegie: "#C41230",
    aei: "#1a365d",
    hudson: "#0d47a1",
    substack_jamestown: "#1a472a",
    substack_rochan: "#0057b7",
    substack_counteroffensive: "#ffd700",
    substack_warwickpowell: "#FF6719",
    substack_professorbonk: "#FF6719",
    espn_news: "#FF0033",
    espn_nfl: "#013369",
    espn_nba: "#174B8A",
    espn_mlb: "#041E42",
    espn_nhl: "#000000",
    espn_soccer: "#FF0033",
    espn_ncf: "#CC0000",
    espn_ncb: "#CC0000",
    espn_ncaa: "#CC0000",
    espn_tennis: "#FF0033",
    on3: "#1a1a1a",
    nbcsports: "#F37021",
    the_athletic: "#1a1a1a",
    wikipedia_historical: "#0d47a1"
  };
  const bg = bgBySource[String(sourceKey || "").toLowerCase()] || "#1f2937";
  const fallback = meta.logoFallback || "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23999'%3E%3Cpath d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z'/%3E%3C/svg%3E";
  return `
    <span class="marker-wrap">
      <span class="pin-head">
        <img class="source-icon" src="${meta.logo}" data-fallback="${fallback.replace(/"/g, "&quot;")}" style="background:${bg}" alt="${meta.name} logo" referrerpolicy="no-referrer" onerror="this.onerror=null;this.src=this.getAttribute('data-fallback')||'';" />
      </span>
      <span class="pin-tip"></span>
      <span class="topic-badge" title="${topic.label}">${topic.icon}</span>
    </span>
  `;
}

function markerIcon(sourceKey, topicKey = "other") {
  return L.divIcon({
    className: "custom-pin",
    html: sourceIconHtml(sourceKey, topicKey),
    iconSize: [14, 20],
    iconAnchor: [7, 19],
    popupAnchor: [0, -16]
  });
}

const GENERIC_ICON_FALLBACK = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23999'%3E%3Cpath d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z'/%3E%3C/svg%3E";
function sportsLeaguePinHtml(leagueKey) {
  const meta = SPORTS_LEAGUE_META[leagueKey] || SPORTS_LEAGUE_META.sports;
  const logo = meta.logo;
  return `
    <span class="marker-wrap">
      <span class="pin-head">
        <img class="source-icon" src="${logo}" data-fallback="${GENERIC_ICON_FALLBACK.replace(/"/g, "&quot;")}" alt="${meta.name}" referrerpolicy="no-referrer" onerror="this.onerror=null;this.src=this.getAttribute('data-fallback')||'';" />
      </span>
      <span class="pin-tip"></span>
    </span>
  `;
}

function sportsMarkerIcon(leagueKey) {
  return L.divIcon({
    className: "custom-pin",
    html: sportsLeaguePinHtml(leagueKey),
    iconSize: [14, 20],
    iconAnchor: [7, 19],
    popupAnchor: [0, -16]
  });
}

function countryStyle() {
  return {
    color: "#708090",
    weight: 1,
    fillColor: "#a7c4e0",
    fillOpacity: 0.06
  };
}

function countryHighlightStyle() {
  return {
    color: "#1557b0",
    weight: 2.2,
    fillColor: "#72a7e0",
    fillOpacity: 0.22
  };
}

function getCountryNameFromFeature(feature) {
  const p = feature?.properties || {};
  return p.ADMIN || p.name || p.NAME || p.name_long || p.sovereignt || "";
}

const REGION_DEFAULT_STYLE = {
  color: "#4B5563",
  weight: 1,
  fillColor: "#111827",
  fillOpacity: 0.1,
};
const REGION_HIGHLIGHT_STYLE = {
  color: "#6B7280",
  weight: 2,
  fillColor: "#1F2937",
  fillOpacity: 0.25,
};

function getRegionNameFromFeature(feature) {
  const p = feature?.properties || {};
  return p.name || p.NAME || p.name_1 || p.admin_1 || p.region || "";
}

function getRegionCountryFromFeature(feature) {
  const p = feature?.properties || {};
  return p.admin || p.ADMIN || p.country || p.iso_a2 || "";
}

function updateMajorTeamsPanel(data) {
  const wrap = document.getElementById("country-major-teams-wrap");
  const el = document.getElementById("country-major-teams");
  if (!wrap || !el) return;
  if (data == null) {
    wrap.style.display = "none";
    el.innerHTML = "";
    return;
  }
  const teams = Array.isArray(data.teams) ? data.teams : (data && data.length ? data : []);
  if (teams.length === 0) {
    wrap.style.display = "none";
    el.innerHTML = "";
    return;
  }
  wrap.style.display = "block";
  el.innerHTML = "<ul class=\"sports-leagues-ul\">" + teams.map((t) => {
    const name = typeof t === "string" ? t : (t.name || t);
    return `<li>${name}</li>`;
  }).join("") + "</ul>";
}

/** Only call when active map is Sports; otherwise use updateMajorTeamsPanel(null). */
async function loadMajorTeamsForLocation(params) {
  const { countryCode, stateName, cityName } = params || {};
  if (getActiveMapKey() !== "sports") {
    updateMajorTeamsPanel(null);
    return;
  }
  try {
    const q = new URLSearchParams();
    if (countryCode) q.set("country", countryCode);
    if (stateName) q.set("state", stateName);
    if (cityName) q.set("city", cityName);
    const res = await fetch("/api/major-teams?" + q.toString());
    if (!res.ok) {
      updateMajorTeamsPanel(null);
      return;
    }
    const data = await res.json();
    updateMajorTeamsPanel(data);
  } catch (err) {
    updateMajorTeamsPanel(null);
  }
}

function onRegionClick(e, feature, context) {
  L.DomEvent.stopPropagation(e);
  if (window.selectedRegionLayer && window.selectedRegionLayer.setStyle) {
    resetRegionStyle(window.selectedRegionLayer);
  }
  window.selectedRegionLayer = e.target;
  highlightRegion(e.target);

  const regionName = getRegionNameFromFeature(feature);
  const countryName = getRegionCountryFromFeature(feature);
  const props = feature.properties || {};
  const isoA2 = props.iso_a2 || props.iso_3166_2 || (countryName ? COUNTRY_TO_ISO2[countryName.toLowerCase().replace(/\s+/g, " ")] : "US");

  if (context && countryName) {
    openCountryPanel(countryName, context.mapKey || activeMapKey);
    const statusEl = document.getElementById("country-search-status");
    if (statusEl) statusEl.textContent = regionName ? `${regionName}, ${countryName}` : `Showing ${countryName}.`;
  }

  const currentMapKey = getActiveMapKey();
  if (currentMapKey === "sports") {
    loadMajorTeamsForLocation({ countryCode: isoA2 || countryName, stateName: regionName || null, cityName: null });
  } else {
    updateMajorTeamsPanel(null);
  }
}

function highlightRegion(layer) {
  if (layer && layer.setStyle) layer.setStyle(REGION_HIGHLIGHT_STYLE);
}

function resetRegionStyle(layer) {
  if (layer && layer.setStyle) layer.setStyle(REGION_DEFAULT_STYLE);
}

const COUNTRY_TO_ISO2 = {
  "afghanistan": "AF", "albania": "AL", "algeria": "DZ", "andorra": "AD", "angola": "AO",
  "antigua and barbuda": "AG", "argentina": "AR", "armenia": "AM", "australia": "AU",
  "austria": "AT", "azerbaijan": "AZ", "bahamas": "BS", "bahrain": "BH", "bangladesh": "BD",
  "barbados": "BB", "belarus": "BY", "belgium": "BE", "belize": "BZ", "benin": "BJ",
  "bhutan": "BT", "bolivia": "BO", "bosnia and herzegovina": "BA", "botswana": "BW",
  "brazil": "BR", "brunei": "BN", "bulgaria": "BG", "burkina faso": "BF", "burundi": "BI",
  "cabo verde": "CV", "cambodia": "KH", "cameroon": "CM", "canada": "CA",
  "central african republic": "CF", "chad": "TD", "chile": "CL", "china": "CN",
  "colombia": "CO", "comoros": "KM", "congo": "CG", "costa rica": "CR", "croatia": "HR",
  "cuba": "CU", "cyprus": "CY", "czechia": "CZ", "czech republic": "CZ",
  "democratic republic of the congo": "CD", "denmark": "DK", "djibouti": "DJ",
  "dominica": "DM", "dominican republic": "DO", "ecuador": "EC", "egypt": "EG",
  "el salvador": "SV", "equatorial guinea": "GQ", "eritrea": "ER", "estonia": "EE",
  "eswatini": "SZ", "swaziland": "SZ", "ethiopia": "ET", "fiji": "FJ", "finland": "FI",
  "france": "FR", "gabon": "GA", "gambia": "GM", "georgia": "GE", "germany": "DE",
  "ghana": "GH", "greece": "GR", "grenada": "GD", "guatemala": "GT", "guinea": "GN",
  "guinea-bissau": "GW", "guyana": "GY", "haiti": "HT", "honduras": "HN", "hungary": "HU",
  "iceland": "IS", "india": "IN", "indonesia": "ID", "iran": "IR", "iraq": "IQ",
  "ireland": "IE", "israel": "IL", "italy": "IT", "ivory coast": "CI", "côte d'ivoire": "CI",
  "cote d'ivoire": "CI", "jamaica": "JM", "japan": "JP", "jordan": "JO", "kazakhstan": "KZ",
  "kenya": "KE", "kiribati": "KI", "kuwait": "KW", "kyrgyzstan": "KG", "laos": "LA",
  "latvia": "LV", "lebanon": "LB", "lesotho": "LS", "liberia": "LR", "libya": "LY",
  "liechtenstein": "LI", "lithuania": "LT", "luxembourg": "LU", "madagascar": "MG",
  "malawi": "MW", "malaysia": "MY", "maldives": "MV", "mali": "ML", "malta": "MT",
  "marshall islands": "MH", "mauritania": "MR", "mauritius": "MU", "mexico": "MX",
  "micronesia": "FM", "moldova": "MD", "monaco": "MC", "mongolia": "MN", "montenegro": "ME",
  "morocco": "MA", "mozambique": "MZ", "myanmar": "MM", "burma": "MM", "namibia": "NA",
  "nauru": "NR", "nepal": "NP", "netherlands": "NL", "new zealand": "NZ", "nicaragua": "NI",
  "niger": "NE", "nigeria": "NG", "north macedonia": "MK", "macedonia": "MK", "norway": "NO",
  "oman": "OM", "pakistan": "PK", "palau": "PW", "palestine": "PS", "panama": "PA",
  "papua new guinea": "PG", "paraguay": "PY", "peru": "PE", "philippines": "PH",
  "poland": "PL", "portugal": "PT", "qatar": "QA", "romania": "RO", "russia": "RU",
  "russian federation": "RU", "rwanda": "RW", "saint kitts and nevis": "KN",
  "saint lucia": "LC", "saint vincent and the grenadines": "VC", "samoa": "WS",
  "san marino": "SM", "sao tome and principe": "ST", "saudi arabia": "SA", "senegal": "SN",
  "serbia": "RS", "seychelles": "SC", "sierra leone": "SL", "singapore": "SG",
  "slovakia": "SK", "slovenia": "SI", "solomon islands": "SB", "somalia": "SO",
  "south africa": "ZA", "south korea": "KR", "korea republic of": "KR", "south sudan": "SS",
  "spain": "ES", "sri lanka": "LK", "sudan": "SD", "suriname": "SR", "sweden": "SE",
  "switzerland": "CH", "syria": "SY", "syrian arab republic": "SY", "taiwan": "TW",
  "tajikistan": "TJ", "tanzania": "TZ", "thailand": "TH", "timor-leste": "TL", "east timor": "TL",
  "togo": "TG", "tonga": "TO", "trinidad and tobago": "TT", "tunisia": "TN", "turkey": "TR",
  "türkiye": "TR", "turkmenistan": "TM", "tuvalu": "TV", "uganda": "UG", "ukraine": "UA",
  "united arab emirates": "AE", "united kingdom": "GB", "united states": "US",
  "united states of america": "US", "usa": "US", "uruguay": "UY", "uzbekistan": "UZ",
  "vanuatu": "VU", "venezuela": "VE", "vietnam": "VN", "viet nam": "VN", "yemen": "YE",
  "zambia": "ZM", "zimbabwe": "ZW"
};

function getCountryFlag(countryName) {
  if (!countryName || typeof countryName !== "string") return "";
  const key = countryName.toLowerCase().trim().replace(/\s+/g, " ");
  const iso2 = COUNTRY_TO_ISO2[key] || COUNTRY_TO_ISO2[key.replace(/\s*\([^)]*\)\s*$/, "").trim()];
  if (!iso2 || iso2.length !== 2) return "";
  const a = 0x1F1E6 - 65;
  return String.fromCodePoint(a + iso2.charCodeAt(0), a + iso2.charCodeAt(1));
}


function getFeatureCenter(feature) {
  const g = feature?.geometry;
  if (!g || !g.coordinates) return null;
  let coords = [];
  if (g.type === "Polygon") coords = g.coordinates[0] || [];
  else if (g.type === "MultiPolygon") coords = (g.coordinates[0] && g.coordinates[0][0]) || [];
  if (coords.length === 0) return null;
  let sumLat = 0, sumLng = 0, n = 0;
  coords.forEach((c) => {
    sumLng += c[0];
    sumLat += c[1];
    n += 1;
  });
  return n ? [sumLat / n, sumLng / n] : null;
}

function normalizeCountryName(name) {
  return String(name || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .replace(/[^a-z0-9 ]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function setCountrySelection(context, layer) {
  if (context.selectedCountryLayer && context.selectedCountryLayer !== layer) {
    context.selectedCountryLayer.setStyle(countryStyle());
  }
  context.selectedCountryLayer = layer;
  layer.setStyle(countryHighlightStyle());
}

function searchAndOpenCountry(rawQuery) {
  const context = mapContexts[activeMapKey];
  const query = normalizeCountryName(rawQuery);
  const statusEl = document.getElementById("country-search-status");
  if (!query) {
    statusEl.textContent = "Enter a country name to search.";
    return;
  }

  let match = context?.countryLayerIndex?.[query] || null;
  if (!match) {
    const key = Object.keys(context?.countryLayerIndex || {}).find((k) => k.includes(query));
    if (key) match = context.countryLayerIndex[key];
  }

  if (!match) {
    statusEl.textContent = `No country found for "${rawQuery}".`;
    return;
  }

  statusEl.textContent = `Showing ${match.countryName}.`;
  setCountrySelection(context, match.layer);
  if (typeof match.layer.getBounds === "function") {
    context.map.fitBounds(match.layer.getBounds(), { maxZoom: 5, padding: [18, 18] });
  }
  openCountryPanel(match.countryName, activeMapKey);
}

function storyCardHtml(story) {
  const title = story.title || "Untitled";
  const url = story.url || "#";
  const readerUrl = toReaderUrl(url);
  const source = sourceMeta(story.source);
  const published = story.published_at || "";
  return `
    <article class="story-item">
      <a href="${readerUrl}" target="_blank" rel="noopener noreferrer">${title}</a>
      <div class="muted">${source.name}${published ? ` - ${published}` : ""}</div>
    </article>
  `;
}

function isXReportSource(sourceKey) {
  return String(sourceKey || "").toLowerCase().startsWith("x_");
}

function canonicalXUrl(rawUrl) {
  const url = String(rawUrl || "").trim();
  if (!url) return "";
  return url
    .replace(/^https?:\/\/nitter\.net\//i, "https://x.com/")
    .replace(/^https?:\/\/nitter\.[^/]+\//i, "https://x.com/");
}

function getVideoEmbed(story) {
  if (!story) return null;
  const text = `${story.url || ""} ${story.summary || ""} ${story.title || ""}`;
  const ytMatch = text.match(/(?:youtube\.com\/watch\?.*v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  if (ytMatch) return { type: "youtube", id: ytMatch[1], embedUrl: `https://www.youtube.com/embed/${ytMatch[1]}?rel=0` };
  const vimeoMatch = text.match(/vimeo\.com\/(?:video\/)?(\d+)/);
  if (vimeoMatch) return { type: "vimeo", id: vimeoMatch[1], embedUrl: `https://player.vimeo.com/video/${vimeoMatch[1]}` };
  const xMatch = text.match(/(?:twitter\.com|x\.com)\/(\w+)\/status\/(\d+)/);
  if (xMatch) return { type: "x", statusId: xMatch[2], url: `https://x.com/${xMatch[1]}/status/${xMatch[2]}` };
  return null;
}

function videoEmbedHtml(story) {
  const video = getVideoEmbed(story);
  if (!video) return "";
  if (video.type === "youtube" || video.type === "vimeo") {
    return `<div class="popup-video-wrap"><iframe class="popup-video" src="${video.embedUrl}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
  }
  if (video.type === "x") {
    return `<div class="popup-video-wrap"><blockquote class="twitter-tweet" data-dnt="true"><a href="${video.url}"></a></blockquote></div>`;
  }
  return "";
}

function relatedVideoEmbedHtml(videoUrl) {
  if (!videoUrl || typeof videoUrl !== "string") return "";
  const url = canonicalXUrl(videoUrl);
  const ytMatch = url.match(/(?:youtube\.com\/watch\?.*v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  if (ytMatch) return `<div class="popup-video-wrap"><iframe class="popup-video" src="https://www.youtube.com/embed/${ytMatch[1]}?rel=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>`;
  const vimeoMatch = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
  if (vimeoMatch) return `<div class="popup-video-wrap"><iframe class="popup-video" src="https://player.vimeo.com/video/${vimeoMatch[1]}" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div>`;
  if (/^(https?:\/\/)?(www\.)?(x\.com|twitter\.com)\/\w+\/status\/\d+/.test(url)) return `<div class="popup-video-wrap"><blockquote class="twitter-tweet" data-dnt="true"><a href="${url}"></a></blockquote></div>`;
  return "";
}

function toReaderUrl(url) {
  const raw = String(url || "").trim();
  if (!raw || raw === "#") return "#";
  const stripped = raw.replace(/^https?:\/\//i, "");
  return `https://r.jina.ai/http://${stripped}`;
}

function escapeAttr(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

async function fetchAiSummary(type, body) {
  const res = await fetch("/api/ai-summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type, ...body })
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data.summary || "";
}

function formatEconSnapshotHtml(snap) {
  const fmtNum = (v) => {
    if (v == null || typeof v !== "number") return "—";
    if (Math.abs(v) >= 1e12) return `$${(v / 1e12).toFixed(2)}T`;
    if (Math.abs(v) >= 1e9) return `$${(v / 1e9).toFixed(2)}B`;
    if (Math.abs(v) >= 1e6) return `$${(v / 1e6).toFixed(2)}M`;
    return `$${v.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
  };
  const fmtPct = (v) => (v != null && typeof v === "number" ? `${v.toFixed(1)}%` : "—");
  const rows = [];
  if (snap.gdp_current_usd != null) rows.push(`<div><b>GDP (current US$):</b> ${fmtNum(snap.gdp_current_usd)}</div>`);
  if (snap.gdp_per_capita_usd != null) rows.push(`<div><b>GDP per capita:</b> ${fmtNum(snap.gdp_per_capita_usd)}</div>`);
  if (snap.gdp_growth_pct != null) rows.push(`<div><b>GDP growth (annual %):</b> ${fmtPct(snap.gdp_growth_pct)}</div>`);
  if (snap.inflation_pct != null) rows.push(`<div><b>Inflation (CPI, annual %):</b> ${fmtPct(snap.inflation_pct)}</div>`);
  if (snap.unemployment_pct != null) rows.push(`<div><b>Unemployment (%):</b> ${fmtPct(snap.unemployment_pct)}</div>`);
  if (snap.debt_pct_gdp != null) rows.push(`<div><b>Gov. debt (% GDP):</b> ${fmtPct(snap.debt_pct_gdp)}</div>`);
  if (snap.fiscal_balance_pct_gdp != null) rows.push(`<div><b>Fiscal balance (% GDP):</b> ${fmtPct(snap.fiscal_balance_pct_gdp)}</div>`);
  if (snap.imf_gdp_growth_pct != null) rows.push(`<div><b>IMF GDP growth (%):</b> ${fmtPct(snap.imf_gdp_growth_pct)}</div>`);
  if (snap.imf_inflation_pct != null) rows.push(`<div><b>IMF inflation (%):</b> ${fmtPct(snap.imf_inflation_pct)}</div>`);
  if (snap.year) rows.push(`<div class="muted"><b>Reference year:</b> ${snap.year}</div>`);
  return rows.length ? rows.join("") : "<div class=\"muted\">No economic data available for this country.</div>";
}

async function openCountryPanel(countryName, mapKey) {
  mapKey = mapKey || activeMapKey;
  const sidePanel = document.getElementById("country-side-panel");
  const titleEl = document.getElementById("country-title");
  const factsEl = document.getElementById("country-facts");
  const factsWrap = document.getElementById("country-facts-wrap");
  const conflictCasualtiesWrap = document.getElementById("country-conflict-casualties-wrap");
  const conflictCasualtiesEl = document.getElementById("country-conflict-casualties");
  const sportsLeaguesWrap = document.getElementById("country-sports-leagues-wrap");
  const sportsLeaguesEl = document.getElementById("country-sports-leagues");
  const allSourcesHeading = document.getElementById("all-sources-heading");
  const recentUpdatesHeading = document.getElementById("recent-updates-heading");
  const graphicDetailSection = document.getElementById("graphic-detail-section");
  const graphicDetailList = document.getElementById("graphic-detail-list");
  const allSourcesListEl = document.getElementById("all-sources-list");
  const storyListEl = document.getElementById("country-story-list");
  const economistRankingsSection = document.getElementById("economist-rankings-section");

  const flagSpan = getCountryFlag(countryName)
    ? `<span class="country-flag" aria-hidden="true">${getCountryFlag(countryName)}</span> `
    : "";
  titleEl.innerHTML = flagSpan;
  titleEl.append(countryName);
  factsEl.innerHTML = "Loading country details...";
  if (conflictCasualtiesWrap) conflictCasualtiesWrap.style.display = "none";
  if (conflictCasualtiesEl) conflictCasualtiesEl.innerHTML = "";
  if (sportsLeaguesWrap) sportsLeaguesWrap.style.display = "none";
  if (sportsLeaguesEl) sportsLeaguesEl.innerHTML = "";
  updateMajorTeamsPanel(null);
  const aiSummaryResult = document.getElementById("country-ai-summary-result");
  if (aiSummaryResult) { aiSummaryResult.textContent = ""; aiSummaryResult.className = "ai-summary-result"; }
  if (graphicDetailSection) graphicDetailSection.style.display = "none";
  graphicDetailList.innerHTML = "";
  allSourcesListEl.innerHTML = "";
  storyListEl.innerHTML = "";
  filterPinsForCountry(countryName);   sidePanel.classList.add("open");
  sidePanel.dataset.currentCountry = "";
  sidePanel.dataset.panelMapKey = mapKey || "";

  try {
    const response = await fetch(`/api/country?name=${encodeURIComponent(countryName)}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const originalName = payload.original_name || countryName;
    const englishName = payload.english_name || countryName;
    const displayName = originalName === englishName
      ? englishName
      : `${originalName} (${englishName})`;
    const flag = getCountryFlag(englishName) || getCountryFlag(originalName) || getCountryFlag(countryName);
    titleEl.innerHTML = flag ? `<span class="country-flag" aria-hidden="true">${flag}</span> ` : "";
    titleEl.append(displayName);
    sidePanel.dataset.currentCountry = englishName || countryName;
    const facts = payload.facts || null;
    const econSnap = payload.econ_snapshot || {};
    const hasEconSnap = Object.keys(econSnap).filter((k) => k !== "sources").length > 0;

    if (facts) {
      const showLegacyGdp = !hasEconSnap && (facts.gdp_ppp || facts.economist_economic_rank);
      factsEl.innerHTML = `
        <div><b>Capital:</b> ${facts.capital || "n/a"}</div>
        <div><b>Population:</b> ${facts.population || "n/a"}</div>
        ${showLegacyGdp ? `<div><b>GDP (PPP):</b> ${facts.gdp_ppp || "n/a"}</div><div><b>Economist economic rank:</b> ${facts.economist_economic_rank || "n/a"}</div>` : ""}
        <div><b>Area:</b> ${facts.area_total || "n/a"}</div>
        <div><b>Government:</b> ${facts.government_type || "n/a"}</div>
      `;
    } else {
      factsEl.innerHTML = "No CIA Factbook data found for this country.";
    }

    const econSnapshotWrap = document.getElementById("country-econ-snapshot-wrap");
    const econSnapshotEl = document.getElementById("country-econ-snapshot");
    if (econSnapshotWrap && econSnapshotEl) {
      if (hasEconSnap) {
        econSnapshotEl.innerHTML = formatEconSnapshotHtml(econSnap);
        econSnapshotWrap.style.display = (mapKey === "economics") ? "block" : "none";
      } else {
        econSnapshotWrap.style.display = "none";
        econSnapshotEl.innerHTML = "";
      }
    }
    const wikiSnippet = payload.wikipedia_snippet;
    if (wikiSnippet) {
      const wrap = document.createElement("div");
      wrap.className = "wikipedia-snippet muted";
      wrap.style.marginTop = "8px";
      const label = document.createElement("strong");
      label.textContent = "From Wikipedia (data only): ";
      wrap.appendChild(label);
      wrap.appendChild(document.createTextNode(wikiSnippet));
      factsEl.appendChild(wrap);
    }

    const economistRankingsSection = document.getElementById("economist-rankings-section");
    const economistRankingsList = document.getElementById("economist-rankings-list");
    const rankings = payload.economist_rankings || [];
    if (economistRankingsSection && economistRankingsList) {
      if (rankings.length > 0) {
        economistRankingsSection.style.display = "block";
        economistRankingsList.innerHTML = rankings.map((r) => {
          const rankStr = r.rank != null ? `#${r.rank}` : "—";
          const scoreStr = r.score != null ? ` (${r.score}/10)` : "";
          const yearStr = r.year ? ` ${r.year}` : "";
          return `<div class="ranking-row"><span class="ranking-label">${r.label}</span><span class="ranking-value">${rankStr}${scoreStr}${yearStr}</span></div>`;
        }).join("");
      } else {
        economistRankingsSection.style.display = "none";
      }
    }

    const graphicDetailStories = payload.graphic_detail_stories || [];
    if (graphicDetailSection && graphicDetailList) {
      if (graphicDetailStories.length > 0) {
        graphicDetailSection.style.display = "block";
        graphicDetailList.innerHTML = graphicDetailStories.map(storyCardHtml).join("");
      } else {
        graphicDetailSection.style.display = "none";
      }
    }

    const allSourceStories = payload.all_source_stories || [];
    allSourcesListEl.innerHTML = allSourceStories.length
      ? allSourceStories.map(storyCardHtml).join("")
      : `<div class="muted">No source coverage matched this country yet.</div>`;

    const recentStories = payload.recent_stories || [];
    const aiSummarySection = document.getElementById("country-ai-summary-section");
    if (mapKey === "conflicts") {
      if (conflictCasualtiesWrap && payload.conflict_casualties) {
        conflictCasualtiesWrap.style.display = "block";
        const c = payload.conflict_casualties;
        conflictCasualtiesEl.innerHTML = `<div class="conflict-casualties-content"><p><strong>Casualty estimates:</strong> ${c.estimate || "—"}</p><p class="muted">Source: ${c.source || "—"}${c.as_of ? ` (${c.as_of})` : ""}</p></div>`;
      }
      if (factsWrap) factsWrap.style.display = "none";
      if (economistRankingsSection) economistRankingsSection.style.display = "none";
      if (aiSummarySection) aiSummarySection.style.display = "none";
      if (graphicDetailSection) graphicDetailSection.style.display = "none";
      if (allSourcesHeading) allSourcesHeading.textContent = "Conflict & military news";
      if (recentUpdatesHeading) recentUpdatesHeading.style.display = "none";
      const conflictStories = (allSourceStories.length ? allSourceStories : recentStories).filter((s) => (s.topic || "geopolitics") === "conflicts");
      storyListEl.innerHTML = conflictStories.length ? conflictStories.map(storyCardHtml).join("") : `<div class="muted">No conflict or military news for this country yet.</div>`;
      allSourcesListEl.innerHTML = "";
    } else if (mapKey === "economics") {
      if (factsWrap) factsWrap.style.display = "block";
      if (aiSummarySection) aiSummarySection.style.display = "block";
      if (economistRankingsSection && hasEconSnap) economistRankingsSection.style.display = "none";
      if (allSourcesHeading) allSourcesHeading.textContent = "Economic coverage";
      if (recentUpdatesHeading) { recentUpdatesHeading.style.display = ""; recentUpdatesHeading.textContent = "Recent mapped updates"; }
      const economicsStories = (allSourceStories.length ? allSourceStories : recentStories).filter((s) => (s.topic || "geopolitics") === "economics");
      allSourcesListEl.innerHTML = economicsStories.length ? economicsStories.map(storyCardHtml).join("") : `<div class="muted">No economic coverage for this country yet.</div>`;
      storyListEl.innerHTML = economicsStories.length ? economicsStories.map(storyCardHtml).join("") : `<div class="muted">No recent mapped stories for this country yet.</div>`;
    } else if (mapKey === "sports") {
      if (sportsLeaguesWrap && (payload.top_sports_leagues || []).length > 0) {
        sportsLeaguesWrap.style.display = "block";
        sportsLeaguesEl.innerHTML = "<ul class=\"sports-leagues-ul\">" + payload.top_sports_leagues.map((l) => `<li>${l}</li>`).join("") + "</ul>";
      }
      if (factsWrap) factsWrap.style.display = "none";
      if (economistRankingsSection) economistRankingsSection.style.display = "none";
      if (aiSummarySection) aiSummarySection.style.display = "none";
      if (graphicDetailSection) graphicDetailSection.style.display = "none";
      if (allSourcesHeading) allSourcesHeading.textContent = "Sports coverage";
      if (recentUpdatesHeading) recentUpdatesHeading.style.display = "none";
      const sportsStories = (allSourceStories.length ? allSourceStories : recentStories).filter((s) => (s.topic || "geopolitics") === "sports");
      storyListEl.innerHTML = sportsStories.length ? sportsStories.map(storyCardHtml).join("") : `<div class="muted">No sports coverage for this country yet.</div>`;
      allSourcesListEl.innerHTML = "";
    } else {
      if (factsWrap) factsWrap.style.display = "block";
      if (aiSummarySection) aiSummarySection.style.display = "block";
      if (allSourcesHeading) allSourcesHeading.textContent = "Geopolitics coverage";
      if (recentUpdatesHeading) { recentUpdatesHeading.style.display = ""; recentUpdatesHeading.textContent = "Recent mapped updates"; }
      const geopoliticsStories = (allSourceStories.length ? allSourceStories : recentStories).filter((s) => (s.topic || "geopolitics") === "geopolitics");
      allSourcesListEl.innerHTML = geopoliticsStories.length ? geopoliticsStories.map(storyCardHtml).join("") : `<div class="muted">No geopolitics coverage for this country yet.</div>`;
      storyListEl.innerHTML = geopoliticsStories.length ? geopoliticsStories.map(storyCardHtml).join("") : `<div class="muted">No recent mapped stories for this country yet.</div>`;
    }
  } catch (error) {
    factsEl.innerHTML = "Failed to load country details.";
    console.error("Country panel load failed:", error);
  }
}

function loadCountryBordersForContext(context) {
  if (!worldCountryGeoJson) return;
  context.countryLayer = L.geoJSON(worldCountryGeoJson, {
    style: countryStyle,
    onEachFeature(feature, layer) {
      const countryName = getCountryNameFromFeature(feature);
      const normalized = normalizeCountryName(countryName);
      if (normalized) {
        context.countryLayerIndex[normalized] = { layer, countryName };
      }
      layer.on("click", () => {
        setCountrySelection(context, layer);
        openCountryPanel(countryName, context.mapKey || activeMapKey);
      });
    }
  }).addTo(context.map);

  const labelsLayer = L.layerGroup();
  (worldCountryGeoJson.features || []).forEach((feature) => {
    const center = getFeatureCenter(feature);
    const name = getCountryNameFromFeature(feature);
    if (!center || !name) return;
    const label = L.marker(center, {
      icon: L.divIcon({
        className: "country-label-wrap",
        html: `<span class="country-label">${name}</span>`,
        iconSize: [80, 14],
        iconAnchor: [40, 7]
      })
    });
    labelsLayer.addLayer(label);
  });
  context.countryLabelsLayer = labelsLayer;
  function updateLabelsVisibility() {
    const z = context.map.getZoom();
    if (z >= 3) {
      if (!context.map.hasLayer(labelsLayer)) labelsLayer.addTo(context.map);
    } else {
      if (context.map.hasLayer(labelsLayer)) context.map.removeLayer(labelsLayer);
    }
  }
  context.map.on("zoomend", updateLabelsVisibility);
  updateLabelsVisibility();
}

function popupHtml(story, countryMajorEvents) {
  const safeTitle = story.title || "Untitled story";
  const safeUrl = story.url || "#";
  const readerUrl = toReaderUrl(safeUrl);
  const source = sourceMeta(story.source);
  const topicKey = classifyStoryTopic(story);
  const topic = TOPIC_META[topicKey] || TOPIC_META.other;
  const published = story.published_at || "unknown date";
  const summary = truncate(story.summary || "");
  const country = story.country || "Unknown";
  const eventKey = normalizeCountryKey(country);
  const countryEvent = (countryMajorEvents || {})[eventKey] || null;
  const linkedTitle = countryEvent?.linked_title || `${majorEventSignal(story)} in ${country}`;
  const briefEventSummary = countryEvent?.brief_summary || summary;
  const sourceHeadline = countryEvent?.source_headline || safeTitle;
  const newBadge = isStoryNew(story.published_at) ? '<span class="popup-new-badge" title="Published in the last 2 hours">NEW</span>' : '';
  return `
    <div>
      <div>${newBadge}<a href="${readerUrl}" target="_blank" rel="noopener noreferrer">${linkedTitle}</a></div>
      <div class="muted popup-source">${sourceIconHtml(story.source, topicKey)} <span>${source.name} - ${published} - ${topic.label}</span></div>
      <p>${briefEventSummary}</p>
      <div class="muted">Source: ${sourceHeadline}</div>
      ${isXReportSource(story.source) ? `
        <blockquote class="twitter-tweet" data-dnt="true">
          <a href="${canonicalXUrl(safeUrl)}"></a>
        </blockquote>
      ` : ""}
      ${!isXReportSource(story.source) ? videoEmbedHtml(story) : ""}
      ${!getVideoEmbed(story) && story.related_video_url ? `
        <div class="popup-related-video">
          <span class="muted">Related video from social media</span>
          ${relatedVideoEmbedHtml(story.related_video_url)}
        </div>
      ` : ""}
      <div class="popup-ai-summary">
        <button type="button" class="ai-summary-btn" data-title="${escapeAttr(safeTitle)}" data-summary="${escapeAttr((story.summary || "").slice(0, 2000))}" data-country="${escapeAttr(country)}" data-source="${escapeAttr(story.source || "")}">AI summary</button>
        <div class="ai-summary-result" aria-live="polite"></div>
      </div>
    </div>
  `;
}

function spreadSportsPins(sportsStories) {
  const round = (v) => Math.round(v * 100) / 100;
  const key = (s) => `${round(s.lat)}_${round(s.lon)}`;
  const groups = new Map();
  sportsStories.forEach((s) => {
    const k = key(s);
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(s);
  });
  const out = [];
  const offsetDeg = 0.15;
  groups.forEach((list) => {
    if (list.length <= 1) {
      out.push(...list);
      return;
    }
    list.forEach((s, i) => {
      const angle = (i / list.length) * 2 * Math.PI;
      out.push({
        ...s,
        lat: s.lat + Math.cos(angle) * offsetDeg,
        lon: s.lon + Math.sin(angle) * offsetDeg
      });
    });
  });
  return out;
}

const TWO_HOURS_MS = 2 * 60 * 60 * 1000;
function isStoryNew(publishedAt) {
  if (!publishedAt) return false;
  try {
    const t = new Date(publishedAt).getTime();
    return !isNaN(t) && (Date.now() - t) < TWO_HOURS_MS;
  } catch (_) { return false; }
}

function addStoryToMap(story, countryMajorEvents) {
  const topic = story.topic || "geopolitics";
  const layerGroup = layersByMapKey[topic] || layersByMapKey.geopolitics;
  if (!layerGroup) return;
  let icon;
  if (topic === "sports") {
    icon = teamOrSportMarkerIcon(story);
  } else {
    const sourceKey = String(story.source || "").toLowerCase();
    icon = sourceIcons[sourceKey] || defaultSourceIcon;
    if (!sourceIcons[sourceKey]) {
      console.warn("Missing icon for source:", story.source);
    }
  }
  const marker = L.marker([story.lat, story.lon], { icon });
  marker.bindPopup(popupHtml(story, countryMajorEvents || {}));
  marker.on("popupopen", () => {
    if (window.twttr && window.twttr.widgets) window.twttr.widgets.load();
  });
  layerGroup.addLayer(marker);
}

function filterPinsForCountry(countryName) {   Object.keys(layersByMapKey).forEach((topic) => layersByMapKey[topic].clearLayers());   const stories = countryName ? allVisibleStories.filter((s) => (s.country || "").toLowerCase() === countryName.toLowerCase()) : allVisibleStories;   const sportsSpread = spreadSportsPins(stories.filter((s) => (s.topic || "geopolitics") === "sports"));   stories.forEach((s) => {     if ((s.topic || "geopolitics") !== "sports") addStoryToMap(s, allCountryMajorEvents);   });   sportsSpread.forEach((s) => addStoryToMap(s, allCountryMajorEvents)); } async function refreshStories() {
  const overlay = document.getElementById("map-loading-overlay");
  if (overlay) overlay.classList.remove("hidden");
  try {
    let url = "/api/stories";
    if (selectedYear !== null && selectedYear !== undefined) {
      url += "?year=" + encodeURIComponent(selectedYear);
    }
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const stories = await response.json();
    const visible = stories.filter((s) => {
      if (typeof s.lat !== "number" || typeof s.lon !== "number") return false;
      if (s.source === "economist_podcast") return false;
      if (s.country === "World" && (s.source || "").toLowerCase() !== "wikipedia_historical") return false;
      return true;
    });
    const countryMajorEvents = buildCountryMajorEvents(visible);
    allVisibleStories = visible;   allCountryMajorEvents = countryMajorEvents;   const byTopic = { economics: [], geopolitics: [], conflicts: [], sports: [] };
    visible.forEach((s) => {
      const topic = s.topic || "geopolitics";
      const bucket = byTopic[topic] || byTopic.geopolitics;
      if (bucket) bucket.push(s);
    });
    const sportsSpread = spreadSportsPins(byTopic.sports || []);
    Object.keys(layersByMapKey).forEach((topic) => layersByMapKey[topic].clearLayers());
    Object.keys(byTopic).forEach((topic) => {
      const list = topic === "sports" ? sportsSpread : (byTopic[topic] || []);
      list.forEach((story) => addStoryToMap(story, countryMajorEvents));
    });
    Object.keys(MAP_DEFS).forEach((mapKey) => {
      const tabBtn = document.querySelector(`.map-tab[data-map-key="${mapKey}"]`);
      if (tabBtn) {
        const label = MAP_DEFS[mapKey] ? MAP_DEFS[mapKey].title : mapKey;
        const count = (mapKey === "sports" ? sportsSpread : (byTopic[mapKey] || [])).length;
        tabBtn.textContent = `${label} (${count})`;
      }
    });
  } catch (error) {
    console.error("Failed to refresh stories:", error);
  } finally {
    if (overlay) overlay.classList.add("hidden");
  }
}
function initMapContexts() {
  Object.keys(MAP_DEFS).forEach((mapKey) => {
    const mapId = MAP_DEFS[mapKey].mapId;
    const m = L.map(mapId, {
      zoomControl: false,
      scrollWheelZoom: true,
      doubleClickZoom: true,
      touchZoom: true,
      boxZoom: true,
      keyboard: true,
      minZoom: 2,
      maxZoom: 19
    }).setView([20, 0], 2);
    L.control.zoom({ position: "topright" }).addTo(m);

    const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>",
      maxZoom: 19
    });
    const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
      attribution: "&copy; Esri",
      maxZoom: 18
    });
    const terrain = L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; <a href=\"https://opentopomap.org\">OpenTopoMap</a>",
      maxZoom: 17
    });

    osm.addTo(m);
    const baseLayers = {
      "Map": osm,
      "Satellite": satellite,
      "Terrain": terrain
    };
    const overlays = {};
    let iswLinesLayer = null;
    if (mapKey === "conflicts") {
      iswLinesLayer = L.layerGroup();
      const iswLineStyle = { color: "#c44", weight: 4, dashArray: "10,8", opacity: 0.95 };
      function addIswGeoJson(geojson) {
        if (!geojson || !geojson.features || !iswLinesLayer) return;
        L.geoJSON(geojson, {
          style: iswLineStyle,
          onEachFeature: function (feature, layer) {
            if (feature.properties && feature.properties.name) {
              layer.bindTooltip(feature.properties.name, { permanent: false, direction: "top" });
            }
          }
        }).addTo(iswLinesLayer);
      }
      fetch("/api/isw-frontlines").then((r) => r.ok ? r.json() : null).then(addIswGeoJson).catch(() => {});
      iswLinesLayer.addTo(m);
      overlays["ISW / Front lines"] = iswLinesLayer;
    }
    L.control.layers(baseLayers, Object.keys(overlays).length ? overlays : null, { position: "topright" }).addTo(m);
    L.control.scale({ imperial: true }).addTo(m);

    L.Control.Fullscreen = L.Control.extend({
      onAdd: function () {
        const div = L.DomUtil.create("div", "leaflet-control leaflet-control-fullscreen");
        div.innerHTML = "\u29BF";
        div.title = "Fullscreen";
        L.DomEvent.disableClickPropagation(div);
        L.DomEvent.on(div, "click", this._toggle, this);
        document.addEventListener("fullscreenchange", () => {
          div.innerHTML = document.fullscreenElement ? "\u2715" : "\u29BF";
          div.title = document.fullscreenElement ? "Exit fullscreen" : "Fullscreen";
        });
        return div;
      },
      _toggle: function () {
        const pane = document.querySelector(".map-pane");
        if (!pane) return;
        if (!document.fullscreenElement) {
          pane.requestFullscreen?.();
        } else {
          document.exitFullscreen?.();
        }
      }
    });
    L.control.fullscreen = function (opts) { return new L.Control.Fullscreen(opts); };
    L.control.fullscreen({ position: "bottomright" }).addTo(m);

    const userLocationLayer = L.layerGroup().addTo(m);
    L.Control.Locate = L.Control.extend({
      onAdd: function (map) {
        const div = L.DomUtil.create("div", "leaflet-control leaflet-control-locate");
        div.innerHTML = "\u2316";
        div.title = "My location";
        L.DomEvent.disableClickPropagation(div);
        L.DomEvent.on(div, "click", () => this._locate(map, div), this);
        return div;
      },
      _locate: function (map, div) {
        if (!navigator.geolocation) {
          alert("Geolocation is not supported by your browser.");
          return;
        }
        const layer = map._userLocationLayer;
        div.style.opacity = "0.6";
        navigator.geolocation.getCurrentPosition(
          function (pos) {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;
            map.flyTo([lat, lng], Math.max(10, map.getZoom()));
            if (layer) {
              layer.clearLayers();
              const circle = L.circleMarker([lat, lng], { radius: 8, color: "#1976d2", fillColor: "#42a5f5", fillOpacity: 0.8, weight: 2 });
              layer.addLayer(circle);
            }
            div.style.opacity = "1";
          },
          function () {
            alert("Unable to get your location.");
            div.style.opacity = "1";
          },
          { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
        );
      }
    });
    m._userLocationLayer = userLocationLayer;
    L.control.locate = function (opts) { return new L.Control.Locate(opts); };
    L.control.locate({ position: "bottomright" }).addTo(m);

    const markerLayer = (typeof L.markerClusterGroup === "function")
      ? L.markerClusterGroup({ maxClusterRadius: 50, spiderfyOnMaxZoom: true }).addTo(m)
      : L.layerGroup().addTo(m);
    mapContexts[mapKey] = {
      map: m,
      markerLayer: markerLayer,
      countryLayer: null,
      countryLayerIndex: {},
      selectedCountryLayer: null,
      mapKey: mapKey,
      iswLinesLayer: iswLinesLayer || undefined
    };
  });
  layersByMapKey = {
    economics: mapContexts.economics.markerLayer,
    geopolitics: mapContexts.geopolitics.markerLayer,
    conflicts: mapContexts.conflicts.markerLayer,
    sports: mapContexts.sports.markerLayer
  };
}

async function loadCountryGeoJsonOnce() {
  const resp = await fetch("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json");
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  worldCountryGeoJson = await resp.json();
  Object.values(mapContexts).forEach((context) => loadCountryBordersForContext(context));
}

function loadAdmin1ForContext(context, data) {
  if (!data || !data.features || !data.features.length) return;
  const regionLayer = L.geoJSON(data, {
    style: () => REGION_DEFAULT_STYLE,
    onEachFeature: (feature, layer) => {
      layer.on({
        click: (e) => onRegionClick(e, feature, context),
        mouseover: () => highlightRegion(layer),
        mouseout: () => resetRegionStyle(layer),
      });
    },
  });
  regionLayer.addTo(context.map);
  context.regionLayer = regionLayer;
}

async function loadAdmin1GeoJsonOnce() {
  try {
    const res = await fetch("/static/geo/admin1.geojson");
    if (!res.ok) return;
    const data = await res.json();
    Object.values(mapContexts).forEach((context) => loadAdmin1ForContext(context, data));
  } catch (err) {
    console.error("Failed to load admin1 geojson", err);
  }
}

function activateMapTab(mapKey) {
  setActiveMapKey(mapKey);
  document.querySelectorAll(".map-tab").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.mapKey === mapKey);
  });
  Object.keys(MAP_DEFS).forEach((key) => {
    const el = document.getElementById(MAP_DEFS[key].mapId);
    el.classList.toggle("active", key === mapKey);
  });
  const labelEl = document.getElementById("maps-dropdown-label");
  if (labelEl && MAP_DEFS[mapKey]) labelEl.textContent = MAP_DEFS[mapKey].title;
  const dd = document.getElementById("maps-dropdown");
  if (dd) dd.classList.remove("open");
  const trigger = document.getElementById("maps-dropdown-trigger");
  if (trigger) trigger.setAttribute("aria-expanded", "false");
  setTimeout(() => mapContexts[mapKey].map.invalidateSize(), 80);
}

function initMapsDropdown() {
  const trigger = document.getElementById("maps-dropdown-trigger");
  const panel = document.getElementById("maps-dropdown-panel");
  const dd = document.getElementById("maps-dropdown");
  const labelEl = document.getElementById("maps-dropdown-label");
  if (!trigger || !panel || !dd) return;
  if (labelEl && MAP_DEFS[activeMapKey]) labelEl.textContent = MAP_DEFS[activeMapKey].title;
  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    const isOpen = dd.classList.toggle("open");
    trigger.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
  document.querySelectorAll(".map-tab").forEach((btn) => {
    btn.addEventListener("click", () => activateMapTab(btn.dataset.mapKey));
  });
  document.addEventListener("click", (e) => {
    if (!dd.contains(e.target)) {
      dd.classList.remove("open");
      trigger.setAttribute("aria-expanded", "false");
    }
  });
}

function initYearSelector() {
  const input = document.getElementById("year-select-input");
  const bcSpan = document.getElementById("year-select-bc");
  if (!input) return;
  function applyYear() {
    const raw = input.value.trim();
    if (raw === "") {
      selectedYear = null;
      if (bcSpan) bcSpan.textContent = "";
      refreshStories();
      return;
    }
    const n = parseInt(input.value, 10);
    if (isNaN(n) || n < -1000 || n > 2030) return;
    selectedYear = n;
    if (bcSpan) bcSpan.textContent = n < 1 ? "BC" : "";
    refreshStories();
  }
  input.addEventListener("change", applyYear);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") applyYear();
  });
}

function enableDraggablePanel() {
  const panel = document.getElementById("live-updates-panel");
  const handle = document.getElementById("live-updates-drag-handle");
  if (!panel || !handle || panel.classList.contains("sidebar-left")) return;

  let dragOffsetX = 0;
  let dragOffsetY = 0;
  let dragging = false;

  function startDrag(event) {
    dragging = true;
    panel.style.right = "auto";
    const rect = panel.getBoundingClientRect();
    dragOffsetX = event.clientX - rect.left;
    dragOffsetY = event.clientY - rect.top;
    event.preventDefault();
  }

  handle.addEventListener("pointerdown", startDrag);
  panel.addEventListener("pointerdown", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    if (target.closest("input, button, a, textarea, select")) return;
    startDrag(event);
  });

  window.addEventListener("pointermove", (event) => {
    if (!dragging) return;
    const maxLeft = Math.max(0, window.innerWidth - panel.offsetWidth);
    const maxTop = Math.max(0, window.innerHeight - panel.offsetHeight);
    const left = Math.min(maxLeft, Math.max(0, event.clientX - dragOffsetX));
    const top = Math.min(maxTop, Math.max(0, event.clientY - dragOffsetY));
    panel.style.left = `${left}px`;
    panel.style.top = `${top}px`;
  });

  window.addEventListener("pointerup", () => {
    dragging = false;
  });
}

function initChat() {
  const chatPanel = document.getElementById("chat-panel");
  const chatToggle = document.getElementById("chat-toggle-btn") || document.querySelector("[data-action='toggle-pvd-chat']");
  const chatClose = document.getElementById("chat-close-btn");
  const chatMessages = document.getElementById("chat-messages");
  const chatInput = document.getElementById("chat-input");
  const chatSend = document.getElementById("chat-send-btn");
  if (!chatPanel || !chatToggle || !chatMessages || !chatInput || !chatSend) {
    if (typeof console !== "undefined" && console.warn) {
      console.warn("PVD chat: required elements not found (chat-panel, chat-toggle-btn, chat-messages, chat-input, chat-send-btn). Chat will be disabled.");
    }
    return;
  }

  function openChat() {
    chatPanel.classList.add("open");
    chatPanel.setAttribute("aria-hidden", "false");
  }
  function closeChat() {
    chatPanel.classList.remove("open");
    chatPanel.setAttribute("aria-hidden", "true");
  }

  chatToggle.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (chatPanel.classList.contains("open")) closeChat(); else openChat();
  });
  chatClose.addEventListener("click", (e) => {
    e.preventDefault();
    closeChat();
  });

  function appendMessage(role, text, isError) {
    const div = document.createElement("div");
    div.className = "chat-msg " + (role === "user" ? "user" : isError ? "error" : "assistant");
    div.textContent = text;
    if (role === "assistant" && !isError) div.style.whiteSpace = "pre-wrap";
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function sendMessage() {
    const msg = (chatInput.value || "").trim();
    if (!msg) return;
    chatInput.value = "";
    chatSend.disabled = true;
    appendMessage("user", msg);
    const sidePanel = document.getElementById("country-side-panel");
    const country = (sidePanel && sidePanel.dataset.currentCountry) || null;
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          map_key: activeMapKey || undefined,
          country: country || undefined
        })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        appendMessage("assistant", data.error || "Chat unavailable. In Render: open your pvdmaproom service → Environment → Add OPENAI_API_KEY with your OpenAI key.", true);
        return;
      }
      if (data.reply) appendMessage("assistant", data.reply);
    } catch (err) {
      appendMessage("assistant", err.message || "Request failed.", true);
    } finally {
      chatSend.disabled = false;
    }
  }

  chatSend.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
}

initMapContexts();
enableDraggablePanel();
loadCountryGeoJsonOnce()
  .then(() => loadAdmin1GeoJsonOnce())
  .catch((error) => {
    console.error("Failed to load country borders:", error);
  });
initMapsDropdown();
window.activeMapKey = activeMapKey;
initYearSelector();
initChat();

document.addEventListener("click", (e) => {
  const a = e.target && e.target.closest ? e.target.closest("a[href^='http']") : null;
  if (!a || !a.href) return;
  const inPanel = document.getElementById("country-side-panel") && document.getElementById("country-side-panel").contains(a);
  const inPopup = a.closest(".leaflet-popup-content");
  if ((inPanel || inPopup) && a.target !== "_blank") {
    e.preventDefault();
    window.open(a.href, "_blank", "noopener,noreferrer");
  }
}, true);

document.getElementById("country-search-btn").addEventListener("click", () => {
  const input = document.getElementById("country-search-input");
  searchAndOpenCountry(input.value);
});
document.getElementById("country-search-input").addEventListener("keydown", (event) => {
  if (event.key !== "Enter") return;
  event.preventDefault();
  searchAndOpenCountry(event.target.value);
});
document.getElementById("country-close-btn").addEventListener("click", () => {
  document.getElementById("country-side-panel").classList.remove("open");
});

document.getElementById("country-ai-summary-btn").addEventListener("click", async () => {
  const panel = document.getElementById("country-side-panel");
  const resultEl = document.getElementById("country-ai-summary-result");
  const country = (panel && panel.dataset.currentCountry) || "";
  if (!country || !resultEl) return;
  const mapKey = (panel && panel.dataset.panelMapKey) || activeMapKey || undefined;
  resultEl.textContent = "Loading…";
  resultEl.className = "ai-summary-result loading";
  try {
    const yearParam = selectedYear !== null && selectedYear !== undefined ? selectedYear : undefined;
    const summary = await fetchAiSummary("country", { country, map_key: mapKey, year: yearParam });
    resultEl.textContent = summary;
    resultEl.className = "ai-summary-result";
  } catch (err) {
    resultEl.textContent = err.message || "AI summary unavailable (set OPENAI_API_KEY on the server).";
    resultEl.className = "ai-summary-result error";
  }
});

document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".ai-summary-btn");
  if (!btn || btn.id === "country-ai-summary-btn") return;
  const popupContent = btn.closest(".leaflet-popup-content");
  if (!popupContent) return;
  const resultEl = popupContent.querySelector(".ai-summary-result");
  if (!resultEl) return;
  const title = btn.dataset.title || "";
  const summary = btn.dataset.summary || "";
  if (!title && !summary) return;
  e.preventDefault();
  resultEl.textContent = "Loading…";
  resultEl.className = "ai-summary-result loading";
  try {
    const text = await fetchAiSummary("story", {
      title,
      summary,
      country: btn.dataset.country || "",
      source: btn.dataset.source || ""
    });
    resultEl.textContent = text;
    resultEl.className = "ai-summary-result";
  } catch (err) {
    resultEl.textContent = err.message || "AI summary unavailable (set OPENAI_API_KEY on the server).";
    resultEl.className = "ai-summary-result error";
  }
});

refreshStories();
setInterval(refreshStories, 30000);
