"""JavaScript : exemples conformes, paramètres, retour, remarques, mots-clés."""

E = {}

def op(sym, ex, k, rq=None):
    E[sym] = dict(ex=ex, k=k, rq=rq or [])

# ---------------- Opérateurs logiques
op("&&", '''let age = 17;
if (age >= 15 && age <= 19) {
  alert("Élève du lycée");   // affiche : Élève du lycée
}''', "et logique and les deux conditions vraies",
   ["Vrai seulement si les deux conditions sont vraies."])
op("||", '''let jour = "samedi";
if (jour == "samedi" || jour == "dimanche") {
  alert("Week-end");          // affiche : Week-end
}''', "ou logique or au moins une condition",
   ["Vrai si au moins une des deux conditions est vraie."])
op("!", '''let trouve = false;
if (!trouve) {
  alert("Élément introuvable");
}''', "non logique not négation inverser")

# ---------------- Comparaison
CMP = {"==": ("égal", 'if (note == 20) {\n  alert("Note maximale");\n}'),
       "!=": ("différent", 'if (reponse != "oui") {\n  alert("Réponse refusée");\n}'),
       ">": ("supérieur strict", 'if (moyenne > 10) {\n  alert("Admis");\n}'),
       "<": ("inférieur strict", 'if (age < 18) {\n  alert("Mineur");\n}'),
       ">=": ("supérieur ou égal", 'if (moyenne >= 10) {\n  alert("Admis");\n}'),
       "<=": ("inférieur ou égal", 'if (ch.length <= 8) {\n  alert("Mot de passe trop court");\n}')}
for s, (mot, ex) in CMP.items():
    op(s, ex, f"comparaison {mot} comparer condition test",
       ["On compare avec == et != : les opérateurs === et !== ne sont pas dans l'annexe."] if s in ("==", "!=") else None)

# ---------------- Arithmétiques
op("+", '''let somme = 12 + 8;          // 20
let texte = "12" + 8;        // "128" : avec une chaîne, + concatène
let total = Number("12") + 8; // 20''', "addition somme plus additionner",
   ["Si un des opérandes est une chaîne, + concatène. Convertir d'abord avec Number() les valeurs lues dans un champ."])
op("-", 'let reste = 50 - 18;   // 32', "soustraction moins différence")
op("*", 'let prix = 3 * 2.5;    // 7.5', "multiplication produit fois")
op("/", '''let moyenne = 31 / 2;  // 15.5
let q = Math.trunc(17 / 5);  // 3 : quotient entier''', "division quotient diviser",
   ["Pas d'opérateur de division entière : utiliser Math.trunc(a / b)."])
op("%", '''let r = 17 % 5;         // 2
if (n % 2 == 0) {
  alert(n + " est pair");
}''', "modulo reste division euclidienne pair impair divisible")

# ---------------- Sorties / entrées
E["alert()"] = dict(
    ex='alert("Inscription enregistrée");',
    p=[("message", "Texte (ou valeur) à afficher dans la boîte de dialogue")],
    r="Aucune valeur.",
    rq=["Dans un contrôle de formulaire : alert() puis return pour arrêter la fonction.",
        "console.log() n'est pas dans l'annexe : on affiche avec alert(), document.write() ou innerHTML."],
    k="afficher message boîte dialogue sortie erreur console.log")
E["document.write()"] = dict(
    ex='''document.write("Bonjour<br>");
document.write("Nous sommes en " + new Date().getFullYear());''',
    p=[("texte", "Chaîne (pouvant contenir des balises HTML) écrite dans la page")],
    r="Aucune valeur.",
    rq=["Appelé après le chargement de la page (dans une fonction déclenchée par un clic), il efface toute la page : pour un résultat, préférer innerHTML."],
    k="écrire afficher page sortie")
