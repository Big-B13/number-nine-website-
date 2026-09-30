/* Storefront beta - clientlogica (NL). Geen dependencies, geen netwerkverzoeken. */
(function () {
  var P = window.__PRODUCTS__ || [];
  var byId = {};
  P.forEach(function (p) { byId[p.id] = p; });

  /* Opslag met fallback: in sandboxed previews (bijv. een file-viewer) is
     localStorage vaak geblokkeerd; de winkelmand werkt dan in-memory verder. */
  var store = (function () {
    try {
      var k = "__beta_probe";
      localStorage.setItem(k, "1");
      localStorage.removeItem(k);
      return localStorage;
    } catch (e) {
      var mem = {};
      return {
        getItem: function (key) { return key in mem ? mem[key] : null; },
        setItem: function (key, val) { mem[key] = String(val); },
        removeItem: function (key) { delete mem[key]; }
      };
    }
  })();

  var KEY = "beta-cart-v1";
  function load() { try { return JSON.parse(store.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(c) { store.setItem(KEY, JSON.stringify(c)); render(); }
  var cart = load();

  function money(n) {
    var s = n.toFixed(2).split(".");
    s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return "\u20AC" + s[0] + "," + s[1];
  }

  function add(id) {
    var l = cart.filter(function (x) { return x.id === id; })[0];
    if (l) l.qty++; else cart.push({ id: id, qty: 1 });
    save(cart);
    toast(byId[id].title + " toegevoegd aan de winkelmand");
  }
  function setQty(id, q) {
    cart = cart.map(function (x) { return x.id === id ? { id: id, qty: q } : x; })
               .filter(function (x) { return x.qty > 0; });
    save(cart);
  }

  function lineHTML(l, p) {
    return '<div class="line">' +
      '<img src="' + p.img + '" alt="">' +
      '<div><span class="card__brand">' + p.brand + '</span>' +
      '<div class="line__title">' + p.title + '</div>' +
      '<div class="qty"><button data-q="' + p.id + '|' + (l.qty - 1) + '">-</button>' +
      '<span>' + l.qty + '</span>' +
      '<button data-q="' + p.id + '|' + (l.qty + 1) + '">+</button></div></div>' +
      '<div>' + money(p.price * l.qty) + '</div></div>';
  }

  function render() {
    var total = 0, count = 0, html = "";
    cart.forEach(function (l) {
      var p = byId[l.id]; if (!p) return;
      total += p.price * l.qty; count += l.qty;
      html += lineHTML(l, p);
    });
    if (!html) html = '<div class="empty">Je winkelmand is leeg.</div>';
    document.querySelectorAll("[data-cart-lines],[data-cart-page]").forEach(function (n) { n.innerHTML = html; });
    document.querySelectorAll("[data-cart-total]").forEach(function (n) { n.textContent = money(total); });
    document.querySelectorAll("[data-cart-count]").forEach(function (n) {
      n.textContent = count; n.style.display = count ? "grid" : "none";
    });
  }

  var t;
  function toast(msg) {
    clearTimeout(t);
    var el = document.querySelector(".toast");
    if (!el) { el = document.createElement("div"); el.className = "toast"; document.body.appendChild(el); }
    el.textContent = msg;
    t = setTimeout(function () { el.remove(); }, 2200);
  }

  /* ---------- drawers met slide-animatie ---------- */
  var REDUCED = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  function openDrawer(d) {
    if (!d) return;
    if (d.__closeTimer) { clearTimeout(d.__closeTimer); d.__closeTimer = null; }
    d.classList.remove("is-closing");
    var p = d.querySelector(".drawer__panel");
    if (p) p.classList.remove("is-closing");
    d.hidden = false;
  }

  function closeDrawer(d) {
    if (!d || d.hidden || d.__closeTimer) return;
    var panel = d.querySelector(".drawer__panel");
    if (!REDUCED && panel) {
      d.classList.add("is-closing");
      panel.classList.add("is-closing");
      d.__closeTimer = setTimeout(function () {
        d.__closeTimer = null;
        d.hidden = true;
        d.classList.remove("is-closing");
        panel.classList.remove("is-closing");
      }, 280);
    } else {
      d.hidden = true;
    }
  }

  /* ---------- navigatie: Menu-knop rechts + slide-out-paneel ----------
     Werkt ook op de bestaande pagina's zonder ze aan te passen:
     - het menupaneel schuift nu vanaf de rechterkant in
     - Home komt bovenaan de lijst te staan
     - de Menu-knop wordt rechts in de header geplaatst              */
  var menu = document.getElementById("menu");
  if (menu) {
    var mPanel = menu.querySelector(".drawer__panel");
    if (mPanel) {
      mPanel.classList.remove("drawer__panel--left");
      mPanel.classList.add("drawer__panel--right", "drawer__panel--nav");
    }
    var mNav = menu.querySelector(".drawer__nav");
    if (mNav && !mNav.querySelector('a[href="index.html"]')) {
      var homeLink = document.createElement("a");
      homeLink.href = "index.html";
      homeLink.textContent = "Home";
      if (/(^|\/)index\.html$/.test(location.pathname) || location.pathname.endsWith("/")) {
        homeLink.className = "is-active";
      }
      mNav.insertBefore(homeLink, mNav.firstChild);
    }
    var actions = document.querySelector(".hdr__actions");
    if (actions && !document.querySelector(".menu-btn")) {
      var menuBtn = document.createElement("button");
      menuBtn.type = "button";
      menuBtn.className = "menu-btn";
      menuBtn.setAttribute("data-open", "menu");
      menuBtn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><span>Menu</span>';
      actions.appendChild(menuBtn);
    }
  }

  /* ---------- filters: categorie + type gecombineerd ---------- */
  var activeCat = "all", activeType = "all";

  function applyFilters() {
    var visible = 0;
    document.querySelectorAll("[data-grid] .card").forEach(function (c) {
      var okCat = activeCat === "all" ||
        (activeCat === "sale" ? c.dataset.sale === "1" : c.dataset.cat === activeCat);
      var okType = activeType === "all" || c.dataset.type === activeType;
      var show = okCat && okType;
      c.style.display = show ? "" : "none";
      if (show) visible++;
    });
    var cnt = document.querySelector("[data-count]");
    if (cnt) cnt.textContent = visible;
  }

  /* ---------- collectiepagina: ?c=dames / heren / sale ---------- */
  var collTitle = document.querySelector("[data-coll-title]");
  if (collTitle) {
    var c = new URLSearchParams(location.search).get("c");
    var names = { dames: "Dames", heren: "Heren", sale: "Sale" };
    if (names[c]) {
      collTitle.textContent = names[c];
      var crumb = document.querySelector("[data-coll-crumb]");
      if (crumb) crumb.textContent = names[c];
      var chip = document.querySelector('.filters:not(.filters--sub) .chip[data-filter="' + c + '"]');
      if (chip) {
        document.querySelectorAll(".filters:not(.filters--sub) .chip").forEach(function (x) { x.classList.remove("is-active"); });
        chip.classList.add("is-active");
        activeCat = c;
        applyFilters();
      }
    }
  }

  /* ---------- globale click-afhandeling ---------- */
  document.addEventListener("click", function (e) {
    var o = e.target.closest("[data-open]");
    if (o) { openDrawer(document.getElementById(o.dataset.open)); return; }

    if (e.target.closest("[data-close]") ||
        (e.target.classList && e.target.classList.contains("drawer"))) {
      closeDrawer(e.target.closest(".drawer")); return;
    }

    var a = e.target.closest("[data-add]");
    if (a) { add(a.dataset.add); return; }

    var q = e.target.closest("[data-q]");
    if (q) { var s = q.dataset.q.split("|"); setQty(s[0], parseInt(s[1], 10)); return; }

    var sz = e.target.closest(".size:not(.is-oos)");
    if (sz) {
      sz.parentNode.querySelectorAll(".size").forEach(function (x) { x.classList.remove("is-active"); });
      sz.classList.add("is-active"); return;
    }

    var chip = e.target.closest(".chip");
    if (chip) {
      var group = chip.closest(".filters") || chip.parentNode;
      if (chip.dataset.filter) {
        group.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("is-active"); });
        chip.classList.add("is-active");
        activeCat = chip.dataset.filter;
      } else if (chip.dataset.type) {
        var was = chip.classList.contains("is-active");
        group.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("is-active"); });
        if (was) { activeType = "all"; }
        else { chip.classList.add("is-active"); activeType = chip.dataset.type; }
      }
      applyFilters(); return;
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.querySelectorAll(".drawer:not([hidden])").forEach(closeDrawer);
  });

  /* ---------- sorteren ---------- */
  var sel = document.querySelector("[data-sort]");
  if (sel) sel.addEventListener("change", function () {
    var g = document.querySelector("[data-grid]");
    var cards = [].slice.call(g.children);
    var v = sel.value;
    cards.sort(function (a, b) {
      if (v === "price-asc") return a.dataset.price - b.dataset.price;
      if (v === "price-desc") return b.dataset.price - a.dataset.price;
      if (v === "title") return a.dataset.title.localeCompare(b.dataset.title);
      return 0;
    });
    cards.forEach(function (c) { g.appendChild(c); });
  });

  /* ---------- zoeken ---------- */
  var si = document.querySelector("[data-search-input]");
  if (si) si.addEventListener("input", function () {
    var v = si.value.toLowerCase().trim();
    var box = document.querySelector("[data-search-results]");
    if (!v) { box.innerHTML = '<p class="muted">Begin met typen om de testcatalogus te doorzoeken.</p>'; return; }
    var hits = P.filter(function (p) {
      return (p.title + " " + p.brand).toLowerCase().indexOf(v) > -1;
    }).slice(0, 8);
    box.innerHTML = hits.length
      ? hits.map(function (p) {
          return '<a class="sr" href="product.html?id=' + p.id + '"><img src="' + p.img + '">' +
                 '<div><div class="card__brand">' + p.brand + '</div><div>' + p.title + '</div>' +
                 '<div class="small">' + money(p.price) + '</div></div></a>';
        }).join("")
      : '<p class="muted">Geen resultaten.</p>';
  });

  /* ---------- PDP-hydratie ---------- */
  if (document.querySelector("[data-pdp-title]")) {
    var id = new URLSearchParams(location.search).get("id") || P[0].id;
    var p = byId[id] || P[0];
    document.querySelector("[data-pdp-title]").textContent = p.title;
    document.querySelector("[data-pdp-crumb]").textContent = p.title;
    document.querySelector("[data-pdp-brand]").textContent = p.brand;
    document.querySelector("[data-pdp-price]").innerHTML =
      money(p.price) + (p.compare ? ' <s class="muted">' + money(p.compare) + "</s>" : "");
    document.querySelector("[data-pdp-img]").src = p.img;
    document.querySelector("[data-pdp-img2]").src = p.img2;
    document.title = p.title + " | BETA STORE (beta)";
    document.querySelector("[data-pdp-add]").addEventListener("click", function () { add(p.id); });
  }

  render();
})();
