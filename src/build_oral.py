#!/usr/bin/env python3
"""Fiches de l'oral à découper : A4 recto verso, 4 fiches A6 par feuille.

Usage : python3 src/build_oral.py
Produit output/G4_Fiches_Oral.pdf et build/oral_notes.json (notes de la présentation).
Impression : recto verso, retournement sur le bord long ; les versos sont en miroir.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import build  # noqa: E402
import oral as O  # noqa: E402
import reponses as REP  # noqa: E402

BUILD, OUT = ROOT / "build", ROOT / "output"
COULEURS = {1: "#0f6b66", 2: "#35558f", 3: "#7a4785", 4: "#5b741c", 5: "#9a5a12", "scene": "#b4462a"}
NBSP = " "


def verifier_citations():
    _, _, full = build.load_novel()
    low = full.lower()
    textes = []
    for t in O.TOURS:
        textes += [t["texte"]] + t["points"]
    bad = []
    for txt in textes:
        for seg in re.findall(r"«\s*(.+?)\s*»", txt):
            if build.squash(seg).lower().rstrip(".!?…") not in low:
                bad.append(seg)
    if bad:
        raise SystemExit("Citations absentes du roman :\n  " + "\n  ".join(bad))
    print(f"[ok] citations de l'oral vérifiées dans le roman")


def fr(s):
    s = html.escape(build.fr_text(s), quote=False)
    return re.sub(r"«(.+?)»", r'<em class="q">«\1»</em>', s)


def secondes(txt):
    return round(len(txt.split()) / 2.3 / 5) * 5


def cartes_parole():
    cartes = []
    for n, nom in O.NOMS.items():
        tours = [t for t in O.TOURS if t["eleve"] == n]
        total = sum(secondes(t["texte"]) for t in tours)
        for i, t in enumerate(tours, 1):
            suite = None
            idx = O.TOURS.index(t)
            if t["relais"]:
                suite = f"Tu passes la parole : « {t['relais']} »" if not t["relais"].startswith("Le groupe") else t["relais"]
            elif idx + 1 < len(O.TOURS) and O.TOURS[idx + 1]["eleve"] == n:
                suite = f"Tu enchaînes avec la diapositive {O.TOURS[idx + 1]['diapo']}."
            couleur = COULEURS[n]
            recto = f"""
              <div class="head"><span class="name" style="background:{couleur}">{nom.upper()}</span><span class="num">Fiche {i} / {len(tours)}</span></div>
              <div class="meta">Diapositive {t['diapo']} · {fr(t['titre'])}<span class="time">≈ {secondes(t['texte'])} s</span></div>
              <p class="read{' long' if len(t['texte'].split()) > 80 else ''}">{fr(t['texte'])}</p>
              {f'<div class="next" style="border-color:{couleur}">▶ {fr(suite)}</div>' if suite else ''}"""
            verso = f"""
              <div class="head"><span class="name small" style="background:{couleur}">{nom}</span><span class="num">Aide-mémoire · diapo {t['diapo']}</span></div>
              <ul class="pts">{''.join(f'<li>{fr(p)}</li>' for p in t['points'])}</ul>
              <div class="keep"><span>À retenir</span>{fr(t['retenir'])}</div>
              <div class="foot">Temps de parole total de {nom} : ≈ {total // 60} min {total % 60:02d} s</div>"""
            cartes.append((recto, verso))
    return cartes


def cartes_scene():
    """Une série de fiches par rôle, avec ses répliques (texte vérifié du roman)."""
    script = None
    for sec in REP.REPONSES[5]["sections"]:
        for kind, val in sec["blocs"]:
            if kind == "script":
                script = build.merge_script(val)
    roles = {}
    temps = ""
    for it in script:
        if len(it) == 2:
            if it[0]:
                temps = it[0]
            continue
        roles.setdefault(it[0], []).append((temps, it[1], it[2]))
    cartes = []
    for role in ["LA MÈRE", "LE PÈRE", "NAGIB", "NARRATEUR"]:
        blocs, courant, taille, dernier = [], [], 0, None
        for temps, dida, ligne in roles[role]:
            h = f'<div class="tps">{fr(temps)}</div>' if temps != dernier else ""
            dernier = temps
            b = h + f'<p class="line">{f"<i>({fr(dida)})</i> " if dida else ""}{fr(ligne)}</p>'
            if taille + len(ligne) > 520 and courant:
                blocs.append("".join(courant))
                courant, taille = [], 0
                b = f'<div class="tps">{fr(temps)} (suite)</div>' + b if not h else b
            courant.append(b)
            taille += len(ligne)
        blocs.append("".join(courant))
        if len(blocs) % 2:
            blocs.append('<p class="line muted">Fin de tes répliques. Reste en scène jusqu’au noir final.</p>')
        nb = len(blocs) // 2
        for k in range(nb):
            tete = lambda face: f"""<div class="head"><span class="name" style="background:{COULEURS['scene']}">SCÈNE · {role}</span><span class="num">Fiche {k + 1} / {nb} · {face}</span></div>
              <div class="meta">Joué par : <span class="fill"></span></div>"""
            cartes.append((tete("recto") + blocs[2 * k], tete("verso") + blocs[2 * k + 1]))
    return cartes


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Inter", sans-serif; color: #1d2433; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.sheet { width: 210mm; height: 297mm; display: grid; grid-template-columns: 105mm 105mm; grid-template-rows: 148.5mm 148.5mm; position: relative; break-after: page; overflow: hidden; }
.sheet::before { content: ""; position: absolute; left: 105mm; top: 0; bottom: 0; border-left: 0.3mm dashed #b9b2a6; }
.sheet::after { content: ""; position: absolute; top: 148.5mm; left: 0; right: 0; border-top: 0.3mm dashed #b9b2a6; }
.card { padding: 8mm 8mm 7mm; display: flex; flex-direction: column; overflow: hidden; }
.head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2.5mm; }
.name { color: #fff; font: 800 13pt/1 "Inter Display", "Inter"; letter-spacing: .06em; padding: 1.8mm 3.2mm; border-radius: 2mm; }
.name.small { font-size: 10.5pt; letter-spacing: .03em; }
.num { font: 600 8pt "Inter"; color: #7b8494; text-transform: uppercase; letter-spacing: .05em; }
.meta { font: 600 8.6pt/1.3 "Inter"; color: #5d6677; padding-bottom: 2.4mm; border-bottom: 0.3mm solid #e2dbcf; margin-bottom: 3mm; display: flex; justify-content: space-between; gap: 2mm; }
.meta .time { white-space: nowrap; color: #9a5a12; }
.meta .fill { display: inline-block; width: 40mm; border-bottom: 0.3mm solid #9aa1ad; margin-left: 1mm; }
p.read { font: 400 13.4pt/1.5 "Inter"; margin: 0; flex: 1; hyphens: auto; }
p.read.long { font-size: 12pt; }
em.q { font-family: "Caladea", serif; font-style: italic; font-size: 1.05em; color: #0d4c4f; }
.next { margin-top: 3mm; font: 600 9.2pt/1.35 "Inter"; padding: 2.4mm 3mm; border-left: 1.2mm solid; background: #f6f2eb; border-radius: 0 1.5mm 1.5mm 0; }
.next em.q { font-family: "Inter"; font-style: normal; font-size: 1em; color: inherit; }
ul.pts { margin: 1mm 0 0; padding-left: 5mm; font: 500 13pt/1.45 "Inter"; flex: 1; }
ul.pts li { margin-bottom: 2.4mm; }
.keep { background: #d6a84e; color: #0a2e33; border-radius: 2mm; padding: 2.6mm 3.2mm; font: 700 11pt/1.35 "Inter"; }
.keep span { display: block; font: 800 7.4pt "Inter"; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .8mm; }
.keep em.q { font-family: "Inter"; font-style: normal; color: inherit; }
.foot { margin-top: 2.5mm; font: 500 8pt "Inter"; color: #7b8494; }
.tps { font: 800 8pt "Inter"; letter-spacing: .1em; text-transform: uppercase; color: #b4462a; margin: 1.6mm 0 1.2mm; }
p.line { font: 400 11pt/1.45 "Inter"; margin: 0 0 2.2mm; }
p.line i { color: #5d6677; }
p.muted { color: #7b8494; font-style: italic; }
.blank { background: repeating-linear-gradient(45deg, #fafafa 0 3mm, #f2f2f2 3mm 6mm); }
"""


def main():
    verifier_citations()
    cartes = cartes_parole() + cartes_scene()
    vide = ('<div class="blank"></div>', '<div class="blank"></div>')
    while len(cartes) % 4:
        cartes.append(vide)
    pages = []
    for k in range(0, len(cartes), 4):
        grp = cartes[k:k + 4]
        rectos = "".join(f'<div class="card" id="c{k + i}r">{c[0]}</div>' if c is not vide else '<div class="card blank"></div>' for i, c in enumerate(grp))
        ordre_verso = [1, 0, 3, 2]  # miroir horizontal pour le retournement bord long
        versos = "".join(f'<div class="card" id="c{k + i}v">{grp[i][1]}</div>' if grp[i] is not vide else '<div class="card blank"></div>' for i in ordre_verso)
        pages.append(f'<section class="sheet">{rectos}</section><section class="sheet">{versos}</section>')
    doc = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Fiches de l’oral</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    BUILD.mkdir(exist_ok=True)
    hp = BUILD / "G4_Fiches_Oral.html"
    hp.write_text(doc, encoding="utf-8")
    jobs = BUILD / "oral_jobs.json"
    jobs.write_text(json.dumps([{"html": str(hp), "pdf": str(OUT / "G4_Fiches_Oral.pdf"), "check": ".card"}]), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "src" / "render_pdf.mjs"), str(jobs)], check=True)
    notes = {t["diapo"]: f"{O.NOMS[t['eleve']].upper()} — {t['texte']}" + (f"\n▶ {t['relais']}" if t["relais"] else "") for t in O.TOURS}
    (BUILD / "oral_notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=1), encoding="utf-8")
    n_pages = len(pages) * 2
    print(f"[ok] {len(cartes)} fiches, {n_pages} pages A4 (recto verso) → output/G4_Fiches_Oral.pdf")


if __name__ == "__main__":
    main()
