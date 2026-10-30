# Sources de l'Assistant Annexe STI

**Annexe 2026 (aides pédagogiques de septembre 2026).** Les fiches sont désormais maintenues dans le
dépôt `guideSTI` (site du guide, vérificateur, application de bureau) et recopiées ici par :

```
cd _source
python3 sync_guide.py ../../guidesti
```

`build.py` reconstruit l'ancienne annexe (avant 2026) : ne plus l'utiliser pour publier.

| Fichier | Contenu |
|---|---|
| `annexe_origine/*.json` | Annexe officielle d'origine (définitions, attributs, syntaxes) |
| `enrichi_html.py`, `enrichi_css.py`, `enrichi_js.py`, `enrichi_sql.py`, `enrichi_php.py` | Pour chaque élément : exemple conforme, paramètres, valeur de retour, valeurs possibles, remarques, mots-clés de recherche |
| `hors_annexe.py` | Techniques fréquentes hors annexe et leur alternative conforme |
| `build.py` | Fusion : écrit les `*.json` enrichis à la racine et `assets/data.js` |

Après une modification :

```
cd _source
python3 build.py
```

Le build signale tout élément de l'annexe sans enrichissement. Le niveau
d'introduction (2ème, 3ème, 4ème) est défini dans `build.py` (N2, N4, CAT4).
