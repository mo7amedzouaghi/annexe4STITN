"""CSS3 : valeurs possibles (annexe), exemples conformes, remarques, mots-clés."""

E = {}

def s(nom, ex, k, v=None, rq=None):
    E[nom] = dict(ex=ex, k=k, v=v, rq=rq or [])

# ---------------- Sélecteurs
s("element", "p {\n  color: #1c2536;\n  font-size: 15px;\n}", "sélecteur balise élément type tous les paragraphes")
s("#id", "/* <header id=\"bandeau\"> */\n#bandeau {\n  background-color: #0D2B6B;\n  color: white;\n}", "sélecteur identifiant id dièse unique",
  rq=["Un id est unique dans la page.", "linear-gradient() n'est pas dans l'annexe : fond uni avec background-color ou image avec background-image."])
s(".class", "/* <p class=\"alerte\"> */\n.alerte {\n  color: #C62828;\n  font-weight: bold;\n}", "sélecteur classe point plusieurs éléments",
  rq=["Une même classe peut être donnée à plusieurs éléments."])
s("element[attr]", "input[required] {\n  border: 2px solid #C62828;\n}", "sélecteur attribut présence crochets", rq=["Niveau 4ème."])
s("element[attr=valeur]", "input[type=\"email\"] {\n  width: 250px;\n}", "sélecteur attribut valeur type crochets", rq=["Niveau 4ème."])
s("element.class", "/* seulement les <p class=\"note\"> */\np.note {\n  color: gray;\n}", "sélecteur élément classe", rq=["Niveau 4ème."])
s("a:link", "a:link {\n  color: #1D4ED8;\n}", "lien non visité pseudo-classe")
s("a:visited", "a:visited {\n  color: #5B2C9F;\n}", "lien visité pseudo-classe")
s("a:hover", "a:hover {\n  color: #D35400;\n}\n.carte:hover {\n  border-color: #F5B800;\n}", "survol souris hover pseudo-classe",
  rq=["Ordre des pseudo-classes de lien : link, visited, hover, active.", "En 3ème, :hover sert surtout à déclencher les transitions."])
s(":focus", "input:focus {\n  border: 2px solid #F5B800;\n  background-color: #fff6d6;\n}", "focus champ actif saisie pseudo-classe",
  rq=["outline n'est pas dans l'annexe : on utilise border et background-color."])
s("a:active", "a:active {\n  color: #C62828;\n}", "lien clic actif pseudo-classe")

# ---------------- Texte
s("font-family", "body {\n  font-family: Arial, Verdana, sans-serif;\n}", "police caractères typographie",
  v="Noms de polices par ordre de préférence, terminés par une famille générique (serif, sans-serif, monospace)",
  rq=["Nom de police contenant un espace : entre guillemets, \"Times New Roman\"."])
s("font-weight", "h2 {\n  font-weight: bold;\n}\n.leger {\n  font-weight: lighter;\n}", "gras graisse épaisseur texte bold",
  v="bold, bolder, lighter", rq=["Le gras se fait en CSS, jamais avec <b> ou <strong>.", "Les valeurs numériques (300, 700) ne sont pas dans l'annexe."])
s("font-style", "cite {\n  font-style: italic;\n}", "italique penché", v="italic",
  rq=["L'italique se fait en CSS, jamais avec <i> ou <em>."])
s("font-size", "h1 {\n  font-size: 28px;\n}\np {\n  font-size: 15px;\n}", "taille texte police grandeur", v="Valeur en px (ou en %)",
  rq=["Unités em, rem, vw, vh hors programme : px ou %."])
s("font", "p {\n  font: italic bold 16px Arial, sans-serif;\n}", "police abrégée raccourci", v="[font-style] [font-weight] font-size font-family",
  rq=["La taille et la police sont obligatoires, dans cet ordre, à la fin.", "line-height n'est pas dans l'annexe."])
s("text-align", "h1 {\n  text-align: center;\n}\np {\n  text-align: justify;\n}", "aligner alignement centrer centré justifier titre texte", v="left, center, right, justify")
s("text-shadow", "h1 {\n  text-shadow: 2px 2px 4px gray;\n}", "ombre texte", v="décalage-x décalage-y [flou] couleur")
s("text-transform", ".lien-menu {\n  text-transform: uppercase;\n}\n.nom {\n  text-transform: capitalize;\n}", "majuscules minuscules casse capitale",
  v="uppercase, lowercase, capitalize")
s("color", "h1 {\n  color: #0D2B6B;\n}\np {\n  color: rgb(40, 40, 40);\n}", "couleur texte",
  v="Nom (red), hexadécimal (#0D2B6B), rgb(r, g, b)")

# ---------------- Listes
s("list-style-type", "ul {\n  list-style-type: square;\n}\nol {\n  list-style-type: upper-roman;\n}", "puce numérotation type liste",
  v="circle, square, upper-roman, lower-alpha", rq=["none (supprimer les puces) n'est pas listé dans l'annexe."])
