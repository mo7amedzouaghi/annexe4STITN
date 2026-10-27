"""PHP : exemples conformes, paramètres, retour, remarques, mots-clés."""

E = {}

def P(code):
    return "<?php\n" + "\n".join("  " + l if l else "" for l in code.strip("\n").split("\n")) + "\n?>"

# ---------------- Types
E["int"] = dict(ex=P('$age = 17;\n$nbEleves = 32;\necho $age + 1;   // 18'), k="entier type nombre integer")
E["float"] = dict(ex=P('$moyenne = 14.75;\n$prix = 2.5;\necho $moyenne;   // 14.75'), k="réel décimal type double",
                  rq=["Le séparateur décimal est le point."])
E["string"] = dict(ex=P('$ville = "Manouba";\n$msg = \'Bonjour\';\necho $msg . " " . $ville;   // Bonjour Manouba'),
                   k="chaîne texte type guillemets")
E["bool"] = dict(ex=P('$admis = true;\nif ($admis) {\n  echo "Félicitations";\n}'), k="booléen vrai faux true false")
E["array"] = dict(ex=P('$jours = array("Lundi", "Mardi", "Mercredi");\necho $jours[0];          // Lundi\necho count($jours);       // 3'),
                  k="tableau liste indice", rq=["En STI, les tableaux sont indicés de 0 à count($t) - 1."])

# ---------------- Transtypage
E["(int)"] = dict(ex=P('$n = (int) "42";      // 42\n$m = (int) 7.9;        // 7 : partie entière\necho (int) "12abc";   // 12'),
                  k="convertir entier transtypage cast partie entière")
E["(float)"] = dict(ex=P('$x = (float) "19.5";   // 19.5\necho $x * 2;            // 39'), k="convertir réel transtypage cast")
E["(string)"] = dict(ex=P('$annee = 2026;\n$ch = (string) $annee;\necho strlen($ch);   // 4 : nombre de chiffres'),
                     k="convertir chaîne transtypage cast")
E["(bool)"] = dict(ex=P('$b = (bool) 0;     // false\n$c = (bool) "STI"; // true\nif (!$b) {\n  echo "0 est converti en false";\n}'),
                   k="convertir booléen transtypage", rq=["var_dump() n'est pas dans l'annexe : on teste la valeur avec if et on affiche avec echo."])
E["(array)"] = dict(ex=P('$t = (array) "Sousse";\necho $t[0];         // Sousse\necho count($t);      // 1'), k="convertir tableau transtypage",
                    rq=["print_r() et var_dump() ne sont pas dans l'annexe."])

# ---------------- Opérateurs
E["&&"] = dict(ex=P('if ($moyenne >= 10 && $absences < 5) {\n  echo "Admis";\n}'), k="et logique and")
E["||"] = dict(ex=P('if ($ville == "Tunis" || $ville == "Ariana") {\n  echo "Grand Tunis";\n}'), k="ou logique or")
E["!"] = dict(ex=P('if (!isset($_POST["nom"])) {\n  echo "Formulaire non envoyé";\n}'), k="non logique négation not")
for s, mot, ex in [("==", "égal", 'if ($login == "admin") {\n  echo "Accès administrateur";\n}'),
                   ("!=", "différent", 'if ($mdp != $confirmation) {\n  echo "Les mots de passe ne correspondent pas";\n}'),
                   ("<", "inférieur", 'if ($note < 10) {\n  echo "Ajourné";\n}'),
                   ("<=", "inférieur ou égal", 'if ($stock <= 5) {\n  echo "Stock faible";\n}'),
                   (">", "supérieur", 'if ($age > 18) {\n  echo "Majeur";\n}'),
                   (">=", "supérieur ou égal", 'if ($moyenne >= 10) {\n  echo "Admis";\n}')]:
    E[s] = dict(ex=P(ex), k=f"comparaison {mot} comparer condition",
                rq=["=== et !== ne sont pas dans l'annexe."] if s in ("==", "!=") else [])
E["+"] = dict(ex=P('$total = $prixHT + $tva;'), k="addition somme plus")
E["-"] = dict(ex=P('$reste = 100 - $depense;'), k="soustraction moins")
E["*"] = dict(ex=P('$ttc = $prix * 1.19;'), k="multiplication produit")
E["/"] = dict(ex=P('$moyenne = $somme / $nb;\n$q = (int) (17 / 5);   // 3 : quotient entier'), k="division quotient",
              rq=["Quotient entier : (int) ($a / $b)."])
E["%"] = dict(ex=P('if ($n % 2 == 0) {\n  echo "$n est pair";\n}'), k="modulo reste pair impair")
E["="] = dict(ex=P('$nom = $_POST["nom"];\n$total = 0;'), k="affectation affecter variable assigner",
              rq=["Ne pas confondre = (affectation) et == (comparaison) dans un if."])
