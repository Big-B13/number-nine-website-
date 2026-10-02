#!/usr/bin/env python3
"""
Statische site-generator voor de BETA webshop-omgeving (NL).

Genereert de HTML-pagina's in de repository-root plus js/data.js, voor een
plain HTML/CSS/JS-site die 1-op-1 op GitHub Pages kan worden gezet:

    index.html  about.html  collection.html  product.html  cart.html
    brands.html  stores.html  account.html  404.html
    css/style.css   <- bron: handmatig bewerken (wordt gelinkt in elke pagina)
    js/app.js       <- bron: handmatig bewerken
    js/data.js      <- door build.py gegenereerd (productdata) — niet handmatig bewerken

Structuur volgt een multi-brand modewinkel: Dames / Heren / Merken / Sale /
Winkels / Over ons. Alle teksten en beelden zijn placeholder-materiaal.

Gebruik:  python3 build.py    ->  herschrijft de pagina's + js/data.js
Lokaal testen:  python3 -m http.server 8080   ->  http://localhost:8080
"""
import json, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).parent
DATA_FILE = ROOT / "js" / "data.js"

SITE = {
    "name": "BETA STORE",
    "description": "Beta-omgeving van een multi-brand concept store — placeholder content.",
    "announcements": [
        "Betaomgeving — er worden geen echte bestellingen verwerkt",
        "Gratis verzending vanaf €50 — voorbeeldtekst",
        "Zes winkels — placeholder",
    ],
}

# ---------------------------------------------------------------- navigatie
NAV = [
    ("Dames", "collection.html?c=dames", [
        ("Nieuw binnen", ["New in dames", "Net binnen", "Preorder"]),
        ("Kleding", ["Jassen", "Truien & vesten", "Tops & blouses",
                     "Jurken & rokken", "Broeken", "Jeans"]),
        ("Accessoires", ["Tassen", "Sieraden", "Riemen", "Sjaals", "Mutsen"]),
        ("Schoenen", ["Sneakers", "Laarzen", "Loafers"]),
    ]),
    ("Heren", "collection.html?c=heren", [
        ("Nieuw binnen", ["New in heren", "Net binnen", "Preorder"]),
        ("Kleding", ["Jassen", "Truien & vesten", "Overhemden", "T-shirts",
                     "Broeken", "Jeans"]),
        ("Accessoires", ["Tassen", "Riemen", "Mutsen", "Sokken"]),
        ("Schoenen", ["Sneakers", "Boots", "Nette schoenen"]),
    ]),
    ("Merken", "brands.html", None),
    ("Sale", "collection.html?c=sale", None),
    ("Winkels", "stores.html", None),
    ("Pop-up Tour", "event.html", None),
    ("Over ons", "about.html", None),
]

# ---------------------------------------------------------------- beelden
def swatch(seed, w=800, h=1000, label="BEELD"):
    """Inline SVG data-URI placeholder — geen netwerk of image-bestanden nodig.
    Eigen fotografie: zet bestanden in images/ en zet bij een product het pad
    (bijv. images/jas-voor.jpg) als img/img2 in de _items-lijst hieronder."""
    label = str(label).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    hues = [("#efe9e1", "#d6cabb"), ("#e3e7ea", "#c4ccd3"), ("#e9e3ea", "#cec5d4"),
            ("#e5eae3", "#c7d1c4"), ("#f1e8e1", "#dbc9bb"), ("#e2e8ec", "#c1ced7")]
    a, b = hues[seed % len(hues)]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>'
           f'</linearGradient></defs><rect width="{w}" height="{h}" fill="url(#g)"/>'
           f'<text x="50%" y="50%" text-anchor="middle" font-family="Helvetica,Arial" '
           f'font-size="{int(w/24)}" fill="#8d8579" letter-spacing="6">{label}</text></svg>')
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)

