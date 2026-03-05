"""Conflict casualties and related data for the Conflicts map sidebar.
Sources: UN/OHCHR, ACLED, and other public estimates. Update periodically."""
from __future__ import annotations

# Normalized country name (lowercase, as from factbook.normalize_country_name) -> casualty info.
# Estimates vary by source; show as indicative. Add/update as needed.
CONFLICT_CASUALTIES: dict[str, dict[str, str]] = {
    "ukraine": {
        "estimate": "Tens of thousands of military and civilian casualties (2022–present).",
        "source": "UN OHCHR / various",
        "as_of": "ongoing",
    },
    "russia": {
        "estimate": "Significant military casualties (Ukraine conflict).",
        "source": "Various estimates",
        "as_of": "ongoing",
    },
    "syria": {
        "estimate": "Hundreds of thousands since 2011.",
        "source": "UN / SOHR",
        "as_of": "ongoing",
    },
    "yemen": {
        "estimate": "Over 150,000 conflict-related deaths (2014–present).",
        "source": "UN / ACLED",
        "as_of": "ongoing",
    },
    "myanmar": {
        "estimate": "Thousands in recent years; civil conflict.",
        "source": "Various",
        "as_of": "ongoing",
    },
    "sudan": {
        "estimate": "Thousands (2023–present conflict).",
        "source": "UN / ACLED",
        "as_of": "ongoing",
    },
    "democratic republic of the congo": {
        "estimate": "Ongoing conflict-related casualties in the east.",
        "source": "UN / Kivu Security Tracker",
        "as_of": "ongoing",
    },
    "israel": {
        "estimate": "Conflict-related casualties (Gaza/Israel conflict).",
        "source": "Various",
        "as_of": "ongoing",
    },
    "palestine": {
        "estimate": "Conflict-related casualties (Gaza/West Bank).",
        "source": "Various",
        "as_of": "ongoing",
    },
    "iraq": {
        "estimate": "Ongoing instability and casualties.",
        "source": "Various",
        "as_of": "ongoing",
    },
    "afghanistan": {
        "estimate": "Ongoing conflict-related casualties.",
        "source": "UNAMA / various",
        "as_of": "ongoing",
    },
    "ethiopia": {
        "estimate": "Conflict-related casualties (Tigray and other regions).",
        "source": "Various",
        "as_of": "ongoing",
    },
    "nigeria": {
        "estimate": "Ongoing conflict-related casualties (NE and elsewhere).",
        "source": "ACLED / various",
        "as_of": "ongoing",
    },
    "mali": {
        "estimate": "Ongoing conflict-related casualties.",
        "source": "UN / ACLED",
        "as_of": "ongoing",
    },
    "somalia": {
        "estimate": "Ongoing conflict-related casualties.",
        "source": "ACLED / various",
        "as_of": "ongoing",
    },
    "libya": {
        "estimate": "Ongoing instability and casualties.",
        "source": "Various",
        "as_of": "ongoing",
    },
}

# Normalized country name -> list of top sports leagues (for Sports map sidebar).
COUNTRY_TOP_LEAGUES: dict[str, list[str]] = {
    "united states": ["NFL", "NBA", "MLB", "NHL", "MLS", "NCAA Football", "NCAA Basketball", "SEC", "Big Ten", "Big 12", "ACC", "Pac-12", "NWSL"],
    "united kingdom": ["Premier League", "Championship", "Scottish Premiership", "WSL", "Premiership Rugby"],
    "spain": ["La Liga", "Segunda División", "ACB", "Liga F"],
    "germany": ["Bundesliga", "2. Bundesliga", "Basketball Bundesliga", "DEL"],
    "italy": ["Serie A", "Serie B", "LBA", "Lega Hockey"],
    "france": ["Ligue 1", "Ligue 2", "Betclic Élite", "Ligue Magnus"],
    "brazil": ["Brasileirão", "Campeonato Brasileiro Série B", "NBB", "Superliga"],
    "argentina": ["Liga Profesional", "Primera B", "Liga Nacional de Básquet", "Superliga"],
    "mexico": ["Liga MX", "Liga de Expansión", "LNBP", "LMB"],
    "canada": ["NHL (Canadian teams)", "CFL", "CBA", "MLS (Canadian teams)"],
    "australia": ["A-League", "NBL", "AFL", "NRL", "Super Rugby"],
    "japan": ["J1 League", "J2 League", "B.League", "NPB"],
    "south korea": ["K League 1", "K League 2", "KBL", "KBO"],
    "china": ["Chinese Super League", "CBA", "Chinese Volleyball League"],
    "netherlands": ["Eredivisie", "Eerste Divisie", "BNXT League", "Eredivisie (hockey)"],
    "portugal": ["Primeira Liga", "Liga Portugal 2", "LPB"],
    "russia": ["Russian Premier League", "VTB United League", "KHL (Russian teams)"],
    "turkey": ["Süper Lig", "TBL", "BSL", "Efeler Ligi"],
    "india": ["Indian Super League", "Pro Kabaddi", "IPL (cricket)", "PKL"],
    "egypt": ["Egyptian Premier League", "Basketball Super League"],
    "south africa": ["DSTV Premiership", "Currie Cup", "Super Rugby"],
    "nigeria": ["NPFL", "Basketball League", "Pro League"],
    "greece": ["Super League", "Greek Basket League", "A1 Ethniki"],
    "poland": ["Ekstraklasa", "PLK", "PGE Ekstraliga"],
    "ukraine": ["Ukrainian Premier League", "Superliga", "VTB / suspended"],
    "belgium": ["Pro League", "BNXT League", "EuroMillions Basketball League"],
    "scotland": ["Scottish Premiership", "Scottish Championship", "SRU"],
    "ireland": ["League of Ireland", "Pro14", "GAA"],
    "saudi arabia": ["Saudi Pro League", "Saudi First Division"],
    "united arab emirates": ["UAE Pro League", "Arabian Gulf League"],
    "qatar": ["Qatar Stars League", "Qatari Basketball League"],
    "puerto rico": ["BSN", "Baloncesto Superior Nacional", "LBPRC"],
    "philippines": ["PBA", "Philippine Cup", "UAAP", "NCAA Philippines"],
    "indonesia": ["Liga 1", "IBL"],
    "thailand": ["Thai League 1", "TBL"],
    "vietnam": ["V.League 1", "VBA"],
    "malaysia": ["Malaysian Super League", "ABL"],
    "singapore": ["Singapore Premier League", "ABL"],
    "new zealand": ["NZ Rugby", "ANZ Premiership", "NBL NZ"],
}