s("list-style-position", "ul {\n  list-style-position: inside;\n}", "position puce intérieur", v="outside, inside")
s("list-style-image", "ul {\n  list-style-image: url(\"images/puce.png\");\n}", "image puce", v="url(\"fichier\")")
s("list-style", "ul {\n  list-style: square inside;\n}", "liste abrégée raccourci", v="type position image")

# ---------------- Arrière-plan
s("background-color", "body {\n  background-color: #F3F6FA;\n}", "fond couleur arrière-plan", v="Nom, hexadécimal, rgb()")
s("background-image", "header {\n  background-image: url(\"../images/sahara.jpg\");\n}", "image de fond arrière-plan", v="url(\"fichier\")",
  rq=["Le chemin est relatif au fichier .css : ../images/ si le CSS est dans un dossier css/."])
s("background-repeat", "body {\n  background-image: url(\"motif.png\");\n  background-repeat: repeat-x;\n}", "répétition fond mosaïque",
  v="repeat, repeat-x, repeat-y", rq=["no-repeat est une valeur CSS standard, mais elle n'est pas listée dans l'annexe."])
s("background-size", "header {\n  background-image: url(\"carthage.jpg\");\n  background-size: cover;\n}", "taille image de fond couvrir",
  v="cover, contain, ou largeur hauteur en px / %")
s("background", "header {\n  background: #0D2B6B url(\"motif.png\") repeat-x;\n}", "fond abrégé raccourci",
  v="couleur image répétition taille")

# ---------------- Transformation, filtre, tableaux
s("transform", ".vignette:hover {\n  transform: rotate(5deg) scale(1.2) translate(10px, 0px);\n}", "transformation rotation agrandir déplacer incliner rotate scale translate skew",
  v="rotate(angle), scale(x [, y]), translate(x, y), skew(x, y)",
  rq=["Toutes les fonctions sur une seule ligne : une seconde déclaration transform remplace la première.",
      "translateX() et translateY() ne sont pas dans l'annexe : translate(x, y)."])
s("filter", "img.archive {\n  filter: grayscale(100%);\n}\nimg.flou {\n  filter: blur(3px);\n}", "filtre image noir et blanc flou négatif",
  v="blur(px), grayscale(%), invert(%)", rq=["Niveau 4ème."])
s("table-layout", "table {\n  table-layout: fixed;\n  width: 100%;\n}", "tableau disposition colonnes largeur fixe", v="auto, fixed",
  rq=["fixed : les colonnes gardent la largeur fixée, quel que soit le contenu."])
s("border-collapse", "table {\n  border-collapse: collapse;\n}\ntd, th {\n  border: 1px solid #0D2B6B;\n}", "bordures fusionnées tableau",
  v="separate, collapse")

# ---------------- Boîtes
s("width", ".colonne {\n  width: 30%;\n}\nimg {\n  width: 250px;\n}", "largeur dimension", v="Valeur en px ou %")
s("height", "html, body {\n  height: 100%;\n}\n.zone {\n  height: 80%;\n}", "hauteur dimension", v="Valeur en px ou %",
  rq=["Une hauteur en % exige une hauteur définie sur le parent : html, body { height: 100%; }.", "vh n'est pas dans l'annexe."])
s("position", ".bandeau {\n  position: fixed;\n  top: 0px;\n  width: 100%;\n}\n.badge {\n  position: absolute;\n  top: 10px;\n  right: 10px;\n}",
  "positionner placement absolu relatif fixe collant", v="absolute, fixed, relative, static, sticky",
  rq=["absolute se place par rapport au premier parent positionné (souvent position: relative sur le parent).",
      "top, left… n'agissent que si position n'est pas static."])
s("float", "nav {\n  float: left;\n  width: 25%;\n}\nsection {\n  float: right;\n  width: 70%;\n}", "flotter flottant côte à côte colonnes mise en page",
  v="left, right, none",
  rq=["Pour arrêter le flottement sous les colonnes : clear: both (absent de l'annexe, proposé à la réforme).",
      "Flexbox (display: flex) et Grid ne sont pas au programme."])
s("padding", ".carte {\n  padding: 15px;            /* 4 côtés */\n  padding: 10px 20px;       /* haut-bas  gauche-droite */\n  padding: 5px 10px 15px 20px; /* haut droite bas gauche */\n}",
  "marge intérieure espacement", v="1 à 4 valeurs en px ou %")
s("margin", "section {\n  margin: 20px;\n}\n.centre {\n  width: 800px;\n  margin: 0px auto;   /* centrage horizontal */\n}", "marge extérieure espacement centrer",
  v="1 à 4 valeurs en px, % ou auto")
