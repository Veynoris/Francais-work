#!/usr/bin/env python3
"""Génère work/*.md et output/*.pdf à partir de src/content.py.

Usage : python3 src/build.py [--png]
  --png : rend aussi chaque page en PNG dans build/preview/ pour inspection.

Étapes : vérification des citations dans Roman.pdf -> contrôles de cohérence
-> Markdown -> HTML (Jinja2) -> PDF (Chromium via Playwright, 2 passes pour le sommaire).
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import pypdf
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
import content as C  # noqa: E402

BUILD = ROOT / "build"
OUT = ROOT / "output"
WORK = ROOT / "work"
NBSP = " "


# ---------------------------------------------------------------------------
# 1. Vérification des citations et des chapitres dans Roman.pdf
# ---------------------------------------------------------------------------
def squash(s):
    s = s.replace("'", "’").replace("ʼ", "’")
    return re.sub(r"\s+", "", s)


def load_novel():
    reader = pypdf.PdfReader(str(ROOT / "Roman.pdf"))
    pages, offsets, buf = [], [], []
    pos = 0
    for p in reader.pages:
        t = squash(p.extract_text() or "")
        offsets.append(pos)
        pages.append(t)
        buf.append(t)
        pos += len(t)
    return pages, offsets, "".join(buf)


def page_of(offset, offsets):
    page = 0
    for i, o in enumerate(offsets):
        if o <= offset:
            page = i + 1
    return page


def verify_novel():
    pages, offsets, full = load_novel()
    errors = []
    for qid, (txt, page, loc) in C.QUOTES.items():
        idx = full.find(squash(txt))
        if idx < 0:
            errors.append(f"{qid}: citation introuvable : {txt}")
            continue
        found = page_of(idx, offsets)
        if found != page:
            errors.append(f"{qid}: page {page} annoncée, trouvée p. {found}")
        a, b = C.CHAPITRES[loc]
        if not (a <= page <= b):
            errors.append(f"{qid}: p. {page} hors du chapitre {loc} ({a}-{b})")
    for (part, ch), (a, b) in C.CHAPITRES.items():
        head = "I" if (part, ch) == ("I", 1) else str(ch)
        if not pages[a - 1].startswith(head):
            errors.append(f"chapitre {part}-{ch}: la page {a} ne commence pas par « {head} »")
    for st in C.CHRONOLOGIE:
        for qid in st["q"]:
            if C.QUOTES[qid][2] not in (st["loc"], st.get("loc2")):
                errors.append(f"étape {st['n']}: {qid} hors des chapitres de l'étape")
    if errors:
        raise SystemExit("Vérification du roman ÉCHOUÉE :\n  " + "\n  ".join(errors))
    print(f"[ok] {len(C.QUOTES)} citations et {len(C.CHAPITRES)} débuts de chapitre vérifiés dans Roman.pdf")


# ---------------------------------------------------------------------------
# 2. Charge de travail et contrôles de cohérence
# ---------------------------------------------------------------------------
PERIODES = [("J1-J3", 1, 3), ("J4-J7", 4, 7), ("J8-J10", 8, 10)]


def parked(st):
    return bool(C.PARTIE_D_EN_ATTENTE and st.get("partie_d"))


def actives():
    return [s for s in C.ETAPES if not parked(s)]


def charge():
    tot = {n: 0.0 for n in C.ELEVES}
    per = {n: {p[0]: 0.0 for p in PERIODES} for n in C.ELEVES}
    for st in actives():
        a, b = st["j"]
        days = b - a + 1
        for n, h in st["h"].items():
            tot[n] += h
            for d in range(a, b + 1):
                for name, lo, hi in PERIODES:
                    if lo <= d <= hi:
                        per[n][name] += h / days
    hypo = {n: sum(st["h"].get(n, 0) for st in actives() if st["niveau"] == "HYPO") for n in C.ELEVES}
    return tot, per, hypo


def ecart(values):
    return (max(values) - min(values)) / max(values) * 100


def checks():
    # chaque sous-question a exactement un propriétaire
    owners = {}
    for n, m in C.MEMBRES.items():
        for q in m["possede"]:
            owners.setdefault(q, []).append(n)
    for qid, _, _ in C.toutes_questions():
        if len(owners.get(qid, [])) != 1:
            raise SystemExit(f"{qid}: propriétaires = {owners.get(qid)}")
    # chaque étape a un responsable, des prérequis existants
    codes = {s["code"] for s in C.ETAPES}
    for s in C.ETAPES:
        if s["code"] != "JJ" and not s["h"]:
            raise SystemExit(f"{s['code']} sans responsable")
        for p in s["prereq"] + s["debloque"]:
            if p not in codes:
                raise SystemExit(f"{s['code']}: référence inconnue {p}")
    tot, _, hypo = charge()
    e_all = ecart(list(tot.values()))
    e_sans = ecart([tot[n] - hypo[n] for n in tot])
    print(f"[ok] questions : 1 propriétaire chacune ; étapes : toutes attribuées")
    print(f"[ok] charge : {', '.join(f'E{n}={h:g} h' for n, h in tot.items())} ; écart {e_all:.1f} % (sans S13 : {e_sans:.1f} %)")
    if max(e_all, e_sans) >= 20:
        raise SystemExit("Écart de charge ≥ 20 %")
    return e_all, e_sans


# ---------------------------------------------------------------------------
# 3. Aides de rendu
# ---------------------------------------------------------------------------
def fr_text(s):
    """Typographie française : espaces insécables avant ; : ! ? » et après «."""
    s = str(s)
    s = re.sub(r"\s+([;:!?»])", NBSP + r"\1", s)
    s = re.sub(r"«\s+", "«" + NBSP, s)
    s = re.sub(r"(\d) (h|min|%|citations|pages|jours)\b", r"\1" + NBSP + r"\2", s)
    s = re.sub(r"\b(p\.|ch\.|n°|Jour|Élève|Élèves|J) (\d)", r"\1" + NBSP + r"\2", s)
    return s


def fr(s):
    s = html.escape(fr_text(s), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\b(I{1,2}-\d+)", r'<span class="nobr">\1</span>', s)
    return Markup(s)


def loc_str(loc, loc2=None):
    s = f"{loc[0]}-{loc[1]}"
    if loc2:
        s += f" à {loc2[0]}-{loc2[1]}"
    return s


def hfmt(h):
    if h == int(h):
        return f"{int(h)} h"
    hh, mm = int(h), round((h - int(h)) * 60)
    return f"{hh} h {mm:02d}" if hh else f"{mm} min"


def quote(qid):
    txt, page, loc = C.QUOTES[qid]
    return {"txt": txt, "page": page, "loc": loc_str(loc), "id": qid}


def owners_str(st):
    if not st["h"]:
        return "Tous"
    ns = sorted(st["h"])
    if len(ns) == 5:
        return "Tous"
    return ", ".join(f"É{n}" for n in ns)


def ctx():
    tot, per, hypo = charge()
    e_all, e_sans = ecart(list(tot.values())), ecart([tot[n] - hypo[n] for n in tot])
    etapes = {s["code"]: s for s in C.ETAPES}
    gantt = {n: {d: [] for d in range(1, 12)} for n in C.ELEVES}
    attente_h = {n: sum(s["h"].get(n, 0) for s in C.ETAPES if parked(s)) for n in C.ELEVES}
    for s in actives():
        a, b = s["j"]
        who = list(s["h"]) if s["h"] else list(C.ELEVES)
        for n in who:
            for d in range(a, b + 1):
                gantt[n][d].append(s)
    return dict(C=C, tot=tot, per=per, hypo=hypo, e_all=e_all, e_sans=e_sans, etapes=etapes,
                gantt=gantt, periodes=[p[0] for p in PERIODES], attente_h=attente_h, parked=parked,
                actives=actives(), parked_steps=[s for s in C.ETAPES if parked(s)], quote=quote, loc_str=loc_str,
                hfmt=hfmt, owners_str=owners_str, niv=lambda k: C.NIVEAUX[k][0])


def perso(n, c):
    """Calendrier personnel de l'élève n : (jour, étapes, livraisons dues, réceptions attendues)."""
    def day_of(txt):
        mm = re.search(r"Jour (\d+)", txt)
        return int(mm.group(1)) if mm else None
    m = C.MEMBRES[n]
    rows = []
    for d in range(1, 12):
        sts = list(c["gantt"][n][d])
        outs = [(w, q) for w, q, t in m["sorties"] if day_of(t) == d]
        ins = [(w, q) for w, q, t in m["entrees"] if day_of(t) == d]
        if sts or outs or ins:
            rows.append((d, sts, outs, ins))
    return rows


