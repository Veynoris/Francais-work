// Présentation orale du Groupe 4 (PowerPoint) — thème « émeraude et or ».
// Usage : NODE_PATH=<node_modules> node src/build_deck.js <quotes.json> <sortie.pptx> <apply_theme.js>
// quotes.json est produit par src/build.py (citations vérifiées dans Roman.pdf).
// Animations (src/animate_deck.py) : une forme nommée « aN-T_… » appartient au bloc N et
// reçoit l'effet T : r = monte en fondu, z = zoom en fondu, w = balayage, f = fondu,
// S = rotation lente et continue (étoiles décoratives).
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const [QUOTES_PATH, OUT, APPLY_THEME] = process.argv.slice(2);
const Q = JSON.parse(fs.readFileSync(QUOTES_PATH, "utf8"));
const { applyTheme } = require(APPLY_THEME);

const THEME = {
  name: "Groupe 4 Emeraude et or",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0A2E33", lt1: "FFFFFF", dk2: "0F4246", lt2: "F3E9D2",
    accent1: "3BA7A0", accent2: "D6A84E", accent3: "C8664A",
    accent4: "5B8FB0", accent5: "9A7BC0", accent6: "7FA65A",
    hlink: "D6A84E", folHlink: "9A7BC0",
  },
};
const HEX = THEME.colors;
const BODY = "E3ECEA";   // texte courant sur fond sombre
const MUTED = "A3BDB9";  // texte secondaire
const REF = "8FB3AF";    // numéros de page
const GOLD = HEX.accent2;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Les péripéties : les étapes de la transformation";
pres.author = "Groupe 4";
const C = pres.SchemeColor;
const X0 = 0.6, CW = 12.13;

// ---------------------------------------------------------------- images générées
async function png(svg) { return (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64"); }
async function jpg(svg) { return (await sharp(Buffer.from(svg)).jpeg({ quality: 88 }).toBuffer()).toString("base64"); }

function background(patternOpacity, cx, glow) {
  const star = (o) => `<g fill="none" stroke="#${GOLD}" stroke-width="1.3" opacity="${o}">
      <rect x="35" y="35" width="50" height="50"/><rect x="35" y="35" width="50" height="50" transform="rotate(45 60 60)"/>
      <circle cx="60" cy="60" r="10"/><path d="M0 0L18 18M120 0L102 18M0 120L18 102M120 120L102 102"/></g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">
    <defs>
      <radialGradient id="g" cx="${cx}" cy="30%" r="85%"><stop offset="0" stop-color="#${glow}"/><stop offset="0.55" stop-color="#0C3A3F"/><stop offset="1" stop-color="#051F23"/></radialGradient>
      <pattern id="z" width="120" height="120" patternUnits="userSpaceOnUse">${star(patternOpacity)}</pattern>
      <radialGradient id="v" cx="50%" cy="50%" r="75%"><stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.35"/></radialGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#g)"/><rect width="1920" height="1080" fill="url(#z)"/><rect width="1920" height="1080" fill="url(#v)"/>
  </svg>`;
}

async function icon(Comp, color, size = 256) {
  return "image/png;base64," + (await png(ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }))));
}
const ICONS = {};
async function loadAssets() {
  const list = {
    lock: fa.FaLock, magic: fa.FaMagic, seed: fa.FaSeedling, book: fa.FaBookOpen, user: fa.FaUser,
    run: fa.FaWalking, clock: fa.FaHourglassHalf, bolt: fa.FaBolt, comment: fa.FaCommentDots, link: fa.FaLink,
    tree: fa.FaTree, egg: fa.FaFeatherAlt, sun: fa.FaSun, key: fa.FaKey, dove: fa.FaDove, question: fa.FaQuestion,
    smile: fa.FaSmile, eye: fa.FaEye, laugh: fa.FaLaughBeam, glasses: fa.FaGlasses, pen: fa.FaPenNib,
    wall: fa.FaShieldAlt, heart: fa.FaHeartBroken, balance: fa.FaBalanceScale, home: fa.FaHome, users: fa.FaUsers,
    female: fa.FaFemale, flag: fa.FaFlag, gem: fa.FaGem, theater: fa.FaTheaterMasks, compass: fa.FaCompass,
    quote: fa.FaQuoteLeft, bulb: fa.FaLightbulb, arrow: fa.FaArrowRight, crown: fa.FaCrown,
  };
  for (const [k, comp] of Object.entries(list)) {
    ICONS[k] = await icon(comp, HEX.dk1);       // sur pastille dorée
    ICONS[k + "_g"] = await icon(comp, GOLD);   // doré
    ICONS[k + "_w"] = await icon(comp, "FFFFFF");
  }
  return {
    content: "image/jpeg;base64," + (await jpg(background(0.05, "78%", "11585B"))),
    hero: "image/jpeg;base64," + (await jpg(background(0.09, "70%", "15686A"))),
  };
}

// ---------------------------------------------------------------- aides
let n = 0, BLOCK = 0, FX = "r";
const A = (k, fx = "r") => { BLOCK = k; FX = fx; };
const uid = (p) => (BLOCK || FX === "S" ? `a${BLOCK}-${FX}_${p}_${++n}` : `${p}_${++n}`);
const q = (id) => { if (!Q[id]) throw new Error("citation inconnue " + id); return Q[id]; };
const T = (s, txt, o) => s.addText(txt, { margin: 0, isTextBox: true, valign: "top", objectName: uid("txt"), ...o });