E["innerHTML"] = dict(
    ex='''// <p id="resultat"></p>
document.getElementById("resultat").innerHTML = "Moyenne : " + moy;
let ancien = document.getElementById("resultat").innerHTML;  // lecture''',
    p=[("valeur", "Chaîne (texte ou HTML) qui remplace le contenu de l'élément")],
    r="En lecture : le contenu HTML de l'élément (chaîne).",
    rq=["Méthode attendue pour afficher le message de succès d'un contrôle de formulaire.",
        "innerText et textContent ne sont pas dans l'annexe."],
    k="afficher résultat contenu modifier élément sortie textContent innerText")
E["prompt()"] = dict(
    ex='''let nom = prompt("Votre nom ?");
let n = Number(prompt("Nombre d'élèves ?"));''',
    p=[("message", "Question affichée à l'utilisateur"), ("défaut (facultatif)", "Valeur proposée dans la zone de saisie")],
    r="Le texte saisi (chaîne), ou null si l'utilisateur clique sur Annuler.",
    rq=["La valeur est toujours une chaîne : convertir avec Number(), parseInt() ou parseFloat() avant un calcul."],
    k="saisir saisie entrée lire demander clavier")

# ---------------- Fonctions de conversion
E["isNaN(ch)"] = dict(
    ex='''isNaN("abc");    // true
isNaN("12");     // false
isNaN("12.5");   // false
isNaN("");       // false  (!)
isNaN(" 12 ");   // false  (!)''',
    p=[("ch", "Valeur à tester")],
    r="true si ch n'est pas convertible en nombre, false sinon.",
    rq=["Ne suffit pas pour tester « chiffres uniquement » (téléphone, CIN, code) : une chaîne vide, des espaces, un point ou un exposant passent le test.",
        "Pour un champ « chiffres uniquement » : parcourir la chaîne avec ch[i] et vérifier que chaque caractère est entre \"0\" et \"9\"."],
    k="tester nombre numérique valide vérifier chiffres not a number")
E["Number(ch)"] = dict(
    ex='''let a = Number("12.5");   // 12.5
let b = Number("12abc");  // NaN
let x = Number(document.getElementById("note").value);''',
    p=[("ch", "Chaîne à convertir")],
    r="Le nombre (entier ou réel) correspondant, ou NaN si la conversion est impossible.",
    rq=["Toute la chaîne doit être numérique, contrairement à parseInt() et parseFloat()."],
    k="convertir nombre conversion chaîne vers nombre")
E["parseFloat(ch)"] = dict(
    ex='''parseFloat("3.14");     // 3.14
parseFloat("3.14 cm");  // 3.14 (s'arrête au premier caractère invalide)
parseFloat("abc");      // NaN''',
    p=[("ch", "Chaîne à convertir")],
    r="Le réel lu au début de la chaîne, ou NaN.",
    rq=["Le séparateur décimal est le point : \"3,5\" donne 3."],
    k="convertir réel décimal virgule conversion")
E["parseInt(ch [, b])"] = dict(
    ex='''parseInt("42");        // 42
parseInt("42.9");      // 42
parseInt("1010", 2);   // 10 (binaire vers décimal)
parseInt("FF", 16);    // 255''',
    p=[("ch", "Chaîne à convertir"), ("b (facultatif)", "Base de numération de ch, de 2 à 36 (10 par défaut)")],
    r="L'entier lu au début de la chaîne (en base 10), ou NaN.",
    rq=["Utile pour les conversions de base (binaire, hexadécimal)."],
    k="convertir entier base binaire hexadécimal conversion")
E["String(a)"] = dict(
    ex='''let ch = String(2026);     // "2026"
let n = String(2026).length;  // 4 : nombre de chiffres''',
    p=[("a", "Valeur (nombre, booléen…) à convertir")],
    r="La chaîne correspondante.",
    rq=["Pratique pour compter les chiffres d'un nombre ou accéder à chacun avec ch[i]."],
    k="convertir chaîne texte conversion nombre vers chaîne")

# ---------------- Sélection
E["document.getElementById()"] = dict(
    ex='''// <input type="text" id="nom">
let nom = document.getElementById("nom").value;''',
    p=[("id", "Valeur de l'attribut id de l'élément (chaîne)")],
    r="L'élément HTML, ou null s'il n'existe pas.",
    rq=["querySelector, getElementsByClassName et getElementsByTagName ne sont pas dans l'annexe.",
        "Un null signale souvent une faute de frappe dans l'id."],
    k="sélectionner élément id accéder récupérer champ value querySelector")
