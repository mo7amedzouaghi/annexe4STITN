/* Mode IA — modèle libre (Qwen 2.5) exécuté dans le navigateur avec WebLLM.
   Chaque question : 1) recherche des fiches de l'annexe, 2) réponse du modèle à partir de ces fiches,
   3) contrôle automatique du code produit (techniques hors annexe). */
import { CreateWebWorkerMLCEngine } from "https://esm.run/@mlc-ai/web-llm@0.2.86";

const M = window.MoteurSTI;
const fil = document.getElementById("fil");
const champ = document.getElementById("question");
const btnEnvoyer = document.getElementById("envoyer");
const btnArreter = document.getElementById("arreter");
const btnCharger = document.getElementById("charger");
const prog = document.getElementById("progression");
const progBarre = document.getElementById("prog-remplie");
const progTexte = document.getElementById("prog-texte");

let engine = null;
let occupe = false;
let historique = [];
let niveau = 0;
try { niveau = Number(localStorage.getItem("sti-niveau")) || 0; } catch (e) { niveau = 0; }

const PRISM = { html: "markup", html5: "markup", xml: "markup", css: "css", js: "javascript", javascript: "javascript",
  sql: "sql", mysql: "sql", php: "php" };
const NOM_LANGUE = { markup: "HTML", css: "CSS", javascript: "JS", sql: "SQL", php: "PHP" };

/* ------------------------------------------------------------------ compatibilité */
let suffixe = "-q4f16_1-MLC";
async function verifierCompatibilite() {
  if (!navigator.gpu) return false;
  try {
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) return false;
    if (!adapter.features.has("shader-f16")) suffixe = "-q4f32_1-MLC";
    return true;
  } catch (e) {
    return false;
  }
}

/* ------------------------------------------------------------------ chargement */
try {
  const choix = localStorage.getItem("sti-modele");
  if (choix) {
    const r = document.querySelector(`input[name="modele"][value="${choix}"]`);
    if (r) r.checked = true;
  }
} catch (e) { /* stockage indisponible */ }

btnCharger.addEventListener("click", async () => {
  const base = document.querySelector('input[name="modele"]:checked').value;
  try { localStorage.setItem("sti-modele", base); } catch (e) { /* ignoré */ }
  btnCharger.disabled = true;
  prog.hidden = false;
  progTexte.textContent = "Démarrage du moteur…";
  try {
    engine = await CreateWebWorkerMLCEngine(
      new Worker(new URL("./ia-worker.js", import.meta.url), { type: "module" }),
      base + suffixe,
      {
        initProgressCallback: (r) => {
          progBarre.style.width = Math.round((r.progress || 0) * 100) + "%";
          progTexte.textContent = traduireProgression(r.text || "");
        },
      }
    );
    document.getElementById("demarrage").remove();
    champ.disabled = false;
    btnEnvoyer.disabled = false;
    champ.placeholder = "Ex. : écris un contrôle de téléphone à 8 chiffres en JS";
    champ.focus();
    accueil();
  } catch (e) {
    progTexte.textContent = "Échec du chargement : " + (e && e.message ? e.message : e) +
      ". Essayez le modèle Léger, fermez les autres onglets, ou utilisez la recherche rapide.";
    btnCharger.disabled = false;
  }
});

function traduireProgression(t) {
  return t
    .replace(/Fetching param cache/i, "Téléchargement du modèle")
    .replace(/Loading model from cache/i, "Chargement du modèle depuis le cache")
    .replace(/Finish loading on WebGPU/i, "Modèle prêt")
    .replace(/secs elapsed/i, "s écoulées")
    .replace(/It can take a while when we first visit this page to populate the cache\.?/i, "Le premier chargement peut prendre plusieurs minutes.")
    .replace(/Later refreshes will become faster\.?/i, "Les visites suivantes seront rapides.");
}

