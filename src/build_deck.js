// Présentation orale du Groupe 4 (PowerPoint).
// Usage : NODE_PATH=<node_modules> node src/build_deck.js <quotes.json> <sortie.pptx> <apply_theme.js>
// quotes.json est produit par src/build.py (citations vérifiées dans Roman.pdf).
// Les formes nommées « aN_… » apparaissent en fondu, bloc par bloc (voir src/animate_deck.py).
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
  name: "Groupe 4 Chraibi",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1C2B33", lt1: "FFFFFF", dk2: "0D4C4F", lt2: "F2F6F6",
    accent1: "0E7C7B", accent2: "D99A2B", accent3: "B5523A",
    accent4: "3E6E8E", accent5: "7A5C99", accent6: "5F7F3A",
    hlink: "0E7C7B", folHlink: "7A5C99",
  },
};
const HEX = THEME.colors;
const MUTED = "5E6B73";
const SOFT = "9FC3C1";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Les péripéties : les étapes de la transformation";
pres.author = "Groupe 4";
const C = pres.SchemeColor;
const X0 = 0.6, CW = 12.13; // marge gauche et largeur utile

// ---------------------------------------------------------------- icônes
async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}
const ICONS = {};
async function loadIcons() {
  const list = {
    lock: fa.FaLock, magic: fa.FaMagic, seed: fa.FaSeedling, book: fa.FaBookOpen, user: fa.FaUser,
    run: fa.FaWalking, clock: fa.FaHourglassHalf, bolt: fa.FaBolt, comment: fa.FaCommentDots, link: fa.FaLink,
    tree: fa.FaTree, egg: fa.FaFeatherAlt, sun: fa.FaSun, key: fa.FaKey, dove: fa.FaDove, question: fa.FaQuestion,
    smile: fa.FaSmile, eye: fa.FaEye, laugh: fa.FaLaughBeam, glasses: fa.FaGlasses, pen: fa.FaPenNib,
    wall: fa.FaShieldAlt, heart: fa.FaHeartBroken, balance: fa.FaBalanceScale, home: fa.FaHome, users: fa.FaUsers,
    female: fa.FaFemale, flag: fa.FaFlag, gem: fa.FaGem, theater: fa.FaTheaterMasks, compass: fa.FaCompass,
    quote: fa.FaQuoteLeft, bulb: fa.FaLightbulb, arrow: fa.FaArrowRight,
  };
  for (const [k, comp] of Object.entries(list)) {
    ICONS[k] = await icon(comp, "FFFFFF");
    ICONS[k + "_t"] = await icon(comp, HEX.accent1);
    ICONS[k + "_s"] = await icon(comp, HEX.accent2);
  }
}

// ---------------------------------------------------------------- mises en page
pres.defineSlideMaster({
  title: "Titre",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.1, w: 8.4, h: 2.2, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.5, w: 8.4, h: 1.3, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Section",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 3.0, w: 8.2, h: 1.4, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.55, w: 8.2, h: 1.0, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 6.95, w: 0.55, h: 0.3, fontSize: 10, color: SOFT, align: "right" },
});
pres.defineSlideMaster({
  title: "Contenu",
  background: { color: HEX.lt2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.72, w: 9.9, h: 0.8, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 6.95, w: 0.55, h: 0.3, fontSize: 10, color: MUTED, align: "right" },
});

// ---------------------------------------------------------------- aides
let n = 0, BLOCK = 0;
const A = (k) => { BLOCK = k; };
const uid = (p) => (BLOCK ? `a${BLOCK}_${p}_${++n}` : `${p}_${++n}`);
const q = (id) => { if (!Q[id]) throw new Error("citation inconnue " + id); return Q[id]; };
const shadow = () => ({ type: "outer", blur: 10, offset: 2, angle: 90, color: "0D4C4F", opacity: 0.12 });
const T = (s, txt, o) => s.addText(txt, { margin: 0, isTextBox: true, valign: "top", objectName: uid("txt"), ...o });

