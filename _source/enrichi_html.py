"""HTML5 : attributs détaillés, exemples conformes, remarques, mots-clés."""

E = {}

def h(nom, ex, k, p=None, rq=None):
    E[nom] = dict(ex=ex, k=k, p=p or [], rq=rq or [])

SQUELETTE = '''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Lycée Oued Ellil</title>
</head>
<body>
  <h1>Bienvenue</h1>
</body>
</html>'''

h("<html>", SQUELETTE, "racine page document squelette structure doctype", p=[("lang", "Langue du contenu : fr, ar, en")],
  rq=["<!DOCTYPE html> précède toujours <html>."])
h("<head>", '<head>\n  <meta charset="UTF-8">\n  <title>Découvrir la Tunisie</title>\n  <link rel="stylesheet" type="text/css" href="css/style.css">\n  <script type="text/javascript" src="js/script.js"></script>\n</head>',
  "en-tête document métadonnées", rq=["Rien de ce qu'il contient n'est affiché dans la page, sauf le titre dans l'onglet."])
h("<body>", "<body>\n  <h1>Lycée Oued Ellil</h1>\n  <p>Bienvenue sur notre site.</p>\n</body>", "corps contenu visible page",
  rq=["onload s'écrit sur <body> : <body onload=\"init()\">."])
h("<link>", '<link rel="stylesheet" type="text/css" href="css/style.css">', "lier feuille de style css externe",
  p=[("rel", "Relation avec la page : stylesheet pour une feuille de style"), ("type", "Type du fichier : text/css"), ("href", "Chemin du fichier relié")],
  rq=["Niveau 3ème : le CSS externe n'est pas au programme de 2ème."])
h("<meta>", '<meta charset="UTF-8">\n<meta name="description" content="Site du club informatique">\n<meta name="author" content="Club info - Lycée Oued Ellil">',
  "encodage utf-8 description accents métadonnée", p=[("charset", "Encodage des caractères : UTF-8"), ("name", "Nom de la métadonnée : description, author, keywords"), ("content", "Valeur de la métadonnée")],
  rq=["Sans charset=\"UTF-8\", les lettres accentuées s'affichent mal."])
h("<script>", '<!-- fichier externe (obligatoire en 4ème) -->\n<script type="text/javascript" src="js/controle.js"></script>\n\n<!-- script interne (3ème) -->\n<script>\n  function saluer() {\n    alert("Bonjour");\n  }\n</script>',
  "javascript script fichier js relier", p=[("src", "Chemin du fichier .js"), ("type", "text/javascript (facultatif)")],
  rq=["En 4ème, le JavaScript est obligatoirement dans un fichier externe.", "Une balise <script src=…> reste vide."])
h("<style>", '<style type="text/css">\n  h1 {\n    color: navy;\n  }\n</style>', "css interne style feuille dans la page",
  p=[("type", "text/css"), ("media", "Support visé : screen, print")], rq=["Se place dans <head>. CSS interne : niveau 2ème."])
h("<title>", "<title>Club informatique - Inscriptions</title>", "titre onglet navigateur favoris", rq=["Obligatoire pour la validation W3C."])
h("<header>", "<header>\n  <h1>Découvrir la Tunisie</h1>\n  <p>Le patrimoine de nos régions</p>\n</header>", "en-tête sémantique bandeau haut de page logo",
  rq=["Balises sémantiques : niveau 3ème."])
h("<nav>", '<nav>\n  <a href="index.html">Accueil</a>\n  <a href="regions.html">Régions</a>\n  <a href="contact.html">Contact</a>\n</nav>', "navigation menu liens sémantique")
h("<footer>", "<footer>\n  <address>Lycée Oued Ellil - Manouba</address>\n</footer>", "pied de page bas sémantique")
h("<section>", "<section>\n  <h2>Sites archéologiques</h2>\n  <article>…</article>\n</section>", "section regroupement thématique sémantique")
h("<article>", "<article>\n  <h3>Carthage</h3>\n  <p>Fondée au IXe siècle av. J.-C.</p>\n</article>", "article contenu autonome fiche sémantique")
h("<aside>", "<aside>\n  <h3>Le saviez-vous ?</h3>\n  <p>El Jem abrite le 3e plus grand amphithéâtre romain.</p>\n</aside>", "encadré contenu annexe latéral sémantique")
h("<main>", "<main>\n  <h2>Nos activités</h2>\n  <p>…</p>\n</main>", "contenu principal sémantique", rq=["Un seul <main> par page."])
h("<cite>", "<p>Notre livre du mois : <cite>Le Prophète</cite> de Gibran.</p>", "citation titre œuvre livre")
h("<p>", "<p>Les inscriptions au club sont ouvertes jusqu'au 15 novembre.</p>", "paragraphe texte bloc")
h("<h1> à <h6>", "<h1>Lycée Oued Ellil</h1>\n<h2>Clubs</h2>\n<h3>Club informatique</h3>", "titre sous-titre niveau hiérarchie",
  rq=["Un seul <h1> par page ; ne pas sauter de niveau.", "Ne pas choisir un titre pour sa taille : la taille se règle en CSS."])