/* ------------------------------------------------------------------ consignes du modèle */
function consignes() {
  return `Tu es l'Assistant STI créé par M. Zouaghi Mohamed (Lycée Oued Ellil, Tunisie) pour les enseignants de Sciences et Technologies de l'Informatique (2ème, 3ème, 4ème année).
Réponds toujours en français, de façon claire, structurée et brève.
${niveau ? `L'enseignant travaille en ${niveau}ème année : n'utilise que des notions de ce niveau ou des niveaux inférieurs.` : ""}
RÈGLES ABSOLUES (annexe officielle) :
- N'utilise que les éléments de l'annexe. Appuie-toi sur les FICHES fournies. Si la demande sort de l'annexe, dis-le et donne l'alternative conforme.
- HTML : aucune mise en forme par balise (pas de b, strong, i, em) : tout en CSS. Bouton = <input type="button" value="…" onclick="fonction()">, jamais <button>.
- CSS : unités px et % uniquement. Mise en page par float et position, jamais flex ni grid. transition déclarée sur l'élément, pas sur :hover ; pas de ease ni linear.
- JavaScript : lecture par document.getElementById(id).value ; erreur = alert("…") puis return ; succès = innerHTML. Caractère : ch[i] (jamais charAt). Sous-chaîne : substring (jamais substr ni slice). Math.trunc et Math.round (jamais floor ni ceil). Pas de console.log, addEventListener, querySelector, ===. Champ « chiffres uniquement » : boucle sur ch[i] entre "0" et "9".
- SQL : jointure dans WHERE (jamais JOIN). Date du jour : DATE(NOW()) (jamais CURDATE). Pas d'AUTO_INCREMENT. Renommer une colonne : CHANGE.
- PHP : mysqli procédural uniquement (mysqli_connect, mysqli_query, mysqli_fetch_array, mysqli_num_rows…), connexion dans connexion.php importée par require. Jamais PDO, ni new mysqli, ni switch, ni hachage de mot de passe.
- Quand un MODÈLE DE RÉFÉRENCE est fourni, suis sa structure et ses conventions.
- Écris le code dans des blocs \`\`\` avec le langage (html, css, js, sql, php), indenté et commenté.`;
}

function ficheTexte(it) {
  let t = `### ${it.e} (${it.l}, ${it.n}ème) : ${it.d}`;
  if (it.syntaxe) t += `\nSyntaxe : ${it.syntaxe}`;
  if (it.p && it.p.length) t += "\nParamètres : " + it.p.map((p) => `${p.nom} = ${p.rôle}`).join(" ; ");
  if (it.v) t += `\nValeurs : ${it.v}`;
  if (it.r) t += `\nRetour : ${it.r}`;
  if (it.ex) t += `\nExemple :\n${it.ex.slice(0, 520)}`;
  if (it.rq && it.rq.length) t += "\nRemarques : " + it.rq.join(" ");
  return t;
}

const RECETTES = (window.RECETTES_STI || []).map((x) => ({ ...x, _k: M.norm(x.k).split(" ") }));