# ---------------------------------------------------------------- catalogus
_items = [
    ("Vest met V-hals", "MERK EEN", 119.99, "dames", "Vesten"),
    ("Gewaxte jas", "MERK TWEE", 379.99, "heren", "Jassen"),
    ("Gebreid vest", "MERK DRIE", 99.99, "dames", "Vesten"),
    ("Wijde broek", "MERK VIER", 119.99, "heren", "Broeken"),
    ("Korte jas", "MERK EEN", 159.99, "dames", "Jassen"),
    ("Zip-hoodie", "MERK VIJF", 169.99, "heren", "Truien"),
    ("Oversized blouse", "MERK TWEE", 89.99, "dames", "Blouses"),
    ("Rechte jeans", "MERK ZES", 109.99, "heren", "Jeans"),
    ("Midi rok", "MERK DRIE", 79.99, "dames", "Rokken"),
    ("Wollen overshirt", "MERK VIER", 189.99, "heren", "Jassen"),
    ("Ribgebreide trui", "MERK VIJF", 94.99, "dames", "Truien"),
    ("Linnen overhemd", "MERK ZES", 74.99, "heren", "Overhemden"),
    ("Leren tas", "MERK EEN", 149.99, "dames", "Tassen"),
    ("Grove sneaker", "MERK TWEE", 139.99, "heren", "Schoenen"),
    ("Gilet", "MERK DRIE", 99.99, "dames", "Jassen"),
    ("Cargobroek", "MERK VIER", 109.99, "heren", "Broeken"),
]
PRODUCTS = []
for i, (t, b, pr, cat, typ) in enumerate(_items):
    sale = i % 5 == 0
    PRODUCTS.append({
        "id": f"p{i+1:02d}", "title": t, "brand": b,
        "price": round(pr * 0.7, 2) if sale else pr,
        "compare": pr if sale else None,
        "cat": cat, "type": typ,
        "tag": "Sale" if sale else ("Nieuw" if i < 4 else ""),
        "img": swatch(i, label=f"PRODUCT {i+1:02d}"),
        "img2": swatch(i + 3, label="2E BEELD"),
    })

BRANDS = sorted({p["brand"] for p in PRODUCTS}) + [f"MERK {n}" for n in
    ["ZEVEN", "ACHT", "NEGEN", "TIEN", "ELF", "TWAALF", "DERTIEN", "VEERTIEN",
     "VIJFTIEN", "ZESTIEN", "ZEVENTIEN", "ACHTTIEN"]]

STORES = [
    ("Winkel Haarlem", "Voorbeeldstraat 9", "2011 AA Haarlem", "023 000 0000"),
    ("Winkel Amsterdam", "Voorbeeldstraat 14", "1011 BB Amsterdam", "020 000 0000"),
    ("Winkel Utrecht", "Voorbeeldstraat 3", "3511 CC Utrecht", "030 000 0000"),
    ("Winkel Alkmaar", "Voorbeeldstraat 21", "1811 DD Alkmaar", "072 000 0000"),
    ("Winkel Leiden", "Voorbeeldstraat 7", "2311 EE Leiden", "071 000 0000"),
    ("Winkel Den Haag", "Voorbeeldstraat 48", "2511 FF Den Haag", "070 000 0000"),
]

# ---------------------------------------------------------------- partials
def mega(cols):
    inner = "".join(
        '<div class="mega__col"><h5>' + head + '</h5>' +
        "".join(f'<a href="collection.html">{l}</a>' for l in links) + "</div>"
        for head, links in cols
    )
    promo = (f'<a class="mega__promo" href="collection.html">'
             f'<img src="{swatch(2, 600, 400, "CAMPAGNE")}" alt="">'
             f'<span>Bekijk de nieuwe collectie</span></a>')
    return f'<div class="mega"><div class="mega__inner">{inner}{promo}</div></div>'