h("<hr>", "<p>Première partie</p>\n<hr>\n<p>Deuxième partie</p>", "ligne séparation horizontale trait")
h("<img>", '<img src="images/dougga.jpg" alt="Théâtre romain de Dougga" width="300">', "image photo illustration",
  p=[("src", "Chemin du fichier image"), ("alt", "Texte de remplacement (obligatoire)")],
  rq=["Sans alt, la page n'est pas valide W3C.", "Les dimensions se règlent de préférence en CSS (width, height)."])
h("<figure>", '<figure>\n  <img src="images/eljem.jpg" alt="Amphithéâtre d\'El Jem">\n  <figcaption>L\'amphithéâtre d\'El Jem</figcaption>\n</figure>', "figure illustration légende image")
h("<figcaption>", '<figure>\n  <img src="carte.png" alt="Carte des gouvernorats">\n  <figcaption>Les 24 gouvernorats</figcaption>\n</figure>', "légende figure")
h("<audio>", '<audio src="sons/hymne.mp3" controls></audio>', "son audio musique lecteur",
  p=[("src", "Chemin du fichier audio (mp3)"), ("controls", "Affiche les boutons lecture, pause, volume")],
  rq=["<source> n'est pas dans l'annexe : le fichier est donné par l'attribut src.", "Sans controls, le lecteur est invisible."])
h("<video>", '<video src="videos/visite.mp4" controls width="400"></video>', "vidéo lecteur film",
  p=[("src", "Chemin du fichier vidéo (mp4)"), ("controls", "Affiche les commandes de lecture")],
  rq=["<source> n'est pas dans l'annexe : le fichier est donné par l'attribut src."])
h("<a>", '<a href="contact.html">Contact</a>\n<a href="https://www.education.tn" target="_blank">Ministère</a>\n<a href="carthage.html" target="cadre">Carthage</a>',
  "lien hypertexte lien navigation url", p=[("href", "Adresse de destination (page, fichier, URL)"), ("target", "_self, _blank, _parent, _top, ou nom d'un iframe")])
h("<br>", "<p>Lycée Oued Ellil<br>Manouba</p>", "retour à la ligne saut de ligne", rq=["Ne sert pas à espacer des blocs : utiliser margin en CSS."])
h("<address>", "<address>\n  Lycée Oued Ellil<br>\n  Tél. : 71 000 000\n</address>", "adresse contact coordonnées")
h("<details>", "<details>\n  <summary>Horaires</summary>\n  <p>Du lundi au samedi, de 8h à 18h.</p>\n</details>", "dépliable replier cacher afficher plus",
  p=[("open", "Bloc déplié dès l'affichage")])
h("<summary>", "<details open>\n  <summary>Conditions d'inscription</summary>\n  <p>Être élève du lycée.</p>\n</details>", "titre bloc dépliable")
h("<span>", '<p>Prix : <span class="prix">15 DT</span></p>', "conteneur en ligne portion texte",
  rq=["Conteneur neutre en ligne : sert à appliquer un style (avec class) à une partie de texte."])
h("<div>", '<div class="carte">\n  <h3>Kairouan</h3>\n  <p>Ville sainte.</p>\n</div>', "conteneur bloc division boîte",
  rq=["Préférer une balise sémantique (section, article…) quand elle existe."])
h("<iframe>", '<a href="carthage.html" target="cadre">Carthage</a>\n<iframe src="accueil.html" name="cadre" width="600" height="300"></iframe>',
  "cadre intégrer page dans page fenêtre", p=[("src", "Page affichée au départ"), ("name", "Nom du cadre, utilisé comme target d'un lien")])
