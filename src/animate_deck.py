#!/usr/bin/env python3
"""Ajoute transitions et animations à la présentation générée par build_deck.js.

Usage : python3 src/animate_deck.py output/G4_Presentation.pptx

- Chaque diapositive reçoit une transition en fondu (lente).
- Les formes nommées « aN_… » apparaissent en fondu, automatiquement, bloc après bloc
  (N croissant, 0,45 s entre deux blocs) : aucun clic n'est nécessaire.
"""
import re
import shutil
import sys
import tempfile
import zipfile

TRANSITION = '<p:transition spd="slow"><p:fade/></p:transition>'
STEP_MS = 450
FIRST_MS = 250
FADE_MS = 600


def effect(cid, spid, delay):
    return (
        f'<p:par><p:cTn id="{cid}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="withEffect">'
        f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>'
        f'<p:set><p:cBhvr><p:cTn id="{cid + 1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
        f'<p:to><p:strVal val="visible"/></p:to></p:set>'
        f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{cid + 2}" dur="{FADE_MS}"/>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
        f'</p:childTnLst></p:cTn></p:par>'
    )


def timing(blocks):
    cid = 5
    effects = []
    for i, (_, ids) in enumerate(sorted(blocks.items())):
        delay = FIRST_MS + i * STEP_MS
        for spid in ids:
            effects.append(effect(cid, spid, delay))
            cid += 3
    return (
        '<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
        '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
        '<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
        '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
        '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
        + "".join(effects)
        + '</p:childTnLst></p:cTn></p:par>'
        '</p:childTnLst></p:cTn></p:par>'
        '</p:childTnLst></p:cTn>'
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
    )


def process(xml):
    if "<p:transition" in xml or "<p:timing" in xml:
        return xml, 0
    blocks = {}
    for spid, block in re.findall(r'<p:cNvPr id="(\d+)" name="a(\d+)_', xml):
        blocks.setdefault(int(block), []).append(spid)
    extra = TRANSITION + (timing(blocks) if blocks else "")
    out = xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + extra, 1)
    if out == xml:
        raise SystemExit("clrMapOvr introuvable")
    return out, sum(len(v) for v in blocks.values())


def main(path):
    tmp = tempfile.mktemp(suffix=".pptx")
    total_slides = total_shapes = 0
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                xml, k = process(data.decode("utf-8"))
                data = xml.encode("utf-8")
                total_slides += 1
                total_shapes += k
            zout.writestr(item, data)
    shutil.move(tmp, path)
    print(f"[ok] {total_slides} transitions en fondu, {total_shapes} formes animées")


if __name__ == "__main__":
    main(sys.argv[1])