# ---------------------------------------------------------------------------
# 4. Markdown (work/)
# ---------------------------------------------------------------------------
def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def mq(qid):
    q = quote(qid)
    return f"« {q['txt']} » ({q['loc']}, p. {q['page']})"


def write_md(c):
    WORK.mkdir(exist_ok=True)
    niv = c["niv"]
    # ---- 01 analyse
    L = ["# Phase 1 — Analyse de la consigne et du roman", "",
         f"Sources : `consigne.jpeg` (source principale), `plan.md`, `Roman.pdf` ({C.META['edition_pdf']}). `infos.md` est absent.", "",
         "## Question centrale", "", C.QUESTION_CENTRALE, "",
         "## Les trois axes de la consigne", ""]
    L += [f"- **{a}** — {t}" for a, t in C.CONSIGNE["axes"]]
    L += ["", "## Sous-questions et propriétaires", "", C.ATTRIBUTION_NOTE, ""]
    rows = []
    for qid, txt, p in C.toutes_questions():
        n = p["eleve"]
        rows.append([qid, txt, f"Élève {n} — {C.ELEVES[n]['role']}", niv("EXIGE")])
    L += [md_table(["Code", "Question (verbatim)", "Propriétaire unique", "Niveau"], rows), ""]
    L += ["### Rôles et productions attendues (verbatim)", ""]
    L += [md_table(["Élève", "Responsabilité", "Production attendue"], [[n, e["role"], e["prod"]] for n, e in C.ELEVES.items()]), ""]
    L += ["### Rôles sans question propre", ""] + [f"- **{a}** : {b}" for a, b in C.ROLES_SANS_QUESTION]
    L += ["", "Contrôle : aucune question orpheline, aucune question avec deux propriétaires.", "",
          "## Exigences implicites", ""] + [f"- [{niv(k)}] {t}" for k, t in C.EXIGENCES_IMPLICITES]
    L += ["", "## Chevauchements et règles de frontière", ""]
    for i, f in enumerate(C.FRONTIERES, 1):
        L += [f"{i}. **{f['zone']}** — {f['regle']} *Test :* {f['test']}"]
    L += ["", "## Repères du roman", ""] + [f"- {r}" for r in C.REPERES_ROMAN]
    L += ["", "## Chronologie de la transformation (12 étapes)", "",
          "Toutes les citations ci-dessous ont été vérifiées mot à mot dans Roman.pdf par `src/build.py`.", ""]
    for st in C.CHRONOLOGIE:
        L += [f"**{st['n']}. {st['titre']}** — {loc_str(st['loc'], st.get('loc2'))}, p. {st['pages']} — axe {st['axe']}", "",
              st["fait"], ""] + [f"- {mq(q)}" for q in st["q"]] + [""]
    L += ["## Épisodes candidats pour la scénette (D)", ""]
    for ep in C.EPISODES:
        L += [f"### {ep['id']} — {ep['titre']} ({loc_str(ep['loc'])}, p. {ep['pages']})", "",
              md_table(["Temps", "Contenu", "Preuve"], [["Situation initiale", ep["si"][0], mq(ep["si"][1])],
                                                       ["Changement", ep["chg"][0], mq(ep["chg"][1])],
                                                       ["Conséquence", ep["csq"][0], mq(ep["csq"][1])]]), "",
              f"- Rôles : {ep['roles']}", f"- Atouts : {ep['atouts']}", f"- Limites : {ep['limites']}",
              f"- Grille ({' / '.join(C.CRITERES_EPISODE)}) : {' / '.join(map(str, ep['score']))} sur 3 — total {sum(ep['score'])}/12",
              f"- Verdict : **{ep['reco']}**", ""]
    L += [f"Épisode écarté : **{C.EPISODE_ECARTE[0]}** — {C.EPISODE_ECARTE[1]}", ""]
    (WORK / "01_analyse.md").write_text("\n".join(L), encoding="utf-8")

    # ---- 02 critique
    tot, per = c["tot"], c["per"]
    L = ["# Phase 2 — Critique du plan initial (`plan.md`)", "", "## Points forts", ""] + [f"- {x}" for x in C.CRITIQUE["forces"]]
    L += ["", "## Constats", ""]
    L += [md_table(["Thème", "Constat", "Gravité"], [[x["theme"], x["constat"], x["gravite"]] for x in C.CRITIQUE["constats"]]), ""]
    L += ["## Charge recalculée", "",
          "Charge du plan initial : heures annoncées (hors 2 h de répétitions). Charge recalculée : somme des heures des étapes de la feuille de route, répétitions et réunions comprises.", ""]
    rows = []
    for n in C.ELEVES:
        p = per[n]
        rows.append([f"Élève {n}", hfmt(C.PLAN_INITIAL_CHARGE[n]), hfmt(tot[n]), *(hfmt(round(p[k] * 2) / 2) for k in c["periodes"]),
                     hfmt(c["hypo"][n]) if c["hypo"][n] else "—"])
    L += [md_table(["Élève", "Plan initial", "Recalculée", *c["periodes"], "dont HYPOTHÈSE (S13)"], rows), "",
          f"Écart max/min : {c['e_all']:.1f} % (avec S13), {c['e_sans']:.1f} % (sans S13). L’écart reste sous 20 %.", "",
          "Profil temporel : l’Élève 1 travaille surtout aux jours 1 à 3 et l’Élève 5 aux jours 7 à 10. L’Élève 5 aide au corpus de la partie II (S04) pour alléger l’Élève 1 ; la vérification (S10) occupe l’Élève 1 au milieu du projet.", "",
          "Partie D en attente : les heures de S05, S09 et S14 ne sont pas comptées ci-dessus (" + ", ".join(f"É{n} {hfmt(h)}" for n, h in c["attente_h"].items() if h) + ").", "",
          "## Corrections proposées", ""]
    L += [f"{i}. {a} — *{b}*" for i, (a, b) in enumerate(C.CRITIQUE["corrections"], 1)]
    L += ["", "## Journal des modifications par rapport à plan.md", "", "Les étiquettes [AJOUT] signalent tout ce qui n’existait pas dans plan.md.", ""]
    L += [f"- [{k}] {t}" for k, t in C.JOURNAL]
    (WORK / "02_critique.md").write_text("\n".join(L), encoding="utf-8")

    # ---- 03 roadmap
    L = ["# Phase 3 — Feuille de route", "", "`infos.md` est absent, d’où un calendrier relatif : Jour 1 à Jour 10, puis Jour J (J11). Le jour 10 sert de tampon.", "",
         "## Étapes", ""]
    rows = []
    for s in C.ETAPES:
        a, b = s["j"]
        rows.append([("◆ " if s["critique"] else "") + ("⏸ " if parked(s) else "") + s["code"], s["titre"] + (" (EN ATTENTE)" if parked(s) else ""), f"J{a}" + (f"-J{b}" if b != a else ""), owners_str(s),
                     ", ".join(s["prereq"]) or "—", s["livrable"], s["validation"], ", ".join(s["debloque"]) or "—", niv(s["niveau"])])
    L += [md_table(["Code", "Étape", "Jours", "Responsables", "Prérequis", "Livrable", "Critère de validation", "Débloque", "Niveau"], rows), "",
          "◆ = sur le chemin critique. ⏸ = en attente (partie D) : hors du calendrier actif.", "",
          f"**Partie D en attente.** {C.ATTENTE_D['statut']} {C.ATTENTE_D['exige']} Décision au plus tard : {C.ATTENTE_D['reprise']}. {C.ATTENTE_D['pourquoi']}", "", "### Actions par étape", ""]
    for s in C.ETAPES:
        L += [f"- **{s['code']}** : " + " ; ".join(s["actions"])]
    L += ["", "## Chemin critique", "", " → ".join(C.CHEMIN_CRITIQUE), "",
          "S03 et S13 ne sont pas critiques. S05, S09 et S14 (partie D) sont en attente.", "",
          "## Points de contrôle", ""]
    for k, cp in C.CHECKPOINTS.items():
        L += [f"### {k} — {c['etapes'][k]['titre']} ({cp['quand']})", "", f"Réussite : {cp['reussite']}", "", "En cas d’échec :"] + [f"- {x}" for x in cp["echec"]] + [""]
    L += ["## Gantt", ""]
    head = ["Élève"] + [f"J{d}" if d < 11 else "Jour J" for d in range(1, 12)] + ["Total"]
    rows = []
    for n in C.ELEVES:
        rows.append([f"É{n}"] + [" ".join(s["code"] for s in c["gantt"][n][d]) or "·" for d in range(1, 12)] + [hfmt(tot[n])])
    L += [md_table(head, rows), "", "## Budget de l’oral (HYPOTHÈSE)", ""]
    L += [md_table(["Partie", "Qui", "Durée"], [[a, f"Élève {b}", d] for a, b, d in C.BUDGET_ORAL["lignes"]])]
    (WORK / "03_roadmap.md").write_text("\n".join(L), encoding="utf-8")

    # ---- 04 membres
    qtxt = {qid: txt for qid, txt, _ in C.toutes_questions()}
    for n, m in C.MEMBRES.items():
        e = C.ELEVES[n]
        L = [f"# Dossier de l’Élève {n} — {e['role']}", "", f"Production attendue (consigne) : *{e['prod']}*", "", "## Mission", ""]
        L += [f"- {x}" for x in m["mission"]] + ["", f"**Pourquoi c’est important.** {m['pourquoi']}", "", "## Ce que tu possèdes (verbatim)", ""]
        if m.get("possede_axes"):
            L += [f"> {C.CONSIGNE['intro']}"] + [f"> - {t}" for _, t in C.CONSIGNE["axes"]]
            L += ["", "Tu n’as pas de question A-D : ta production attendue est le socle de toutes les autres."]
        for q in m["possede"]:
            L += [f"- **{q}** — {qtxt[q]}"]
        L += ["", "## Frontières", ""] + [f"- {x}" for x in m["frontieres"]]
        fm = C.FICHE_METHODE[n]
        L += ["", f"## Fiche méthode : {fm['titre']}", ""] + md_method(n, fm)
        L += ["", "## Entrées (ce dont tu as besoin)", "", md_table(["De qui", "Quoi", "Quand"], m["entrees"]),
              "", "## Sorties (ce que les autres attendent de toi)", "", md_table(["Pour qui", "Quoi", "Quand"], m["sorties"]),
              "", "## Ton calendrier", ""]
        L += [md_table(["Jour", "Étapes"], [[f"J{d}" if d < 11 else "Jour J", " ; ".join(f"{s['code']} {s['titre']}" + (f" ({hfmt(s['h'][n])})" if n in s["h"] else "") for s in sts)] for d, sts, _, _ in perso(n, c)])]
        L += ["", f"Charge totale : {hfmt(tot[n])}.", "", "## Définition de « terminé »", ""] + [f"- [ ] {x}" for x in m["termine"]]
        L += ["", "## Règles communes", ""] + [f"- **{a}** : {b}" for a, b in C.REGLES_COMMUNES]
        L += ["", "Modèle de compte rendu :", ""] + [f"    {x}" for x in C.ORGANISATION["compte_rendu"]]
        (WORK / f"04_membre_{n}.md").write_text("\n".join(L), encoding="utf-8")
    print(f"[ok] work/ : 01_analyse.md, 02_critique.md, 03_roadmap.md, 04_membre_1..5.md")


