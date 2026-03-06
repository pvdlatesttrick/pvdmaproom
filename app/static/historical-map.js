/**
 * Historical Map: separate view from News Map. Uses historical borders and pins keyed by year.
 * Data structures (for later replacement with real data):
 *
 * @typedef {{ id: string, year: number, name: string, polygons: number[][][] }} HistoricalBorder
 * @typedef {{ title: string, summary: string, sourceUrl: string, coords: [number, number], yearStart: number, yearEnd: number, region: string }} HistoricalPin
 */

(function () {
  "use strict";

  const BORDER_YEARS = [1960, 1989, 2000, 2025];

  /** @type {Record<number, L.GeoJSON>} */
  let borderLayerByYear = {};
  /** @type {L.GeoJSON | null} */
  let currentBorderLayer = null;
  /** @type {L.LayerGroup} */
  let pinsLayer = null;
  /** @type {number} */
  let selectedYear = 1989;
  /** @type {{ name: string, year: number } | null} */
  let selectedCountryYear = null;

  /**
   * Placeholder historical pins. Replace with real data; year range is [yearStart, yearEnd].
   * @type {HistoricalPin[]}
   */
  const historicalPins = [
    {
      title: "Fall of the Berlin Wall",
      summary: "The Berlin Wall opened on 9 November 1989, leading to the collapse of the Eastern Bloc and the reunification of Germany in 1990.",
      sourceUrl: "https://en.wikipedia.org/wiki/Fall_of_the_Berlin_Wall",
      coords: [52.5163, 13.3777],
      yearStart: 1989,
      yearEnd: 1991,
      region: "Europe",
    },
    {
      title: "Tiananmen Square protests",
      summary: "Pro-democracy demonstrations in Beijing in 1989 were suppressed by the Chinese government.",
      sourceUrl: "https://en.wikipedia.org/wiki/Tiananmen_Square_protests_of_1989",
      coords: [39.9042, 116.4074],
      yearStart: 1989,
      yearEnd: 1989,
      region: "Asia",
    },
    {
      title: "Collapse of the Soviet Union",
      summary: "The USSR dissolved in 1991; the 1989–1991 period saw the end of Communist rule across Eastern Europe.",
      sourceUrl: "https://en.wikipedia.org/wiki/Dissolution_of_the_Soviet_Union",
      coords: [55.7558, 37.6176],
      yearStart: 1989,
      yearEnd: 1991,
      region: "Europe",
    },
    {
      title: "World War I outbreak",
      summary: "Archduke Franz Ferdinand was assassinated in Sarajevo in 1914, triggering the First World War.",
      sourceUrl: "https://en.wikipedia.org/wiki/Assassination_of_Archduke_Franz_Ferdinand",
      coords: [43.8516, 18.3564],
      yearStart: 1914,
      yearEnd: 1918,
      region: "Europe",
    },
    {
      title: "End of World War II in Europe",
      summary: "VE Day, 8 May 1945, marked the end of the war in Europe after the surrender of Nazi Germany.",
      sourceUrl: "https://en.wikipedia.org/wiki/Victory_in_Europe_Day",
      coords: [52.52, 13.405],
      yearStart: 1945,
      yearEnd: 1945,
      region: "Europe",
    },
  ];

  let map = null;

  function getSelectedYear() {
    const input = document.getElementById("historical-year-input");
    if (!input) return selectedYear;
    const n = parseInt(input.value, 10);
    return Number.isNaN(n) ? selectedYear : n;
  }

  function getBorderYear() {
    const sel = document.getElementById("historical-borders-select");
    if (!sel) return 1989;
    const n = parseInt(sel.value, 10);
    return Number.isNaN(n) ? 1989 : n;
  }

  function loadBordersForYear(year) {
    const url = `/static/borders/borders_${year}.geojson`;
    fetch(url)
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (geojson) {
        if (currentBorderLayer && map) map.removeLayer(currentBorderLayer);
        currentBorderLayer = null;
        if (!geojson || !geojson.features || !geojson.features.length) {
          console.warn("No border data for year", year);
          return;
        }
        currentBorderLayer = L.geoJSON(geojson, {
          style: { color: "#4B5563", weight: 1, fillOpacity: 0.1 },
          onEachFeature: function (feature, layer) {
            layer.on("click", function (e) {
              const props = feature.properties || {};
              const name = props.name || props.name_long || "Unknown";
              const code = props.iso_code || props.iso_a2 || props.ccode || null;
              selectedCountryYear = { name, year: getSelectedYear() };
              showHistoricalSummary(name, getSelectedYear());
              if (window.selectedBorderLayer) window.selectedBorderLayer.setStyle({ weight: 1 });
              window.selectedBorderLayer = e.target;
              e.target.setStyle({ weight: 2 });
            });
          },
        });
        if (map) currentBorderLayer.addTo(map);
      })
      .catch(function (err) { console.error("Failed to load borders for year", year, err); });
  }

  function showHistoricalSummary(countryName, year) {
    const block = document.getElementById("historical-summary-block");
    const heading = document.getElementById("historical-summary-heading");
    const text = document.getElementById("historical-summary-text");
    const resultEl = document.getElementById("historical-ai-summary-result");
    if (!block || !heading || !text) return;
    block.style.display = "block";
    heading.textContent = countryName + " · " + year;
    text.textContent = "Select a country and optionally click \"Generate AI summary\" for a 2–3 sentence summary for this country in this year.";
    text.classList.add("historical-summary-placeholder");
    if (resultEl) resultEl.textContent = "";
  }

  function renderPins() {
    if (!pinsLayer || !map) return;
    pinsLayer.clearLayers();
    const year = getSelectedYear();
    historicalPins.forEach(function (pin) {
      if (year < pin.yearStart || year > pin.yearEnd) return;
      const marker = L.marker(pin.coords).addTo(pinsLayer);
      const popupHtml =
        "<strong>" + escapeHtml(pin.title) + "</strong><br><p>" + escapeHtml(pin.summary) + "</p>" +
        '<a href="' + escapeHtml(pin.sourceUrl) + '" target="_blank" rel="noopener noreferrer">Source</a>';
      marker.bindPopup(popupHtml);
    });
  }

  function escapeHtml(s) {
    if (!s) return "";
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function initMap() {
    const container = document.getElementById("historical-map");
    if (!container) return;
    map = L.map("historical-map").setView([20, 0], 2);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);
    pinsLayer = L.layerGroup().addTo(map);
    loadBordersForYear(getBorderYear());
    renderPins();
  }

  function wireYearAndBorders() {
    const yearInput = document.getElementById("historical-year-input");
    const bordersSelect = document.getElementById("historical-borders-select");
    if (yearInput) {
      yearInput.addEventListener("change", function () {
        selectedYear = getSelectedYear();
        renderPins();
      });
    }
    if (bordersSelect) {
      bordersSelect.addEventListener("change", function () {
        loadBordersForYear(getBorderYear());
      });
    }
  }

  function wireAiSummaryButton() {
    const btn = document.getElementById("historical-ai-summary-btn");
    const resultEl = document.getElementById("historical-ai-summary-result");
    if (!btn || !resultEl) return;
    btn.addEventListener("click", function () {
      if (!selectedCountryYear) {
        resultEl.textContent = "Select a country on the map first.";
        return;
      }
      resultEl.textContent = "Loading…";
      fetch("/api/ai-summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "country",
          country: selectedCountryYear.name,
          year: selectedCountryYear.year,
        }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.summary) {
            resultEl.textContent = data.summary;
          } else {
            resultEl.textContent = data.error || "Summary unavailable.";
          }
        })
        .catch(function () {
          resultEl.textContent = "Request failed.";
        });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initMap();
      wireYearAndBorders();
      wireAiSummaryButton();
    });
  } else {
    initMap();
    wireYearAndBorders();
    wireAiSummaryButton();
  }
})();
