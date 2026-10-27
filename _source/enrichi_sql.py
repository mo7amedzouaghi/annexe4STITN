"""SQL : exemples conformes (base « ecole » commune), paramètres, remarques, mots-clés."""

E = {}

# Base d'exemple commune : Classe(idClasse, niveau), Eleve(idEleve, nom, prenom, dateNais, moyenne, ville, idClasse#),
# Livre(idLivre, titre, annee, prix), Emprunt(idLivre#, idEleve#, dateEmprunt, dateRetour)

# ---------------- Types
TYPES = {
    "INT": ("idEleve INT", "Entier : identifiants, quantités, années.", "entier nombre"),
    "DECIMAL": ("moyenne DECIMAL(4,2)   -- de -99.99 à 99.99", "DECIMAL(p,d) : p chiffres au total dont d après la virgule.", "réel décimal virgule prix moyenne"),
    "CHAR": ("codePostal CHAR(4)     -- toujours 4 caractères", "Longueur fixe : codes, sexe (CHAR(1)).", "chaîne fixe caractères"),
    "VARCHAR": ("nom VARCHAR(30)        -- 30 caractères au maximum", "Longueur variable : noms, adresses, e-mails.", "chaîne variable texte nom"),
    "TEXT": ("resume TEXT", "Texte long : commentaires, descriptions.", "texte long description"),
    "DATE": ("dateNais DATE         -- 'AAAA-MM-JJ'", "Format 'AAAA-MM-JJ', entre apostrophes.", "date jour format"),
    "TIME": ("heureDebut TIME       -- 'HH:MM:SS'", "Format 'HH:MM:SS'.", "heure temps horaire"),
    "DATETIME": ("dateEmprunt DATETIME  -- 'AAAA-MM-JJ HH:MM:SS'", "Date et heure.", "date heure horodatage"),
}
for t, (col, rq, k) in TYPES.items():
    E[t] = dict(ex=f"CREATE TABLE Exemple (\n  {col}\n);", rq=[rq], k="type " + k)
E["DATE"]["rq"].append("BOOLEAN n'est pas dans l'annexe : utiliser CHAR(1) ou INT (0/1).")

# ---------------- Comparaison
for s, ex, k in [
    ("=", "SELECT nom, prenom FROM Eleve\nWHERE ville = 'Manouba';", "égal égalité"),
    ("<>", "SELECT nom FROM Eleve\nWHERE ville <> 'Tunis';", "différent"),
    (">", "SELECT nom, moyenne FROM Eleve\nWHERE moyenne > 15;", "supérieur"),
    ("<", "SELECT titre FROM Livre\nWHERE annee < 2000;", "inférieur"),
    (">=", "SELECT nom FROM Eleve\nWHERE moyenne >= 10;", "supérieur ou égal"),
    ("<=", "SELECT titre, prix FROM Livre\nWHERE prix <= 20;", "inférieur ou égal")]:
    E[s] = dict(ex=s and ex, k="comparaison " + k + " condition where",
                rq=["Valeurs texte et dates entre apostrophes : 'Tunis', '2026-10-27'."] if s == "=" else (["!= est accepté par MySQL, mais l'annexe utilise <>."] if s == "<>" else []))
E["IN"] = dict(ex="SELECT nom, ville FROM Eleve\nWHERE ville IN ('Tunis', 'Ariana', 'Manouba');", k="liste valeurs parmi appartient",
               p=[("liste", "Valeurs entre parenthèses, séparées par des virgules (ou une sous-requête en 4ème)")],
               rq=["Équivaut à plusieurs conditions reliées par OR. NOT IN : aucune des valeurs."])
E["BETWEEN"] = dict(ex="SELECT nom, moyenne FROM Eleve\nWHERE moyenne BETWEEN 10 AND 12;\n\nSELECT * FROM Emprunt\nWHERE dateEmprunt BETWEEN '2026-10-01' AND '2026-10-31';",
                    p=[("min", "Borne inférieure (incluse)"), ("max", "Borne supérieure (incluse)")],
                    rq=["Les deux bornes sont incluses."], k="intervalle entre bornes plage")