def md_method(n, fm):
    L = []
    if n == 1:
        L += [f"{i}. {x}" for i, x in enumerate(fm["etapes"], 1)]
        L += ["", "Chronologie de référence (à vérifier et à compléter) :", "",
              md_table(["Étape", "Réf.", "Citation(s) n°"], [[f"{s['n']}. {s['titre']}", f"{loc_str(s['loc'], s.get('loc2'))}, p. {s['pages']}", ""] for s in C.CHRONOLOGIE]),
              "", md_table(fm["colonnes"], [[i] + [""] * 5 for i in range(1, 6)]), "", "Rapport de vérification :", "",
              md_table(fm["verif_colonnes"], [[""] * 4 for _ in range(3)])]
    elif n == 2:
        for r, aide in fm["rubriques"]:
            L += [f"**{r}** — {aide}", "", md_table(fm["colonnes"], [[""] * 3] * fm["lignes_par_rubrique"]), ""]
    elif n == 3:
        L += [md_table(["Procédé", "Repère", *fm["colonnes"][1:]], [[a, b, "", ""] for a, b in fm["procedes"]]), "",
              "B2 :", "", md_table(["Type", "Citation", "Effet"], [[x, "", ""] for x in fm["b2"]]), "",
              "B3 :", "", md_table(["Narrateur", "Marques du regard", "Valorise ou interroge ?"], [[x, "", ""] for x in fm["b3"]])]
    elif n == 4:
        L += [md_table(["Bloc", "Contenu attendu", "Ta réponse"], [[a, b, ""] for a, b in fm["structure"]]), "",
              "C1 :", "", md_table(fm["c1_colonnes"], [[""] * 4] * 4), "", "C4 — positions possibles :", ""]
        L += [f"- **{a}** : {b}" for a, b in fm["c4_positions"]]
        L += ["", "Notre thèse en une phrase : ______", "", "Enjeux à nommer : " + ", ".join(fm["enjeux"])]
    elif n == 5:
        if C.PARTIE_D_EN_ATTENTE:
            A = C.ATTENTE_D
            L += [f"> **Partie D en attente** (décision au plus tard au {A['reprise'].lower()}). {A['exige']} {A['pourquoi']}", "",
                  "Épisodes déjà analysés : voir 01_analyse.md (EP-A, EP-B, EP-C). Recommandation : EP-B, repli EP-A.", ""]
        else:
            L += ["Épisodes candidats : voir 01_analyse.md (EP-A, EP-B, EP-C).", "",
                  md_table(["Rubrique", "À remplir"], [[x, ""] for x in fm["script_entete"]]), ""]
            for t, aide in fm["temps"]:
                L += [f"**{t}** — {aide}", "", md_table(fm["temps_colonnes"], [[""] * 3] * 2), ""]
            L += [md_table(["Répétition", "Quand", "Contenu"], fm["repetitions"]), ""]
        L += ["Plan de la synthèse orale :", ""]
        L += [f"{i}. **{a}** — {b} : ______" for i, (a, b) in enumerate(fm["synthese"], 1)]
    return L


