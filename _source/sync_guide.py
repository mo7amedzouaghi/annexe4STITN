"""Annexe 2026 : les données sont maintenues dans le dépôt guideSTI (mêmes fiches que le site du guide,
son vérificateur et l'application de bureau). Ce script les recopie ici.
Usage : python3 sync_guide.py [chemin du dépôt guideSTI]   (par défaut ../../guidesti)"""
import os, shutil, sys
ICI = os.path.dirname(os.path.abspath(__file__)); RACINE = os.path.dirname(ICI)
G = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "..", "guidesti"))
for f in ("html5", "css3", "javascript", "sql", "php"):
    shutil.copy(os.path.join(G, "_source", "annexe", f + ".json"), os.path.join(RACINE, f + ".json"))
shutil.copy(os.path.join(G, "eleves", "assets", "data.js"), os.path.join(RACINE, "assets", "data.js"))
print("Annexe synchronisée depuis", G)