E["."] = dict(ex=P('$prenom = "Rim";\necho "Bonjour " . $prenom . " !";   // Bonjour Rim !\n$ligne = "<td>" . $nom . "</td>";'),
              k="concaténation concaténer point assembler chaînes")

# ---------------- Mathématiques
E["abs()"] = dict(ex=P('echo abs(-12);   // 12'), p=[("nombre", "Valeur numérique")], r="La valeur absolue.", k="valeur absolue")
E["sqrt()"] = dict(ex=P('echo sqrt(81);   // 9'), p=[("nombre", "Valeur positive ou nulle")], r="La racine carrée (réel).", k="racine carrée")
E["round()"] = dict(ex=P('echo round(14.567);      // 15\necho round(14.567, 2);   // 14.57'),
                    p=[("nombre", "Valeur à arrondir"), ("précision (facultatif)", "Nombre de décimales conservées (0 par défaut)")],
                    r="La valeur arrondie (réel).", k="arrondir arrondi décimales")
E["rand()"] = dict(ex=P('$de = rand(1, 6);         // entier de 1 à 6\n$code = rand(1000, 9999);  // code à 4 chiffres'),
                   p=[("min", "Plus petite valeur possible"), ("max", "Plus grande valeur possible (incluse)")],
                   r="Un entier aléatoire entre min et max inclus.", k="aléatoire hasard tirage random")

# ---------------- Chaînes
E["chr()"] = dict(ex=P('echo chr(65);   // A\n$lettre = chr(rand(65, 90));   // majuscule aléatoire'),
                  p=[("code", "Code ASCII (0 à 255)")], r="Le caractère correspondant.", k="caractère code ascii lettre")
E["ord()"] = dict(ex=P('echo ord("A");   // 65\necho ord("a");   // 97'), p=[("caractère", "Chaîne dont on prend le premier caractère")],
                  r="Le code ASCII du premier caractère.", k="code ascii valeur caractère")
E["strlen()"] = dict(ex=P('echo strlen("Kairouan");   // 8\nif (strlen($mdp) < 6) {\n  echo "Mot de passe trop court";\n}'),
                     p=[("chaîne", "Chaîne à mesurer")], r="Le nombre de caractères (octets).",
                     rq=["Un caractère accentué (é, à) compte pour 2 en UTF-8."], k="longueur taille nombre caractères")
E["substr()"] = dict(ex=P('echo substr("Oued Ellil", 0, 4);   // Oued\necho substr("Oued Ellil", 5);      // Ellil\necho substr("2026-10-27", 0, 4);   // 2026'),
                     p=[("chaîne", "Chaîne source"), ("début", "Position du premier caractère (0 = début)"),
                        ("longueur (facultatif)", "Nombre de caractères extraits ; sans ce paramètre, jusqu'à la fin")],
                     r="La sous-chaîne extraite.",
                     rq=["En PHP le 3e paramètre est une longueur, alors qu'en JavaScript substring(d, f) prend une position de fin."],
                     k="sous-chaîne extraire partie couper")
E["strpos()"] = dict(ex=P('echo strpos("Bonjour", "jour");   // 3\nif (strpos($email, "@") == false) {\n  echo "Adresse invalide";   // @ absent ou en 1re position\n}'),
                     p=[("chaîne", "Chaîne où l'on cherche"), ("recherche", "Chaîne recherchée")],
                     r="La position de la première occurrence (à partir de 0), ou false si elle est absente.",
                     rq=["Avec ==, une position 0 est évaluée comme false : le test ci-dessus refuse aussi un @ en première position, ce qui convient pour une adresse e-mail.",
                         "=== n'est pas dans l'annexe."],
                     k="position chercher trouver occurrence contient")
E["strcmp()"] = dict(ex=P('$r = strcmp("abc", "abd");   // valeur négative\nif (strcmp($login, "admin") == 0) {\n  echo "Identiques";\n}'),
                     p=[("chaîne1", "Première chaîne"), ("chaîne2", "Seconde chaîne")],
                     r="0 si les chaînes sont égales, un nombre négatif si chaîne1 < chaîne2, positif sinon.",
                     rq=["Comparaison sensible à la casse et à l'ordre alphabétique (codes ASCII)."], k="comparer chaînes ordre alphabétique égalité")
E["str_replace()"] = dict(ex=P('echo str_replace(" ", "_", "mon fichier.txt");   // mon_fichier.txt'),
                          p=[("recherche", "Chaîne à remplacer"), ("remplacement", "Nouvelle chaîne"), ("chaîne", "Chaîne dans laquelle on remplace")],
                          r="Une nouvelle chaîne où toutes les occurrences sont remplacées.",
                          rq=["Remplace toutes les occurrences, contrairement à replace() en JavaScript."], k="remplacer substituer")
