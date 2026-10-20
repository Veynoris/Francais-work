# Groupe 4 — Les péripéties : les étapes de la transformation

Plan de travail du groupe sur *La Civilisation, ma Mère !…* (Driss Chraïbi).

## Entrées
- `consigne.jpeg` — consigne officielle (source principale)
- `plan.md` — premier plan du groupe
- `Roman.pdf` — le roman (pages citées = pages de ce PDF)

## Sorties
- `work/` — analyse (01), critique du plan (02), feuille de route (03), dossiers individuels (04_membre_1..5)
- `output/` — `G4_00_Plan_Complet.pdf`, `G4_Membre1..5.pdf`, `G4_Tableau_Suivi.pdf`

## Régénérer après modification
Tout le contenu est dans `src/content.py`, la mise en page dans `src/templates/`.

    python3 src/build.py          # Markdown + PDF
    python3 src/build.py --png    # + aperçus PNG dans build/preview/

Le script s'arrête si une citation n'est pas trouvée mot à mot dans `Roman.pdf` (ou pas à la page annoncée), si une sous-question n'a pas exactement un propriétaire, si l'écart de charge atteint 20 %, ou si une page est vide.
Dépendances : Python 3 avec `pypdf` et `jinja2`, Node avec `playwright` (Chromium), `pdftoppm` pour les aperçus.

## Partie D (scénette) en attente
`PARTIE_D_EN_ATTENTE = True` dans `src/content.py` retire S05, S09 et S14 du calendrier actif (Gantt, Kanban, calendriers personnels, charge).
Pour la réactiver : passer à `False`, revoir les textes des dossiers (`MEMBRES`) et relancer le build.