s("box-shadow", ".carte {\n  box-shadow: 4px 4px 8px gray;\n}", "ombre boîte", v="décalage-x décalage-y [flou] couleur")
s("display", ".lien-menu {\n  display: inline-block;\n  width: 120px;\n}", "affichage bloc en ligne", v="inline, block, inline-block",
  rq=["flex, grid et none ne sont pas listés dans l'annexe."])
s("top", ".badge {\n  position: absolute;\n  top: 10px;\n}", "décalage haut position", v="Valeur en px ou %")
s("bottom", ".pied {\n  position: fixed;\n  bottom: 0px;\n}", "décalage bas position", v="Valeur en px ou %")
s("left", ".menu {\n  position: absolute;\n  left: 0px;\n}", "décalage gauche position", v="Valeur en px ou %")
s("right", ".fermer {\n  position: absolute;\n  right: 10px;\n}", "décalage droite position", v="Valeur en px ou %")
s("overflow", ".actualites {\n  height: 150px;\n  overflow: scroll;\n}", "débordement défilement barre", v="visible, hidden, clip, scroll, auto")
s("opacity", ".filigrane {\n  opacity: 0.3;\n}", "transparence opacité", v="Nombre de 0 (transparent) à 1 (opaque)")

# ---------------- Bordures
s("border-color", ".cadre {\n  border-style: solid;\n  border-color: #F5B800;\n}", "couleur bordure", v="Nom, hexadécimal, rgb()")
s("border-style", ".cadre {\n  border-style: dashed;\n}", "style bordure trait pointillé", v="solid, dashed, dotted, double…",
  rq=["Sans border-style, la bordure ne s'affiche pas."])
s("border-radius", ".carte {\n  border-radius: 10px;\n}\nimg.profil {\n  border-radius: 50%;   /* cercle */\n}", "coins arrondis cercle", v="Valeur en px ou %")
s("border-width", ".cadre {\n  border-width: 3px;\n}", "épaisseur bordure", v="medium, thin, thick, ou valeur en px")
s("border", "td {\n  border: 1px solid #0D2B6B;\n}", "bordure abrégée cadre", v="épaisseur style couleur")

# ---------------- Transitions
s("transition-delay", ".bouton {\n  transition-property: background-color;\n  transition-duration: 1s;\n  transition-delay: 0.5s;\n}", "délai attente transition",
  v="Durée en s (ou ms)")
s("transition-duration", ".bouton {\n  transition-property: width;\n  transition-duration: 2s;\n}", "durée transition", v="Durée en s (ou ms)")
s("transition-property", ".bouton {\n  transition-property: background-color;\n  transition-duration: 1s;\n}", "propriété animée transition",
  v="Nom d'une propriété CSS (width, background-color…)")
s("transition", ".bouton {\n  background-color: #0D2B6B;\n  transition: background-color 1s 0.2s;\n}\n.bouton:hover {\n  background-color: #F5B800;\n}",
  "transition effet progressif survol animation douce", v="propriété durée [délai]",
  rq=["Se déclare sur l'élément, jamais dans :hover (sinon l'effet ne joue qu'à l'aller).",
      "transition-timing-function (ease, linear…) n'est pas dans l'annexe."])

# ---------------- Animations
s("@keyframes", "@keyframes clignote {\n  0%   { opacity: 1; }\n  50%  { opacity: 0.2; }\n  100% { opacity: 1; }\n}", "animation étapes images clés",
  v="Étapes en % (0% à 100%)", rq=["Pour animer left ou top, l'élément doit être positionné (position: relative)."])
s("animation-name", ".alerte {\n  animation-name: clignote;\n  animation-duration: 1s;\n}", "nom animation", v="Nom défini par @keyframes")
s("animation-delay", ".titre {\n  animation-name: glisser;\n  animation-duration: 2s;\n  animation-delay: 1s;\n}", "délai animation", v="Durée en s (ou ms)")
s("animation-duration", ".titre {\n  animation-name: glisser;\n  animation-duration: 2s;\n}", "durée animation cycle", v="Durée en s (ou ms)")
s("animation-iteration-count", ".alerte {\n  animation-name: clignote;\n  animation-duration: 1s;\n  animation-iteration-count: infinite;\n}",
  "répétition nombre infini animation", v="Nombre entier, ou infinite")
s("animation-direction", ".bateau {\n  animation-name: traversee;\n  animation-duration: 3s;\n  animation-iteration-count: infinite;\n  animation-direction: alternate;\n}",
  "sens direction aller retour animation", v="normal, reverse, alternate")
s("animation", "@keyframes traversee {\n  0%   { left: 0px; }\n  100% { left: 300px; }\n}\n.bateau {\n  position: relative;\n  animation: traversee 3s 0s infinite alternate;\n}",
  "animation abrégée mouvement", v="nom durée [délai] [répétitions] [direction]",
  rq=["Les fonctions de rythme (linear, ease…) ne sont pas dans l'annexe."])