E["strtolower()"] = dict(ex=P('echo strtolower("SOUSSE");   // sousse'), p=[("chaîne", "Chaîne à convertir")], r="La chaîne en minuscules.",
                         k="minuscules casse")
E["strtoupper()"] = dict(ex=P('echo strtoupper("sousse");   // SOUSSE'), p=[("chaîne", "Chaîne à convertir")], r="La chaîne en majuscules.",
                         k="majuscules casse")
E["trim()"] = dict(ex=P('$nom = trim($_POST["nom"]);\nif (strlen($nom) == 0) {\n  echo "Nom obligatoire";\n}'),
                   p=[("chaîne", "Chaîne à nettoyer")], r="La chaîne sans espaces au début et à la fin.", k="espaces nettoyer supprimer vide")

# ---------------- Date
E["checkdate()"] = dict(ex=P('if (checkdate(2, 29, 2028)) {\n  echo "Date valide";      // 2028 est bissextile\n}\nif (!checkdate(2, 30, 2026)) {\n  echo "Date invalide";\n}'),
                        p=[("mois", "Mois de 1 à 12"), ("jour", "Jour du mois"), ("année", "Année sur 4 chiffres")],
                        r="true si la date existe, false sinon.",
                        rq=["Ordre des paramètres : mois, jour, année (et non jour, mois, année)."], k="vérifier date valide existe bissextile")
E["date()"] = dict(ex=P('echo date("d/m/Y");          // 27/10/2026\necho date("H:i");            // 10:45\necho date("Y");              // 2026\necho date("d/m/Y", $timestamp);'),
                   p=[("format", "d jour, m mois, Y année sur 4 chiffres, H heure, i minutes, s secondes"),
                      ("timestamp (facultatif)", "Date à formater ; date du jour par défaut")],
                   r="La date formatée (chaîne).", k="date du jour aujourd'hui formater format heure année")
E["time()"] = dict(ex=P('$t = time();\necho date("d/m/Y", $t + 7 * 24 * 3600);   // dans une semaine'),
                   p=[], r="Le timestamp actuel : nombre de secondes depuis le 1er janvier 1970.", k="timestamp maintenant secondes heure actuelle")
E["strtotime()"] = dict(ex=P('$t = strtotime("2026-12-31");\necho date("d/m/Y", $t);   // 31/12/2026\n$jours = (strtotime("2026-12-31") - time()) / 86400;'),
                        p=[("texte", "Date en anglais ou au format AAAA-MM-JJ (ex. \"2026-12-31\", \"+1 week\")")],
                        r="Le timestamp correspondant, ou false si le texte n'est pas une date.",
                        rq=["Différence en jours entre deux dates : (t2 - t1) / 86400."], k="convertir date timestamp différence jours")

# ---------------- Tableaux
E["array()"] = dict(ex=P('$notes = array(12, 15.5, 9);\nfor ($i = 0; $i < count($notes); $i++) {\n  echo $notes[$i] . "<br>";\n}'),
                    p=[("valeurs", "Éléments du tableau, séparés par des virgules")], r="Un tableau indicé à partir de 0.",
                    k="tableau créer liste éléments")
E["count()"] = dict(ex=P('$t = array("Tunis", "Sfax", "Sousse");\necho count($t);   // 3'), p=[("tableau", "Tableau dont on compte les éléments")],
                    r="Le nombre d'éléments.", k="nombre éléments taille tableau compter")
E["echo"] = dict(ex=P('echo "Bonjour";\necho "<p>Moyenne : " . $moy . "</p>";'), p=[("expression", "Chaîne ou valeur à afficher")],
                 r="—", rq=["Structure du langage : les parenthèses sont facultatives."], k="afficher écrire sortie print")

# ---------------- mysqli
E["mysqli_connect()"] = dict(
    ex=P('// connexion.php\n$cnx = mysqli_connect("localhost", "root", "", "ecole")\n       or die("Connexion impossible");'),
    p=[("serveur", "Nom du serveur MySQL : \"localhost\""), ("utilisateur", "Compte MySQL : \"root\" sous XAMPP"),
       ("mot de passe", "Mot de passe du compte : \"\" sous XAMPP"), ("base", "Nom de la base de données")],
    r="Un identifiant de connexion, ou false en cas d'échec.",
    rq=["Écrite une seule fois dans connexion.php, importée par require dans chaque page.",
        "PDO, new mysqli() et mysqli_connect_error() ne sont pas dans l'annexe."],
    k="connexion connecter base mysql serveur pdo")
