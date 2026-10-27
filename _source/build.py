"""Fusionne l'annexe (JSON) et les enrichissements, puis écrit :
- les fichiers *.json enrichis à la racine du dépôt ;
- assets/data.js (données chargées par le chatbot, fonctionne aussi hors connexion).
Usage : python3 build.py"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

import enrichi_html, enrichi_css, enrichi_js, enrichi_sql, enrichi_php  # noqa: E402
from hors_annexe import HORS_ANNEXE  # noqa: E402

LANGUES = [("html5", "HTML5", enrichi_html.E), ("css3", "CSS3", enrichi_css.E), ("javascript", "JavaScript", enrichi_js.E),
           ("sql", "SQL", enrichi_sql.E), ("php", "PHP", enrichi_php.E)]
CLES = ("balise", "sélecteur", "propriété", "méthode", "fonction", "opérateur", "événement",
        "attribut", "commande", "contrainte", "variable", "type")

N2 = {
    "html5": {"<html>", "<head>", "<body>", "<meta>", "<title>", "<style>", "<p>", "<h1> à <h6>", "<hr>", "<img>",
              "<audio>", "<video>", "<a>", "<br>", "<ul>", "<ol>", "<li>", "<table>", "<thead>", "<tbody>", "<tfoot>",
              "<tr>", "<th>", "<td>", "<caption>", "<form>", "<fieldset>", "<legend>", "<label>", "<input>",
              "<textarea>", "<select>", "<option>", "style", "lang"},
    "css3": {"element", "font-family", "font-weight", "font-style", "font-size", "font", "text-align", "color",
             "border-color", "border-style", "border-width", "border", "background-color", "background-image",
             "background-repeat", "background"},
}
N4 = {
    "html5": {"<datalist>", "onmouseover", "onmouseout", "onplay", "onpause", "onsubmit", "onkeydown", "onkeyup"},
    "css3": {"element[attr]", "element[attr=valeur]", "element.class", "a:link", "a:visited", ":focus", "a:active", "filter"},
    "javascript": {"document.getElementsByName()"},
    "sql": {"ON UPDATE CASCADE", "ON DELETE CASCADE"},
}
CAT4 = {
    "javascript": {"Modification du contenu, des attributs ou des styles des éléments HTML"},
    "sql": {"Fonctions définies sur le type date", "Fonctions d'agrégation", "Définition des données"},
}


def niveau(lang, cat, nom):
    if lang == "php":
        return 4
    if nom in N4.get(lang, ()) or cat in CAT4.get(lang, ()):
        return 4
    if nom in N2.get(lang, ()):
        return 2
    return 3


def main():
    tout, manquants = [], []
    for lang, nom_lang, E in LANGUES:
        src = json.load(open(os.path.join(ICI, "annexe_origine", f"{lang}.json"), encoding="utf-8"))
        sortie = {}
        for cat, items in src.items():
            sortie[cat] = []
            for it in items:
                nom = next(it[k] for k in CLES if k in it)
                cle_nom = next(k for k in CLES if k in it)
                if lang == "javascript" and nom == "+" and cat == "Les chaînes de caractères":
                    e = enrichi_js.CONCAT
                else:
                    e = E.get(nom)
                if not e:
                    manquants.append(f"{nom_lang} | {cat} | {nom}")
                    e = {}
                n = niveau(lang, cat, nom)
                neuf = dict(it)
                neuf["définition"] = it.get("définition", "").replace("*", "")
                if e.get("ex"):
                    neuf["exemple"] = e["ex"]
                if e.get("p"):
                    neuf["paramètres"] = [{"nom": a, "rôle": b} for a, b in e["p"]]
                if e.get("r"):
                    neuf["retour"] = e["r"]
                if e.get("v"):
                    neuf["valeurs"] = e["v"]
                if e.get("rq"):
                    neuf["remarques"] = e["rq"]
                neuf["niveau"] = n
                neuf["motsClés"] = e.get("k", "")
                sortie[cat].append(neuf)
                fiche = {"l": nom_lang, "c": cat, "e": nom, "t": cle_nom, "d": neuf["définition"], "n": n,
                         "ex": neuf.get("exemple", ""), "p": neuf.get("paramètres", []), "r": neuf.get("retour", ""),
                         "v": neuf.get("valeurs", ""), "rq": neuf.get("remarques", []), "k": neuf["motsClés"]}
                for extra in ("attributs", "valeurs_attributs", "types", "syntaxe"):
                    if extra in it:
                        fiche[extra] = it[extra]
                tout.append(fiche)
        with open(os.path.join(RACINE, f"{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(sortie, f, ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(RACINE, "assets"), exist_ok=True)
    with open(os.path.join(RACINE, "assets", "data.js"), "w", encoding="utf-8") as f:
        f.write("window.ANNEXE = " + json.dumps(tout, ensure_ascii=False, separators=(",", ":")) + ";\n")
        f.write("window.HORS_ANNEXE = " + json.dumps(HORS_ANNEXE, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(len(tout), "éléments ;", len(HORS_ANNEXE), "entrées hors annexe")
    if manquants:
        print("Sans enrichissement :")
        print("\n".join(manquants))


if __name__ == "__main__":
    main()