function star(s, x, y, size, color, transparency, width = 1.75) {
  const keep = [BLOCK, FX];
  A(0, "S");
  for (const rot of [0, 45]) {
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: size, h: size, rotate: rot, objectName: uid("etoile"), fill: { type: "none" }, line: { color, width, transparency } });
  }
  A(...keep);
}
function quoteRuns(id, size = 15, color = HEX.lt2) {
  const o = q(id);
  return [
    { text: `« ${o.t} »`, options: { italic: true, fontFace: THEME.headFontFace, fontSize: size, color } },
    { text: `  (p. ${o.p})`, options: { fontSize: 12, color: REF, italic: false } },
  ];
}
function medal(s, key, x, y, d = 0.66, fill = GOLD) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: "FFFFFF", width: 1, transparency: 70 }, objectName: uid("medaille") });
  const p = d * 0.27;
  s.addImage({ data: ICONS[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: uid("icone") });
}
function glass(s, x, y, w, h, gold = false) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, objectName: uid("carte"),
    fill: { color: gold ? GOLD : "FFFFFF", transparency: gold ? 84 : 93 },
    line: { color: GOLD, width: gold ? 1.25 : 0.75, transparency: gold ? 20 : 60 },
  });
}
const SECTIONS = ["Introduction", "A · La langue", "B · L’écriture", "C · Le sens", "D · La scène", "Conclusion"];
function tracker(s, current) {
  const runs = [];
  SECTIONS.forEach((t, i) => {
    const on = i === current;
    runs.push({ text: (on ? "◆ " : "") + t, options: { bold: on, color: on ? GOLD : "6F918D" } });
    if (i < SECTIONS.length - 1) runs.push({ text: "      ", options: {} });
  });
  T(s, runs, { x: X0, y: 6.97, w: 10.5, h: 0.3, fontSize: 10, valign: "middle" });
}
function header(s, kicker, who) {
  A(0);
  T(s, kicker.toUpperCase(), { x: X0, y: 0.42, w: 9.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: GOLD });
  if (who) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.85, y: 0.8, w: 1.88, h: 0.52, rectRadius: 0.26, fill: { color: GOLD, transparency: 88 }, line: { color: GOLD, width: 1, transparency: 30 }, objectName: uid("pastille") });
    s.addImage({ data: ICONS.user_g, x: 11.06, y: 0.94, w: 0.24, h: 0.24, objectName: uid("pastille_ic") });
    T(s, who, { x: 11.4, y: 0.8, w: 1.3, h: 0.52, fontSize: 14, bold: true, color: GOLD, valign: "middle" });
  }
}
function retenir(s, sentence, y = 5.95) {
  A(9, "w");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y, w: CW, h: 0.7, rectRadius: 0.12, fill: { color: GOLD }, line: { type: "none" }, objectName: uid("retenir") });
  s.addImage({ data: ICONS.bulb, x: X0 + 0.3, y: y + 0.2, w: 0.3, h: 0.3, objectName: uid("retenir_ic") });
  T(s, [{ text: "À RETENIR   ", options: { bold: true, color: HEX.dk1, fontSize: 12, charSpacing: 2 } }, { text: sentence, options: { color: HEX.dk1, fontSize: 17, bold: true } }],
    { x: X0 + 0.78, y, w: CW - 1.0, h: 0.7, valign: "middle" });
  A(0);
}
function content(title, kicker, sectionTitle, idx, who) {
  const s = pres.addSlide({ masterName: "Contenu", sectionTitle });
  s.addText(title, { placeholder: "title" });
  header(s, kicker, who);
  tracker(s, idx);
  return s;
}
function divider(sectionTitle, idx, letter, title, sub, who) {
  const s = pres.addSlide({ masterName: "Section", sectionTitle });
  star(s, 8.95, 0.95, 3.6, GOLD, 35, 2);
  star(s, 9.85, 1.85, 1.8, "FFFFFF", 75, 1.25);
  A(1, "z");
  T(s, letter, { x: 8.95, y: 0.95, w: 3.6, h: 3.6, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 120, bold: true, color: GOLD });
  A(0);
  s.addText(title, { placeholder: "title" });
  s.addText([{ text: sub, options: { breakLine: true } }, { text: who, options: { bold: true, color: GOLD } }], { placeholder: "body" });
  tracker(s, idx);
  return s;
}
// Carte : médaille, étiquette dorée, titre, phrase simple, citation
function infoCard(s, x, y, w, h, o) {
  glass(s, x, y, w, h, o.gold);
  const cy = y + 0.3;
  if (o.stack) {
    medal(s, o.icon, x + 0.3, cy, 0.64, o.iconColor || GOLD);
    T(s, o.label.toUpperCase(), { x: x + 1.08, y: cy, w: w - 1.3, h: 0.64, fontSize: 11, bold: true, charSpacing: 3, color: GOLD, valign: "middle" });
    T(s, o.title, { x: x + 0.3, y: cy + 0.82, w: w - 0.6, h: 0.45, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: "FFFFFF" });
    T(s, o.text, { x: x + 0.3, y: cy + 1.3, w: w - 0.6, h: 0.45, fontSize: 16, color: MUTED });
    T(s, quoteRuns(o.quote, 16), { x: x + 0.3, y: cy + 1.9, w: w - 0.6, h: y + h - cy - 2.1 });
    return;
  }
  medal(s, o.icon, x + 0.3, cy, 0.64, o.iconColor || GOLD);
  T(s, o.label.toUpperCase(), { x: x + 1.12, y: cy - 0.02, w: w - 1.35, h: 0.28, fontSize: 11, bold: true, charSpacing: 3, color: GOLD });
  T(s, o.title, { x: x + 1.12, y: cy + 0.24, w: w - 1.35, h: 0.45, fontFace: THEME.headFontFace, fontSize: o.titleSize || 20, bold: true, color: "FFFFFF" });
  let ty = cy + 0.98;
  if (o.text) { T(s, o.text, { x: x + 0.3, y: ty, w: w - 0.6, h: o.textH || 0.8, fontSize: 17, color: BODY }); ty += (o.textH || 0.8) + 0.15; }
  if (o.quote) T(s, quoteRuns(o.quote, 16), { x: x + 0.3, y: ty, w: w - 0.6, h: y + h - ty - 0.2 });
}