E["LIKE"] = dict(ex="SELECT nom FROM Eleve WHERE nom LIKE 'Ben%';     -- commence par Ben\nSELECT nom FROM Eleve WHERE nom LIKE '%a';       -- se termine par a\nSELECT nom FROM Eleve WHERE nom LIKE '_a%';      -- 2e lettre : a\nSELECT titre FROM Livre WHERE titre LIKE '%info%'; -- contient info",
                 p=[("motif", "% : n'importe quelle suite de caractères (même vide) ; _ : exactement un caractère")],
                 k="motif commence par contient se termine filtre texte joker %")
E["IS NULL"] = dict(ex="SELECT idLivre FROM Emprunt\nWHERE dateRetour IS NULL;     -- livres non rendus\n\nSELECT nom FROM Eleve\nWHERE idClasse IS NOT NULL;",
                    rq=["On n'écrit jamais = NULL : la comparaison avec NULL n'est jamais vraie."], k="vide null absent non renseigné manquant")

# ---------------- Logiques
E["AND"] = dict(ex="SELECT nom FROM Eleve\nWHERE moyenne >= 10 AND ville = 'Manouba';", k="et les deux conditions")
E["OR"] = dict(ex="SELECT nom FROM Eleve\nWHERE ville = 'Tunis' OR ville = 'Ariana';", k="ou une des conditions",
               rq=["Mélange AND / OR : mettre des parenthèses, AND étant prioritaire."])
E["NOT"] = dict(ex="SELECT nom FROM Eleve\nWHERE NOT (ville = 'Tunis');\n\nSELECT titre FROM Livre\nWHERE idLivre NOT IN (SELECT idLivre FROM Emprunt);", k="non négation sauf")

# ---------------- Dates
E["DATE()"] = dict(ex="SELECT DATE(dateEmprunt) FROM Emprunt;\nSELECT * FROM Emprunt WHERE DATE(dateEmprunt) = DATE(NOW());",
                   p=[("d", "Valeur de type DATETIME ou date sous forme de chaîne")], r="La partie date (AAAA-MM-JJ).",
                   rq=["Date du jour : DATE(NOW()). CURDATE() n'est pas dans l'annexe."], k="date du jour extraire aujourd'hui curdate")
E["DAY()"] = dict(ex="SELECT nom, DAY(dateNais) AS jour FROM Eleve;", p=[("d", "Date")], r="Le jour du mois (1 à 31).", k="jour du mois")
E["MONTH()"] = dict(ex="SELECT nom FROM Eleve\nWHERE MONTH(dateNais) = MONTH(NOW());   -- anniversaires du mois", p=[("d", "Date")],
                    r="Le mois (1 à 12).", k="mois")
E["YEAR()"] = dict(ex="SELECT nom, YEAR(NOW()) - YEAR(dateNais) AS age FROM Eleve;", p=[("d", "Date")], r="L'année (4 chiffres).", k="année âge")
E["NOW()"] = dict(ex="INSERT INTO Emprunt (idLivre, idEleve, dateEmprunt)\nVALUES (12, 25, NOW());", p=[], r="La date et l'heure courantes (DATETIME).",
                  rq=["Pour la date seule : DATE(NOW())."], k="maintenant date heure actuelle aujourd'hui")
E["ADDDATE()"] = dict(ex="SELECT idLivre, ADDDATE(dateEmprunt, 15) AS retourPrevu FROM Emprunt;\nSELECT ADDDATE('2026-10-27', INTERVAL 1 MONTH);   -- 2026-11-27",
                      p=[("d", "Date de départ"), ("n", "Nombre de jours à ajouter (négatif pour retrancher), ou INTERVAL n DAY / MONTH / YEAR")],
                      r="La nouvelle date.", k="ajouter jours date échéance retour prévu")
E["DATEDIFF()"] = dict(ex="SELECT idLivre, DATEDIFF(DATE(NOW()), dateEmprunt) AS joursEmprunt\nFROM Emprunt\nWHERE dateRetour IS NULL;",
                       p=[("d1", "Date la plus récente"), ("d2", "Date la plus ancienne")], r="Le nombre de jours d1 - d2 (négatif si d1 < d2).",
                       rq=["L'ordre compte : DATEDIFF(fin, début)."], k="différence jours entre deux dates durée retard")