def header(active):
    ann = "".join(f'<span class="ann__item">{a}</span>' for a in SITE["announcements"] * 2)
    nav = ""
    for label, href, cols in NAV:
        cls = " is-active" if label == active else ""
        if cols:
            nav += (f'<div class="nav__item has-mega"><a class="nav__link{cls}" href="{href}">{label}</a>'
                    f'{mega(cols)}</div>')
        else:
            nav += f'<div class="nav__item"><a class="nav__link{cls}" href="{href}">{label}</a></div>'
    mob = ""
    for label, href, cols in NAV:
        if cols:
            sub = "".join(f'<a href="collection.html">{l}</a>'
                          for _, links in cols for l in links)
            mob += (f'<details><summary>{label}</summary><div class="drawer__sub">'
                    f'<a href="{href}"><strong>Alles in {label}</strong></a>{sub}</div></details>')
        else:
            mob += f'<a class="drawer__top" href="{href}">{label}</a>'
    return f"""
<div class="beta-flag">BETA / TESTOMGEVING — placeholder content</div>
<div class="ann"><div class="ann__track">{ann}</div></div>
<header class="hdr">
  <div class="hdr__inner">
    <button class="icon-btn hdr__burger" aria-label="Menu" data-open="menu">
      <svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <a class="logo" href="index.html">{SITE['name']}</a>
    <div class="hdr__actions">
      <button class="icon-btn" aria-label="Zoeken" data-open="search">
        <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      </button>
      <a class="icon-btn" href="account.html" aria-label="Account">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/></svg>
      </a>
      <button class="icon-btn" aria-label="Winkelmand" data-open="cart">
        <svg viewBox="0 0 24 24"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7V5a3 3 0 016 0v2"/></svg>
        <span class="cart-count" data-cart-count>0</span>
      </button>
    </div>
  </div>
  <nav class="nav">{nav}</nav>
</header>

<div class="drawer" id="menu" hidden>
  <div class="drawer__panel drawer__panel--left">
    <div class="drawer__head"><strong>Menu</strong><button class="icon-btn" data-close>&times;</button></div>
    <nav class="drawer__nav">{mob}</nav>
  </div>
</div>

<div class="drawer" id="search" hidden>
  <div class="drawer__panel drawer__panel--top">
    <div class="drawer__head"><strong>Zoeken</strong><button class="icon-btn" data-close>&times;</button></div>
    <input class="search-input" type="search" placeholder="Zoek op product of merk..." data-search-input>
    <div class="search-results" data-search-results><p class="muted">Begin met typen om de testcatalogus te doorzoeken.</p></div>
  </div>
</div>

<div class="drawer" id="cart" hidden>
  <div class="drawer__panel drawer__panel--right">
    <div class="drawer__head"><strong>Winkelmand</strong><button class="icon-btn" data-close>&times;</button></div>
    <div class="cart-lines" data-cart-lines></div>
    <div class="cart-foot">
      <div class="cart-total"><span>Subtotaal</span><span data-cart-total>&euro;0,00</span></div>
      <p class="muted small">Betaomgeving — afrekenen is uitgeschakeld.</p>
      <a class="btn btn--block" href="cart.html">Naar winkelmand</a>
    </div>
  </div>
</div>
"""

FOOTER = f"""
<footer class="ftr">
  <div class="ftr__grid">
    <div><h4>Klantenservice</h4>
      <a href="#">Verzending</a><a href="#">Retourneren</a><a href="#">Maattabel</a>
      <a href="#">Veelgestelde vragen</a><a href="#">Contact</a></div>
    <div><h4>Shoppen</h4>
      <a href="collection.html?c=dames">Dames</a><a href="collection.html?c=heren">Heren</a>
      <a href="brands.html">Merken</a><a href="collection.html?c=sale">Sale</a>
      <a href="#">Cadeaubon</a></div>
    <div><h4>Over</h4>
      <a href="about.html">Over ons</a><a href="stores.html">Onze winkels</a>
      <a href="event.html">Pop-up Tour</a>
      <a href="#">Werken bij</a><a href="#">Algemene voorwaarden</a><a href="#">Privacy</a></div>
    <div class="ftr__news"><h4>Nieuwsbrief</h4>
      <p class="muted small">Placeholder-formulier — verstuurt niets.</p>
      <form class="news" onsubmit="return false;">
        <input type="email" placeholder="jouw@email.nl" required>
        <button class="btn" type="submit">Aanmelden</button>
      </form>
      <div class="pay"><span>iDEAL</span><span>Klarna</span><span>PayPal</span><span>Visa</span></div>
    </div>
  </div>
  <div class="ftr__bar">
    <span>&copy; 2026 {SITE['name']} — betaomgeving</span>
    <span class="muted small">Alle teksten en beelden in deze build zijn placeholder-materiaal.</span>
  </div>
</footer>
"""