h("<ul>", "<ul>\n  <li>Carthage</li>\n  <li>Dougga</li>\n</ul>", "liste à puces non ordonnée")
h("<ol>", '<ol type="I" start="3">\n  <li>Troisième</li>\n  <li>Quatrième</li>\n</ol>\n<ol reversed>\n  <li>Trois</li>\n  <li>Deux</li>\n</ol>',
  "liste numérotée ordonnée", p=[("type", "1, A, a, I, i"), ("start", "Numéro du premier élément"), ("reversed", "Numérotation décroissante")])
h("<li>", "<ul>\n  <li>Élément de liste</li>\n</ul>", "élément de liste item")
h("<table>", '<table border="1">\n  <caption>Résultats du 1er trimestre</caption>\n  <tr>\n    <th>Nom</th>\n    <th>Moyenne</th>\n  </tr>\n  <tr>\n    <td>Rim</td>\n    <td>15.25</td>\n  </tr>\n</table>',
  "tableau grille données", rq=["Un tableau se construit ligne par ligne : <tr>, puis les cellules."])
for t, k in [("<thead>", "en-tête tableau"), ("<tbody>", "corps tableau"), ("<tfoot>", "pied tableau total")]:
    h(t, '<table border="1">\n  <thead>\n    <tr><th>Article</th><th>Prix</th></tr>\n  </thead>\n  <tbody>\n    <tr><td>Clé USB</td><td>25</td></tr>\n  </tbody>\n  <tfoot>\n    <tr><td>Total</td><td>25</td></tr>\n  </tfoot>\n</table>', k)
h("<tr>", "<tr>\n  <td>Lundi</td>\n  <td>Informatique</td>\n</tr>", "ligne tableau row")
h("<th>", "<tr>\n  <th>Jour</th>\n  <th>Matière</th>\n</tr>", "cellule en-tête tableau titre colonne")
h("<td>", "<tr>\n  <td>Mardi</td>\n  <td>Physique</td>\n</tr>", "cellule donnée tableau")
h("<caption>", "<table border=\"1\">\n  <caption>Emploi du temps</caption>\n  <tr><th>Heure</th><th>Matière</th></tr>\n</table>", "titre légende tableau",
  rq=["Se place juste après <table>."])

# ---------------- Événements
EV = {
    "onblur": ('<input type="text" id="nom" onblur="verifierNom()">', "perte focus quitter champ", "3ème"),
    "onclick": ('<input type="button" value="Valider" onclick="verifier()">', "clic cliquer bouton", "3ème"),
    "onfocus": ('<input type="text" id="cin" onfocus="aide()">', "focus entrer champ", "3ème"),
    "oninput": ('<input type="range" id="note" min="0" max="20" oninput="afficher()">\n<span id="val"></span>', "saisie temps réel curseur valeur change", "3ème"),
    "onload": ('<body onload="init()">', "chargement page démarrage", "3ème"),
    "onmouseover": ('<img src="carte.png" alt="Carte" id="carte" onmouseover="agrandir()">', "survol souris entrer", "4ème"),
    "onmouseout": ('<img src="carte.png" alt="Carte" id="carte" onmouseout="reduire()">', "souris sortir quitter", "4ème"),
    "onplay": ('<video src="visite.mp4" controls onplay="debut()"></video>', "lecture vidéo audio démarre", "4ème"),
    "onpause": ('<audio src="hymne.mp3" controls onpause="pause()"></audio>', "pause média", "4ème"),
    "onsubmit": ('<form action="ajout.php" method="post" onsubmit="return verifier()">\n  …\n  <input type="submit" value="Envoyer">\n</form>', "envoi formulaire soumettre php", "4ème"),
    "onchange": ('<select id="gouv" onchange="afficherVilles()">\n  <option>-- Choisir --</option>\n  <option>Manouba</option>\n</select>', "changement valeur liste sélection", "3ème"),
    "onkeydown": ('<input type="text" id="code" onkeydown="compter()">', "touche clavier enfoncée", "4ème"),
    "onkeyup": ('<input type="text" id="cin" onkeyup="compter()">', "touche clavier relâchée compter caractères", "4ème"),
}
for ev, (ex, k, n) in EV.items():
    rq = []
    if ev == "onclick":
        rq = ["Le bouton est <input type=\"button\"> : <button> n'est pas dans l'annexe.", "addEventListener n'est pas au programme : l'événement s'écrit dans la balise."]
    if ev == "onsubmit":
        rq = ["Uniquement sur <form>, avec return : la fonction renvoie false pour bloquer l'envoi, true pour l'autoriser.",
              "Jamais sur un bouton : pour un contrôle sans envoi, input type=\"button\" + onclick."]
    if ev == "oninput":
        rq = ["oninput réagit à chaque modification ; onchange seulement quand la valeur est validée."]
    E[ev] = dict(ex=ex, k="événement " + k, p=[("valeur", "Appel d'une fonction JavaScript : nomFonction()")], rq=rq)