function recette(question) {
  const mots = M.norm(question).split(/[\s,;?!:.'’]+/).filter((m) => m.length >= 3);
  let meilleure = null, max = 0;
  for (const x of RECETTES) {
    let s = 0;
    for (const m of mots) {
      const r = m.length > 4 ? m.replace(/(es|s|x)$/, "") : m;
      if (x._k.some((k) => k === m || k === r || (r.length >= 5 && k.indexOf(r) === 0))) s++;
    }
    if (s > max) { max = s; meilleure = x; }
  }
  return max >= 2 ? meilleure : null;
}

function contexte(question) {
  const r = M.rechercher(question, niveau);
  const rec = recette(question);
  const meilleurs = [];
  const seuil = r.res.length ? r.res[0].s * 0.3 : 0;
  for (const x of r.res) {
    if (meilleurs.length >= 4 || x.s < seuil) break;
    meilleurs.push(x.it);
  }
  let txt = "";
  for (const it of meilleurs) {
    const f = ficheTexte(it);
    if (txt.length + f.length > (rec ? 3000 : 4200)) break;
    txt += f + "\n\n";
  }
  for (const h of r.hors.slice(0, 2)) {
    txt += `### HORS ANNEXE (${h.l}) : ${h.x}\nAlternative conforme :\n${h.a}\n\n`;
  }
  if (rec) txt += `### MODÈLE DE RÉFÉRENCE CONFORME : ${rec.t}\n${rec.c}\n\n`;
  return { texte: txt.trim(), fiches: meilleurs, hors: r.hors.slice(0, 2), recette: rec };
}

/* ------------------------------------------------------------------ rendu markdown simple et sûr */
function rendre(md, enCours) {
  const morceaux = md.split(/```/);
  let html = "";
  morceaux.forEach((m, i) => {
    if (i % 2 === 1) {
      const nl = m.indexOf("\n");
      const lang = (nl === -1 ? "" : m.slice(0, nl)).trim().toLowerCase();
      const code = nl === -1 ? m : m.slice(nl + 1);
      const cls = PRISM[lang] || "none";
      html += `<div class="code"><div class="code-tete"><span><b>${NOM_LANGUE[cls] || "Code"}</b></span><button type="button" class="copier">Copier</button></div>` +
        `<pre class="language-${cls}"><code class="language-${cls}">${M.esc(code.replace(/\n$/, ""))}</code></pre></div>`;
    } else {
      html += texteVersHtml(m);
    }
  });
  return html + (enCours ? '<span class="curseur"></span>' : "");
}

function enLigne(s) {
  return M.esc(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

function texteVersHtml(t) {
  const lignes = t.split("\n");
  let html = "", liste = null, para = [];
  const fermerPara = () => { if (para.length) { html += "<p>" + para.join("<br>") + "</p>"; para = []; } };
  const fermerListe = () => { if (liste) { html += `</${liste}>`; liste = null; } };
  for (const brut of lignes) {
    const l = brut.trim();
    let m;
    if (!l) { fermerPara(); fermerListe(); continue; }
    if ((m = l.match(/^#{1,4}\s+(.*)$/))) { fermerPara(); fermerListe(); html += `<h4>${enLigne(m[1])}</h4>`; continue; }
    if ((m = l.match(/^[-*•]\s+(.*)$/))) { fermerPara(); if (liste !== "ul") { fermerListe(); html += "<ul>"; liste = "ul"; } html += `<li>${enLigne(m[1])}</li>`; continue; }
    if ((m = l.match(/^\d+[.)]\s+(.*)$/))) { fermerPara(); if (liste !== "ol") { fermerListe(); html += "<ol>"; liste = "ol"; } html += `<li>${enLigne(m[1])}</li>`; continue; }
    fermerListe();
    para.push(enLigne(l));
  }
  fermerPara(); fermerListe();
  return html;
}

/* ------------------------------------------------------------------ contrôle de conformité du code produit */
const CONTROLES = [
  [/\.charAt\s*\(/, "charat", "charAt()"], [/\.substr\s*\(/, "substr", "substr()"], [/\.slice\s*\(/, "slice", "slice()"],
  [/Math\.(floor|ceil)\s*\(/, "math.floor", "Math.floor / Math.ceil"], [/\.toFixed\s*\(/, "tofixed", "toFixed()"],
  [/console\.log/, "console.log", "console.log()"], [/addEventListener/, "addeventlistener", "addEventListener"],
  [/querySelector|getElementsByClassName|getElementsByTagName/, "queryselector", "querySelector / getElementsBy…"],
  [/\.textContent|\.innerText/, "textcontent", "textContent / innerText"], [/\.getDay\s*\(/, "getday", "getDay()"],
  [/[!=]==/, "===", "=== / !=="], [/<button[\s>]/i, "<button>", "<button>"],
  [/<(b|strong|i|em|u)>/i, "<b>", "balise de mise en forme"], [/\bpattern\s*=/, "pattern", "attribut pattern"],
  [/<source[\s>]/i, "<source>", "<source>"],
  [/display\s*:\s*(flex|grid)/i, "flex", "display: flex / grid"], [/\d(\.\d+)?(em|rem|vh|vw)\b/, "em", "unités em / rem / vh / vw"],
  [/linear-gradient/i, "linear-gradient", "linear-gradient"], [/line-height/i, "line-height", "line-height"],
  [/text-decoration/i, "text-decoration", "text-decoration"], [/translate[XY]\s*\(/, "translatex", "translateX / translateY"],
  [/\bJOIN\b/i, "join", "JOIN"], [/CURDATE\s*\(/i, "curdate", "CURDATE()"], [/AUTO_INCREMENT/i, "auto_increment", "AUTO_INCREMENT"],
  [/\bMODIFY\b|RENAME\s+COLUMN/i, "modify", "MODIFY / RENAME COLUMN"], [/IF\s+(NOT\s+)?EXISTS/i, "if exists", "IF EXISTS"],
  [/\bLIMIT\s+\d/i, "limit", "LIMIT"],
  [/new\s+PDO|new\s+mysqli/i, "pdo", "PDO / new mysqli"], [/mysqli_fetch_assoc|mysqli_connect_error/, "mysqli_fetch_assoc", "fonction mysqli hors annexe"],
  [/md5\s*\(|sha1\s*\(|password_hash|password_verify/i, "md5", "hachage du mot de passe"],
  [/\$_SESSION|session_start|setcookie/, "session", "sessions / cookies"], [/var_dump|print_r/, "var_dump", "var_dump / print_r"],
  [/\bforeach\b/, "foreach", "foreach"], [/\binclude(_once)?\b|require_once/, "include", "include / require_once"],
];
const CONTROLES_CSS = [[/\b(ease|ease-in|ease-out|linear)\b/, "ease", "fonction de rythme (ease, linear)"]];
const CONTROLES_PHP = [[/\bswitch\s*\(/, "switch", "switch en PHP"]];

function trouverHors(cle) {
  const n = M.norm(cle);
  return M.hors.find((h) => h._m.indexOf(n) !== -1);
}

function controler(md) {
  const blocs = [];
  md.split(/```/).forEach((m, i) => {
    if (i % 2 === 1) {
      const nl = m.indexOf("\n");
      blocs.push({ lang: (nl === -1 ? "" : m.slice(0, nl)).trim().toLowerCase(), code: nl === -1 ? m : m.slice(nl + 1) });
    }
  });
  const trouves = new Map();
  blocs.forEach((b) => {
    let liste = CONTROLES.slice();
    if (b.lang === "css" || /\{[^}]*:[^}]*;/.test(b.code) && !/function|<\?php/.test(b.code)) liste = liste.concat(CONTROLES_CSS);
    if (b.lang === "php" || /<\?php|\$\w+/.test(b.code)) liste = liste.concat(CONTROLES_PHP);
    liste.forEach(([re, cle, libelle]) => {
      if (re.test(b.code) && !trouves.has(cle)) trouves.set(cle, libelle);
    });
  });
  return { blocs: blocs.length, problemes: [...trouves.entries()] };
}

function blocControle(md) {
  const c = controler(md);
  if (!c.blocs) return "";
  if (!c.problemes.length) {
    return '<div class="controle ok">✔ Contrôle automatique : aucune technique hors annexe détectée dans le code.</div>';
  }
  let h = '<div class="controle ko"><strong>✗ Contrôle automatique : code non conforme à l\'annexe</strong><ul>';
  c.problemes.forEach(([cle, libelle]) => {
    const e = trouverHors(cle);
    h += `<li><strong>${M.esc(libelle)}</strong> : ${M.esc(e ? e.x : "hors annexe.")}`;
    if (e) h += `<div class="code"><div class="code-tete"><span><b>${M.esc(e.l)}</b> Alternative conforme</span><button type="button" class="copier">Copier</button></div><pre class="language-none"><code class="language-none">${M.esc(e.a)}</code></pre></div>`;
    h += "</li>";
  });
  return h + "</ul></div>";
}

/* ------------------------------------------------------------------ conversation */
function defiler() { fil.scrollTop = fil.scrollHeight; }

function msgMoi(t) {
  const d = document.createElement("div");
  d.className = "msg moi apparition";
  d.innerHTML = `<div class="bulle">${M.esc(t)}</div>`;
  fil.appendChild(d);
  defiler();
}

function msgBot(html) {
  const d = document.createElement("div");
  d.className = "msg bot apparition";
  d.innerHTML = `<div class="avatar" aria-hidden="true">IA</div><div class="corps">${html}</div>`;
  fil.appendChild(d);
  defiler();
  return d;
}

function brancher(zone) {
  zone.querySelectorAll("code[class*='language-']").forEach((c) => { if (window.Prism) Prism.highlightElement(c); });
  zone.querySelectorAll(".copier").forEach((b) => {
    b.addEventListener("click", () => {
      const t = b.closest(".code").querySelector("code").innerText;
      const ok = () => { b.textContent = "Copié ✓"; setTimeout(() => { b.textContent = "Copier"; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });
  zone.querySelectorAll("[data-q]").forEach((b) => b.addEventListener("click", () => poser(b.getAttribute("data-q"))));
}

function accueil() {
  fil.innerHTML = "";
  historique = [];
  const ex = ["Écris un contrôle de téléphone à 8 chiffres en JavaScript", "Différence entre WHERE et HAVING",
    "Comment placer deux blocs côte à côte en CSS ?", "Afficher la liste des élèves en PHP avec mysqli",
    "Explique transition avec un exemple", "Calculer l'âge à partir de la date de naissance en JS"];
  const d = msgBot(`<div class="bulle"><p><strong>L'assistant est prêt.</strong> Posez votre question en français : explication, exemple de code, correction, comparaison.</p>` +
    `<p>Je réponds à partir des fiches de l'annexe et je vérifie chaque code que je propose.</p></div>` +
    `<div class="puces">${ex.map((e) => `<button type="button" class="puce" data-q="${M.esc(e)}">${M.esc(e)}</button>`).join("")}</div>`);
  brancher(d);
}

async function poser(q) {
  q = (q || "").trim();
  if (!q || !engine || occupe) return;
  occupe = true;
  champ.value = "";
  btnEnvoyer.hidden = true;
  btnArreter.hidden = false;
  msgMoi(q);

  const ctx = contexte(q);
  const messages = [{ role: "system", content: consignes() }];
  historique.slice(-2).forEach((h) => { messages.push({ role: "user", content: h.q }); messages.push({ role: "assistant", content: h.r }); });
  messages.push({
    role: "user",
    content: (ctx.texte ? `FICHES DE L'ANNEXE (à utiliser) :\n${ctx.texte}\n\n` : "Aucune fiche de l'annexe ne correspond directement.\n\n") + `QUESTION : ${q}`,
  });

  const bulle = msgBot('<div class="reponse"><span class="curseur"></span></div>');
  const zone = bulle.querySelector(".reponse");
  let texte = "";
  let dernier = 0;
  try {
    const flux = await engine.chat.completions.create({ messages, stream: true, temperature: 0.2, max_tokens: 900 });
    for await (const morceau of flux) {
      texte += morceau.choices[0]?.delta?.content || "";
      const t = performance.now();
      if (t - dernier > 80) { zone.innerHTML = rendre(texte, true); dernier = t; defiler(); }
    }
  } catch (e) {
    texte += "\n\n(Réponse interrompue : " + (e && e.message ? e.message : e) + ")";
  }
  zone.innerHTML = rendre(texte, false) + blocControle(texte) +
    (ctx.recette ? `<div class="sources">Modèle de référence : <strong>${M.esc(ctx.recette.t)}</strong></div>` : "") +
    (ctx.fiches.length ? `<div class="sources">Fiches utilisées : ${ctx.fiches.map((it) =>
      `<a href="./?q=${encodeURIComponent(it.e)}" target="_blank" rel="noopener">${M.esc(it.e)}</a>`).join("")}</div>` : "");
  brancher(bulle);
  defiler();
  historique.push({ q, r: texte.slice(0, 700) });
  occupe = false;
  btnEnvoyer.hidden = false;
  btnArreter.hidden = true;
  champ.focus();
}

document.getElementById("saisie").addEventListener("submit", (e) => { e.preventDefault(); poser(champ.value); });
btnArreter.addEventListener("click", () => { if (engine) engine.interruptGenerate(); });
document.getElementById("effacer").addEventListener("click", () => { if (engine) accueil(); });

/* niveau */
const boutonsNiv = document.querySelectorAll(".niveau-choix button");
function majNiveau() { boutonsNiv.forEach((b) => b.setAttribute("aria-pressed", Number(b.dataset.n) === niveau ? "true" : "false")); }
boutonsNiv.forEach((b) => b.addEventListener("click", () => {
  niveau = Number(b.dataset.n);
  try { localStorage.setItem("sti-niveau", String(niveau)); } catch (e) { /* ignoré */ }
  majNiveau();
}));
majNiveau();

/* démarrage */
verifierCompatibilite().then((ok) => {
  if (!ok) {
    document.getElementById("incompatible").hidden = false;
    document.getElementById("modeles").hidden = true;
    btnCharger.hidden = true;
  }
});

/* exposé pour les tests */
window._iaTest = { contexte, controler, rendre, consignes };