FAVICON = ("data:image/svg+xml," + urllib.parse.quote(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" fill="#15130f"/>'
    '<text x="16" y="22" text-anchor="middle" font-family="Helvetica,Arial" '
    'font-size="17" font-weight="700" fill="#ffffff">B</text></svg>'))

def eur(v):
    return "&euro;" + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def card(p):
    tag = f'<span class="card__tag">{p["tag"]}</span>' if p["tag"] else ""
    cmp_ = f'<s>{eur(p["compare"])}</s>' if p["compare"] else ""
    return f"""
<article class="card" data-cat="{p['cat']}" data-title="{p['title']}" data-brand="{p['brand']}" data-price="{p['price']}" data-sale="{1 if p['compare'] else 0}">
  <a class="card__media" href="product.html?id={p['id']}">
    {tag}
    <img src="{p['img']}" alt="{p['title']}" loading="lazy">
    <img class="card__alt" src="{p['img2']}" alt="" loading="lazy">
  </a>
  <div class="card__body">
    <span class="card__brand">{p['brand']}</span>
    <a class="card__title" href="product.html?id={p['id']}">{p['title']}</a>
    <div class="card__price">{eur(p['price'])} {cmp_}</div>
    <button class="btn btn--ghost btn--sm" data-add="{p['id']}">In winkelmand</button>
  </div>
</article>"""

def page(title, active, body):
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="description" content="{SITE['description']}">
<title>{title} | {SITE['name']} (beta)</title>
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="js/data.js"></script>
<script src="js/i18n.js"></script>
<script src="js/app.js"></script>
</body>
</html>"""

# ---------------------------------------------------------------- pagina's
def home():
    return page("Home", "", f"""
<section class="hero-split">
  <a class="hero-card" href="collection.html?c=heren">
    <img src="{swatch(1, 1200, 1400, 'CAMPAGNE HEREN')}" alt="">
    <div class="hero-card__copy"><h2>New in store</h2><span class="btn btn--light">Shop heren</span></div>
  </a>
  <a class="hero-card" href="collection.html?c=dames">
    <img src="{swatch(4, 1200, 1400, 'CAMPAGNE DAMES')}" alt="">
    <div class="hero-card__copy"><h2>New in store</h2><span class="btn btn--light">Shop dames</span></div>
  </a>
</section>

<a class="tour-teaser" href="event.html">
  <img src="img/tour/hero.jpg" alt="">
  <div class="tour-teaser__copy">
    <p class="tour-eyebrow">Pop-up tour &middot; Germany &middot; 2027</p>
    <h2>ROUTE <span>NINE</span></h2>
    <p>Dortmund, D&uuml;sseldorf, M&uuml;nchen, Berlijn &mdash; vier steden, twee weken per stad, en de grootste namen uit geur en mode op de gastenlijst.</p>
    <span class="btn btn--light">Bekijk de tour</span>
  </div>
</a>

<section class="usp">
  <div>Gratis verzending vanaf &euro;50</div><div>Zes winkels</div>
  <div>30 dagen bedenktijd</div><div>Persoonlijk stijladvies</div>
</section>

<section class="section">
  <div class="section__head"><h2>Nieuw binnen</h2><a class="link" href="collection.html">Bekijk alles</a></div>
  <div class="grid">{''.join(card(p) for p in PRODUCTS[:8])}</div>
</section>

<section class="section">
  <div class="section__head"><h2>Shop per categorie</h2></div>
  <div class="tiles">{''.join(f'''
    <a class="tile" href="collection.html">
      <img src="{swatch(i+2, 900, 700, n.upper())}" alt="">
      <span class="tile__label">{n}</span></a>''' for i, n in
      enumerate(["Jassen", "Truien & vesten", "Broeken", "Accessoires"]))}</div>
</section>

<section class="split">
  <img src="{swatch(3, 1000, 800, 'WINKELBEELD')}" alt="">
  <div class="split__copy">
    <p class="eyebrow">Over ons</p>
    <h2>Een multi-brand concept store</h2>
    <p>Korte introductietekst over het concept, de winkels en de manier van inkopen.
       Vervang deze alinea door je eigen copy.</p>
    <a class="btn" href="about.html">Lees meer</a>
  </div>