# ---------------- Agrégats
AGG = {"AVG()": ("SELECT AVG(moyenne) AS moyenneGenerale FROM Eleve;\nSELECT idClasse, AVG(moyenne) FROM Eleve GROUP BY idClasse;", "La moyenne des valeurs non nulles.", "moyenne"),
       "COUNT()": ("SELECT COUNT(*) AS effectif FROM Eleve;\nSELECT COUNT(DISTINCT ville) FROM Eleve;   -- nombre de villes différentes", "Le nombre de lignes (COUNT(*)) ou de valeurs non nulles (COUNT(colonne)).", "compter nombre effectif"),
       "MAX()": ("SELECT MAX(moyenne) AS meilleure FROM Eleve;", "La plus grande valeur.", "maximum plus grand meilleure"),
       "MIN()": ("SELECT MIN(prix) FROM Livre;", "La plus petite valeur.", "minimum plus petit"),
       "SUM()": ("SELECT SUM(prix) AS valeurStock FROM Livre;", "La somme des valeurs.", "somme total additionner")}
for f, (ex, r, k) in AGG.items():
    E[f] = dict(ex=ex, p=[("colonne", "Colonne numérique" if f not in ("COUNT()", "MAX()", "MIN()") else "Colonne, ou * pour COUNT")], r=r,
                rq=["Une condition sur un agrégat s'écrit dans HAVING, jamais dans WHERE.", "Niveau 4ème."], k="agrégation statistique " + k)

# ---------------- Manipulation
E["SELECT"] = dict(
    ex="""-- Une table (3ème)
SELECT DISTINCT ville FROM Eleve ORDER BY ville ASC;

-- Jointure, regroupement, filtre sur groupe (4ème)
SELECT C.niveau, COUNT(*) AS effectif, AVG(E.moyenne) AS moy
FROM Eleve E, Classe C
WHERE E.idClasse = C.idClasse
GROUP BY C.niveau
HAVING COUNT(*) > 20
ORDER BY moy DESC;""",
    p=[("DISTINCT", "Supprime les lignes en double"), ("AS alias", "Renomme une colonne ou une table"),
       ("FROM", "Table(s) interrogée(s), séparées par des virgules"), ("WHERE", "Conditions sur les lignes, et conditions de jointure"),
       ("GROUP BY", "Regroupement des lignes"), ("HAVING", "Conditions sur les groupes"), ("ORDER BY … ASC / DESC", "Tri croissant ou décroissant")],
    rq=["Ordre obligatoire des clauses : SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY.",
        "Jointure en syntaxe classique : tables dans FROM, condition dans WHERE. JOIN … ON n'est pas dans l'annexe.",
        "3ème : une seule table, sans GROUP BY ni HAVING. 4ème : jointures, agrégats, sous-requêtes non corrélées."],
    k="sélectionner consulter afficher requête jointure jointures relier tables join tri trier group by having order by distinct sous-requête")
E["INSERT INTO"] = dict(
    ex="INSERT INTO Eleve (idEleve, nom, prenom, ville)\nVALUES (25, 'Ben Salah', 'Rim', 'Manouba');\n\nINSERT INTO Classe\nVALUES ('4SI1', 4);   -- toutes les colonnes, dans l'ordre",
    p=[("table", "Table qui reçoit la ligne"), ("(colonnes)", "Liste des colonnes renseignées (facultative si toutes le sont, dans l'ordre)"),
       ("VALUES (…)", "Valeurs dans le même ordre que les colonnes")],
    rq=["Les colonnes omises prennent leur valeur DEFAULT ou NULL.", "La clé primaire est saisie explicitement (pas d'AUTO_INCREMENT)."],
    k="ajouter insérer nouvelle ligne enregistrement")