E["document.getElementsByName()"] = dict(
    ex='''// <input type="radio" name="niveau" value="3ème">
let t = document.getElementsByName("niveau");
let choix = "";
for (let i = 0; i < t.length; i++) {
  if (t[i].checked) {
    choix = t[i].value;
  }
}
if (choix == "") {
  alert("Choisir un niveau");
}''',
    p=[("nom", "Valeur de l'attribut name commune aux éléments")],
    r="Une liste d'éléments (accès par indice t[i], taille t.length).",
    rq=["Niveau 4ème. En 3ème, chaque bouton radio est lu par getElementById.",
        "Usage type : retrouver le bouton radio coché d'un groupe."],
    k="radio groupe name boutons cases coché checked parcourir")

# ---------------- Math
E["Math.abs(x)"] = dict(ex='Math.abs(-7);   // 7\nMath.abs(7);    // 7', p=[("x", "Nombre")], r="La valeur absolue de x.",
                         k="valeur absolue positif écart distance")
E["Math.sqrt(x)"] = dict(ex='Math.sqrt(25);  // 5\nMath.sqrt(2);   // 1.4142…\nMath.sqrt(-4);  // NaN', p=[("x", "Nombre positif ou nul")],
                          r="La racine carrée de x (NaN si x est négatif).", k="racine carrée carré parfait")
E["Math.round(x)"] = dict(
    ex='''Math.round(4.5);   // 5
Math.round(4.49);  // 4
Math.round(-4.5);  // -4
Math.round(12.678 * 100) / 100;  // 12.68 : arrondi à 2 décimales''',
    p=[("x", "Nombre")], r="L'entier le plus proche de x.",
    rq=["Arrondir à n décimales : Math.round(x * 10ⁿ) / 10ⁿ (toFixed n'est pas dans l'annexe)."],
    k="arrondir arrondi nombre entier proche décimales toFixed")
E["Math.trunc(x)"] = dict(
    ex='''Math.trunc(7.9);    // 7
Math.trunc(-7.9);   // -7
Math.trunc(17 / 5); // 3 : quotient entier''',
    p=[("x", "Nombre")], r="La partie entière de x (partie décimale supprimée).",
    rq=["Remplace Math.floor() et Math.ceil(), qui ne sont pas dans l'annexe."],
    k="partie entière tronquer floor ceil division entière quotient")
E["Math.random()"] = dict(
    ex='''let r = Math.random();                    // réel dans [0, 1[
let de = Math.trunc(Math.random() * 6) + 1;   // entier de 1 à 6
let n = Math.trunc(Math.random() * (b - a + 1)) + a;  // entier de a à b''',
    p=[], r="Un réel aléatoire dans [0, 1[.",
    rq=["Entier aléatoire de 1 à n : Math.trunc(Math.random() * n) + 1."],
    k="aléatoire hasard tirage random nombre aléatoire dé captcha")

# ---------------- Chaînes
E["ch.length"] = dict(
    ex='''let ch = "Tunisie";
ch.length;              // 7
ch[0];                  // "T" : premier caractère
ch[ch.length - 1];      // "e" : dernier caractère''',
    p=[], r="Le nombre de caractères de ch.",
    rq=["Accès à un caractère : ch[i], de 0 à ch.length - 1. charAt() n'est pas dans l'annexe."],
    k="longueur taille nombre caractères charAt ch[i] caractère indice")
E["ch.indexOf(ch1 [, p])"] = dict(
    ex='''let ch = "programmation";
ch.indexOf("m");       // 6
ch.indexOf("m", 7);    // 7
ch.indexOf("z");       // -1 : absent
if (email.indexOf("@") == -1) {
  alert("Adresse e-mail invalide");
}''',
    p=[("ch1", "Chaîne recherchée"), ("p (facultatif)", "Position de départ de la recherche (0 par défaut)")],
    r="La position de la première occurrence de ch1, ou -1 si elle est absente.",
    rq=["includes() n'est pas dans l'annexe : tester indexOf(…) != -1."],
    k="position caractère chercher rechercher trouver contient includes occurrence")