</section>

<section class="section">
  <div class="section__head"><h2>Onze merken</h2><a class="link" href="brands.html">Alle merken</a></div>
  <div class="brand-strip">{''.join(f'<a href="brands.html">{b}</a>' for b in BRANDS[:10])}</div>
</section>
""")

def about():
    return page("Over ons", "Over ons", f"""
<div class="page page--narrow">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Over ons</span></nav>
  <img class="page__hero" src="{swatch(0, 1400, 700, 'WINKELPUI')}" alt="">
  <h1>Over ons</h1>
  <p class="lede">Openingszin: wie je bent, wanneer de winkel is gestart en waar het begon.</p>
  <p>Alinea 1 — het aanbod: dames- en herencollecties, accessoires en lifestyleproducten,
     van gevestigde namen tot nieuwe labels.</p>
  <p>Alinea 2 — de inkoopfilosofie: hoe de collectie wordt samengesteld en hoe de balans
     tussen prijs en kwaliteit wordt bewaakt.</p>
  <p>Alinea 3 — het winkelnetwerk: het aantal vestigingen, hoe elke winkel een eigen
     assortiment heeft en dat de volledige collectie online staat.</p>
  <p>Alinea 4 — wat de klant in de winkel kan verwachten: service, stijladvies en sfeer.</p>
  <p>Afsluitende welkomstzin.</p>
  <div class="cta-row">
    <a class="btn" href="stores.html">Vind een winkel</a>
    <a class="btn btn--ghost" href="collection.html">Shop de collectie</a>
  </div>
</div>
""")

def collection():
    types = sorted({p["type"] for p in PRODUCTS})
    tchips = "".join(f'<button class="chip" data-type="{t}">{t}</button>' for t in types)
    return page("Collectie", "", f"""
<div class="page">
  <nav class="crumbs"><a href="index.html">Home</a> / <span data-coll-crumb>Collectie</span></nav>
  <h1 data-coll-title>Alle producten</h1>
  <p class="muted"><span data-count>{len(PRODUCTS)}</span> producten</p>

  <div class="toolbar">
    <div class="filters">
      <button class="chip is-active" data-filter="all">Alles</button>
      <button class="chip" data-filter="dames">Dames</button>
      <button class="chip" data-filter="heren">Heren</button>
      <button class="chip" data-filter="sale">Sale</button>
    </div>
    <select class="select" data-sort>
      <option value="featured">Aanbevolen</option>
      <option value="price-asc">Prijs: laag naar hoog</option>
      <option value="price-desc">Prijs: hoog naar laag</option>
      <option value="title">Alfabetisch</option>
    </select>
  </div>
  <div class="filters filters--sub">{tchips}</div>

  <div class="grid" data-grid>{''.join(card(p) for p in PRODUCTS)}</div>
</div>
""")

def product():
    return page("Product", "", f"""
<div class="page">
  <nav class="crumbs"><a href="index.html">Home</a> / <a href="collection.html">Collectie</a> / <span data-pdp-crumb></span></nav>
  <div class="pdp">
    <div class="pdp__media">
      <img data-pdp-img src="" alt=""><img data-pdp-img2 src="" alt="">
    </div>
    <div class="pdp__info">
      <span class="card__brand" data-pdp-brand></span>
      <h1 data-pdp-title></h1>
      <div class="pdp__price" data-pdp-price></div>
      <div class="pdp__sizes">
        <span class="label">Maat</span>
        <div class="sizes">
          <button class="size">XS</button><button class="size is-active">S</button>
          <button class="size">M</button><button class="size">L</button>
          <button class="size is-oos">XL</button>
        </div>
      </div>
      <button class="btn btn--block" data-pdp-add>In winkelmand</button>
      <p class="muted small">Betaomgeving — er wordt niet betaald.</p>
      <ul class="pdp__usp"><li>Gratis verzending vanaf &euro;50</li>
        <li>30 dagen retourrecht</li><li>Op voorraad in de winkel</li></ul>
      <details open><summary>Omschrijving</summary><p>Placeholder productomschrijving. Hier komen materiaal, pasvorm en wasvoorschrift.</p></details>
      <details><summary>Verzending &amp; retour</summary><p>Placeholder verzend- en retourinformatie.</p></details>
      <details><summary>Over het merk</summary><p>Placeholder merkverhaal.</p></details>
    </div>
  </div>
  <section class="section">
    <div class="section__head"><h2>Anderen bekeken ook</h2></div>
    <div class="grid">{''.join(card(p) for p in PRODUCTS[4:8])}</div>
  </section>