# ---------------- Attributs globaux
h("class", '<p class="alerte">Inscriptions closes</p>\n<p class="alerte important">Dernier délai</p>', "classe style css plusieurs éléments",
  rq=["Plusieurs classes séparées par un espace."])
h("hidden", '<p id="msg" hidden>Inscription enregistrée</p>', "caché masquer invisible")
h("id", '<input type="text" id="nom" name="nom">', "identifiant unique getElementById label", rq=["Unique dans la page ; utilisé par getElementById, label for et le sélecteur #id."])
h("lang", '<html lang="fr">\n…\n<p lang="ar">مرحبا</p>', "langue")
h("style", '<p style="color: green; font-size: 18px;">Inscriptions ouvertes</p>', "css en ligne inline style",
  rq=["CSS en ligne : niveau 2ème. À partir de la 3ème, préférer la feuille de style externe."])
h("title", '<img src="logo.png" alt="Logo" title="Lycée Oued Ellil">', "infobulle survol texte aide",
  rq=["<abbr> n'est pas dans l'annexe."])

# ---------------- Formulaires
h("<form>", '<form action="inscription.php" method="post">\n  …\n</form>', "formulaire envoyer données",
  p=[("action", "Page qui traite les données (ex. inscription.php)"), ("method", "get (données dans l'URL) ou post (données cachées)"),
     ("target", "_self, _blank, _parent, _top, ou nom d'un iframe")])
h("<fieldset>", '<fieldset>\n  <legend>Identité</legend>\n  <label for="nom">Nom :</label>\n  <input type="text" id="nom" name="nom">\n</fieldset>', "groupe champs cadre formulaire")
h("<legend>", '<fieldset>\n  <legend>Coordonnées</legend>\n  …\n</fieldset>', "titre groupe fieldset")
h("<label>", '<label for="email">E-mail :</label>\n<input type="email" id="email" name="email">', "étiquette libellé champ",
  p=[("for", "id du champ associé")], rq=["Cliquer sur l'étiquette place le curseur dans le champ."])
h("<input>", '<input type="text" name="nom" placeholder="Votre nom" required>\n<input type="number" name="age" min="15" max="20">\n<input type="radio" name="sexe" value="F"> Fille\n<input type="radio" name="sexe" value="G"> Garçon\n<input type="checkbox" name="photo" value="oui" checked>\n<input type="button" value="Valider" onclick="verifier()">',
  "champ saisie formulaire bouton type text number radio checkbox email password date range",
  rq=["2ème : text, number, radio, checkbox, submit, reset. 3ème : email, tel, password, date, time, range, button.",
      "Les boutons radio d'un même groupe partagent le même name."])
h("<textarea>", '<textarea name="message" rows="4" cols="40" maxlength="300" placeholder="Votre message"></textarea>', "zone de texte multiligne commentaire message",
  p=[("name", "Nom de la donnée envoyée"), ("rows", "Nombre de lignes visibles"), ("cols", "Nombre de colonnes visibles"),
     ("maxlength", "Nombre maximal de caractères"), ("placeholder", "Texte indicatif"), ("readonly / required / disabled", "Lecture seule / obligatoire / désactivé")])
h("<select>", '<select id="gouv" name="gouv">\n  <option value="">-- Choisir --</option>\n  <option value="Manouba">Manouba</option>\n  <option value="Ariana">Ariana</option>\n</select>',
  "liste déroulante choix menu", p=[("name", "Nom de la donnée"), ("multiple", "Plusieurs choix possibles"), ("required / disabled", "Obligatoire / désactivé")],
  rq=["En JavaScript, on teste selectedIndex == 0 pour vérifier qu'un choix a été fait."])
h("<datalist>", '<input type="text" name="ville" list="villes">\n<datalist id="villes">\n  <option value="Tunis">\n  <option value="Sousse">\n  <option value="Sfax">\n</datalist>',
  "suggestions saisie autocomplétion liste", rq=["Relié au champ par l'attribut list = id du datalist.", "Niveau 4ème."])
h("<option>", '<select name="classe">\n  <option value="3SI1">3ème SI 1</option>\n  <option value="3SI2" selected>3ème SI 2</option>\n</select>',
  "option choix liste", p=[("value", "Valeur envoyée"), ("selected", "Option choisie par défaut")])