function star(s, x, y, size, color, transparency, width = 2) {
  for (const rot of [0, 45]) {
    s.addShape(pres.shapes.RECTANGLE, { x, y, w: size, h: size, rotate: rot, objectName: uid("etoile"), fill: { type: "none" }, line: { color, width, transparency } });
  }
}
function quoteRuns(id, size = 14, color = C.text1) {
  const o = q(id);
  const onDark = color === C.background1 || color === C.background2;
  return [
    { text: `« ${o.t} »`, options: { italic: true, fontFace: THEME.headFontFace, fontSize: size, color } },
    { text: `  (p. ${o.p})`, options: { fontSize: 12, color: onDark ? SOFT : MUTED, italic: false } },
  ];
}
function iconCircle(s, key, x, y, d = 0.7, fill = C.accent1) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: uid("rond") });
  const p = d * 0.27;
  s.addImage({ data: ICONS[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: uid("icone") });
}
function card(s, x, y, w, h, fill = C.background1, withShadow = true) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: fill }, line: { type: "none" }, shadow: withShadow ? shadow() : undefined, objectName: uid("carte") });
}
const SECTIONS = ["Introduction", "A · La langue", "B · L’écriture", "C · Le sens", "D · La scène", "Conclusion"];
function tracker(s, current, dark = false) {
  const runs = [];
  SECTIONS.forEach((t, i) => {
    const on = i === current;
    runs.push({ text: (on ? "● " : "") + t, options: { bold: on, color: on ? (dark ? HEX.accent2 : HEX.accent1) : (dark ? SOFT : "A3AEB4") } });
    if (i < SECTIONS.length - 1) runs.push({ text: "     ", options: {} });
  });
  T(s, runs, { x: X0, y: 6.95, w: 10.5, h: 0.3, fontSize: 10, valign: "middle" });
}
function header(s, kicker, who) {
  T(s, kicker.toUpperCase(), { x: X0, y: 0.42, w: 9.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: C.accent1 });
  if (who) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.85, y: 0.82, w: 1.88, h: 0.52, rectRadius: 0.26, fill: { color: C.background1 }, line: { color: "D5E2E1", width: 1 }, objectName: uid("pastille") });
    s.addImage({ data: ICONS.user_t, x: 11.05, y: 0.96, w: 0.24, h: 0.24, objectName: uid("pastille_ic") });
    T(s, who, { x: 11.38, y: 0.82, w: 1.3, h: 0.52, fontSize: 14, bold: true, color: C.text2, valign: "middle" });
  }
}
function retenir(s, sentence, y = 5.95) {
  A(9);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X0, y, w: CW, h: 0.68, rectRadius: 0.1, fill: { color: C.text2 }, line: { type: "none" }, objectName: uid("retenir") });
  s.addImage({ data: ICONS.bulb_s, x: X0 + 0.28, y: y + 0.19, w: 0.3, h: 0.3, objectName: uid("retenir_ic") });
  T(s, [{ text: "À RETENIR   ", options: { bold: true, color: C.accent2, fontSize: 12, charSpacing: 2 } }, { text: sentence, options: { color: C.background1, fontSize: 16 } }],
    { x: X0 + 0.75, y, w: CW - 1.0, h: 0.68, valign: "middle" });
  A(0);
}
function content(title, kicker, sectionTitle, idx, who) {
  const s = pres.addSlide({ masterName: "Contenu", sectionTitle });
  A(0);
  s.addText(title, { placeholder: "title" });
  header(s, kicker, who);
  tracker(s, idx);
  return s;
}
function divider(sectionTitle, idx, letter, title, sub, who) {
  const s = pres.addSlide({ masterName: "Section", sectionTitle });
  A(1);
  star(s, 9.1, 1.05, 3.3, HEX.accent2, 45);
  T(s, letter, { x: 9.1, y: 1.05, w: 3.3, h: 3.3, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 110, bold: true, color: C.accent2 });
  A(0);
  s.addText(title, { placeholder: "title" });
  s.addText([{ text: sub, options: { breakLine: true } }, { text: who, options: { bold: true, color: C.accent2 } }], { placeholder: "body" });
  tracker(s, idx, true);
  return s;
}
// Carte standard : icône, étiquette, titre, phrase simple, citation
function infoCard(s, x, y, w, h, o) {
  card(s, x, y, w, h, o.dark ? C.text2 : C.background1);
  const fg = o.dark ? C.background1 : C.text2;
  let cy = y + 0.3;
  if (o.stack) {
    iconCircle(s, o.icon, x + 0.3, cy, 0.62, o.iconColor || C.accent1);
    T(s, o.label.toUpperCase(), { x: x + 1.05, y: cy, w: w - 1.3, h: 0.62, fontSize: 11, bold: true, charSpacing: 2, color: o.labelColor || C.accent1, valign: "middle" });
    T(s, o.title, { x: x + 0.3, y: cy + 0.8, w: w - 0.6, h: 0.45, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: fg });
    T(s, o.text, { x: x + 0.3, y: cy + 1.3, w: w - 0.6, h: 0.45, fontSize: 16, color: MUTED });
    T(s, quoteRuns(o.quote, 16, "34454E"), { x: x + 0.3, y: cy + 1.9, w: w - 0.6, h: y + h - cy - 2.1 });
    return;
  }
  if (o.icon) { iconCircle(s, o.icon, x + 0.3, cy, 0.62, o.iconColor || C.accent1); }
  const tx = o.icon ? x + 1.1 : x + 0.3;
  if (o.label) T(s, o.label.toUpperCase(), { x: tx, y: cy - 0.02, w: w - (tx - x) - 0.25, h: 0.28, fontSize: 11, bold: true, charSpacing: 2, color: o.dark ? C.accent2 : (o.labelColor || C.accent1) });
  T(s, o.title, { x: tx, y: o.label ? cy + 0.24 : cy, w: w - (tx - x) - 0.25, h: o.label ? 0.42 : 0.62, fontFace: THEME.headFontFace, fontSize: o.titleSize || 19, bold: true, color: fg, valign: o.label ? "top" : "middle" });
  cy += 0.95;
  if (o.text) { T(s, o.text, { x: x + 0.3, y: cy, w: w - 0.6, h: o.textH || 0.75, fontSize: 17, color: o.dark ? C.background1 : C.text1 }); cy += (o.textH || 0.75) + 0.15; }
  if (o.quote) {
    T(s, quoteRuns(o.quote, 16, o.dark ? C.background2 : "34454E"), { x: x + 0.3, y: cy, w: w - 0.6, h: y + h - cy - 0.2 });
  }
}