</div>
""")

def cart():
    return page("Winkelmand", "", """
<div class="page page--narrow">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Winkelmand</span></nav>
  <h1>Winkelmand</h1>
  <div data-cart-page></div>
  <div class="cart-foot cart-foot--page">
    <div class="cart-total"><span>Subtotaal</span><span data-cart-total>&euro;0,00</span></div>
    <p class="muted small">Verzendkosten worden berekend bij het afrekenen.</p>
    <button class="btn btn--block" disabled>Afrekenen uitgeschakeld in beta</button>
  </div>
</div>
""")

def brands():
    return page("Merken", "Merken", f"""
<div class="page">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Merken</span></nav>
  <h1>Merken</h1>
  <p class="muted">{len(BRANDS)} placeholder-merken in de testcatalogus.</p>
  <div class="brand-grid">{''.join(f'<a class="brand-tile" href="collection.html">{b}</a>' for b in BRANDS)}</div>
</div>
""")

def stores():
    cards = "".join(f"""
    <article class="store">
      <img src="{swatch(i, 800, 600, 'WINKEL ' + str(i+1))}" alt="">
      <h3>{n}</h3>
      <p class="muted">{a}
{c}
{tel}</p>
      <p class="small">ma–za 10:00–18:00
zo 12:00–17:00</p>
      <a class="link" href="#">Route</a>
    </article>""" for i, (n, a, c, tel) in enumerate(STORES))
    return page("Winkels", "Winkels", f"""
<div class="page">
  <nav class="crumbs"><a href="index.html">Home</a> / <span>Winkels</span></nav>
  <h1>Onze winkels</h1>
  <p class="muted">Zes placeholder-vestigingen.</p>
  <div class="stores">{cards}</div>
</div>
""")

def account():
    return page("Account", "", """
<div class="page page--narrow">
  <h1>Mijn account</h1>
  <div class="auth">
    <form onsubmit="return false;">
      <h3>Inloggen</h3>
      <label>E-mail<input type="email" required></label>
      <label>Wachtwoord<input type="password" required></label>
      <button class="btn btn--block">Inloggen</button>
      <p class="muted small">Inloggen is gestubd in deze betabuild.</p>
    </form>
    <form onsubmit="return false;">
      <h3>Account aanmaken</h3>
      <label>Voornaam<input></label>
      <label>E-mail<input type="email"></label>
      <label>Wachtwoord<input type="password"></label>
      <button class="btn btn--ghost btn--block">Registreren</button>
    </form>
  </div>
</div>
""")

def notfound():
    return page("Niet gevonden", "", """
<div class="page page--narrow center">
  <h1>404</h1><p class="muted">Deze pagina bestaat niet in de betabuild.</p>
  <a class="btn" href="index.html">Terug naar home</a>
</div>
""")

PAGES = {
    "index.html": home, "about.html": about, "collection.html": collection,
    "product.html": product, "cart.html": cart, "brands.html": brands,
    "stores.html": stores, "account.html": account, "404.html": notfound,
}

if __name__ == "__main__":
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        "/* Gegenereerd door build.py -- niet handmatig bewerken. */\n"
        "window.__PRODUCTS__ = " + json.dumps(PRODUCTS) + ";\n",
        encoding="utf-8",
    )
    print("geschreven: js/data.js", f"({DATA_FILE.stat().st_size // 1024}kb)")
    for name, fn in PAGES.items():
        html = fn()
        (ROOT / name).write_text(html, encoding="utf-8")
        print("geschreven:", name, f"({len(html) // 1024}kb)")
    (ROOT / ".nojekyll").write_text("")
    print(".nojekyll bijgewerkt")
    print("Klaar. Lokaal testen:  python3 -m http.server 8080")
