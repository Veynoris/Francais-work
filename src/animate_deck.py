#!/usr/bin/env python3
"""Ajoute transitions et animations à la présentation générée par build_deck.js.

Usage : python3 src/animate_deck.py output/G4_Presentation.pptx

Transitions : fondu lent ; fondu par le noir sur les diapositives de titre et de section.
Animations, toutes automatiques (aucun clic) :
  - titre de la diapositive : balayage depuis la gauche, puis sous-titre en fondu ;
  - formes « aN-T_… » : bloc N, effet T (r monte, z zoom, w balayage, f fondu),
    un bloc après l'autre ;
  - formes « a0-S_… » : rotation lente et continue (étoiles décoratives).
"""
import re
import shutil
import sys
import tempfile
import zipfile

STEP_MS, FIRST_MS, DUR = 380, 650, 700
PRESET = {"r": 42, "z": 53, "w": 22, "f": 10}


class Ids:
    def __init__(self):
        self.n = 4

    def __call__(self):
        self.n += 1
        return self.n


def tgt(spid):
    return f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'


def visible(ids, spid):
    return (f'<p:set><p:cBhvr><p:cTn id="{ids()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'{tgt(spid)}<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:to><p:strVal val="visible"/></p:to></p:set>')


def anim(ids, spid, attr, start, end):
    return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{ids()}" dur="{DUR}" decel="100000" fill="hold"/>'
            f'{tgt(spid)}<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:tavLst><p:tav tm="0"><p:val><p:strVal val="{start}"/></p:val></p:tav>'
            f'<p:tav tm="100000"><p:val><p:strVal val="{end}"/></p:val></p:tav></p:tavLst></p:anim>')


def entrance(ids, spid, fx, delay):
    cid = ids()
    parts = [visible(ids, spid)]
    if fx == "w":
        parts.append(f'<p:animEffect transition="in" filter="wipe(left)"><p:cBhvr><p:cTn id="{ids()}" dur="{DUR}"/>{tgt(spid)}</p:cBhvr></p:animEffect>')
    else:
        parts.append(f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{ids()}" dur="{DUR}"/>{tgt(spid)}</p:cBhvr></p:animEffect>')
    if fx == "r":
        parts.append(anim(ids, spid, "ppt_y", "#ppt_y+0.05", "#ppt_y"))
    if fx == "z":
        parts.append(anim(ids, spid, "ppt_w", "#ppt_w*0.70", "#ppt_w"))
        parts.append(anim(ids, spid, "ppt_h", "#ppt_h*0.70", "#ppt_h"))
    sub = 8 if fx == "w" else 0
    return (f'<p:par><p:cTn id="{cid}" presetID="{PRESET[fx]}" presetClass="entr" presetSubtype="{sub}" fill="hold" nodeType="withEffect">'
            f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>{"".join(parts)}</p:childTnLst></p:cTn></p:par>')


def spin(ids, spid):
    cid = ids()
    return (f'<p:par><p:cTn id="{cid}" presetID="8" presetClass="emph" presetSubtype="0" repeatCount="indefinite" fill="hold" nodeType="withEffect">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:animRot by="21600000"><p:cBhvr><p:cTn id="{ids()}" dur="40000" fill="hold"/>{tgt(spid)}'
            f'<p:attrNameLst><p:attrName>r</p:attrName></p:attrNameLst></p:cBhvr></p:animRot>'
            f'</p:childTnLst></p:cTn></p:par>')


def placeholders(xml):
    """(id du titre, id du sous-titre) des espaces réservés de la diapositive."""
    title = body = None
    for chunk in xml.split("<p:sp>")[1:]:
        m = re.search(r'<p:cNvPr id="(\d+)"', chunk)
        if not m:
            continue
        if '<p:ph type="title"' in chunk:
            title = m.group(1)
        elif '<p:ph type="body"' in chunk:
            body = m.group(1)
    return title, body


def timing(xml):
    ids = Ids()
    effects = []
    title, body = placeholders(xml)
    for spid in re.findall(r'<p:cNvPr id="(\d+)" name="a0-S_', xml):
        effects.append(spin(ids, spid))
    if title:
        effects.append(entrance(ids, title, "w", 0))
    if body:
        effects.append(entrance(ids, body, "f", 350))
    blocks = {}
    for spid, block, fx in re.findall(r'<p:cNvPr id="(\d+)" name="a(\d+)-([rzwf])_', xml):
        blocks.setdefault(int(block), []).append((spid, fx))
    for i, (_, items) in enumerate(sorted(blocks.items())):
        for spid, fx in items:
            effects.append(entrance(ids, spid, fx, FIRST_MS + i * STEP_MS))
    if not effects:
        return "", 0
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
            '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
            '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(effects)
            + '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn>'
            '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
            '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'), len(effects)


def process(xml):
    if "<p:transition" in xml or "<p:timing" in xml:
        return xml, 0
    hero = 'name="a0-S_' in xml
    transition = f'<p:transition spd="slow"><p:fade{" thruBlk=\"1\"" if hero else ""}/></p:transition>'
    tm, k = timing(xml)
    out = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + transition + tm, 1)
    if out == xml:
        raise SystemExit("clrMapOvr introuvable")
    return out, k


def main(path):
    tmp = tempfile.mktemp(suffix=".pptx")
    slides = effects = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                xml, k = process(data.decode("utf-8"))
                data = xml.encode("utf-8")
                slides += 1
                effects += k
            zout.writestr(item, data)
    shutil.move(tmp, path)
    print(f"[ok] {slides} transitions, {effects} effets d'animation")


if __name__ == "__main__":
    main(sys.argv[1])