// ---------------------------------------------------------------- diapositives
async function main() {
  const BG = await loadAssets();
  pres.defineSlideMaster({
    title: "Titre",
    background: { data: BG.hero },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 8.2, h: 2.4, fontFace: THEME.headFontFace, fontSize: 46, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.65, w: 8.2, h: 1.3, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "Section",
    background: { data: BG.hero },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.95, w: 7.9, h: 1.45, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.6, w: 7.9, h: 1.0, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
    ],
    slideNumber: { x: 12.2, y: 6.97, w: 0.55, h: 0.3, fontSize: 10, color: "6F918D", align: "right" },
  });
  pres.defineSlideMaster({
    title: "Contenu",
    background: { data: BG.content },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.72, w: 9.9, h: 0.8, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "" } },
    ],
    slideNumber: { x: 12.2, y: 6.97, w: 0.55, h: 0.3, fontSize: 10, color: "6F918D", align: "right" },
  });
  let s;

  // 1. Titre
  pres.addSection({ title: "Introduction" });
  s = pres.addSlide({ masterName: "Titre", sectionTitle: "Introduction" });
  star(s, 9.2, 1.25, 3.9, GOLD, 30, 2.25);
  star(s, 10.2, 2.25, 1.9, "FFFFFF", 70, 1.25);
  star(s, 10.75, 2.8, 0.8, GOLD, 20, 1.5);
  A(1, "f");
  T(s, "GROUPE 4 · FRANÇAIS", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 6, color: GOLD });
  A(2, "f");
  T(s, "Présenté par : ________________________________", { x: 0.8, y: 6.35, w: 8, h: 0.4, fontSize: 14, color: MUTED });
  A(0);
  s.addText("Les péripéties : les étapes de la transformation", { placeholder: "title" });
  s.addText([{ text: "La Civilisation, ma Mère !…", options: { italic: true, fontFace: THEME.headFontFace, color: GOLD, breakLine: true } }, { text: "Driss Chraïbi (1972)" }], { placeholder: "body" });
  s.addNotes("ÉLÈVE 5 — Bonjour. Nous sommes le groupe 4. Nous allons vous présenter La Civilisation, ma Mère !… de Driss Chraïbi, publié en 1972, et plus précisément les étapes de la transformation de la mère.");

  // 2. Question
  s = content("Notre question", "Introduction", "Introduction", 0, "Élève 5");
  A(1, "z");
  glass(s, X0, 1.75, CW, 1.55, true);
  s.addImage({ data: ICONS.quote_g, x: X0 + 0.4, y: 2.05, w: 0.5, h: 0.5, objectName: uid("guillemet") });
  T(s, "Comment les péripéties font-elles passer la mère de l’enfermement à l’émancipation ? Gagne-t-elle un savoir, ou une nouvelle identité ?",
    { x: X0 + 1.2, y: 1.75, w: CW - 1.6, h: 1.55, fontFace: THEME.headFontFace, fontSize: 23, italic: true, color: "FFFFFF", valign: "middle" });
  [["A", "La langue", "Les mots suivent la mère", "book"], ["B", "L’écriture", "Le style rend le changement visible", "pen"], ["C", "Le sens", "Ce que signifie sa liberté", "compass"], ["D", "La scène", "Une transformation jouée", "theater"]].forEach(([l, t, d, ic], i) => {
    A(2 + i);
    const w = 2.86, x = X0 + i * (w + 0.23);
    glass(s, x, 3.55, w, 2.15);
    medal(s, ic, x + 0.3, 3.8, 0.62);
    T(s, l, { x: x + w - 0.85, y: 3.72, w: 0.55, h: 0.75, align: "right", fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: GOLD });
    T(s, t, { x: x + 0.3, y: 4.6, w: w - 0.6, h: 0.42, fontSize: 19, bold: true, color: "FFFFFF" });
    T(s, d, { x: x + 0.3, y: 5.02, w: w - 0.6, h: 0.6, fontSize: 15, color: MUTED });
  });
  retenir(s, "Notre fil rouge : la mère cherche-t-elle un savoir, ou une identité ?");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Ses deux fils font découvrir à une mère enfermée la radio, le téléphone, la rue, puis le savoir. Nous nous sommes demandé : comment ces péripéties la font-elles passer de l’enfermement à l’émancipation, et que gagne-t-elle au bout du compte, un savoir ou une identité ? Nous verrons d’abord la langue, puis l’écriture, ensuite le sens, et enfin une scène jouée. »");

  // 3. Roman
  s = content("Le roman en deux temps", "Introduction · Le roman", "Introduction", 0, "Élève 1");
  [["Partie I", "« Être »", "seed", HEX.accent1, "Raconté par le fils cadet", "La mère découvre : la radio, le téléphone, la rue, le cinéma, la lecture.", "seuil"],
   ["Partie II", "« Avoir »", "flag", HEX.accent3, "Raconté par Nagib, le fils aîné", "La mère agit : elle tient tête au père, étudie, instruit d’autres femmes.", "consciente"]].forEach(([p, t, ic, col, nar, d, qid], i) => {
    A(1 + i);
    const w = 5.95, x = X0 + i * (w + 0.23);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, iconColor: col, label: p, title: t, titleSize: 26, text: [{ text: nar, options: { bold: true, color: "FFFFFF", breakLine: true } }, { text: d }], textH: 1.35, quote: qid });
  });
  retenir(s, "Partie I : elle découvre le monde. Partie II : elle agit sur le monde.");
  s.addNotes("ÉLÈVE 1 — Pour le dire :\n« Le roman a deux parties. Dans la première, “Être”, racontée par le fils cadet, la mère découvre le monde : au début, “jamais elle n’en avait franchi le seuil”. Dans la seconde, “Avoir”, racontée par Nagib, elle agit et finit par dire : “Je suis à présent consciente, entièrement responsable de ma vie”. »");

  // 4. Chronologie
  s = content("Douze étapes de la transformation", "Introduction · Chronologie", "Introduction", 0, "Élève 1");
  const chrono = ["La recluse", "La radio", "Les objets, le téléphone", "Première sortie", "Le cinéma", "Apprendre, naître à soi", "La falaise : le doute", "L’engagement public", "Face au père", "Enterrer le passé", "Instruire les femmes", "Le départ"];
  A(1, "f");
  glass(s, X0, 1.75, CW, 3.95);
  [0, 1].forEach((row) => {
    A(2 + row, "w");
    const y = 2.25 + row * 1.75;
    s.addShape(pres.shapes.LINE, { x: X0 + 0.75, y: y + 0.3, w: CW - 1.5, h: 0, line: { color: GOLD, width: 1.5, transparency: 45 }, objectName: uid("ligne") });
    for (let i = 0; i < 6; i++) {
      A(4 + row * 6 + i, "z");
      const k = row * 6 + i, x = X0 + 0.25 + i * 1.98, col = k < 7 ? HEX.accent1 : HEX.accent3;
      s.addShape(pres.shapes.OVAL, { x: x + 0.45, y, w: 0.6, h: 0.6, fill: { color: col }, line: { color: GOLD, width: 1.5 }, objectName: uid("pastille") });
      T(s, String(k + 1), { x: x + 0.45, y, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 17, bold: true, color: "FFFFFF" });
      T(s, chrono[k], { x: x + 0.05, y: y + 0.72, w: 1.85, h: 0.65, align: "center", fontSize: 15, color: BODY });
    }
  });
  retenir(s, "Des étapes 1 à 7, elle découvre ; des étapes 8 à 12, elle agit.");
  s.addNotes("ÉLÈVE 1 — Pour le dire :\n« Voici les douze étapes. D’abord, la recluse, qui n’a jamais quitté sa maison. Ensuite, les découvertes : la radio, le téléphone, la première sortie, le cinéma, la lecture. Puis le doute, sur la falaise. Enfin, dans la deuxième partie, elle agit : elle s’engage, affronte son mari, enterre son passé, instruit d’autres femmes et part pour la France. »");

  // 5. A
  pres.addSection({ title: "A · Analyse linguistique" });
  s = divider("A · Analyse linguistique", 1, "A", "Analyse linguistique", "La langue suit la mère pas à pas", "Élève 2");
  s.addNotes("ÉLÈVE 2 — « Commençons par les mots eux-mêmes : nous allons voir comment la langue suit la mère pas à pas. »");

  // 6. A1
  s = content("Des mots qui changent avec elle", "A1 · Champs lexicaux", "A · Analyse linguistique", 1, "Élève 2");
  [["Enfermement", "lock", HEX.accent3, "prison, tombeau", "tombeau"], ["Merveilleux", "magic", HEX.accent3, "magie, magicien, génie", "magicien"], ["Naissance", "seed", HEX.accent1, "naître, nid, coquille", "naitre"], ["Savoir", "book", GOLD, "école, livres, examens", "inscrite"]].forEach(([t, ic, col, mots, qid], i) => {
    A(1 + i);
    const w = 2.86, x = X0 + i * (w + 0.23);
    infoCard(s, x, 1.75, w, 3.95, { stack: true, icon: ic, iconColor: col, label: `Étape ${i + 1}`, title: t, text: mots, quote: qid, gold: i === 3 });
  });
  retenir(s, "Les mots passent de l’enfermement au savoir : apprendre, c’est naître une seconde fois.");
  s.addNotes("ÉLÈVE 2 — Pour le dire :\n« Les champs lexicaux évoluent avec la mère. D’abord, celui de l’enfermement : la maison est un “tombeau”. Ensuite, celui du merveilleux : la radio est un “magicien”. Puis celui de la naissance : “nous la voyions naître”. Enfin, celui du savoir : “elle s’est inscrite dans une école”. Cela montre qu’apprendre, pour elle, c’est naître une seconde fois. »");

  // 7. A2
  s = content("D’objet à sujet de ses actes", "A2 · Verbes d’action", "A · Analyse linguistique", 1, "Élève 2");
  A(1);
  infoCard(s, X0, 1.75, 5.75, 3.95, { icon: "user", iconColor: HEX.accent3, label: "Avant · Partie I", title: "Ses fils agissent sur elle", text: "Elle est le complément des verbes.", textH: 0.5, quote: "habillames" });
  A(2, "z");
  s.addShape(pres.shapes.OVAL, { x: 6.27, y: 3.3, w: 0.8, h: 0.8, fill: { color: GOLD }, line: { color: HEX.dk1, width: 3 }, objectName: uid("rond") });
  s.addImage({ data: ICONS.arrow, x: 6.49, y: 3.52, w: 0.36, h: 0.36, objectName: uid("fleche") });
  A(3);
  infoCard(s, 6.98, 1.75, 5.75, 3.95, { gold: true, icon: "run", label: "Après · Partie II", title: "Elle agit, décide, commande", text: "Elle est le sujet des verbes.", textH: 0.5, quote: "telephona" });
  retenir(s, "La mère passe de complément à sujet : elle devient actrice de sa vie.");
  s.addNotes("ÉLÈVE 2 — Pour le dire :\n« Au début, la mère est le complément des verbes : ce sont ses fils qui agissent, “nous réveillâmes maman, la coiffâmes, l’habillâmes”. Dans la deuxième partie, elle devient le sujet : “elle a téléphoné à Meknès, Fès, Marrakech…”, elle peint la maison, elle s’inscrit à l’école. Ce renversement montre qu’elle devient actrice de sa vie. »");

  // 8. A3
  s = content("Un temps qui s’accélère", "A3 · Temps verbaux et indicateurs", "A · Analyse linguistique", 1, "Élève 2");
  [["Imparfait", "clock", "La vie d’avant se répète", "revenais"], ["Passé simple", "bolt", "Les premières fois, les ruptures", "lumiere"], ["Indicateurs", "run", "Le rythme s’accélère", "bruler"]].forEach(([t, ic, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, label: `Repère ${i + 1}`, title: t, text: d, textH: 0.85, quote: qid });
  });
  retenir(s, "Le récit suit son rythme : de la routine, aux ruptures, puis à l’accélération.");
  s.addNotes("ÉLÈVE 2 — Pour le dire :\n« Les temps verbaux suivent aussi le changement. L’imparfait installe la répétition de la vie d’avant. Le passé simple marque les premières fois : “la lumière fut dans la chambre”. Enfin, les indicateurs de temps montrent l’accélération : “il fallait brûler les étapes”. D’ailleurs, elle a 35 ans dans la partie I, puis “trente-sept ans” dans la partie II : on mesure le chemin parcouru. »");

  // 9. Énonciation et connecteurs
  s = content("Qui raconte, et comment", "Énonciation et connecteurs", "A · Analyse linguistique", 1, "Élève 2");
  A(1);
  infoCard(s, X0, 1.75, 5.95, 3.95, { icon: "comment", label: "Énonciation", title: "Racontée par ses fils", text: "Le cadet, puis Nagib. La mère ne raconte jamais, mais sa parole prend de plus en plus de place.", textH: 1.2, quote: "langage" });
  A(2);
  glass(s, 6.78, 1.75, 5.95, 3.95, true);
  medal(s, "link", 7.08, 2.05, 0.64);
  T(s, "CONNECTEURS", { x: 7.9, y: 2.03, w: 4.5, h: 0.28, fontSize: 11, bold: true, charSpacing: 3, color: GOLD });
  T(s, "Des étapes bien liées", { x: 7.9, y: 2.27, w: 4.6, h: 0.45, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: "FFFFFF" });
  [["Mais", "l’obstacle, puis son dépassement"], ["C’est ainsi que", "une étape en amène une autre"], ["Alors", "le basculement"], ["Tandis que", "avant et maintenant"]].forEach(([c, d], i) => {
    A(3 + i, "w");
    const y = 3.0 + i * 0.64;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.08, y, w: 1.95, h: 0.46, rectRadius: 0.23, fill: { color: GOLD }, line: { type: "none" }, objectName: uid("puce") });
    T(s, c, { x: 7.08, y, w: 1.95, h: 0.46, align: "center", valign: "middle", fontSize: 14, bold: true, color: HEX.dk1 });
    T(s, d, { x: 9.2, y, w: 3.35, h: 0.46, valign: "middle", fontSize: 16, color: BODY });
  });
  retenir(s, "Elle est racontée par ses fils, mais sa parole prend de plus en plus de place.");
  s.addNotes("ÉLÈVE 2 — Pour le dire :\n« Le roman a deux narrateurs : le fils cadet, puis Nagib. La mère ne raconte jamais, mais sa parole grandit : le père lui-même remarque qu’elle a “adopté un langage bizarre”. Enfin, les connecteurs, comme “mais”, “c’est ainsi que” ou “alors”, enchaînent les étapes : la transformation n’est pas un hasard. »");

  // 10. B
  pres.addSection({ title: "B · Analyse stylistique" });
  s = divider("B · Analyse stylistique", 2, "B", "Analyse stylistique", "L’écriture rend la transformation visible", "Élève 3");
  s.addNotes("ÉLÈVE 3 — « Les mots changent ; mais comment l’écriture nous fait-elle voir ce changement ? »");

  // 11. B1
  s = content("Images et symboles", "B1 · Procédés d’écriture", "B · Analyse stylistique", 2, "Élève 3");
  [["Métaphore de l’arbre", "tree", "Une prison, mais un printemps possible"], ["Naissance", "egg", "Apprendre, c’est renaître"], ["Allusion biblique", "sun", "« la lumière fut » : son éveil est une création"],
   ["Symboles concrets", "key", "Robe, tache verte, serviette « MOI »"], ["Personnification", "dove", "Elle dit adieu à ses objets comme à des amis"], ["Accumulation", "question", "« mon âme ? où est-elle ? »"]].forEach(([t, ic, d], i) => {
    A(1 + i);
    const col = i % 3, row = Math.floor(i / 3), w = 3.9, h = 1.85, x = X0 + col * (w + 0.215), y = 1.75 + row * (h + 0.25);
    glass(s, x, y, w, h);
    medal(s, ic, x + 0.3, y + 0.3, 0.62, row ? HEX.accent3 : GOLD);
    T(s, t, { x: x + 1.1, y: y + 0.3, w: w - 1.3, h: 0.62, fontFace: THEME.headFontFace, fontSize: 19, bold: true, color: "FFFFFF", valign: "middle" });
    T(s, d, { x: x + 0.3, y: y + 1.05, w: w - 0.6, h: 0.7, fontSize: 16, color: BODY });
  });
  retenir(s, "Chaque étape de sa transformation est rendue visible par une image ou un objet.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« Plusieurs procédés rendent la transformation visible. La métaphore de l’arbre : elle est “cerclée dans une cour de prison”, mais peut fleurir. La naissance : apprendre, c’est renaître. Une allusion biblique : “la lumière fut”. Des symboles concrets : la tache verte, la serviette “MOI”. La personnification : elle parle à ses objets avant de les enterrer. Enfin, l’accumulation de questions : “mon âme ? où est-elle ?”. »");

  // 12. B2
  s = content("Un humour au service de sa liberté", "B2 · Humour, ironie, décalage", "B · Analyse stylistique", 2, "Élève 3");
  [["Décalage", "smile", "Elle lit la technique avec ses propres repères", "bonsoir"], ["Ironie", "glasses", "Un progrès d’objets, pas d’idées", "objets"], ["Humour de Nagib", "laugh", "Le rire allège les scènes graves", "poils"]].forEach(([t, ic, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, label: `Effet ${i + 1}`, title: t, text: d, textH: 0.85, quote: qid });
  });
  retenir(s, "Le rire est tendre : il rend la mère attachante et critique la société sans violence.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« L’humour est partout, mais il sert sa liberté. D’abord, le décalage : elle souhaite “bonsoir” au magicien de la radio. Ensuite, l’ironie : le père est “moderniste d’objets, non d’idées”. Enfin, l’humour de Nagib allège les scènes graves. Ce rire est tendre : il rend la mère attachante et critique la société sans violence. »");

  // 13. B3
  s = content("Le regard des narrateurs", "B3 · Regard du narrateur", "B · Analyse stylistique", 2, "Élève 3");
  A(1);
  infoCard(s, X0, 1.75, 5.95, 3.95, { icon: "eye", iconColor: HEX.accent1, label: "Partie I", title: "Le fils cadet", text: "Il admire sa mère, mais doute parfois de sa méthode.", textH: 0.85, quote: "soleil" });
  A(2);
  infoCard(s, 6.78, 1.75, 5.95, 3.95, { icon: "laugh", iconColor: HEX.accent3, label: "Partie II", title: "Nagib", text: "Il est étonné, drôle, et accepte d’être dépassé.", textH: 0.85, quote: "connaissais" });
  retenir(s, "Les narrateurs admirent la mère, sans cacher le prix de sa liberté.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« Le regard des narrateurs valorise la mère. Le fils cadet l’admire : il assiste à “un lever de soleil sur sa solitude”. Nagib, lui, est étonné : “Je ne connaissais plus ma mère”. Mais ce regard reste lucide : la liberté a un prix, la solitude. Même le père finit par reconnaître qu’elle est “la conscience d’un monde inconscient”. »");

  // 14. C
  pres.addSection({ title: "C · Analyse thématique" });
  s = divider("C · Analyse thématique", 3, "C", "Analyse thématique", "Ce que signifie cette émancipation", "Élève 4");
  s.addNotes("ÉLÈVE 4 — « Ces procédés rendent la transformation visible. Reste à comprendre ce qu’elle signifie. »");

  // 15. C1
  s = content("Une émancipation par cercles", "C1 · Les étapes de l’émancipation", "C · Analyse thématique", 3, "Élève 4");
  A(1, "f");
  glass(s, X0, 1.75, CW, 3.95);
  A(2, "f");
  T(s, [{ text: "« Être »", options: { bold: true, color: HEX.accent1, breakLine: true } }, { text: "devenir soi", options: { color: MUTED } }], { x: X0 + 0.5, y: 2.05, w: 2.0, h: 0.7, fontSize: 17 });
  T(s, [{ text: "« Avoir »", options: { bold: true, color: HEX.accent3, breakLine: true } }, { text: "prendre sa place", options: { color: MUTED } }], { x: X0 + 2.7, y: 2.05, w: 2.2, h: 0.7, fontSize: 17 });
  ["Enfermement", "Éveil", "Sortie", "Savoir", "Doute", "Affirmation", "Rupture", "Transmission"].forEach((t, i) => {
    A(3 + i, "r");
    const w = 1.3, gap = 0.12, x = X0 + 0.5 + i * (w + gap), h = 0.55 + i * 0.3, y = 5.4 - h;
    const col = i < 5 ? HEX.accent1 : (i === 7 ? GOLD : HEX.accent3);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: col, transparency: i < 5 ? 50 - i * 10 : 0 }, line: { color: GOLD, width: 0.75, transparency: 50 }, objectName: uid("marche") });
    T(s, String(i + 1), { x, y: y + 0.08, w, h: 0.4, align: "center", fontSize: 16, bold: true, color: i === 7 ? HEX.dk1 : "FFFFFF" });
    T(s, t, { x: x - 0.1, y: y - 0.42, w: w + 0.2, h: 0.38, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "bottom" });
  });
  retenir(s, "Elle avance par cercles de plus en plus larges : soi, la famille, la société, le monde.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« L’émancipation avance par étapes, comme des marches : l’enfermement, l’éveil par les objets, la première sortie, le savoir, le doute ; puis l’affirmation face au père, la rupture avec le passé, et la transmission aux autres femmes. Ce sont des cercles de plus en plus larges : soi, la famille, la société, le monde. »");

  // 16. C2
  s = content("Ce qui la freine", "C2 · Obstacles et contradictions", "C · Analyse thématique", 3, "Élève 4");
  [["Obstacles extérieurs", "wall", HEX.accent3, "Le père et la loi, la société des hommes, la colonisation.", "pierres"], ["Résistances intérieures", "heart", HEX.accent3, "La peur, le sentiment d’avoir perdu sa vie, la solitude.", "solitude"], ["Contradictions", "balance", GOLD, "Libérée par ses fils, elle doit aussi refuser leur protection.", "tutelle"]].forEach(([t, ic, col, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, iconColor: col, label: ["Du dehors", "En elle", "Paradoxe"][i], title: t, titleSize: 18, text: d, textH: 1.15, quote: qid });
  });
  retenir(s, "Ce qui la freine vient du dehors, mais aussi d’elle-même.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Trois types d’obstacles apparaissent. Du dehors : le père, la loi, les hommes du village, qui jettent des pierres. En elle : la peur, l’angoisse, la solitude. Et une contradiction : ce sont ses fils qui la libèrent, alors elle doit aussi refuser leur protection. »");

  // 17. C3
  s = content("Une famille qui se transforme", "C3 · Les rapports familiaux", "C · Analyse thématique", 3, "Élève 4");
  A(1, "f");
  T(s, "AVANT", { x: 3.05, y: 1.72, w: 4.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: HEX.accent3 });
  T(s, "APRÈS", { x: 8.15, y: 1.72, w: 4.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 4, color: GOLD });
  [["Le père", "home", "Il l’a épousée à treize ans et décide de tout", "Il la redécouvre et se lève quand elle entre"], ["Les fils", "users", "Ils sont ses professeurs et la guident", "Elle refuse leur protection et devient le guide"], ["La société", "female", "Trois personnes, une maison fermée", "Un réseau d’amies, puis un mouvement de femmes"]].forEach(([t, ic, av, ap], i) => {
    const y = 2.1 + i * 1.22, h = 1.02;
    A(2 + i * 2, "r");
    medal(s, ic, X0, y + 0.17, 0.68);
    T(s, t, { x: X0 + 0.85, y, w: 1.55, h, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: "FFFFFF", valign: "middle" });
    glass(s, 3.05, y, 4.55, h);
    T(s, av, { x: 3.3, y, w: 4.1, h, fontSize: 16, color: BODY, valign: "middle" });
    A(3 + i * 2, "w");
    s.addImage({ data: ICONS.arrow_g, x: 7.72, y: y + 0.36, w: 0.3, h: 0.3, objectName: uid("fleche") });
    glass(s, 8.15, y, 4.58, h, true);
    T(s, ap, { x: 8.4, y, w: 4.1, h, fontSize: 16, bold: true, color: "FFFFFF", valign: "middle" });
  });
  retenir(s, "La famille dominée par le père devient une famille d’égaux.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Les apprentissages changent toute la famille. Le père l’a épousée à treize ans ; à la fin, il avoue : “c’est comme si j’avais épousé une nouvelle femme”, et il se lève quand elle entre. Les fils étaient ses professeurs ; à la fin, elle refuse leur protection. Et sa vie s’ouvre : d’une maison fermée à un mouvement de femmes. »");

  // 18. C4
  s = pres.addSlide({ masterName: "Section", sectionTitle: "C · Analyse thématique" });
  star(s, 10.3, 0.55, 2.1, GOLD, 40, 1.75);
  A(0);
  T(s, "C4 · SAVOIR OU IDENTITÉ ?", { x: 0.8, y: 0.8, w: 9, h: 0.4, fontSize: 14, bold: true, charSpacing: 5, color: GOLD });
  A(1, "w");
  T(s, "Le savoir est l’outil qui lui permet de conquérir son identité, puis d’agir pour les autres.", { x: 0.8, y: 1.45, w: 9.4, h: 1.95, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: "FFFFFF" });
  [["Elle veut être", "etre"], ["Elle dit « moi »", "moi"], ["Elle agit pour les autres", "actes"]].forEach(([t, qid], i) => {
    A(2 + i);
    const w = 3.65, x = 0.8 + i * (w + 0.25);
    glass(s, x, 3.75, w, 2.55, i === 2);
    T(s, `${i + 1}. ${t}`, { x: x + 0.3, y: 3.95, w: w - 0.6, h: 0.4, fontSize: 18, bold: true, color: GOLD });
    T(s, quoteRuns(qid, 16), { x: x + 0.3, y: 4.45, w: w - 0.6, h: 1.7 });
  });
  A(0);
  T(s, "Élève 4", { x: 10.3, y: 6.35, w: 2.43, h: 0.4, fontSize: 14, bold: true, color: GOLD, align: "right" });
  tracker(s, 3);
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Notre réponse : la mère ne cherche pas seulement à apprendre. D’abord, elle veut être : le roman dit qu’elle cherche “à être et non à avoir ou posséder”. Ensuite, elle s’affirme : elle brode le mot “MOI”. Enfin, elle agit pour les autres : “il faut que je les traduise en actes”. Le savoir est donc l’outil d’une conquête d’identité. »");

  // 19. Enjeux
  s = content("Ce que le roman dénonce", "Enjeux sociaux et philosophiques", "C · Analyse thématique", 3, "Élève 4");
  [["Condition des femmes", "female", "Les femmes n’ont pas voix au chapitre"], ["Tradition et modernité", "compass", "La vraie civilisation, ce sont les idées"], ["Colonisation", "flag", "Sa libération suit celle du pays"], ["Liberté et solitude", "heart", "La liberté a un prix"], ["Être et avoir", "gem", "Elle choisit d’abord l’être"]].forEach(([t, ic, d], i) => {
    A(1 + i, "z");
    const w = 2.25, x = X0 + i * (w + 0.22);
    glass(s, x, 1.75, w, 3.95, i === 4);
    medal(s, ic, x + (w - 0.9) / 2, 2.1, 0.9, i % 2 ? HEX.accent3 : GOLD);
    T(s, t, { x: x + 0.2, y: 3.2, w: w - 0.4, h: 0.85, fontSize: 18, bold: true, color: "FFFFFF", align: "center" });
    T(s, d, { x: x + 0.2, y: 4.1, w: w - 0.4, h: 1.3, fontSize: 16, color: BODY, align: "center" });
  });
  retenir(s, "Le roman parle d’une mère, mais aussi de toute une société en train de changer.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Au-delà de la mère, le roman pose cinq grandes questions : la condition des femmes, le lien entre tradition et modernité, la colonisation et l’indépendance, la liberté et la solitude, et enfin le choix entre être et avoir. »");

  // 20. D
  pres.addSection({ title: "D · Scénette" });
  s = divider("D · Scénette", 4, "D", "La scène", "L’affrontement entre la mère et le père", "Élève 5 et le groupe");
  s.addNotes("ÉLÈVE 5 — « Pour vous montrer cette transformation en direct, nous allons jouer une scène : l’affrontement entre la mère et le père. »");

  // 21. D contenu
  s = content("Une transformation jouée", "D · Deuxième partie, chapitre 3", "D · Scénette", 4, "Élève 5");
  [["Situation initiale", "Le père domine : il a tout payé, il décide de tout.", "paye"], ["Changement", "La mère lui tient tête et réclame une âme.", "ame"], ["Conséquence", "Elle refuse même la protection de Nagib.", "consciente"]].forEach(([t, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    glass(s, x, 1.75, w, 3.95, i === 2);
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 2.05, w: 0.64, h: 0.64, fill: { color: GOLD }, line: { type: "none" }, objectName: uid("num") });
    T(s, String(i + 1), { x: x + 0.3, y: 2.05, w: 0.64, h: 0.64, align: "center", valign: "middle", fontSize: 21, bold: true, color: HEX.dk1 });
    T(s, `TEMPS ${i + 1}`, { x: x + 1.12, y: 2.03, w: 2.5, h: 0.28, fontSize: 11, bold: true, charSpacing: 3, color: GOLD });
    T(s, t, { x: x + 1.12, y: 2.27, w: w - 1.35, h: 0.45, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: "FFFFFF" });
    T(s, d, { x: x + 0.3, y: 3.0, w: w - 0.6, h: 0.85, fontSize: 17, color: BODY });
    T(s, quoteRuns(qid, 16), { x: x + 0.3, y: 3.95, w: w - 0.6, h: 1.6 });
  });
  retenir(s, "Rôles : la mère, le père, Nagib et un narrateur · Durée : 3 à 4 minutes.");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« La scène se passe la nuit, dans le salon. D’abord, le père domine : il rappelle qu’il a “tout payé”. Ensuite, la mère lui tient tête et demande : “mon âme ? où est-elle ?”. Enfin, elle refuse même l’aide de son fils : “Je suis à présent consciente, entièrement responsable de ma vie”. »\nPuis le groupe joue la scène (script complet dans le dossier de l’Élève 5).");

  // 22. Synthèse
  pres.addSection({ title: "Conclusion" });
  s = content("Ce que conquiert la mère", "Synthèse", "Conclusion", 5, "Élève 5");
  [["A · La langue", "D’objet à sujet : elle agit et commande", "book"], ["B · L’écriture", "De la prison à la naissance, avec humour", "pen"], ["C · Le sens", "Le savoir au service de l’identité", "compass"]].forEach(([t, d, ic], i) => {
    A(1 + i);
    const y = 1.75 + i * 1.33;
    glass(s, X0, y, 6.4, 1.13);
    medal(s, ic, X0 + 0.25, y + 0.24, 0.65);
    T(s, [{ text: t, options: { bold: true, color: GOLD, breakLine: true } }, { text: d, options: { color: "FFFFFF" } }], { x: X0 + 1.15, y, w: 5.1, h: 1.13, fontSize: 17, valign: "middle" });
  });
  A(4, "z");
  glass(s, 7.28, 1.75, 5.45, 3.79, true);
  s.addImage({ data: ICONS.crown_g, x: 7.6, y: 2.05, w: 0.42, h: 0.42, objectName: uid("couronne") });
  T(s, "NOTRE RÉPONSE", { x: 8.15, y: 2.1, w: 4.3, h: 0.32, fontSize: 12, bold: true, charSpacing: 4, color: GOLD });
  T(s, "La mère conquiert une identité, et le savoir en est le moyen. Cette liberté a un prix, la solitude, mais elle transforme toute la famille.", { x: 7.6, y: 2.65, w: 4.85, h: 2.75, fontFace: THEME.headFontFace, fontSize: 21, bold: true, color: "FFFFFF" });
  retenir(s, "Elle ne veut pas seulement savoir : elle veut être.");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Pour conclure, trois constats se rejoignent. D’abord, la langue change avec elle : elle passe d’objet à sujet. Ensuite, l’écriture rend ce changement visible, avec des images de naissance et un humour tendre. Enfin, le sens est clair : elle cherche à être. Notre réponse : la mère conquiert une identité, et le savoir en est le moyen. »");

  // 23. Ouverture
  s = pres.addSlide({ masterName: "Titre", sectionTitle: "Conclusion" });
  star(s, 9.2, 1.25, 3.9, GOLD, 30, 2.25);
  star(s, 10.2, 2.25, 1.9, "FFFFFF", 70, 1.25);
  star(s, 10.75, 2.8, 0.8, GOLD, 20, 1.5);
  A(1, "f");
  T(s, "POUR OUVRIR", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 6, color: GOLD });
  A(2, "z");
  T(s, "Merci de votre attention", { x: 0.8, y: 6.3, w: 8, h: 0.5, fontSize: 20, bold: true, color: GOLD });
  A(0);
  s.addText("La vraie civilisation, c’est la mère elle-même", { placeholder: "title" });
  s.addText(quoteRuns("conscience", 20, HEX.lt2), { placeholder: "body" });
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Le titre, La Civilisation, ma Mère !…, prend alors tout son sens. La vraie civilisation, ce n’est ni la radio ni le fer à repasser : c’est la mère elle-même, devenue, selon le mot du père, “la conscience d’un monde inconscient”. Merci de votre attention. »");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ok", OUT);
}
main().catch((e) => { console.error(e); process.exit(1); });
