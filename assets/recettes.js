/* Modèles de code de référence, conformes à l'annexe et aux conventions du Lycée Oued Ellil.
   Le Mode IA en transmet un au modèle quand la question s'y rapporte. */
window.RECETTES_STI = [
  {
    t: "Contrôle de formulaire (JavaScript)",
    k: "controle formulaire verifier valider saisie champ nom telephone tel chiffres obligatoire erreur alert return innerHTML bouton",
    c: `<!-- inscription.html -->
<input type="text" id="nom">
<input type="text" id="tel">
<input type="button" value="Valider" onclick="verifier()">
<p id="msg"></p>

// controle.js
function estChiffres(ch) {
  if (ch.length == 0) {
    return false;
  }
  for (let i = 0; i < ch.length; i++) {
    if (ch[i] < "0" || ch[i] > "9") {
      return false;
    }
  }
  return true;
}
function verifier() {
  let nom = document.getElementById("nom").value;
  let tel = document.getElementById("tel").value;
  if (nom.length < 3) {
    alert("Le nom doit contenir au moins 3 caractères");
    return;
  }
  if (tel.length != 8 || !estChiffres(tel)) {
    alert("Le téléphone doit contenir 8 chiffres");
    return;
  }
  document.getElementById("msg").innerHTML = "Inscription enregistrée";
}`,
  },
  {
    t: "Boutons radio et liste déroulante (JavaScript, 4ème)",
    k: "radio bouton coche checked groupe getelementsbyname liste deroulante select option selectedindex choix",
    c: `function verifierChoix() {
  let t = document.getElementsByName("niveau");
  let choix = "";
  for (let i = 0; i < t.length; i++) {
    if (t[i].checked) {
      choix = t[i].value;
    }
  }
  if (choix == "") {
    alert("Choisir un niveau");
    return;
  }
  let liste = document.getElementById("gouv");
  if (liste.selectedIndex == 0) {
    alert("Choisir un gouvernorat");
    return;
  }
  document.getElementById("msg").innerHTML = choix + " - " + liste.value;
}`,
  },
  {
    t: "Dates en JavaScript (âge, mois)",
    k: "date age naissance annee mois jour calculer getfullyear getmonth getdate aujourd hui",
    c: `function calculerAge() {
  let n = new Date(document.getElementById("naissance").value);  // <input type="date">
  let auj = new Date();
  let age = auj.getFullYear() - n.getFullYear();
  if (auj.getMonth() < n.getMonth() || (auj.getMonth() == n.getMonth() && auj.getDate() < n.getDate())) {
    age = age - 1;
  }
  document.getElementById("res").innerHTML = "Âge : " + age + " ans, né(e) le " +
    n.getDate() + "/" + (n.getMonth() + 1) + "/" + n.getFullYear();
}`,
  },
  {
    t: "CAPTCHA et nombres aléatoires (JavaScript)",
    k: "captcha aleatoire hasard random code lettre chiffre generer tirage",
    c: `function genererCaptcha() {
  let code = "";
  for (let i = 0; i < 4; i++) {
    code = code + String(Math.trunc(Math.random() * 10));          // chiffre de 0 à 9
  }
  code = code + String.fromCharCode(Math.trunc(Math.random() * 26) + 65);  // lettre A à Z
  document.getElementById("captcha").innerHTML = code;
}
function verifierCaptcha() {
  let saisi = document.getElementById("saisie").value;
  if (saisi != document.getElementById("captcha").innerHTML) {
    alert("Code incorrect");
    return;
  }
  document.getElementById("msg").innerHTML = "Code correct";
}`,
  },
  {
    t: "Mise en page en colonnes (CSS, 3ème)",
    k: "mise en page colonnes cote a cote float position bloc gauche droite structure page layout menu header footer pleine hauteur",
    c: `html, body {
  height: 100%;
  margin: 0px;
}
header {
  height: 15%;
  background-color: #0D2B6B;
  color: white;
}
nav {
  float: left;
  width: 20%;
  height: 75%;
  background-color: #e9eef8;
}
section {
  float: right;
  width: 78%;
  height: 75%;
}
footer {
  clear: both;          /* arrêt du flottement */
  height: 10%;
  text-align: center;
}`,
  },
  {
    t: "Transition, transformation, animation (CSS, 3ème)",
    k: "transition survol hover effet animation keyframes transform rotate scale translate deplacer agrandir tourner",
    c: `.vignette {
  width: 150px;
  transition: width 1s 0.2s;          /* sur l'élément, jamais sur :hover */
}
.vignette:hover {
  width: 200px;
  transform: rotate(5deg) scale(1.1); /* toutes les fonctions sur une ligne */
}
@keyframes defiler {
  0%   { left: 0px; }
  100% { left: 300px; }
}
.bandeau {
  position: relative;                  /* obligatoire pour animer left */
  animation: defiler 4s 0s infinite alternate;
}`,
  },
  {
    t: "Page HTML5 sémantique (3ème)",
    k: "page structure semantique squelette header nav main section article aside footer html5 site",
    c: `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Découvrir la Tunisie</title>
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <script type="text/javascript" src="js/script.js"></script>
</head>
<body>
  <header><h1>Découvrir la Tunisie</h1></header>
  <nav><a href="index.html">Accueil</a> <a href="regions.html">Régions</a></nav>
  <main>
    <section>
      <article>
        <h2>Carthage</h2>
        <figure>
          <img src="images/carthage.jpg" alt="Ruines de Carthage">
          <figcaption>Les thermes d'Antonin</figcaption>
        </figure>
      </article>
    </section>
    <aside>Le saviez-vous ?</aside>
  </main>
  <footer><address>Lycée Oued Ellil</address></footer>
</body>
</html>`,
  },
  {
    t: "Requêtes SQL avancées (4ème)",
    k: "sql requete jointure jointures relier tables group by having regrouper agregat count avg sum moyenne nombre sous requete where",
    c: `-- Jointure (syntaxe classique)
SELECT E.nom, E.prenom, C.niveau
FROM Eleve E, Classe C
WHERE E.idClasse = C.idClasse;

-- Regroupement : WHERE filtre les lignes, HAVING filtre les groupes
SELECT C.niveau, COUNT(*) AS effectif, AVG(E.moyenne) AS moy
FROM Eleve E, Classe C
WHERE E.idClasse = C.idClasse
GROUP BY C.niveau
HAVING COUNT(*) > 20
ORDER BY moy DESC;

-- Sous-requête non corrélée
SELECT nom FROM Eleve
WHERE moyenne > (SELECT AVG(moyenne) FROM Eleve);`,
  },
  {
    t: "Création de tables (SQL, 4ème)",
    k: "creer table create table contrainte cle primaire etrangere foreign key primary key alter ajouter colonne",
    c: `CREATE TABLE Classe (
  idClasse VARCHAR(10),
  niveau   INT NOT NULL,
  CONSTRAINT pk_classe PRIMARY KEY (idClasse)
);
CREATE TABLE Eleve (
  idEleve  INT,
  nom      VARCHAR(30) NOT NULL,
  moyenne  DECIMAL(4,2) CHECK (moyenne BETWEEN 0 AND 20),
  idClasse VARCHAR(10),
  CONSTRAINT pk_eleve PRIMARY KEY (idEleve),
  CONSTRAINT fk_eleve_classe FOREIGN KEY (idClasse)
    REFERENCES Classe(idClasse) ON DELETE CASCADE
);
ALTER TABLE Eleve ADD tel VARCHAR(8);
ALTER TABLE Eleve CHANGE nom nomEleve VARCHAR(40);`,
  },
  {
    t: "PHP : afficher une table MySQL",
    k: "php afficher liste tableau resultat select mysqli connexion base parcourir lignes fetch",
    c: `<?php
  // connexion.php
  $cnx = mysqli_connect("localhost", "root", "", "ecole") or die("Connexion impossible");
?>
<?php
  // liste.php
  require("connexion.php");
  $req = "SELECT nom, prenom, moyenne FROM Eleve ORDER BY nom";
  $res = mysqli_query($cnx, $req) or die(mysqli_error($cnx));
  echo "<p>" . mysqli_num_rows($res) . " élève(s)</p>";
  echo "<table border='1'><tr><th>Nom</th><th>Prénom</th><th>Moyenne</th></tr>";
  while ($ligne = mysqli_fetch_array($res)) {
    echo "<tr><td>" . $ligne["nom"] . "</td><td>" . $ligne["prenom"] . "</td><td>" . $ligne["moyenne"] . "</td></tr>";
  }
  echo "</table>";
  mysqli_close($cnx);
?>`,
  },
  {
    t: "PHP : ajouter depuis un formulaire",
    k: "php ajouter inserer insert formulaire post enregistrer isset ajout modifier supprimer update delete",
    c: `<!-- ajout.html : <form action="ajout.php" method="post"> ... <input type="submit" value="Ajouter"> -->
<?php
  require("connexion.php");
  if (isset($_POST["id"]) && isset($_POST["nom"])) {
    $id = $_POST["id"];
    $nom = $_POST["nom"];
    $verif = mysqli_query($cnx, "SELECT idEleve FROM Eleve WHERE idEleve = $id");
    if (mysqli_num_rows($verif) > 0) {
      echo "Cet identifiant existe déjà";
    } else {
      mysqli_query($cnx, "INSERT INTO Eleve (idEleve, nom) VALUES ($id, '$nom')") or die(mysqli_error($cnx));
      echo mysqli_affected_rows($cnx) . " élève ajouté";
    }
  }
  mysqli_close($cnx);
?>`,
  },
  {
    t: "PHP : authentification",
    k: "php authentification connexion login mot de passe utilisateur identifier session compte",
    c: `<?php
  require("connexion.php");
  if (isset($_POST["login"]) && isset($_POST["mdp"])) {
    $login = $_POST["login"];
    $mdp = $_POST["mdp"];             // comparé tel quel, sans hachage
    $req = "SELECT nom FROM Utilisateur WHERE login = '$login' AND mdp = '$mdp'";
    $res = mysqli_query($cnx, $req) or die(mysqli_error($cnx));
    if (mysqli_num_rows($res) == 1) {
      $ligne = mysqli_fetch_row($res);
      echo "Bienvenue " . $ligne[0];
    } else {
      echo "Login ou mot de passe incorrect";
    }
  }
  mysqli_close($cnx);
?>`,
  },
];