E["ch.lastIndexOf(ch1 [, p])"] = dict(
    ex='''let f = "photo.vacances.jpg";
let pos = f.lastIndexOf(".");          // 14
let ext = f.substring(pos + 1, f.length);  // "jpg"''',
    p=[("ch1", "Chaîne recherchée"), ("p (facultatif)", "Position à partir de laquelle on cherche vers le début")],
    r="La position de la dernière occurrence de ch1, ou -1.",
    k="dernière position occurrence chercher extension")
E["ch.substring(d, f)"] = dict(
    ex='''let ch = "Oued Ellil";
ch.substring(0, 4);           // "Oued"
ch.substring(5, ch.length);   // "Ellil"
ch.substring(4, 0);           // "Oued" : bornes inversées automatiquement''',
    p=[("d", "Position du premier caractère extrait"), ("f", "Position de fin, exclue")],
    r="La sous-chaîne de d à f - 1.",
    rq=["substr() et slice() ne sont pas dans l'annexe.",
        "Le caractère d'indice f n'est pas inclus : substring(0, 3) donne 3 caractères."],
    k="sous-chaîne extraire partie couper substr slice")
E["ch.replace(ch1, ch2)"] = dict(
    ex='''let ch = "Bonjour Ali, Ali";
ch.replace("Ali", "Sami");   // "Bonjour Sami, Ali" : seule la 1ère occurrence''',
    p=[("ch1", "Chaîne à remplacer"), ("ch2", "Chaîne de remplacement")],
    r="Une nouvelle chaîne ; ch n'est pas modifiée.",
    rq=["Ne remplace que la première occurrence. Pour toutes : boucle while (ch.indexOf(ch1) != -1)."],
    k="remplacer substituer modifier chaîne")
E["ch.toLowerCase()"] = dict(ex='"TUNIS".toLowerCase();   // "tunis"', p=[], r="Une copie de ch en minuscules.",
                              rq=["Utile pour comparer sans tenir compte de la casse."], k="minuscules casse convertir")
E["ch.toUpperCase()"] = dict(ex='''"tunis".toUpperCase();   // "TUNIS"
let initiale = nom[0].toUpperCase();''', p=[], r="Une copie de ch en majuscules.", k="majuscules casse convertir initiale")
E["ch.trim()"] = dict(ex='''"  Sami  ".trim();     // "Sami"
if (nom.trim().length == 0) {
  alert("Nom obligatoire");
}''', p=[], r="Une copie de ch sans les espaces de début et de fin.",
    rq=["Utile pour refuser un champ rempli seulement d'espaces."], k="espaces supprimer nettoyer vide")
E["String.fromCharCode(num, ..., numN)"] = dict(
    ex='''String.fromCharCode(65);           // "A"
String.fromCharCode(83, 84, 73);   // "STI"
// lettre majuscule aléatoire
let lettre = String.fromCharCode(Math.trunc(Math.random() * 26) + 65);''',
    p=[("num, …, numN", "Un ou plusieurs codes ASCII (A = 65, a = 97, 0 = 48)")],
    r="La chaîne formée des caractères correspondants.",
    rq=["charCodeAt() n'est pas dans l'annexe : pour comparer des lettres, on compare directement les caractères (ch[i] >= \"A\")."],
    k="code ascii caractère lettre captcha charCodeAt")
E["+"] = E.get("+")  # opérateur arithmétique déjà défini ; la concaténation est traitée par CONCAT

CONCAT = dict(ex='''let prenom = "Rim";
let message = "Bonjour " + prenom + " !";   // "Bonjour Rim !"
let s = "" + 2026;                          // "2026"''',
              k="concaténer concaténation assembler chaînes joindre", rq=["L'opérateur + concatène dès qu'un opérande est une chaîne."])

# ---------------- Date
E["new Date()"] = dict(ex='let d = new Date();   // date et heure actuelles', p=[], r="Un objet Date contenant la date et l'heure courantes.",
                        k="date du jour aujourd'hui maintenant heure actuelle")
