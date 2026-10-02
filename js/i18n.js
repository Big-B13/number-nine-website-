/* ------------------------------------------------------------------
   Taalwissel EN / NL / DE voor de hele site.

   Twee mechanismen:
   1. data-i18n="key"  -> opzoeken in window.__TOUR_I18N__ (zie js/tour-i18n.js,
      gegenereerd door build_tour.py). Gebruikt op event.html.
   2. CHROME           -> woordenboek op basis van de Nederlandse brontekst, voor
      menu, footer, knoppen en andere vaste teksten op de overige pagina's.
      Staat een tekst er niet in, dan blijft hij staan zoals hij is.

   De keuze wordt bewaard in localStorage ("n9-lang") en geldt voor alle
   pagina's. De schakelaar wordt automatisch in de header gezet als een pagina
   er zelf geen heeft.
------------------------------------------------------------------- */
(function () {
  "use strict";

  /* event.html bakt dit script in; voorkom dubbel koppelen als een
     pagina het daarnaast ook nog als los bestand laadt. */
  if (window.__N9_I18N__) return;
  window.__N9_I18N__ = true;

  var LANGS = ["en", "nl", "de"];
  var LABEL = { en: "ENG", nl: "NL", de: "DE" };
  var KEY = "n9-lang";
  var DEFAULT = "en";   /* taal bij een eerste bezoek — zet op "nl" of "de" naar smaak */

  /* ---------- opslag met fallback (sandboxed previews) ---------- */
  var store = (function () {
    try {
      localStorage.setItem("__n9probe", "1");
      localStorage.removeItem("__n9probe");
      return localStorage;
    } catch (e) {
      var mem = {};
      return {
        getItem: function (k) { return k in mem ? mem[k] : null; },
        setItem: function (k, v) { mem[k] = String(v); }
      };
    }
  })();

  /* ---------- vaste teksten: NL (bron) -> EN / DE ---------- */
  var CHROME = {
    /* navigatie */
    "Menu": ["Menu", "Menü"],
    "Home": ["Home", "Start"],
    "Dames": ["Women", "Damen"],
    "Heren": ["Men", "Herren"],
    "Merken": ["Brands", "Marken"],
    "Sale": ["Sale", "Sale"],
    "Winkels": ["Stores", "Filialen"],
    "Over ons": ["About us", "Über uns"],
    "Pop-up Tour": ["Pop-up Tour", "Pop-up-Tour"],
    "Alles in Dames": ["All womenswear", "Alles für Damen"],
    "Alles in Heren": ["All menswear", "Alles für Herren"],
    "Nieuw binnen": ["New in", "Neu da"],
    "New in dames": ["New in women", "Neu bei Damen"],
    "New in heren": ["New in men", "Neu bei Herren"],
    "Net binnen": ["Just landed", "Gerade eingetroffen"],
    "Preorder": ["Pre-order", "Vorbestellen"],
    "Kleding": ["Clothing", "Kleidung"],
    "Accessoires": ["Accessories", "Accessoires"],
    "Schoenen": ["Shoes", "Schuhe"],
    "Jassen": ["Coats & jackets", "Jacken & Mäntel"],
    "Truien & vesten": ["Knitwear", "Strick & Westen"],
    "Tops & blouses": ["Tops & blouses", "Tops & Blusen"],
    "Jurken & rokken": ["Dresses & skirts", "Kleider & Röcke"],
    "Broeken": ["Trousers", "Hosen"],
    "Jeans": ["Jeans", "Jeans"],
    "Overhemden": ["Shirts", "Hemden"],
    "T-shirts": ["T-shirts", "T-Shirts"],
    "Tassen": ["Bags", "Taschen"],
    "Sieraden": ["Jewellery", "Schmuck"],
    "Riemen": ["Belts", "Gürtel"],
    "Sjaals": ["Scarves", "Schals"],
    "Mutsen": ["Beanies", "Mützen"],
    "Sokken": ["Socks", "Socken"],
    "Sneakers": ["Sneakers", "Sneaker"],
    "Laarzen": ["Boots", "Stiefel"],
    "Loafers": ["Loafers", "Loafer"],
    "Boots": ["Boots", "Boots"],
    "Nette schoenen": ["Dress shoes", "Business-Schuhe"],

    /* header / drawers */
    "Zoeken": ["Search", "Suche"],
    "Winkelmand": ["Cart", "Warenkorb"],
    "Account": ["Account", "Konto"],
    "Subtotaal": ["Subtotal", "Zwischensumme"],
    "Naar winkelmand": ["Go to cart", "Zum Warenkorb"],
    "Zoek op product of merk...": ["Search by product or brand...",
                                   "Nach Produkt oder Marke suchen..."],
    "Begin met typen om de testcatalogus te doorzoeken.":
      ["Start typing to search the test catalogue.",
       "Tippe los, um den Testkatalog zu durchsuchen."],
    "Betaomgeving — afrekenen is uitgeschakeld.":
      ["Beta environment — checkout is disabled.",
       "Beta-Umgebung — Checkout ist deaktiviert."],
    "Je winkelmand is leeg.": ["Your cart is empty.", "Dein Warenkorb ist leer."],

    /* footer */
    "Klantenservice": ["Customer service", "Kundenservice"],
    "Verzending": ["Shipping", "Versand"],
    "Retourneren": ["Returns", "Rücksendungen"],
    "Maattabel": ["Size guide", "Größentabelle"],
    "Veelgestelde vragen": ["FAQ", "Häufige Fragen"],
    "Contact": ["Contact", "Kontakt"],
    "Shoppen": ["Shop", "Shoppen"],
    "Cadeaubon": ["Gift card", "Geschenkkarte"],
    "Over": ["About", "Über"],
    "Onze winkels": ["Our stores", "Unsere Filialen"],
    "Werken bij": ["Careers", "Karriere"],
    "Algemene voorwaarden": ["Terms & conditions", "AGB"],
    "Privacy": ["Privacy", "Datenschutz"],
    "Nieuwsbrief": ["Newsletter", "Newsletter"],
    "Aanmelden": ["Sign up", "Anmelden"],
    "Placeholder-formulier — verstuurt niets.":
      ["Placeholder form — sends nothing.", "Platzhalter-Formular — sendet nichts."],
    "Prijzen incl. btw • Geen officiële shop":
      ["Prices incl. VAT • Not an official shop",
       "Preise inkl. MwSt. • Kein offizieller Shop"],
    "© 2026 BETA STORE — Concept store testomgeving":
      ["© 2026 BETA STORE — Concept store test environment",
       "© 2026 BETA STORE — Concept-Store-Testumgebung"],

    /* losse labels */
    "In winkelmand": ["Add to cart", "In den Warenkorb"],
    "Bekijk alles": ["View all", "Alle ansehen"],
    "Alle merken": ["All brands", "Alle Marken"],
    "Lees meer": ["Read more", "Mehr lesen"],
    "Nieuw": ["New", "Neu"],
    "Maat": ["Size", "Größe"],
    "Aanbevolen": ["Featured", "Empfohlen"],
    "Alles": ["All", "Alle"],
    "producten": ["products", "Produkte"],
    "Vind een winkel": ["Find a store", "Filiale finden"],
    "Shop de collectie": ["Shop the collection", "Kollektion shoppen"],

    /* about.html */
    "Onze missie ;": ["Our mission ;", "Unsere Mission ;"],
    "Over N\u00b09": ["About N\u00b09", "\u00dcber N\u00b09"],
    "Onze eigenaren ;": ["Our owners ;", "Unsere Inhaber ;"],
    "Achtergrond": ["Background", "Hintergrund"],

    /* tour-teaser op de homepage */
    "Pop-uptour \u00b7 Duitsland \u00b7 2027": ["Pop-up tour \u00b7 Germany \u00b7 2027",
                                             "Pop-up-Tour \u00b7 Deutschland \u00b7 2027"],
    "Dortmund, D\u00fcsseldorf, M\u00fcnchen, Berlijn \u2014 vier steden, twee weken per stad, en de grootste namen uit geur en mode op de gastenlijst.":
      ["Dortmund, D\u00fcsseldorf, Munich, Berlin \u2014 four cities, two weeks each, and the biggest names in scent and fashion on the guest list.",
       "Dortmund, D\u00fcsseldorf, M\u00fcnchen, Berlin \u2014 vier St\u00e4dte, je zwei Wochen, und die gr\u00f6\u00dften Namen aus Duft und Mode auf der G\u00e4steliste."],
    "Bekijk de tour": ["See the tour", "Zur Tour"]
  };

  /* Omgekeerde index: voor elke taal een map van "tekst in willekeurige taal"
     -> rij, zodat je ook van EN terug naar NL kunt. */
  var ROWS = [];
  Object.keys(CHROME).forEach(function (nl) {
    ROWS.push({ nl: nl, en: CHROME[nl][0], de: CHROME[nl][1] });
  });
  var INDEX = {};
  ROWS.forEach(function (row) {
    LANGS.forEach(function (l) {
      var t = row[l];
      if (t && !(t in INDEX)) INDEX[t] = row;
    });
  });

  var DICT = window.__TOUR_I18N__ || {};

  function current() {
    var saved = store.getItem(KEY);
    return LANGS.indexOf(saved) > -1 ? saved : DEFAULT;
  }

  /* ---------- tekstknopen vertalen via het chrome-woordenboek ----------
     Eén keer scannen, daarna alleen nog nodeValue zetten. Zo kun je heen en
     weer schakelen zonder de pagina te herladen. */
  var SKIP = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1 };
  var textHits = [];   /* {node, lead, tail, row} */
  var attrHits = [];   /* {el, attr, row} */

  function scanChrome() {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = n.parentNode;
        if (!p || SKIP[p.nodeName]) return NodeFilter.FILTER_REJECT;
        if (p.closest && p.closest("[data-i18n]")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = walker.nextNode())) {
      var raw = n.nodeValue;
      var trimmed = raw.trim();
      var row = INDEX[trimmed];
      if (!row) continue;
      var at = raw.indexOf(trimmed);
      textHits.push({ node: n, lead: raw.slice(0, at), tail: raw.slice(at + trimmed.length), row: row });
    }

    ["placeholder", "aria-label", "title"].forEach(function (attr) {
      document.querySelectorAll("[" + attr + "]").forEach(function (elm) {
        if (attr === "placeholder" && elm.hasAttribute("data-i18n-ph")) return;
        var row = INDEX[(elm.getAttribute(attr) || "").trim()];
        if (row) attrHits.push({ el: elm, attr: attr, row: row });
      });
    });
  }

  function applyChrome(lang) {
    textHits.forEach(function (h) {
      if (h.row[lang]) h.node.nodeValue = h.lead + h.row[lang] + h.tail;
    });
    attrHits.forEach(function (h) {
      if (h.row[lang]) h.el.setAttribute(h.attr, h.row[lang]);
    });
  }

  /* ---------- keyed vertalingen (tourpagina) ---------- */
  function applyKeys(lang) {
    document.querySelectorAll("[data-i18n]").forEach(function (elm) {
      var entry = DICT[elm.getAttribute("data-i18n")];
      if (entry && entry[lang]) elm.textContent = entry[lang];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (elm) {
      var entry = DICT[elm.getAttribute("data-i18n-ph")];
      if (entry && entry[lang]) elm.setAttribute("placeholder", entry[lang]);
    });
  }

  function apply(lang) {
    applyKeys(lang);
    applyChrome(lang);
    document.documentElement.setAttribute("lang", lang);
    document.querySelectorAll(".lang-switch [data-lang]").forEach(function (a) {
      var on = a.getAttribute("data-lang") === lang;
      a.classList.toggle("is-active", on);
      a.setAttribute("aria-current", on ? "true" : "false");
    });
  }

  function set(lang) {
    if (LANGS.indexOf(lang) < 0) return;
    store.setItem(KEY, lang);
    apply(lang);
  }

  /* ---------- schakelaar ---------- */
  function switchMarkup() {
    var html = '<div class="lang-switch" role="group" aria-label="Language">';
    LANGS.forEach(function (l, i) {
      if (i) html += '<span class="lang-switch__sep">/</span>';
      html += '<a href="#" class="lang-switch__item" data-lang="' + l + '">' + LABEL[l] + "</a>";
    });
    return html + "</div>";
  }

  function mountSwitch() {
    /* Bestaande, nog niet werkende schakelaar (about.html) overschrijven. */
    document.querySelectorAll(".lang-switch").forEach(function (sw) {
      if (!sw.querySelector("[data-lang]")) sw.outerHTML = switchMarkup();
    });
    /* Anders: er zelf een in de header hangen. */
    if (!document.querySelector(".lang-switch")) {
      var actions = document.querySelector(".hdr__actions");
      if (actions) {
        var holder = document.createElement("div");
        holder.className = "lang-switch lang-switch--hdr";
        holder.innerHTML = switchMarkup();
        actions.insertBefore(holder.firstChild, actions.firstChild);
      }
    }
    document.addEventListener("click", function (e) {
      var a = e.target.closest(".lang-switch [data-lang]");
      if (!a) return;
      e.preventDefault();
      set(a.getAttribute("data-lang"));
    });
  }

  function init() {
    mountSwitch();
    scanChrome();
    apply(current());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