E["mysqli_query()"] = dict(
    ex=P('$req = "SELECT nom, moyenne FROM Eleve WHERE moyenne >= 10";\n$res = mysqli_query($cnx, $req) or die(mysqli_error($cnx));'),
    p=[("connexion", "Identifiant renvoyé par mysqli_connect"), ("requête", "Requête SQL (chaîne)")],
    r="Pour SELECT : un résultat à parcourir. Pour INSERT, UPDATE, DELETE : true, ou false en cas d'erreur.",
    rq=["Tester d'abord la requête dans l'onglet SQL de phpMyAdmin.", "Les valeurs texte sont entourées d'apostrophes dans la requête : '$nom'."],
    k="exécuter requête sql envoyer")
E["mysqli_close()"] = dict(ex=P('mysqli_close($cnx);'), p=[("connexion", "Identifiant de connexion")], r="true si la fermeture réussit.",
                           k="fermer connexion déconnecter")
E["mysqli_fetch_array()"] = dict(
    ex=P('while ($ligne = mysqli_fetch_array($res)) {\n  echo "<tr><td>" . $ligne["nom"] . "</td><td>" . $ligne[1] . "</td></tr>";\n}'),
    p=[("résultat", "Résultat renvoyé par mysqli_query (SELECT)")],
    r="La ligne suivante, accessible par nom de colonne ou par indice ; null quand il n'y a plus de ligne.",
    rq=["mysqli_fetch_assoc() n'est pas dans l'annexe."], k="parcourir lignes résultat afficher tableau lire")
E["mysqli_fetch_row()"] = dict(
    ex=P('$ligne = mysqli_fetch_row($res);\necho $ligne[0];   // première colonne'),
    p=[("résultat", "Résultat renvoyé par mysqli_query (SELECT)")],
    r="La ligne suivante, accessible uniquement par indice (0, 1, 2…) ; null s'il n'y en a plus.",
    k="lire ligne indice résultat")
E["mysqli_num_rows()"] = dict(
    ex=P('if (mysqli_num_rows($res) == 0) {\n  echo "Aucun résultat";\n}'),
    p=[("résultat", "Résultat d'un SELECT")], r="Le nombre de lignes du résultat.",
    rq=["Usage type : authentification (== 1) ou vérifier qu'un élément existe déjà avant un ajout."],
    k="nombre lignes résultat existe compter authentification")
E["mysqli_affected_rows()"] = dict(
    ex=P('mysqli_query($cnx, "DELETE FROM Eleve WHERE idEleve = $id");\nif (mysqli_affected_rows($cnx) == 0) {\n  echo "Aucun élève supprimé";\n}'),
    p=[("connexion", "Identifiant de connexion (et non le résultat)")],
    r="Le nombre de lignes touchées par le dernier INSERT, UPDATE ou DELETE.",
    k="lignes modifiées supprimées insérées affectées")
E["mysqli_error()"] = dict(ex=P('$res = mysqli_query($cnx, $req) or die(mysqli_error($cnx));'),
                           p=[("connexion", "Identifiant de connexion")], r="Le message de la dernière erreur MySQL (chaîne vide s'il n'y en a pas).",
                           k="erreur message déboguer")
E["$_GET"] = dict(ex=P('// liste.php : <a href="fiche.php?id=12">Voir</a>\n// fiche.php\nif (isset($_GET["id"])) {\n  $id = $_GET["id"];\n}'),
                  k="url paramètre lien get transmettre",
                  rq=["Les données sont visibles dans l'URL : réservé aux identifiants et aux filtres."])
E["$_POST"] = dict(ex=P('// <form action="ajout.php" method="post"> … <input name="nom"> …\nif (isset($_POST["nom"])) {\n  $nom = $_POST["nom"];\n}'),
                   k="formulaire post récupérer données envoyer",
                   rq=["La clé est l'attribut name du champ, pas son id."])
E["die()"] = dict(ex=P('$cnx = mysqli_connect("localhost", "root", "", "ecole") or die("Connexion impossible");'),
                  p=[("message (facultatif)", "Texte affiché avant l'arrêt")], r="—", rq=["Arrête immédiatement l'exécution du script."],
                  k="arrêter stopper erreur quitter exit")
E["isset()"] = dict(ex=P('if (isset($_POST["login"]) && isset($_POST["mdp"])) {\n  // traitement\n} else {\n  echo "Formulaire incomplet";\n}'),
                    p=[("variable", "Variable ou élément de tableau à tester")], r="true si la variable existe et n'est pas null.",
                    k="tester existe défini formulaire envoyé")
E["require()"] = dict(ex=P('require("connexion.php");'), p=[("fichier", "Chemin du fichier PHP à importer")], r="—",
                      rq=["Si le fichier est introuvable, le script s'arrête (erreur fatale)."], k="importer inclure fichier connexion include")