E["new Date(ch)"] = dict(
    ex='''let d = new Date("2026-12-31");
let n = new Date(document.getElementById("naissance").value);  // champ type="date"''',
    p=[("ch", "Date sous forme de chaîne au format AAAA-MM-JJ")],
    r="Un objet Date correspondant à ch.",
    rq=["La valeur d'un champ <input type=\"date\"> est déjà au format AAAA-MM-JJ."],
    k="date chaîne créer date naissance")
E["d.getDate()"] = dict(ex='new Date("2026-10-27").getDate();   // 27', p=[], r="Le jour du mois, de 1 à 31.", k="jour quantième")
E["d.getMonth()"] = dict(
    ex='''let d = new Date("2026-10-27");
d.getMonth();        // 9 (!)
d.getMonth() + 1;    // 10 : octobre''', p=[], r="Le mois, de 0 (janvier) à 11 (décembre).",
    rq=["Ajouter 1 pour l'affichage : (d.getMonth() + 1), entre parenthèses dans une concaténation."],
    k="mois numéro du mois")
E["d.getFullYear()"] = dict(
    ex='''let age = new Date().getFullYear() - new Date(naissance).getFullYear();''', p=[], r="L'année sur 4 chiffres.",
    k="année âge calculer")
E["d.toString()"] = dict(
    ex='''let d = new Date("2026-10-27");
d.toString();                  // "Tue Oct 27 2026 00:00:00 GMT+0100 …"
d.toString().substring(0, 3);  // "Tue" : jour de la semaine''',
    p=[], r="La date complète sous forme de chaîne (en anglais).",
    rq=["getDay() n'est pas dans l'annexe : le jour de la semaine s'obtient par d.toString().substring(0, 3)."],
    k="date chaîne jour de la semaine getDay")

# ---------------- Modification d'éléments
E["element.attribute = valeur"] = dict(
    ex='''document.getElementById("photo").src = "images/sousse.jpg";
document.getElementById("envoyer").disabled = true;
document.getElementById("accord").checked = false;
document.getElementById("cin").readOnly = true;
document.getElementById("video").muted = true;''',
    p=[("attribute", "Attribut à modifier : value, checked, disabled, readOnly, src, muted…"), ("valeur", "Nouvelle valeur")],
    r="—",
    rq=["En JavaScript, l'attribut readonly s'écrit readOnly (O majuscule).", "setAttribute() n'est pas dans l'annexe."],
    k="modifier attribut src value checked disabled readonly muted image")
E["element.style.propriété = valeur"] = dict(
    ex='''let z = document.getElementById("zone");
z.style.color = "white";
z.style.background = "navy";
z.style.border = "2px solid gold";
z.style.width = "300px";''',
    p=[("propriété", "Propriété CSS (color, background, border, font, width, height)"), ("valeur", "Valeur CSS sous forme de chaîne, avec l'unité")],
    r="—",
    rq=["Une propriété CSS avec tiret s'écrit en camelCase : background-color devient backgroundColor.",
        "Toujours préciser l'unité : \"300px\", pas 300."],
    k="modifier style couleur css dynamique changer apparence")
E["element.méthode()"] = dict(
    ex='''let v = document.getElementById("video");
v.play();    // lance la lecture
v.pause();   // met en pause''',
    p=[("méthode", "play() ou pause() pour un élément audio ou vidéo")], r="—",
    k="play pause vidéo audio lecture média")
E["selectedIndex"] = dict(
    ex='''// <select id="gouv"><option>-- Choisir --</option><option>Manouba</option>…</select>
let liste = document.getElementById("gouv");
if (liste.selectedIndex == 0) {
  alert("Choisir un gouvernorat");
  return;
}
let choix = liste.value;''',
    p=[], r="L'indice de l'option choisie (0 pour la première).",
    rq=["La première option sert de consigne (« -- Choisir -- ») : selectedIndex == 0 signifie « rien choisi ».",
        "La valeur choisie se lit avec liste.value."],
    k="liste déroulante select option choisie choix index")