E["UPDATE"] = dict(
    ex="UPDATE Eleve\nSET ville = 'Ariana', idClasse = '4SI2'\nWHERE idEleve = 25;\n\nUPDATE Livre SET prix = prix * 1.1;   -- toutes les lignes",
    p=[("table", "Table modifiée"), ("SET col = valeur, …", "Nouvelles valeurs"), ("WHERE", "Lignes concernées")],
    rq=["Sans WHERE, toutes les lignes de la table sont modifiées."], k="modifier mettre à jour changer valeur")
E["DELETE FROM"] = dict(
    ex="DELETE FROM Emprunt\nWHERE dateRetour IS NOT NULL\n  AND YEAR(dateRetour) < 2025;",
    p=[("table", "Table concernée"), ("WHERE", "Lignes à supprimer")],
    rq=["Sans WHERE, toute la table est vidée.", "Une ligne référencée par une clé étrangère ne peut être supprimée que si la contrainte prévoit ON DELETE CASCADE."],
    k="supprimer effacer ligne enregistrement")

# ---------------- Contraintes
CONTR = {
    "NOT NULL": ("nom VARCHAR(30) NOT NULL", "La valeur est obligatoire.", "obligatoire non vide"),
    "DEFAULT": ("ville VARCHAR(30) DEFAULT 'Manouba'", "Valeur utilisée si rien n'est fourni à l'insertion.", "valeur par défaut"),
    "CHECK": ("moyenne DECIMAL(4,2) CHECK (moyenne BETWEEN 0 AND 20)", "Condition que chaque valeur doit respecter.", "vérifier condition domaine intervalle"),
    "PRIMARY KEY": ("CONSTRAINT pk_eleve PRIMARY KEY (idEleve)", "Identifiant unique et non nul ; une seule par table, éventuellement sur plusieurs colonnes : PRIMARY KEY (idLivre, idEleve, dateEmprunt).", "clé primaire identifiant unique"),
    "UNIQUE": ("email VARCHAR(60) UNIQUE", "Interdit les doublons (NULL autorisé).", "unique sans doublon"),
    "FOREIGN KEY": ("CONSTRAINT fk_eleve_classe FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)", "La valeur doit exister comme clé primaire dans la table référencée.", "clé étrangère lien relation référence"),
    "REFERENCES": ("FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)", "Désigne la table et la colonne référencées par la clé étrangère.", "référence table liée"),
    "ON UPDATE CASCADE": ("FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)\n    ON UPDATE CASCADE", "Si la clé référencée change, la clé étrangère est mise à jour automatiquement.", "cascade modification propagation"),
    "ON DELETE CASCADE": ("FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)\n    ON DELETE CASCADE", "Si la ligne référencée est supprimée, les lignes qui en dépendent le sont aussi.", "cascade suppression propagation"),
}
for c, (decl, rq, k) in CONTR.items():
    E[c] = dict(ex=f"CREATE TABLE Eleve (\n  idEleve INT PRIMARY KEY,\n  {decl}\n);" if not c.startswith(("PRIMARY", "FOREIGN", "REFERENCES", "ON ")) else
                f"CREATE TABLE Eleve (\n  idEleve INT,\n  idClasse VARCHAR(10),\n  CONSTRAINT pk_eleve PRIMARY KEY (idEleve),\n  " + (decl if c != "PRIMARY KEY" else "CONSTRAINT fk_eleve_classe FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)") + "\n);",
                rq=[rq, "En 3ème, les contraintes se définissent en mode assisté (phpMyAdmin) ; en 4ème, on les écrit en SQL."], k="contrainte intégrité " + k)

# ---------------- Définition des données (4ème)
E["CREATE DATABASE"] = dict(ex="CREATE DATABASE ecole;", p=[("nom", "Nom de la base")], k="créer base de données",
                            rq=["IF NOT EXISTS n'est pas dans l'annexe."])
E["DROP DATABASE"] = dict(ex="DROP DATABASE ecole;", p=[("nom", "Nom de la base")], k="supprimer base de données",
                          rq=["Supprime la base, ses tables et toutes les données, sans confirmation."])