// ---------------------------------------------------------------- diapositives
async function main() {
  await loadIcons();
  let s;

  // 1. Titre
  pres.addSection({ title: "Introduction" });
  s = pres.addSlide({ masterName: "Titre", sectionTitle: "Introduction" });
  A(1); star(s, 9.4, 1.4, 3.6, HEX.accent2, 40); star(s, 10.35, 2.35, 1.7, HEX.lt1, 70); A(0);
  T(s, "GROUPE 4 · FRANÇAIS", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2 });
  s.addText("Les péripéties : les étapes de la transformation", { placeholder: "title" });
  s.addText([{ text: "La Civilisation, ma Mère !…", options: { italic: true, fontFace: THEME.headFontFace, breakLine: true } }, { text: "Driss Chraïbi (1972)" }], { placeholder: "body" });
  A(2); T(s, "Présenté par : ________________________________", { x: 0.8, y: 6.35, w: 8, h: 0.4, fontSize: 14, color: SOFT }); A(0);
  s.addNotes("ÉLÈVE 5 — Bonjour. Nous sommes le groupe 4. Nous allons vous présenter La Civilisation, ma Mère !… de Driss Chraïbi, publié en 1972, et plus précisément les étapes de la transformation de la mère.");

  // 2. Question
  s = content("Notre question", "Introduction", "Introduction", 0, "Élève 5");
  A(1);
  card(s, X0, 1.75, CW, 1.55, C.text2);
  s.addImage({ data: ICONS.quote_s, x: X0 + 0.4, y: 2.05, w: 0.5, h: 0.5, objectName: uid("guillemet") });
  T(s, "Comment les péripéties font-elles passer la mère de l’enfermement à l’émancipation ? Gagne-t-elle un savoir, ou une nouvelle identité ?",
    { x: X0 + 1.2, y: 1.75, w: CW - 1.6, h: 1.55, fontFace: THEME.headFontFace, fontSize: 22, italic: true, color: C.background1, valign: "middle" });
  [["A", "La langue", "Les mots suivent la mère", "book"], ["B", "L’écriture", "Le style rend le changement visible", "pen"], ["C", "Le sens", "Ce que signifie sa liberté", "compass"], ["D", "La scène", "Une transformation jouée", "theater"]].forEach(([l, t, d, ic], i) => {
    A(2 + i);
    const w = 2.86, x = X0 + i * (w + 0.23);
    card(s, x, 3.55, w, 2.15);
    iconCircle(s, ic, x + 0.3, 3.8, 0.62);
    T(s, l, { x: x + w - 0.85, y: 3.75, w: 0.55, h: 0.7, align: "right", fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.accent2 });
    T(s, t, { x: x + 0.3, y: 4.6, w: w - 0.6, h: 0.42, fontSize: 18, bold: true, color: C.text2 });
    T(s, d, { x: x + 0.3, y: 5.02, w: w - 0.6, h: 0.6, fontSize: 15, color: MUTED });
  });
  retenir(s, "Notre fil rouge : la mère cherche-t-elle un savoir, ou une identité ?");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Ses deux fils font découvrir à une mère enfermée la radio, le téléphone, la rue, puis le savoir. Nous nous sommes demandé : comment ces péripéties la font-elles passer de l’enfermement à l’émancipation, et que gagne-t-elle au bout du compte, un savoir ou une identité ? Nous verrons d’abord la langue, puis l’écriture, ensuite le sens, et enfin une scène jouée. »");

  // 3. Roman en deux temps
  s = content("Le roman en deux temps", "Introduction · Le roman", "Introduction", 0, "Élève 1");
  [["Partie I", "« Être »", "seed", C.accent1, "Raconté par le fils cadet", "La mère découvre : la radio, le téléphone, la rue, le cinéma, la lecture.", "seuil"],
   ["Partie II", "« Avoir »", "flag", C.accent3, "Raconté par Nagib, le fils aîné", "La mère agit : elle tient tête au père, étudie, instruit d’autres femmes.", "consciente"]].forEach(([p, t, ic, col, nar, d, qid], i) => {
    A(1 + i);
    const w = 5.95, x = X0 + i * (w + 0.23);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, iconColor: col, label: p, labelColor: col, title: t, titleSize: 26, text: [{ text: nar, options: { bold: true, breakLine: true } }, { text: d }], textH: 1.35, quote: qid });
  });
  retenir(s, "Partie I : elle découvre le monde. Partie II : elle agit sur le monde.");
  s.addNotes("ÉLÈVE 1 — Pour le dire :\n« Le roman a deux parties. Dans la première, “Être”, racontée par le fils cadet, la mère découvre le monde : au début, “jamais elle n’en avait franchi le seuil”. Dans la seconde, “Avoir”, racontée par Nagib, elle agit et finit par dire : “Je suis à présent consciente, entièrement responsable de ma vie”. »");

  // 4. Chronologie
  s = content("Douze étapes de la transformation", "Introduction · Chronologie", "Introduction", 0, "Élève 1");
  const chrono = ["La recluse", "La radio", "Les objets, le téléphone", "Première sortie", "Le cinéma", "Apprendre, naître à soi", "La falaise : le doute", "L’engagement public", "Face au père", "Enterrer le passé", "Instruire les femmes", "Le départ"];
  A(1);
  card(s, X0, 1.75, CW, 3.95);
  [0, 1].forEach((row) => {
    A(1 + row);
    const y = 2.25 + row * 1.75;
    s.addShape(pres.shapes.LINE, { x: X0 + 0.75, y: y + 0.3, w: CW - 1.5, h: 0, line: { color: "D5E2E1", width: 2.5 }, objectName: uid("ligne") });
    for (let i = 0; i < 6; i++) {
      const k = row * 6 + i, x = X0 + 0.25 + i * 1.98, col = k < 7 ? C.accent1 : C.accent3;
      s.addShape(pres.shapes.OVAL, { x: x + 0.45, y, w: 0.6, h: 0.6, fill: { color: col }, line: { color: C.background1, width: 3 }, objectName: uid("pastille") });
      T(s, String(k + 1), { x: x + 0.45, y, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 17, bold: true, color: C.background1 });
      T(s, chrono[k], { x: x + 0.05, y: y + 0.72, w: 1.85, h: 0.65, align: "center", fontSize: 14, color: C.text1 });
    }
  });
  retenir(s, "Des étapes 1 à 7, elle découvre ; des étapes 8 à 12, elle agit.");
  s.addNotes("ÉLÈVE 1 — Pour le dire :\n« Voici les douze étapes. D’abord, la recluse, qui n’a jamais quitté sa maison. Ensuite, les découvertes : la radio, le téléphone, la première sortie, le cinéma, la lecture. Puis le doute, sur la falaise. Enfin, dans la deuxième partie, elle agit : elle s’engage, affronte son mari, enterre son passé, instruit d’autres femmes et part pour la France. Toutes nos preuves viennent de ces étapes. »");

  // 5. A
  pres.addSection({ title: "A · Analyse linguistique" });
  s = divider("A · Analyse linguistique", 1, "A", "Analyse linguistique", "La langue suit la mère pas à pas", "Élève 2");
  s.addNotes("ÉLÈVE 2 — « Commençons par les mots eux-mêmes : nous allons voir comment la langue suit la mère pas à pas. »");

  // 6. A1
  s = content("Des mots qui changent avec elle", "A1 · Champs lexicaux", "A · Analyse linguistique", 1, "Élève 2");
  [["Enfermement", "lock", C.accent3, "prison, tombeau", "tombeau"], ["Merveilleux", "magic", C.accent3, "magie, magicien, génie", "magicien"], ["Naissance", "seed", C.accent1, "naître, nid, coquille", "naitre"], ["Savoir", "book", C.accent1, "école, livres, examens", "inscrite"]].forEach(([t, ic, col, mots, qid], i) => {
    A(1 + i);
    const w = 2.86, x = X0 + i * (w + 0.23);
    infoCard(s, x, 1.75, w, 3.95, { stack: true, icon: ic, iconColor: col, label: `Étape ${i + 1}`, labelColor: col, title: t, text: mots, quote: qid });
  });
  retenir(s, "Les mots passent de l’enfermement au savoir : apprendre, c’est naître une seconde fois.");
  s.addNotes("ÉLÈVE 2 — Pour le dire :\n« Les champs lexicaux évoluent avec la mère. D’abord, celui de l’enfermement : la maison est un “tombeau”. Ensuite, celui du merveilleux : la radio est un “magicien”. Puis celui de la naissance : “nous la voyions naître”. Enfin, celui du savoir : “elle s’est inscrite dans une école”. Cela montre qu’apprendre, pour elle, c’est naître une seconde fois. »");

  // 7. A2
  s = content("D’objet à sujet de ses actes", "A2 · Verbes d’action", "A · Analyse linguistique", 1, "Élève 2");
  A(1);
  infoCard(s, X0, 1.75, 5.75, 3.95, { icon: "user", iconColor: C.accent3, label: "Avant · Partie I", labelColor: C.accent3, title: "Ses fils agissent sur elle", text: "Elle est le complément des verbes.", textH: 0.5, quote: "habillames" });
  A(2);
  s.addShape(pres.shapes.OVAL, { x: 6.27, y: 3.3, w: 0.8, h: 0.8, fill: { color: C.accent2 }, line: { color: C.background1, width: 4 }, objectName: uid("rond") });
  s.addImage({ data: ICONS.arrow, x: 6.49, y: 3.52, w: 0.36, h: 0.36, objectName: uid("fleche") });
  A(3);
  infoCard(s, 6.98, 1.75, 5.75, 3.95, { dark: true, icon: "run", iconColor: C.accent2, label: "Après · Partie II", title: "Elle agit, décide, commande", text: "Elle est le sujet des verbes.", textH: 0.5, quote: "telephona" });
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
  card(s, 6.78, 1.75, 5.95, 3.95, C.text2);
  iconCircle(s, "link", 7.08, 2.05, 0.62, C.accent2);
  T(s, "CONNECTEURS", { x: 7.88, y: 2.03, w: 4.5, h: 0.28, fontSize: 11, bold: true, charSpacing: 2, color: C.accent2 });
  T(s, "Des étapes bien liées", { x: 7.88, y: 2.27, w: 4.6, h: 0.42, fontFace: THEME.headFontFace, fontSize: 19, bold: true, color: C.background1 });
  [["Mais", "l’obstacle, puis son dépassement"], ["C’est ainsi que", "une étape en amène une autre"], ["Alors", "le basculement"], ["Tandis que", "avant et maintenant"]].forEach(([c, d], i) => {
    const y = 3.0 + i * 0.64;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.08, y, w: 1.95, h: 0.46, rectRadius: 0.23, fill: { color: C.accent2 }, line: { type: "none" }, objectName: uid("puce") });
    T(s, c, { x: 7.08, y, w: 1.95, h: 0.46, align: "center", valign: "middle", fontSize: 14, bold: true, color: C.text1 });
    T(s, d, { x: 9.2, y, w: 3.35, h: 0.46, valign: "middle", fontSize: 15, color: C.background1 });
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
    card(s, x, y, w, h);
    iconCircle(s, ic, x + 0.3, y + 0.3, 0.62, row ? C.accent3 : C.accent1);
    T(s, t, { x: x + 1.1, y: y + 0.3, w: w - 1.3, h: 0.62, fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.text2, valign: "middle" });
    T(s, d, { x: x + 0.3, y: y + 1.05, w: w - 0.6, h: 0.7, fontSize: 16, color: C.text1 });
  });
  retenir(s, "Chaque étape de sa transformation est rendue visible par une image ou un objet.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« Plusieurs procédés rendent la transformation visible. La métaphore de l’arbre : elle est “cerclée dans une cour de prison”, mais peut fleurir. La naissance : apprendre, c’est renaître. Une allusion biblique : “la lumière fut”. Des symboles concrets : la tache verte, la serviette “MOI”. La personnification : elle parle à ses objets avant de les enterrer. Enfin, l’accumulation de questions : “mon âme ? où est-elle ?”. »");

  // 12. B2
  s = content("Un humour au service de sa liberté", "B2 · Humour, ironie, décalage", "B · Analyse stylistique", 2, "Élève 3");
  [["Décalage", "smile", "Elle lit la technique avec ses propres repères", "bonsoir"], ["Ironie", "glasses", "Un progrès d’objets, pas d’idées", "objets"], ["Humour de Nagib", "laugh", "Le rire allège les scènes graves", "poils"]].forEach(([t, ic, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, iconColor: C.accent2, label: `Effet ${i + 1}`, labelColor: C.accent2, title: t, text: d, textH: 0.85, quote: qid });
  });
  retenir(s, "Le rire est tendre : il rend la mère attachante et critique la société sans violence.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« L’humour est partout, mais il sert sa liberté. D’abord, le décalage : elle souhaite “bonsoir” au magicien de la radio. Ensuite, l’ironie : le père est “moderniste d’objets, non d’idées”. Enfin, l’humour de Nagib allège les scènes graves. Ce rire est tendre : il rend la mère attachante et critique la société sans violence. »");

  // 13. B3
  s = content("Le regard des narrateurs", "B3 · Regard du narrateur", "B · Analyse stylistique", 2, "Élève 3");
  A(1);
  infoCard(s, X0, 1.75, 5.95, 3.95, { icon: "eye", label: "Partie I", title: "Le fils cadet", text: "Il admire sa mère, mais doute parfois de sa méthode.", textH: 0.85, quote: "soleil" });
  A(2);
  infoCard(s, 6.78, 1.75, 5.95, 3.95, { icon: "laugh", iconColor: C.accent3, label: "Partie II", labelColor: C.accent3, title: "Nagib", text: "Il est étonné, drôle, et accepte d’être dépassé.", textH: 0.85, quote: "connaissais" });
  retenir(s, "Les narrateurs admirent la mère, sans cacher le prix de sa liberté.");
  s.addNotes("ÉLÈVE 3 — Pour le dire :\n« Le regard des narrateurs valorise la mère. Le fils cadet l’admire : il assiste à “un lever de soleil sur sa solitude”. Nagib, lui, est étonné : “Je ne connaissais plus ma mère”. Mais ce regard reste lucide : la liberté a un prix, la solitude. Même le père finit par reconnaître qu’elle est “la conscience d’un monde inconscient”. »");

  // 14. C
  pres.addSection({ title: "C · Analyse thématique" });
  s = divider("C · Analyse thématique", 3, "C", "Analyse thématique", "Ce que signifie cette émancipation", "Élève 4");
  s.addNotes("ÉLÈVE 4 — « Ces procédés rendent la transformation visible. Reste à comprendre ce qu’elle signifie. »");

  // 15. C1
  s = content("Une émancipation par cercles", "C1 · Les étapes de l’émancipation", "C · Analyse thématique", 3, "Élève 4");
  A(1);
  card(s, X0, 1.75, CW, 3.95);
  const ph = ["Enfermement", "Éveil", "Sortie", "Savoir", "Doute", "Affirmation", "Rupture", "Transmission"];
  ph.forEach((t, i) => {
    A(1 + Math.floor(i / 2));
    const w = 1.3, gap = 0.12, x = X0 + 0.5 + i * (w + gap), h = 0.55 + i * 0.3, y = 5.4 - h;
    const col = i < 5 ? C.accent1 : C.accent3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: col, transparency: i < 5 ? 45 - i * 10 : 0 }, line: { type: "none" }, objectName: uid("marche") });
    T(s, String(i + 1), { x, y: y + 0.08, w, h: 0.4, align: "center", fontSize: 16, bold: true, color: C.background1 });
    T(s, t, { x: x - 0.1, y: y - 0.42, w: w + 0.2, h: 0.38, fontSize: 14, bold: true, color: C.text2, align: "center", valign: "bottom" });
  });
  A(5);
  T(s, [{ text: "« Être »", options: { bold: true, color: C.accent1, breakLine: true } }, { text: "devenir soi", options: { color: MUTED } }], { x: X0 + 0.5, y: 2.05, w: 2.0, h: 0.7, fontSize: 16 });
  T(s, [{ text: "« Avoir »", options: { bold: true, color: C.accent3, breakLine: true } }, { text: "prendre sa place", options: { color: MUTED } }], { x: X0 + 2.7, y: 2.05, w: 2.2, h: 0.7, fontSize: 16 });
  retenir(s, "Elle avance par cercles de plus en plus larges : soi, la famille, la société, le monde.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« L’émancipation avance par étapes, comme des marches : l’enfermement, l’éveil par les objets, la première sortie, le savoir, le doute ; puis l’affirmation face au père, la rupture avec le passé, et la transmission aux autres femmes. Ce sont des cercles de plus en plus larges : soi, la famille, la société, le monde. »");

  // 16. C2
  s = content("Ce qui la freine", "C2 · Obstacles et contradictions", "C · Analyse thématique", 3, "Élève 4");
  [["Obstacles extérieurs", "wall", C.accent3, "Le père et la loi, la société des hommes, la colonisation.", "pierres"], ["Résistances intérieures", "heart", C.accent3, "La peur, le sentiment d’avoir perdu sa vie, la solitude.", "solitude"], ["Contradictions", "balance", C.accent2, "Libérée par ses fils, elle doit aussi refuser leur protection.", "tutelle"]].forEach(([t, ic, col, d, qid], i) => {
    A(1 + i);
    const w = 3.9, x = X0 + i * (w + 0.215);
    infoCard(s, x, 1.75, w, 3.95, { icon: ic, iconColor: col, label: ["Du dehors", "En elle", "Paradoxe"][i], labelColor: col, title: t, titleSize: 17, text: d, textH: 1.15, quote: qid });
  });
  retenir(s, "Ce qui la freine vient du dehors, mais aussi d’elle-même.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Trois types d’obstacles apparaissent. Du dehors : le père, la loi, les hommes du village, qui jettent des pierres. En elle : la peur, l’angoisse, la solitude. Et une contradiction : ce sont ses fils qui la libèrent, alors elle doit aussi refuser leur protection. »");

  // 17. C3
  s = content("Une famille qui se transforme", "C3 · Les rapports familiaux", "C · Analyse thématique", 3, "Élève 4");
  A(1);
  T(s, "AVANT", { x: 3.05, y: 1.72, w: 4.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: C.accent3 });
  T(s, "APRÈS", { x: 8.15, y: 1.72, w: 4.5, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: C.accent1 });
  [["Le père", "home", "Il l’a épousée à treize ans et décide de tout", "Il la redécouvre et se lève quand elle entre"], ["Les fils", "users", "Ils sont ses professeurs et la guident", "Elle refuse leur protection et devient le guide"], ["La société", "female", "Trois personnes, une maison fermée", "Un réseau d’amies, puis un mouvement de femmes"]].forEach(([t, ic, av, ap], i) => {
    A(2 + i);
    const y = 2.1 + i * 1.22, h = 1.02;
    iconCircle(s, ic, X0, y + 0.17, 0.68, C.text2);
    T(s, t, { x: X0 + 0.85, y, w: 1.55, h, fontFace: THEME.headFontFace, fontSize: 19, bold: true, color: C.text2, valign: "middle" });
    card(s, 3.05, y, 4.55, h);
    T(s, av, { x: 3.3, y, w: 4.1, h, fontSize: 15, color: C.text1, valign: "middle" });
    s.addImage({ data: ICONS.arrow_s, x: 7.72, y: y + 0.36, w: 0.3, h: 0.3, objectName: uid("fleche") });
    card(s, 8.15, y, 4.58, h, C.text2);
    T(s, ap, { x: 8.4, y, w: 4.1, h, fontSize: 15, color: C.background1, valign: "middle" });
  });
  retenir(s, "La famille dominée par le père devient une famille d’égaux.");
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Les apprentissages changent toute la famille. Le père l’a épousée à treize ans ; à la fin, il avoue : “c’est comme si j’avais épousé une nouvelle femme”, et il se lève quand elle entre. Les fils étaient ses professeurs ; à la fin, elle refuse leur protection. Et sa vie s’ouvre : d’une maison fermée à un mouvement de femmes. »");

  // 18. C4
  s = pres.addSlide({ masterName: "Section", sectionTitle: "C · Analyse thématique" });
  A(0);
  T(s, "C4 · SAVOIR OU IDENTITÉ ?", { x: 0.8, y: 0.8, w: 9, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2 });
  T(s, "Élève 4", { x: 10.2, y: 0.8, w: 2.4, h: 0.4, fontSize: 14, bold: true, color: C.accent2, align: "right" });
  A(1);
  T(s, "Le savoir est l’outil qui lui permet de conquérir son identité, puis d’agir pour les autres.", { x: 0.8, y: 1.45, w: 11.0, h: 1.9, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.background1 });
  [["Elle veut être", "etre"], ["Elle dit « moi »", "moi"], ["Elle agit pour les autres", "actes"]].forEach(([t, qid], i) => {
    A(2 + i);
    const w = 3.65, x = 0.8 + i * (w + 0.25);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 3.75, w, h: 2.55, rectRadius: 0.1, fill: { color: C.background1, transparency: 90 }, line: { color: C.background1, width: 1, transparency: 75 }, objectName: uid("carte") });
    T(s, `${i + 1}. ${t}`, { x: x + 0.3, y: 3.95, w: w - 0.6, h: 0.4, fontSize: 17, bold: true, color: C.accent2 });
    T(s, quoteRuns(qid, 16, C.background1), { x: x + 0.3, y: 4.45, w: w - 0.6, h: 1.7 });
  });
  tracker(s, 3, true);
  s.addNotes("ÉLÈVE 4 — Pour le dire :\n« Notre réponse : la mère ne cherche pas seulement à apprendre. D’abord, elle veut être : le roman dit qu’elle cherche “à être et non à avoir ou posséder”. Ensuite, elle s’affirme : elle brode le mot “MOI”. Enfin, elle agit pour les autres : “il faut que je les traduise en actes”. Le savoir est donc l’outil d’une conquête d’identité. »");

  // 19. Enjeux
  s = content("Ce que le roman dénonce", "Enjeux sociaux et philosophiques", "C · Analyse thématique", 3, "Élève 4");
  [["Condition des femmes", "female", "Les femmes n’ont pas voix au chapitre"], ["Tradition et modernité", "compass", "La vraie civilisation, ce sont les idées"], ["Colonisation", "flag", "Sa libération suit celle du pays"], ["Liberté et solitude", "heart", "La liberté a un prix"], ["Être et avoir", "gem", "Elle choisit d’abord l’être"]].forEach(([t, ic, d], i) => {
    A(1 + i);
    const w = 2.25, x = X0 + i * (w + 0.22);
    card(s, x, 1.75, w, 3.95);
    iconCircle(s, ic, x + (w - 0.9) / 2, 2.1, 0.9, i % 2 ? C.accent3 : C.accent1);
    T(s, t, { x: x + 0.2, y: 3.2, w: w - 0.4, h: 0.85, fontSize: 17, bold: true, color: C.text2, align: "center" });
    T(s, d, { x: x + 0.2, y: 4.1, w: w - 0.4, h: 1.3, fontSize: 16, color: C.text1, align: "center" });
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
    const w = 3.9, x = X0 + i * (w + 0.215), dark = i === 2;
    card(s, x, 1.75, w, 3.95, dark ? C.text2 : C.background1);
    s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 2.05, w: 0.62, h: 0.62, fill: { color: C.accent2 }, line: { type: "none" }, objectName: uid("num") });
    T(s, String(i + 1), { x: x + 0.3, y: 2.05, w: 0.62, h: 0.62, align: "center", valign: "middle", fontSize: 20, bold: true, color: C.text1 });
    T(s, `TEMPS ${i + 1}`, { x: x + 1.1, y: 2.03, w: 2.5, h: 0.28, fontSize: 11, bold: true, charSpacing: 2, color: C.accent2 });
    T(s, t, { x: x + 1.1, y: 2.27, w: w - 1.3, h: 0.42, fontFace: THEME.headFontFace, fontSize: 19, bold: true, color: dark ? C.background1 : C.text2 });
    T(s, d, { x: x + 0.3, y: 3.0, w: w - 0.6, h: 0.85, fontSize: 17, color: dark ? C.background1 : C.text1 });
    T(s, quoteRuns(qid, 16, dark ? C.background2 : "34454E"), { x: x + 0.3, y: 3.95, w: w - 0.6, h: 1.6 });
  });
  retenir(s, "Rôles : la mère, le père, Nagib et un narrateur · Durée : 3 à 4 minutes.");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« La scène se passe la nuit, dans le salon. D’abord, le père domine : il rappelle qu’il a “tout payé”. Ensuite, la mère lui tient tête et demande : “mon âme ? où est-elle ?”. Enfin, elle refuse même l’aide de son fils : “Je suis à présent consciente, entièrement responsable de ma vie”. »\nPuis le groupe joue la scène (script complet dans le dossier de l’Élève 5).");

  // 22. Synthèse
  pres.addSection({ title: "Conclusion" });
  s = content("Ce que conquiert la mère", "Synthèse", "Conclusion", 5, "Élève 5");
  [["A · La langue", "D’objet à sujet : elle agit et commande", "book"], ["B · L’écriture", "De la prison à la naissance, avec humour", "pen"], ["C · Le sens", "Le savoir au service de l’identité", "compass"]].forEach(([t, d, ic], i) => {
    A(1 + i);
    const y = 1.75 + i * 1.33;
    card(s, X0, y, 6.4, 1.13);
    iconCircle(s, ic, X0 + 0.25, y + 0.24, 0.65);
    T(s, [{ text: t, options: { bold: true, color: C.text2, breakLine: true } }, { text: d, options: { color: C.text1 } }], { x: X0 + 1.15, y, w: 5.1, h: 1.13, fontSize: 16, valign: "middle" });
  });
  A(4);
  card(s, 7.28, 1.75, 5.45, 3.79, C.text2);
  T(s, "NOTRE RÉPONSE", { x: 7.6, y: 2.05, w: 4.8, h: 0.3, fontSize: 12, bold: true, charSpacing: 3, color: C.accent2 });
  T(s, "La mère conquiert une identité, et le savoir en est le moyen. Cette liberté a un prix, la solitude, mais elle transforme toute la famille.", { x: 7.6, y: 2.5, w: 4.85, h: 2.85, fontFace: THEME.headFontFace, fontSize: 21, bold: true, color: C.background1 });
  retenir(s, "Elle ne veut pas seulement savoir : elle veut être.");
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Pour conclure, trois constats se rejoignent. D’abord, la langue change avec elle : elle passe d’objet à sujet. Ensuite, l’écriture rend ce changement visible, avec des images de naissance et un humour tendre. Enfin, le sens est clair : elle cherche à être. Notre réponse : la mère conquiert une identité, et le savoir en est le moyen. »");

  // 23. Ouverture
  s = pres.addSlide({ masterName: "Titre", sectionTitle: "Conclusion" });
  A(1); star(s, 9.4, 1.4, 3.6, HEX.accent2, 40); star(s, 10.35, 2.35, 1.7, HEX.lt1, 70); A(0);
  T(s, "POUR OUVRIR", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2 });
  s.addText("La vraie civilisation, c’est la mère elle-même", { placeholder: "title" });
  s.addText(quoteRuns("conscience", 20, C.background2), { placeholder: "body" });
  A(2); T(s, "Merci de votre attention", { x: 0.8, y: 6.3, w: 8, h: 0.5, fontSize: 18, bold: true, color: C.accent2 }); A(0);
  s.addNotes("ÉLÈVE 5 — Pour le dire :\n« Le titre, La Civilisation, ma Mère !…, prend alors tout son sens. La vraie civilisation, ce n’est ni la radio ni le fer à repasser : c’est la mère elle-même, devenue, selon le mot du père, “la conscience d’un monde inconscient”. Merci de votre attention. »");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ok", OUT);
}
main().catch((e) => { console.error(e); process.exit(1); });