# ---------------------------------------------------------------------------
# 5. HTML -> PDF
# ---------------------------------------------------------------------------
def env():
    e = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=True, trim_blocks=True, lstrip_blocks=True)
    e.filters["fr"] = fr
    e.filters["h"] = hfmt
    return e


def print_pdfs(jobs):
    spec = BUILD / "jobs.json"
    spec.write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(SRC / "render_pdf.mjs"), str(spec)], check=True)


def pdf_pages_text(path):
    return [squash(p.extract_text() or "") for p in pypdf.PdfReader(str(path)).pages]


def find_toc_pages(pdf, titles, after):
    pages = pdf_pages_text(pdf)
    res = {}
    for key, title in titles:
        t = squash(title)
        for i in range(after, len(pages)):
            if t in pages[i]:
                res[key] = i + 1
                break
    return res


def build_docs(c, png=False):
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    e = env()
    css = (SRC / "templates" / "style.css").read_text(encoding="utf-8")
    docs = [("G4_00_Plan_Complet", "plan.html.j2", {"toc_after": 2})]
    docs += [(f"G4_Membre{n}", "membre.html.j2", {"n": n, "mb": C.MEMBRES[n], "e": C.ELEVES[n], "fm": C.FICHE_METHODE[n],
                                                  "perso": perso(n, c), "toc_after": 1}) for n in C.MEMBRES]
    docs += [("G4_Tableau_Suivi", "kanban.html.j2", {})]

    def render(toc_pages):
        jobs = []
        for name, tpl, extra in docs:
            h = e.get_template(tpl).render(css=Markup(css), toc_pages=toc_pages.get(name, {}), **c, **extra)
            hp = BUILD / f"{name}.html"
            hp.write_text(h, encoding="utf-8")
            jobs.append({"html": str(hp), "pdf": str(OUT / f"{name}.pdf")})
        print_pdfs(jobs)

    # passe 1 : sans numéros de page ; passe 2 : sommaire numéroté
    render({})
    toc = {}
    for name, tpl, extra in docs:
        titles = re.findall(r'data-toc="([^"]+)" data-title="([^"]+)"', (BUILD / f"{name}.html").read_text(encoding="utf-8"))
        if titles:
            titles = [(k, html.unescape(t)) for k, t in titles]
            toc[name] = find_toc_pages(OUT / f"{name}.pdf", titles, after=extra["toc_after"])
    render(toc)
    afters = {name: extra.get("toc_after", 1) for name, _, extra in docs}
    toc2 = {name: find_toc_pages(OUT / f"{name}.pdf",
                                 [(k, html.unescape(t)) for k, t in re.findall(r'data-toc="([^"]+)" data-title="([^"]+)"', (BUILD / f"{name}.html").read_text(encoding="utf-8"))], afters[name])
            for name in toc}
    if toc2 != toc:
        raise SystemExit("Le sommaire a changé entre les deux passes")

    # contrôles sur les fichiers produits
    report = []
    for name, _, extra in docs:
        pdf = OUT / f"{name}.pdf"
        n_pages = len(pypdf.PdfReader(str(pdf)).pages)
        report.append((name, n_pages))
    member_text = {n: squash(html.unescape(re.sub(r"<[^>]+>", " ", (BUILD / f"G4_Membre{n}.html").read_text(encoding="utf-8"))).replace(NBSP, " ")) for n in C.MEMBRES}
    for qid, txt, p in C.toutes_questions():
        where = [n for n, t in member_text.items() if squash(fr_text(txt).replace(NBSP, " ")) in t]
        if where != [p["eleve"]]:
            raise SystemExit(f"{qid} apparaît dans les dossiers {where}, attendu [{p['eleve']}]")
    # aucune page vide ; numéros de page cités = vérifiés
    for name, _ in report:
        for i, t in enumerate(pdf_pages_text(OUT / f"{name}.pdf"), 1):
            if len(t) < 40:
                raise SystemExit(f"{name} p. {i} : page vide ou quasi vide")
    print("[ok] chaque sous-question apparaît dans exactement un dossier individuel ; aucune page vide")
    for name, n_pages in report:
        print(f"     {name}.pdf : {n_pages} page(s)")
    if png:
        prev = BUILD / "preview"
        prev.mkdir(exist_ok=True)
        for old in prev.glob("*.png"):
            old.unlink()
        for name, _ in report:
            subprocess.run(["pdftoppm", "-r", "60", "-png", str(OUT / f"{name}.pdf"), str(prev / name)], check=True)
        print(f"[ok] aperçus PNG dans {prev.relative_to(ROOT)}/")
    return report


def main():
    verify_novel()
    checks()
    c = ctx()
    write_md(c)
    build_docs(c, png="--png" in sys.argv)


if __name__ == "__main__":
    main()