E["CREATE TABLE"] = dict(
    ex="""CREATE TABLE Eleve (
  idEleve  INT,
  nom      VARCHAR(30) NOT NULL,
  prenom   VARCHAR(30) NOT NULL,
  dateNais DATE,
  moyenne  DECIMAL(4,2) CHECK (moyenne BETWEEN 0 AND 20),
  ville    VARCHAR(30) DEFAULT 'Manouba',
  idClasse VARCHAR(10),
  CONSTRAINT pk_eleve PRIMARY KEY (idEleve),
  CONSTRAINT fk_eleve_classe FOREIGN KEY (idClasse)
    REFERENCES Classe(idClasse)
    ON DELETE CASCADE
);""",
    p=[("table", "Nom de la table"), ("colonne type [contrainte]", "Une ligne par colonne"),
       ("[CONSTRAINT nom] contrainte", "Contraintes de table : clé primaire, clé étrangère, UNIQUE, CHECK")],
    rq=["AUTO_INCREMENT n'est pas dans l'annexe : la clé primaire est saisie explicitement.",
        "Créer d'abord les tables référencées (Classe) puis celles qui les référencent (Eleve)."],
    k="créer table structure colonnes")
E["ALTER TABLE ADD"] = dict(ex="ALTER TABLE Eleve ADD tel VARCHAR(8);\nALTER TABLE Eleve ADD email VARCHAR(60) UNIQUE;",
                            p=[("colonne type [contrainte]", "Définition de la nouvelle colonne")], k="ajouter colonne modifier structure")
E["ALTER TABLE DROP"] = dict(ex="ALTER TABLE Eleve DROP tel;", p=[("colonne", "Colonne à supprimer")], k="supprimer colonne",
                             rq=["Syntaxe de l'annexe : DROP colonne (le mot COLUMN est facultatif sous MySQL)."])
E["ALTER TABLE ALTER"] = dict(
    ex="-- Syntaxe de l'annexe :\n-- ALTER TABLE Eleve ALTER nom VARCHAR(50);\n\n-- Forme exécutable sous MySQL :\nALTER TABLE Eleve CHANGE nom nom VARCHAR(50);",
    p=[("colonne", "Colonne dont on change le type"), ("type", "Nouveau type")],
    rq=["Sous MySQL, ALTER colonne ne permet pas de changer le type : on utilise CHANGE ancien_nom nouveau_nom type.", "MODIFY n'est pas dans l'annexe."],
    k="modifier type colonne changer taille change modify")
E["ALTER TABLE RENAME"] = dict(
    ex="-- Renommer la table :\nALTER TABLE Eleve RENAME TO Eleves;\n\n-- Renommer une colonne (MySQL) :\nALTER TABLE Eleve CHANGE prenom prenomEleve VARCHAR(30);",
    p=[("nom1", "Ancien nom"), ("nom2", "Nouveau nom")],
    rq=["Pour une colonne, on enseigne CHANGE (ancien nom, nouveau nom, type). RENAME COLUMN n'est pas dans l'annexe."],
    k="renommer colonne table nom change")
E["ALTER TABLE ADD CONSTRAINT"] = dict(
    ex="ALTER TABLE Eleve\nADD CONSTRAINT fk_eleve_classe\nFOREIGN KEY (idClasse) REFERENCES Classe(idClasse);\n\nALTER TABLE Eleve ADD CONSTRAINT ck_moy CHECK (moyenne BETWEEN 0 AND 20);",
    p=[("nom", "Nom donné à la contrainte (pour pouvoir la supprimer)"), ("contrainte", "PRIMARY KEY, FOREIGN KEY, UNIQUE ou CHECK")],
    k="ajouter contrainte clé étrangère")
E["ALTER TABLE DROP CONSTRAINT"] = dict(ex="ALTER TABLE Eleve DROP CONSTRAINT ck_moy;", p=[("nom", "Nom de la contrainte")],
                                        rq=["D'où l'intérêt de nommer les contraintes avec CONSTRAINT nom."], k="supprimer contrainte")
E["DROP TABLE"] = dict(ex="DROP TABLE Emprunt;", p=[("table", "Table à supprimer")],
                       rq=["Supprimer d'abord les tables qui référencent celle-ci.", "IF EXISTS n'est pas dans l'annexe."], k="supprimer table")
