/* Assistant Annexe STI — recherche et fiches */
(function () {
  "use strict";

  var DATA = window.ANNEXE || [];
  var HORS = window.HORS_ANNEXE || [];
  var fil = document.getElementById("fil");
  var champ = document.getElementById("question");
  var GUIDE = "https://mo7amedzouaghi.github.io/guideSTI/";
  var LANGUES = ["HTML5", "CSS3", "JavaScript", "SQL", "PHP"];
  var PRISM = { HTML5: "markup", CSS3: "css", JavaScript: "javascript", SQL: "sql", PHP: "php" };
  var COULEUR_N = { 2: "var(--n2)", 3: "var(--n3)", 4: "var(--n4)" };
  var niveau = 0;
  try { niveau = Number(localStorage.getItem("sti-niveau")) || 0; } catch (e) { niveau = 0; }

  /* ---------------------------------------------------------- outils */
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function norm(s) {
    return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/[’']/g, " ").replace(/\s+/g, " ").trim();
  }
  function coeur(s) {
    // "ch.substring(d, f)" -> "substring" ; "<input>" -> "input" ; "Math.trunc(x)" -> "math.trunc"
    var n = norm(s).replace(/\(.*$/, "").replace(/^ch\.|^d\.|^document\.|^element\./, "").replace(/[<>\[\]]/g, "");
    return n.trim();
  }
  var VIDES = ("a au aux avec ce ces c comment dans de des du elle en est et faire faut il je j la le les leur lui ma me mes mon ne " +
    "on ou par pas pour qu que quel quelle quels quelles qui sa se ses son sur ta te tes ton tu un une vos votre veux voudrais " +
    "puis peut peux comment quoi est-ce l d s n m t y svp merci bonjour donne donner exemple exemples utiliser utilise sert " +
    "signifie definition definir expliquer explique moyen maniere facon methode fonction propriete balise").split(" ");
  var VIDE = {}; VIDES.forEach(function (m) { VIDE[m] = true; });
  var ALIAS_LANGUE = { html: "HTML5", html5: "HTML5", css: "CSS3", css3: "CSS3", js: "JavaScript", javascript: "JavaScript",
    sql: "SQL", mysql: "SQL", php: "PHP" };

  /* index pré-calculé */
  DATA.forEach(function (it, i) {
    it.i = i;
    it._nom = norm(it.e);
    it._coeur = coeur(it.e);
    it._mots = norm(it.k || "").split(" ");
    it._def = norm(it.d + " " + (it.rq || []).join(" "));
    it._cat = norm(it.c);
  });
  HORS.forEach(function (h) { h._m = h.m.map(norm); });

  /* rareté des mots-clés : un mot présent dans peu de fiches pèse davantage */
  var DF = {};
  DATA.forEach(function (it) {
    var vus = {};
    it._mots.forEach(function (m) { if (m && !vus[m]) { vus[m] = true; DF[m] = (DF[m] || 0) + 1; } });
  });
  var LOGN = Math.log(DATA.length + 1);
  function poids(m) {
    var df = DF[m] || DF[racine(m)] || 1;
    return 0.5 + Math.log((DATA.length + 1) / (df + 1)) / LOGN;
  }

  /* ---------------------------------------------------------- recherche */
  function analyser(q) {
    var qn = norm(q);
    var langue = null;
    var mots = qn.split(/[\s,;?!]+/).filter(Boolean);
    var restants = [];
    mots.forEach(function (m) {
      if (ALIAS_LANGUE[m] && mots.length > 1) { langue = ALIAS_LANGUE[m]; return; }
      if (!VIDE[m]) restants.push(m);
    });
    return { qn: qn, langue: langue, mots: restants, coeur: coeur(qn) };
  }

  function racine(m) { return m.length > 4 ? m.replace(/(es|s|x)$/, "") : m; }

  function scorer(it, a) {
    var s = 0;
    if (a.langue && it.l !== a.langue) return 0;
    if (a.qn === it._nom || (a.coeur && a.coeur === it._coeur)) s += 200;
    else if (a.qn.length >= 2 && it._nom.indexOf(a.qn) !== -1) s += 70;
    else if (it._coeur.length >= 2 && (" " + a.mots.join(" ") + " ").indexOf(" " + it._coeur + " ") !== -1) s += a.mots.length > 1 ? 20 : 50;
    var trouves = 0;
    a.mots.forEach(function (m) {
      var r = racine(m), ok = false;
      var w = poids(m);
      if (m === it._coeur) { s += a.mots.length > 1 ? 20 : 40; ok = true; }
      else if (m.length >= 3 && it._nom.indexOf(m) !== -1) { s += 10; ok = true; }
      if (it._mots.indexOf(m) !== -1 || it._mots.indexOf(r) !== -1) { s += Math.round(16 * w); ok = true; }
      else if (r.length >= 4 && it._mots.some(function (k) { return k.indexOf(r) === 0 || (k.length >= 5 && r.indexOf(k) === 0); })) { s += Math.round(8 * w); ok = true; }
      if (r.length >= 4 && it._def.indexOf(r) !== -1) { s += 3; ok = true; }
      if (r.length >= 4 && it._cat.indexOf(r) !== -1) { s += 3; ok = true; }
      if (ok) trouves++;
    });
    if (a.mots.length > 1) s += Math.round(20 * trouves / a.mots.length);
    if (niveau && it.n > niveau) s = Math.round(s * 0.6);
    return s;
  }

  function horsAnnexe(a) {
    var res = [];
    var mots = " " + a.mots.join(" ") + " ";
    HORS.forEach(function (h) {
      if (a.langue && h.l !== a.langue) return;
      var touche = h._m.some(function (t) {
        if (a.qn === t) return true;
        if (/[^a-z0-9 ]/.test(t)) return a.qn.indexOf(t) !== -1;
        return mots.indexOf(" " + t + " ") !== -1;
      });
      if (touche) res.push(h);
    });
    return res;
  }

  function rechercher(q) {
    var a = analyser(q);
    var res = DATA.map(function (it) { return { it: it, s: scorer(it, a) }; })
      .filter(function (r) { return r.s >= 12; })
      .sort(function (x, y) { return y.s - x.s || x.it.n - y.it.n; });
    return { a: a, res: res, hors: horsAnnexe(a) };
  }

  /* ---------------------------------------------------------- affichage */
  function defiler() { fil.scrollTop = fil.scrollHeight; }

  function msgMoi(texte) {
    var d = document.createElement("div");
    d.className = "msg moi apparition";
    d.innerHTML = '<div class="bulle">' + esc(texte) + "</div>";
    fil.appendChild(d);
  }

  function msgBot(html) {
    var d = document.createElement("div");
    d.className = "msg bot apparition";
    d.innerHTML = '<div class="avatar" aria-hidden="true">STI</div><div class="corps">' + html + "</div>";
    fil.appendChild(d);
    d.querySelectorAll("code[class*='language-']").forEach(function (c) { if (window.Prism) Prism.highlightElement(c); });
    brancher(d);
    defiler();
    return d;
  }

  function nbNiveau(n) { return '<span class="nb n' + n + '">' + n + "ème</span>"; }

  function puceElement(it) {
    return '<button type="button" class="puce mono" data-fiche="' + it.i + '">' + esc(it.e) +
      (it.l !== "HTML5" || true ? ' <span class="nb n' + it.n + '">' + it.n + "</span>" : "") + "</button>";
  }

  function blocCode(code, langue, titre) {
    var cls = PRISM[langue] || "none";
    return '<div class="code"><div class="code-tete"><span><b>' + esc(langue) + "</b> " + esc(titre || "Exemple conforme") +
      '</span><button type="button" class="copier">Copier</button></div><pre class="language-' + cls + '"><code class="language-' + cls + '">' +
      esc(code) + "</code></pre></div>";
  }

  function fiche(it) {
    var h = '<article class="fiche" style="--niv:' + COULEUR_N[it.n] + '"><div class="fiche-tete"><div><h2>' + esc(it.e) +
      '</h2><div class="ariane">' + esc(it.l) + " · " + esc(it.c) + "</div></div>" + nbNiveau(it.n) + '</div><div class="fiche-corps">';
    if (niveau && it.n > niveau) {
      h += '<p class="avertissement">Introduit en ' + it.n + "ème : pas encore au programme de " + niveau + "ème.</p>";
    }
    h += "<h3>Définition</h3><p class=\"definition\">" + esc(it.d) + "</p>";
    if (it.syntaxe) h += "<h3>Syntaxe</h3><div class=\"syntaxe\">" + esc(it.syntaxe) + "</div>";
    if (it.p && it.p.length) {
      var titreP = it.l === "HTML5" ? (it.t === "événement" ? "Valeur" : "Attributs") : (it.l === "SQL" && it.t === "commande" ? "Clauses et paramètres" : "Paramètres");
      h += "<h3>" + titreP + "</h3><table class=\"t\"><thead><tr><th>" + (it.l === "HTML5" ? "Attribut" : "Paramètre") +
        "</th><th>Rôle</th></tr></thead><tbody>" + it.p.map(function (p) {
          return "<tr><td>" + esc(p.nom) + "</td><td>" + esc(p.rôle) + "</td></tr>";
        }).join("") + "</tbody></table>";
    } else if (it.attributs && it.attributs.length) {
      h += "<h3>Attributs (annexe)</h3><p>" + it.attributs.map(function (x) { return "<code>" + esc(x) + "</code>"; }).join(" ") + "</p>";
    }
    if (it.types) {
      h += "<h3>Types et attributs autorisés</h3><table class=\"t\"><thead><tr><th>type</th><th>Attributs</th></tr></thead><tbody>" +
        it.types.map(function (t) {
          return "<tr><td>" + esc(t.type) + "</td><td>" + esc(t.attributs_generiques.concat(t.attributs_specifiques).join(", ")) + "</td></tr>";
        }).join("") + "</tbody></table>";
    }
    if (it.valeurs_attributs) {
      h += "<h3>Valeurs des attributs</h3><table class=\"t\"><tbody>" + Object.keys(it.valeurs_attributs).map(function (k) {
        return "<tr><td>" + esc(k) + "</td><td>" + esc(it.valeurs_attributs[k].join(", ")) + "</td></tr>";
      }).join("") + "</tbody></table>";
    }
    if (it.v) h += "<h3>Valeurs possibles (annexe)</h3><p class=\"valeurs\">" + esc(it.v) + "</p>";
    if (it.r) h += "<h3>Valeur de retour</h3><p class=\"retour\">" + esc(it.r) + "</p>";
    if (it.ex) h += "<h3>Exemple</h3>" + blocCode(it.ex, it.l);
    if (it.rq && it.rq.length) h += "<h3>Remarques</h3><ul class=\"remarques\">" + it.rq.map(function (r) { return "<li>" + esc(r) + "</li>"; }).join("") + "</ul>";
    h += '</div><div class="fiche-pied"><button type="button" data-cat="' + esc(it.l) + "|" + esc(it.c) + '">Même catégorie</button>' +
      '<a href="' + GUIDE + "annexe.html?q=" + encodeURIComponent(it.e) + '" target="_blank" rel="noopener">Voir dans le Guide STI</a></div></article>';
    return h;
  }

  function ficheHors(h) {
    var s = '<article class="fiche hors"><div class="fiche-tete"><div><h2>Hors annexe</h2><div class="ariane">' + esc(h.l) +
      '</div></div><span class="etiquette-hors">Ne pas enseigner</span></div><div class="fiche-corps">' +
      "<p class=\"definition\">" + esc(h.x) + "</p><h3>Alternative conforme</h3>" + blocCode(h.a, h.l, "À utiliser") +
      '</div><div class="fiche-pied">' + h.v.map(function (nom) {
        var it = DATA.filter(function (d) { return d.e === nom && (d.l === h.l || h.l === "HTML5" || h.l === "JavaScript"); })[0] ||
          DATA.filter(function (d) { return d.e === nom; })[0];
        return it ? '<button type="button" data-fiche="' + it.i + '">Fiche ' + esc(it.e) + "</button>" : "";
      }).join("") + "</div></article>";
    return s;
  }

  /* ---------------------------------------------------------- réponses */
  function repondre(q) {
    var r = rechercher(q);
    var h = "";
    if (r.hors.length) {
      h += r.hors.slice(0, 2).map(ficheHors).join("");
    }
    if (r.res.length) {
      var meilleur = r.res[0];
      var exact = meilleur.s >= 150;
      if (!r.hors.length || exact) {
        h += fiche(meilleur.it);
        var autres = r.res.slice(1, 9).filter(function (x) { return x.s >= Math.min(30, meilleur.s * 0.25); });
        if (autres.length) {
          h += '<p class="groupe-titre">Autres éléments liés</p><div class="puces">' + autres.map(function (x) { return puceElement(x.it); }).join("") + "</div>";
        }
      } else {
        h += '<p class="groupe-titre">Éléments de l\'annexe liés à votre question</p><div class="puces">' +
          r.res.slice(0, 8).map(function (x) { return puceElement(x.it); }).join("") + "</div>";
      }
    }
    if (!h) {
      h = '<div class="bulle"><p>Aucun élément de l\'annexe ne correspond à « ' + esc(q) + " ».</p>" +
        "<p>Essayez le nom exact (<code>substring</code>, <code>float</code>, <code>GROUP BY</code>) ou un besoin (« arrondir », « liste déroulante », « date du jour »). " +
        "Si une technique n'apparaît pas ici, elle n'est pas dans l'annexe : elle ne s'enseigne pas.</p></div>" + suggestions();
    }
    msgBot(h);
  }

  function ouvrirFiche(i) {
    var it = DATA[i];
    msgMoi(it.e + " (" + it.l + ")");
    msgBot(fiche(it));
  }

  function suggestions() {
    var ex = ["arrondir un nombre", "float", "transition", "charAt", "jointure", "date du jour", "getElementsByName", "mysqli_connect", "liste déroulante", "flex"];
    return '<div class="puces">' + ex.map(function (e) { return '<button type="button" class="puce" data-q="' + esc(e) + '">' + esc(e) + "</button>"; }).join("") + "</div>";
  }

  function parcourir() {
    msgBot('<div class="bulle"><p>Choisissez un langage.</p></div><div class="puces">' + LANGUES.map(function (l) {
      var nb = DATA.filter(function (d) { return d.l === l && (!niveau || d.n <= niveau); }).length;
      return '<button type="button" class="puce langue" data-langue="' + l + '">' + l + ' <span class="nb n3" style="background:var(--marine)">' + nb + "</span></button>";
    }).join("") + "</div>");
  }

  function categories(l) {
    var cats = [];
    DATA.forEach(function (d) { if (d.l === l && cats.indexOf(d.c) === -1) cats.push(d.c); });
    msgMoi(l);
    msgBot('<div class="bulle"><p>' + esc(l) + " : choisissez une catégorie.</p></div><div class=\"puces\">" +
      '<button type="button" class="puce retour" data-action="parcourir">Retour aux langages</button>' +
      cats.map(function (c) {
        var nb = DATA.filter(function (d) { return d.l === l && d.c === c && (!niveau || d.n <= niveau); }).length;
        return '<button type="button" class="puce" data-cat="' + esc(l + "|" + c) + '">' + esc(c) + " (" + nb + ")</button>";
      }).join("") + "</div>");
  }

  function elements(cle, silencieux) {
    var p = cle.split("|"), l = p[0], c = p.slice(1).join("|");
    var items = DATA.filter(function (d) { return d.l === l && d.c === c; });
    if (!silencieux) msgMoi(c);
    var visibles = items.filter(function (d) { return !niveau || d.n <= niveau; });
    var caches = items.length - visibles.length;
    msgBot('<div class="bulle"><p>' + esc(l) + " · " + esc(c) + " : " + visibles.length + " élément(s)" +
      (caches ? " (" + caches + " réservé(s) à un niveau supérieur, masqué(s))" : "") + ".</p></div><div class=\"puces\">" +
      '<button type="button" class="puce retour" data-langue="' + esc(l) + '">Retour aux catégories</button>' +
      visibles.map(puceElement).join("") + "</div>");
  }

  function accueil() {
    fil.innerHTML = "";
    msgBot('<div class="bulle"><p><strong>Bonjour !</strong> Je connais chaque élément de l\'annexe officielle STI : définition, paramètres, valeur de retour, exemple conforme et remarques.</p>' +
      "<p>Écrivez un nom (<code>substring</code>, <code>border-collapse</code>, <code>HAVING</code>) ou un besoin (« arrondir », « centrer un titre », « compter les lignes »). " +
      "Je signale aussi les techniques <strong>hors annexe</strong> et leur alternative conforme.</p>" +
      (niveau ? "<p>Niveau choisi : " + niveau + "ème.</p>" : "<p>Choisissez votre niveau en haut de la page pour filtrer les réponses.</p>") +
      "</div>" + suggestions() +
      '<div class="puces"><button type="button" class="puce retour" data-action="parcourir">Parcourir l\'annexe par langage</button></div>');
  }

  /* ---------------------------------------------------------- événements */
  function brancher(zone) {
    zone.querySelectorAll("[data-fiche]").forEach(function (b) { b.addEventListener("click", function () { ouvrirFiche(Number(b.getAttribute("data-fiche"))); }); });
    zone.querySelectorAll("[data-q]").forEach(function (b) { b.addEventListener("click", function () { envoyer(b.getAttribute("data-q")); }); });
    zone.querySelectorAll("[data-langue]").forEach(function (b) { b.addEventListener("click", function () { categories(b.getAttribute("data-langue")); }); });
    zone.querySelectorAll("[data-cat]").forEach(function (b) { b.addEventListener("click", function () { elements(b.getAttribute("data-cat")); }); });
    zone.querySelectorAll("[data-action='parcourir']").forEach(function (b) { b.addEventListener("click", function () { msgMoi("Parcourir l'annexe"); parcourir(); }); });
    zone.querySelectorAll(".copier").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.closest(".code").querySelector("code").innerText;
        var ok = function () { b.textContent = "Copié ✓"; setTimeout(function () { b.textContent = "Copier"; }, 1500); };
        if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
      });
    });
  }

  function envoyer(q) {
    q = (q || "").trim();
    if (!q) return;
    msgMoi(q);
    repondre(q);
  }

  document.getElementById("saisie").addEventListener("submit", function (e) {
    e.preventDefault();
    envoyer(champ.value);
    champ.value = "";
    champ.focus();
  });
  document.getElementById("effacer").addEventListener("click", accueil);
  document.getElementById("parcourir").addEventListener("click", function () { msgMoi("Parcourir l'annexe"); parcourir(); });

  var boutonsNiv = document.querySelectorAll(".niveau-choix button");
  function majNiveau() {
    boutonsNiv.forEach(function (b) { b.setAttribute("aria-pressed", Number(b.getAttribute("data-n")) === niveau ? "true" : "false"); });
  }
  boutonsNiv.forEach(function (b) {
    b.addEventListener("click", function () {
      niveau = Number(b.getAttribute("data-n"));
      try { localStorage.setItem("sti-niveau", String(niveau)); } catch (e) { /* stockage indisponible */ }
      majNiveau();
      msgBot('<div class="bulle"><p>' + (niveau ? "Niveau " + niveau + "ème : les éléments des niveaux supérieurs sont signalés et masqués dans la navigation." : "Tous les niveaux sont affichés.") + "</p></div>");
    });
  });
  majNiveau();

  /* question passée dans l'adresse : ?q=substring */
  accueil();
  var q = new URLSearchParams(location.search).get("q");
  if (q) envoyer(q);
})();
