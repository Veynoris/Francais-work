// Présentation orale du Groupe 4 (PowerPoint).
// Usage : NODE_PATH=<node_modules> node src/build_deck.js <quotes.json> <sortie.pptx> <apply_theme.js>
// quotes.json est produit par src/build.py (citations vérifiées dans Roman.pdf).
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
    dk1: "1C2B33", lt1: "FFFFFF", dk2: "0D4C4F", lt2: "EEF4F3",
    accent1: "0E7C7B", accent2: "D99A2B", accent3: "B5523A",
    accent4: "3E6E8E", accent5: "7A5C99", accent6: "5F7F3A",
    hlink: "0E7C7B", folHlink: "7A5C99",
  },
};
const HEX = THEME.colors;
const MUTED = "5E6B73";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Les péripéties : les étapes de la transformation";
pres.author = "Groupe 4";
const C = pres.SchemeColor;
const W = 13.333;

// ---------------------------------------------------------------- icônes
async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const ICONS = {};
async function loadIcons() {
  const list = {
    lock: fa.FaLock, magic: fa.FaMagic, seed: fa.FaSeedling, book: fa.FaBookOpen,
    user: fa.FaUserAlt, run: fa.FaWalking, clock: fa.FaHourglassHalf, bolt: fa.FaBolt, comment: fa.FaCommentDots,
    tree: fa.FaTree, egg: fa.FaFeatherAlt, sun: fa.FaSun, key: fa.FaKey, ghost: fa.FaDove, question: fa.FaQuestion,
    smile: fa.FaSmile, eye: fa.FaEye, laugh: fa.FaLaughBeam, glasses: fa.FaGlasses, pen: fa.FaPenNib,
    stair: fa.FaChartLine, wall: fa.FaShieldAlt, heart: fa.FaHeartBroken, balance: fa.FaBalanceScale,
    home: fa.FaHome, users: fa.FaUsers, female: fa.FaFemale, flag: fa.FaFlag, dove: fa.FaDove, gem: fa.FaGem,
    theater: fa.FaTheaterMasks, compass: fa.FaCompass, quote: fa.FaQuoteLeft,
  };
  for (const [k, comp] of Object.entries(list)) {
    ICONS[k] = await icon(comp, "FFFFFF");
    ICONS[k + "_t"] = await icon(comp, HEX.accent1);
  }
}

// ---------------------------------------------------------------- mises en page
pres.defineSlideMaster({
  title: "Titre",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.1, w: 8.6, h: 2.2, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.5, w: 8.6, h: 1.3, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "Section",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 3.0, w: 8.2, h: 1.4, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.55, w: 8.2, h: 1.0, fontSize: 20, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
    { text: { text: "La Civilisation, ma Mère !… · Groupe 4", options: { x: 0.8, y: 6.85, w: 8, h: 0.35, fontSize: 11, color: "9FC3C1", margin: 0 } } },
  ],
  slideNumber: { x: 12.2, y: 6.85, w: 0.6, h: 0.35, fontSize: 11, color: "9FC3C1", align: "right" },
});
pres.defineSlideMaster({
  title: "Contenu",
  background: { color: HEX.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 10.0, h: 0.95, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: "La Civilisation, ma Mère !… · Groupe 4", options: { x: 0.6, y: 6.95, w: 8, h: 0.3, fontSize: 10, color: MUTED, margin: 0 } } },
  ],
  slideNumber: { x: 12.15, y: 6.95, w: 0.6, h: 0.3, fontSize: 10, color: MUTED, align: "right" },
});

// ---------------------------------------------------------------- aides
let n = 0;
const uid = (p) => `${p}_${++n}`;
const q = (id) => {
  if (!Q[id]) throw new Error("citation inconnue " + id);
  return Q[id];
};
function star(slide, x, y, size, color, transparency) {
  // étoile à huit branches (motif zellige) : deux carrés superposés
  for (const rot of [0, 45]) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: size, h: size, rotate: rot, objectName: uid("etoile"),
      fill: { type: "none" }, line: { color, width: 2, transparency },
    });
  }
}
function presenter(slide, label) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 10.95, y: 0.62, w: 1.8, h: 0.5, rectRadius: 0.25, objectName: uid("presentateur"),
    fill: { color: C.background2 }, line: { type: "none" },
  });
  slide.addText(label, { x: 10.95, y: 0.62, w: 1.8, h: 0.5, align: "center", valign: "middle", fontSize: 14, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("presentateur_txt") });
}
function iconCircle(slide, key, x, y, d = 0.7, fill = C.accent1) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { type: "none" }, objectName: uid("rond") });
  const p = d * 0.26;
  slide.addImage({ data: ICONS[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: uid("icone") });
}
function card(slide, x, y, w, h, fill = C.background2) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { type: "none" }, objectName: uid("carte") });
}
function quoteRuns(id, size = 14, color = C.text1) {
  const o = q(id);
  return [
    { text: `« ${o.t} »`, options: { italic: true, fontFace: THEME.headFontFace, fontSize: size, color } },
    { text: `  p. ${o.p}`, options: { fontSize: 11, color: MUTED } },
  ];
}
function content(title, section, who) {
  const s = pres.addSlide({ masterName: "Contenu", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  if (who) presenter(s, who);
  return s;
}
function divider(section, letter, title, sub, who) {
  const s = pres.addSlide({ masterName: "Section", sectionTitle: section });
  star(s, 9.2, 1.0, 3.3, HEX.accent2, 55);
  s.addText(letter, { x: 9.2, y: 1.0, w: 3.3, h: 3.3, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 110, bold: true, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("lettre") });
  s.addText(title, { placeholder: "title" });
  s.addText([{ text: sub, options: { breakLine: true } }, { text: who, options: { bold: true, color: C.accent2 } }], { placeholder: "body" });
  return s;
}
const body = { fontSize: 15, color: C.text1, margin: 0, isTextBox: true, valign: "top" };

// ---------------------------------------------------------------- diapositives
async function main() {
  await loadIcons();

  // 1. Titre
  pres.addSection({ title: "Ouverture" });
  let s = pres.addSlide({ masterName: "Titre", sectionTitle: "Ouverture" });
  star(s, 9.4, 1.4, 3.6, HEX.accent2, 40);
  star(s, 10.35, 2.35, 1.7, HEX.lt1, 70);
  s.addText("GROUPE 4 · FRANÇAIS", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("surtitre") });
  s.addText("Les péripéties : les étapes de la transformation", { placeholder: "title" });
  s.addText([{ text: "La Civilisation, ma Mère !…", options: { italic: true, fontFace: THEME.headFontFace, breakLine: true } }, { text: "Driss Chraïbi (1972)" }], { placeholder: "body" });
  s.addText("Présenté par : ________________________________", { x: 0.8, y: 6.4, w: 8, h: 0.4, fontSize: 14, color: "9FC3C1", margin: 0, isTextBox: true, objectName: uid("noms") });
  s.addNotes("Élève 5 ouvre la présentation et annonce le roman et le groupe.");

  // 2. Problématique
  s = content("Notre question", "Ouverture", "Élève 5");
  card(s, 0.6, 1.6, 12.13, 1.9, C.text2);
  s.addImage({ data: ICONS.quote, x: 1.0, y: 1.95, w: 0.55, h: 0.55, objectName: uid("guillemet") });
  s.addText("Comment les péripéties font-elles passer la mère de l’enfermement à l’émancipation, et que conquiert-elle au bout du compte : un savoir, ou une nouvelle identité ?",
    { x: 1.85, y: 1.75, w: 10.5, h: 1.6, fontFace: THEME.headFontFace, fontSize: 22, italic: true, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("problematique") });
  const steps = [
    ["A", "La langue", "Comment les mots suivent la mère", "book"],
    ["B", "L’écriture", "Comment le style rend le changement visible", "pen"],
    ["C", "Le sens", "Ce que signifie cette émancipation", "compass"],
    ["D", "La scène", "Une transformation jouée devant vous", "theater"],
  ];
  steps.forEach(([l, t, d, ic], i) => {
    const x = 0.6 + i * 3.11;
    card(s, x, 3.95, 2.85, 2.6);
    iconCircle(s, ic, x + 0.3, 4.2, 0.75);
    s.addText(l, { x: x + 1.95, y: 4.15, w: 0.7, h: 0.8, fontFace: THEME.headFontFace, fontSize: 36, bold: true, color: C.accent2, align: "right", margin: 0, isTextBox: true, objectName: uid("lettre") });
    s.addText(t, { x: x + 0.3, y: 5.1, w: 2.4, h: 0.45, fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("etape_t") });
    s.addText(d, { x: x + 0.3, y: 5.55, w: 2.4, h: 0.85, ...body, fontSize: 14, color: MUTED, objectName: uid("etape_d") });
  });
  s.addNotes("Dans La Civilisation, ma Mère !…, publié en 1972, Driss Chraïbi raconte la métamorphose d’une mère marocaine, mariée à treize ans et enfermée dans sa maison. Ses deux fils lui font découvrir la radio, le téléphone, la rue, puis le savoir. Notre question : que conquiert-elle, un savoir ou une identité ? Nous verrons la langue, l’écriture, le sens, puis une scène.");

  // 3. Le roman en bref
  s = content("Le roman en deux temps", "Ouverture", "Élève 1");
  const parts = [
    ["Partie I", "« Être »", "Raconté par le fils cadet", "La mère découvre : la radio, l’électricité, le téléphone, la rue, le cinéma, la lecture.", "seed", C.accent1],
    ["Partie II", "« Avoir »", "Raconté par Nagib, le fils aîné", "La mère agit : elle tient tête au père, étudie, instruit d’autres femmes, part pour la France.", "flag", C.accent3],
  ];
  parts.forEach(([p, t, nar, d, ic, col], i) => {
    const x = 0.6 + i * 6.17;
    card(s, x, 1.65, 5.96, 4.95);
    iconCircle(s, ic, x + 0.45, 2.0, 0.9, col);
    s.addText(p.toUpperCase(), { x: x + 1.6, y: 2.0, w: 4, h: 0.4, fontSize: 14, bold: true, charSpacing: 3, color: col, margin: 0, isTextBox: true, objectName: uid("partie") });
    s.addText(t, { x: x + 1.6, y: 2.35, w: 4, h: 0.7, fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("partie_t") });
    s.addText(nar, { x: x + 0.45, y: 3.45, w: 5.1, h: 0.45, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: uid("narr") });
    s.addText(d, { x: x + 0.45, y: 3.95, w: 5.1, h: 1.3, ...body, fontSize: 17, objectName: uid("desc") });
    s.addText(quoteRuns(i === 0 ? "seuil" : "consciente", 16, C.text2), { x: x + 0.45, y: 5.35, w: 5.1, h: 1.0, ...body, objectName: uid("q") });
  });
  s.addNotes("Le roman a deux parties : « Être », racontée par le fils cadet, où la mère découvre le monde ; « Avoir », racontée par Nagib, où elle agit. La mère est toujours vue par ses fils, jamais narratrice.");

  // 4. Chronologie
  s = content("Douze étapes de la transformation", "Ouverture", "Élève 1");
  const chrono = [
    ["La recluse", "I"], ["La radio", "I"], ["Les objets, le téléphone", "I"], ["Première sortie", "I"], ["Le cinéma", "I"], ["Apprendre, naître à soi", "I"],
    ["La falaise : le doute", "I"], ["L’engagement public", "II"], ["Face au père", "II"], ["Enterrer le passé", "II"], ["Instruire les femmes", "II"], ["Le départ", "II"],
  ];
  [0, 1].forEach((row) => {
    const y = 2.3 + row * 1.95;
    s.addShape(pres.shapes.LINE, { x: 1.05, y: y + 0.32, w: 11.25, h: 0, line: { color: HEX.lt2, width: 3 }, objectName: uid("ligne") });
    for (let i = 0; i < 6; i++) {
      const k = row * 6 + i;
      const [t, part] = chrono[k];
      const x = 0.75 + i * 2.05;
      const col = part === "I" ? C.accent1 : C.accent3;
      s.addShape(pres.shapes.OVAL, { x: x + 0.3, y, w: 0.64, h: 0.64, fill: { color: col }, line: { color: C.background1, width: 3 }, objectName: uid("pastille") });
      s.addText(String(k + 1), { x: x + 0.3, y, w: 0.64, h: 0.64, align: "center", valign: "middle", fontSize: 18, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: uid("num") });
      s.addText(t, { x, y: y + 0.8, w: 1.85, h: 0.8, fontSize: 15, color: C.text1, align: "left", valign: "top", margin: 0, isTextBox: true, objectName: uid("etape") });
    }
  });
  s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.6, w: 0.28, h: 0.28, fill: { color: C.accent1 }, line: { type: "none" }, objectName: uid("legende") });
  s.addText("Partie I : elle découvre", { x: 0.98, y: 1.52, w: 3, h: 0.44, fontSize: 14, color: MUTED, margin: 0, isTextBox: true, objectName: uid("legende_t") });
  s.addShape(pres.shapes.OVAL, { x: 4.0, y: 1.6, w: 0.28, h: 0.28, fill: { color: C.accent3 }, line: { type: "none" }, objectName: uid("legende") });
  s.addText("Partie II : elle agit", { x: 4.38, y: 1.52, w: 3, h: 0.44, fontSize: 14, color: MUTED, margin: 0, isTextBox: true, objectName: uid("legende_t") });
  card(s, 0.6, 5.85, 12.13, 0.8, C.text2);
  s.addText([{ text: "Nos preuves : ", options: { bold: true, color: C.accent2 } }, { text: "87 citations relevées dans le roman, classées selon les trois axes de la consigne.", options: { color: C.background1 } }],
    { x: 0.95, y: 5.85, w: 11.5, h: 0.8, fontSize: 16, valign: "middle", margin: 0, isTextBox: true, objectName: uid("bande") });
  s.addNotes("Élève 1 parcourt les douze étapes : de la recluse qui n’a jamais franchi le seuil à la femme qui part découvrir le monde. Toutes nos preuves viennent de ce corpus de citations.");

  // 5. Section A
  pres.addSection({ title: "A · Analyse linguistique" });
  divider("A · Analyse linguistique", "A", "Analyse linguistique", "La langue suit la mère pas à pas", "Élève 2");

  // 6. A1
  s = content("Des mots qui changent avec elle", "A · Analyse linguistique", "Élève 2");
  s.addText("A1 · Champs lexicaux des découvertes et des apprentissages", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const lex = [
    ["Enfermement", "lock", "tombeau", "prison, tombeau"],
    ["Merveilleux", "magic", "magicien", "magie, magicien, génie"],
    ["Naissance", "seed", "naitre", "naître, nid, coquille"],
    ["Savoir", "book", "inscrite", "école, livres, examens"],
  ];
  lex.forEach(([t, ic, qid, mots], i) => {
    const x = 0.6 + i * 3.11;
    card(s, x, 2.0, 2.85, 4.6);
    iconCircle(s, ic, x + 0.3, 2.3, 0.8, i < 2 ? C.accent3 : C.accent1);
    s.addText(t, { x: x + 0.3, y: 3.25, w: 2.4, h: 0.5, fontSize: 20, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("lex_t") });
    s.addText(mots, { x: x + 0.3, y: 3.75, w: 2.4, h: 0.5, fontSize: 14, color: MUTED, margin: 0, isTextBox: true, objectName: uid("lex_m") });
    s.addText(quoteRuns(qid, 14), { x: x + 0.3, y: 4.35, w: 2.4, h: 2.05, ...body, objectName: uid("lex_q") });
    if (i < 3) s.addText("›", { x: x + 2.83, y: 3.7, w: 0.3, h: 0.6, fontSize: 30, bold: true, color: C.accent2, align: "center", margin: 0, isTextBox: true, objectName: uid("fleche") });
  });
  s.addNotes("Le vocabulaire passe de l’enfermement et de la magie au vocabulaire de la naissance et du savoir. Apprendre, c’est naître une seconde fois.");

  // 7. A2
  s = content("D’objet à sujet de ses actes", "A · Analyse linguistique", "Élève 2");
  s.addText("A2 · Verbes d’action : la mère devient actrice de sa vie", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  card(s, 0.6, 2.0, 5.7, 4.6);
  card(s, 7.03, 2.0, 5.7, 4.6, C.text2);
  s.addText("AVANT · Partie I", { x: 1.0, y: 2.3, w: 5, h: 0.4, fontSize: 14, bold: true, charSpacing: 3, color: C.accent3, margin: 0, isTextBox: true, objectName: uid("lab") });
  s.addText("Elle est le complément : ses fils agissent sur elle", { x: 1.0, y: 2.75, w: 4.9, h: 0.9, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("h") });
  s.addText(quoteRuns("habillames", 15), { x: 1.0, y: 3.85, w: 4.9, h: 2.4, ...body, objectName: uid("q") });
  s.addText("APRÈS · Partie II", { x: 7.43, y: 2.3, w: 5, h: 0.4, fontSize: 14, bold: true, charSpacing: 3, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("lab") });
  s.addText("Elle est le sujet : elle agit, décide, commande", { x: 7.43, y: 2.75, w: 4.9, h: 0.9, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: uid("h") });
  s.addText([...quoteRuns("telephona", 15, C.background1), { text: "", options: { breakLine: true } }, ...quoteRuns("peint", 15, C.background1), { text: "", options: { breakLine: true } }, ...quoteRuns("debout", 15, C.background1)],
    { x: 7.43, y: 3.85, w: 4.9, h: 2.5, ...body, paraSpaceAfter: 8, objectName: uid("q") });
  s.addShape(pres.shapes.OVAL, { x: 6.22, y: 3.85, w: 0.9, h: 0.9, fill: { color: C.accent2 }, line: { color: C.background1, width: 4 }, objectName: uid("rond") });
  s.addText("→", { x: 6.22, y: 3.85, w: 0.9, h: 0.9, fontSize: 28, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: uid("fleche") });
  s.addNotes("Au début, la mère est le complément des verbes : nous réveillâmes maman, la coiffâmes, l’habillâmes. En partie II, elle est le sujet : elle téléphone, peint, s’inscrit, donne des ordres. Ce renversement prouve qu’elle devient actrice de sa vie.");

  // 8. A3
  s = content("Un temps qui s’accélère", "A · Analyse linguistique", "Élève 2");
  s.addText("A3 · Temps verbaux et indicateurs temporels", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const tps = [
    ["Imparfait", "La répétition de la vie d’avant", "revenais", "clock"],
    ["Passé simple", "Les ruptures, les premières fois", "lumiere", "bolt"],
    ["Indicateurs", "Un rythme de plus en plus rapide", "bruler", "run"],
  ];
  tps.forEach(([t, d, qid, ic], i) => {
    const x = 0.6 + i * 4.15;
    card(s, x, 2.0, 3.9, 3.55);
    iconCircle(s, ic, x + 0.35, 2.3, 0.75);
    s.addText(t, { x: x + 1.3, y: 2.3, w: 2.4, h: 0.75, fontFace: THEME.headFontFace, fontSize: 24, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.35, y: 3.25, w: 3.25, h: 0.65, ...body, fontSize: 16, bold: true, objectName: uid("d") });
    s.addText(quoteRuns(qid, 15), { x: x + 0.35, y: 3.95, w: 3.25, h: 1.45, ...body, objectName: uid("q") });
  });
  card(s, 0.6, 5.8, 12.13, 0.85, C.text2);
  s.addText([{ text: "Avant / maintenant : ", options: { bold: true, color: C.accent2 } }, { text: "35 ans en partie I, « trente-sept ans » en partie II : on mesure le chemin parcouru.", options: { color: C.background1 } }],
    { x: 0.95, y: 5.8, w: 11.5, h: 0.85, fontSize: 16, valign: "middle", margin: 0, isTextBox: true, objectName: uid("bande") });
  s.addNotes("L’imparfait installe la répétition, le passé simple marque les ruptures, et les indicateurs (dès le lendemain, il fallait brûler les étapes, jour après jour) montrent l’accélération. La partie II, racontée par Nagib dans une lettre, passe au passé composé.");

  // 9. Énonciation et connecteurs
  s = content("Qui raconte, et comment", "A · Analyse linguistique", "Élève 2");
  card(s, 0.6, 1.65, 6.0, 4.95);
  iconCircle(s, "comment", 0.95, 1.95, 0.75);
  s.addText("Énonciation", { x: 1.9, y: 1.95, w: 4.5, h: 0.75, fontFace: THEME.headFontFace, fontSize: 24, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
  s.addText([
    { text: "Deux narrateurs, deux fils : le cadet (I), puis Nagib (II).", options: { bullet: true, breakLine: true } },
    { text: "La mère est toujours vue par ses fils, jamais narratrice.", options: { bullet: true, breakLine: true } },
    { text: "Sa parole prend de la place : de courtes questions, puis de longues tirades.", options: { bullet: true, breakLine: true } },
    { text: "Le père le remarque lui-même :", options: { bullet: true } },
  ], { x: 0.95, y: 2.95, w: 5.35, h: 2.3, ...body, fontSize: 16, paraSpaceAfter: 6, objectName: uid("liste") });
  s.addText(quoteRuns("langage", 15), { x: 0.95, y: 5.3, w: 5.35, h: 1.1, ...body, objectName: uid("q") });
  card(s, 6.85, 1.65, 5.88, 4.95, C.text2);
  s.addText("Connecteurs", { x: 7.2, y: 1.95, w: 5, h: 0.75, fontFace: THEME.headFontFace, fontSize: 24, bold: true, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
  const con = [["Mais", "l’obstacle, puis son dépassement"], ["C’est ainsi que", "les étapes s’enchaînent"], ["Alors", "le basculement"], ["Tandis que", "avant / maintenant"]];
  con.forEach(([c, d], i) => {
    const y = 2.95 + i * 0.85;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.2, y, w: 2.1, h: 0.6, rectRadius: 0.3, fill: { color: C.accent2 }, line: { type: "none" }, objectName: uid("puce") });
    s.addText(c, { x: 7.2, y, w: 2.1, h: 0.6, align: "center", valign: "middle", fontSize: 15, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: uid("puce_t") });
    s.addText(d, { x: 9.5, y, w: 3.0, h: 0.6, valign: "middle", fontSize: 16, color: C.background1, margin: 0, isTextBox: true, objectName: uid("puce_d") });
  });
  s.addNotes("Deux narrateurs : le fils cadet en partie I, Nagib en partie II, qui écrit à son frère. Les connecteurs (mais, c’est ainsi que, alors, tandis que) construisent le récit comme une suite d’étapes logiques.");

  // 10. Section B
  pres.addSection({ title: "B · Analyse stylistique" });
  divider("B · Analyse stylistique", "B", "Analyse stylistique", "L’écriture rend la transformation visible", "Élève 3");

  // 11. B1
  s = content("Images et symboles", "B · Analyse stylistique", "Élève 3");
  s.addText("B1 · Procédés qui rendent la transformation perceptible", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const proc = [
    ["Métaphore de l’arbre", "tree", "Une prison, mais un printemps possible"],
    ["Naissance", "egg", "Apprendre, c’est naître une seconde fois"],
    ["Allusion biblique", "sun", "« la lumière fut » : son éveil est une création"],
    ["Symboles concrets", "key", "Tache verte, robe, serviette « MOI », cheveux coupés"],
    ["Personnification", "dove", "Elle dit adieu à ses objets comme à des amis"],
    ["Accumulation", "question", "« mon âme ? où est-elle ? » : la parole explose"],
  ];
  proc.forEach(([t, ic, d], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.15, y = 2.0 + row * 2.35;
    card(s, x, y, 3.9, 2.1);
    iconCircle(s, ic, x + 0.3, y + 0.3, 0.7, row === 0 ? C.accent1 : C.accent3);
    s.addText(t, { x: x + 1.2, y: y + 0.3, w: 2.5, h: 0.7, fontSize: 18, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.3, y: y + 1.15, w: 3.35, h: 0.8, ...body, fontSize: 15, objectName: uid("d") });
  });
  s.addNotes("Métaphore de l’arbre cerclé dans une cour de prison mais qui peut fleurir ; métaphore filée de la naissance ; allusion à la Genèse quand la lumière s’allume ; symboles concrets (tache verte, objets enterrés, serviette « MOI », cheveux coupés) ; personnification des objets ; accumulation de questions sur son âme.");

  // 12. B2
  s = content("Un humour au service de l’émancipation", "B · Analyse stylistique", "Élève 3");
  s.addText("B2 · Humour, ironie et décalage", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const hum = [
    ["Décalage", "smile", "Elle lit la technique avec ses propres repères", "bonsoir"],
    ["Ironie", "glasses", "Un progrès d’objets, pas d’idées", "objets"],
    ["Humour de Nagib", "laugh", "Le rire désamorce les scènes graves", "poils"],
  ];
  hum.forEach(([t, ic, d, qid], i) => {
    const x = 0.6 + i * 4.15;
    card(s, x, 2.0, 3.9, 3.45);
    iconCircle(s, ic, x + 0.35, 2.3, 0.75, C.accent2);
    s.addText(t, { x: x + 1.3, y: 2.3, w: 2.45, h: 0.75, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.35, y: 3.25, w: 3.25, h: 0.7, ...body, fontSize: 16, bold: true, objectName: uid("d") });
    s.addText(quoteRuns(qid, 15), { x: x + 0.35, y: 4.0, w: 3.25, h: 1.3, ...body, objectName: uid("q") });
  });
  card(s, 0.6, 5.7, 12.13, 0.95, C.text2);
  s.addText("Le rire est tendre, jamais méprisant : il rend la mère attachante et critique la société sans violence.", { x: 0.95, y: 5.7, w: 11.5, h: 0.95, fontSize: 17, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("bande") });
  s.addNotes("Le décalage comique (elle souhaite bonsoir au « magicien » de la radio), l’ironie contre un père « moderniste d’objets, non d’idées », et l’humour de Nagib qui désamorce le drame. L’humour sert l’émancipation.");

  // 13. B3
  s = content("Le regard des narrateurs", "B · Analyse stylistique", "Élève 3");
  s.addText("B3 · Un regard qui valorise, mais reste lucide", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const reg = [
    ["Le fils cadet", "Partie I", "Admiratif et engagé, mais il doute de sa méthode", "soleil", "eye", C.accent1],
    ["Nagib", "Partie II", "Étonné, drôle, prêt à être dépassé par sa mère", "connaissais", "laugh", C.accent3],
  ];
  reg.forEach(([t, p, d, qid, ic, col], i) => {
    const x = 0.6 + i * 6.17;
    card(s, x, 2.0, 5.96, 3.3);
    iconCircle(s, ic, x + 0.4, 2.3, 0.85, col);
    s.addText(p.toUpperCase(), { x: x + 1.5, y: 2.3, w: 4, h: 0.35, fontSize: 13, bold: true, charSpacing: 3, color: col, margin: 0, isTextBox: true, objectName: uid("p") });
    s.addText(t, { x: x + 1.5, y: 2.62, w: 4, h: 0.55, fontFace: THEME.headFontFace, fontSize: 26, bold: true, color: C.text2, margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.4, y: 3.4, w: 5.2, h: 0.65, ...body, fontSize: 17, bold: true, objectName: uid("d") });
    s.addText(quoteRuns(qid, 16), { x: x + 0.4, y: 4.1, w: 5.2, h: 1.0, ...body, objectName: uid("q") });
  });
  card(s, 0.6, 5.55, 12.13, 1.1, C.text2);
  s.addText([{ text: "Même le père finit par le reconnaître : ", options: { color: C.background2 } }, ...quoteRuns("conscience", 17, C.background1)], { x: 0.95, y: 5.55, w: 11.5, h: 1.1, fontSize: 17, valign: "middle", margin: 0, isTextBox: true, objectName: uid("bande") });
  s.addNotes("Le fils cadet admire sa mère mais reconnaît ses limites ; Nagib l’observe avec humour et accepte d’être dépassé. Les narrateurs valorisent l’émancipation tout en montrant son prix : la solitude, l’hostilité.");

  // 14. Section C
  pres.addSection({ title: "C · Analyse thématique" });
  divider("C · Analyse thématique", "C", "Analyse thématique", "Ce que signifie cette émancipation", "Élève 4");

  // 15. C1
  s = content("Une émancipation par cercles", "C · Analyse thématique", "Élève 4");
  s.addText("C1 · Les principales étapes : de l’intime au monde", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const ph = ["Enfermement", "Éveil par les objets", "Sortie", "Savoir", "Doute", "Affirmation", "Rupture avec le passé", "Transmission et départ"];
  ph.forEach((t, i) => {
    const w = 1.42, gap = 0.1, x = 0.6 + i * (w + gap);
    const h = 0.9 + i * 0.47;
    const y = 6.55 - h;
    const col = i < 5 ? C.accent1 : C.accent3;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: col, transparency: i < 5 ? 40 - i * 8 : 0 }, line: { type: "none" }, objectName: uid("marche") });
    s.addText(String(i + 1), { x, y: y + 0.1, w, h: 0.5, align: "center", fontSize: 20, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: uid("num") });
    s.addText(t, { x: x + 0.05, y: y - 0.85, w: w - 0.1, h: 0.8, fontSize: 14, bold: true, color: C.text2, align: "center", valign: "bottom", margin: 0, isTextBox: true, objectName: uid("t") });
  });
  s.addText([{ text: "« Être »", options: { bold: true, color: C.accent1, breakLine: true } }, { text: "devenir soi", options: { color: MUTED } }], { x: 0.6, y: 2.0, w: 2.2, h: 0.8, fontSize: 16, margin: 0, isTextBox: true, objectName: uid("leg") });
  s.addText([{ text: "« Avoir »", options: { bold: true, color: C.accent3, breakLine: true } }, { text: "prendre sa place", options: { color: MUTED } }], { x: 2.9, y: 2.0, w: 2.4, h: 0.8, fontSize: 16, margin: 0, isTextBox: true, objectName: uid("leg") });
  s.addNotes("L’émancipation progresse en cercles de plus en plus larges : l’intime, la famille, la société, le monde. Les étapes suivent les titres des deux parties : « Être » puis « Avoir ».");

  // 16. C2
  s = content("Ce qui résiste", "C · Analyse thématique", "Élève 4");
  s.addText("C2 · Obstacles, résistances et contradictions", { x: 0.6, y: 1.3, w: 10, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const obs = [
    ["Obstacles extérieurs", "wall", ["Le père et la loi", "La société des hommes", "La colonisation"], "pierres"],
    ["Résistances intérieures", "heart", ["La peur", "Le sentiment d’avoir perdu sa vie", "La solitude"], "solitude"],
    ["Contradictions", "balance", ["Libérée par des hommes, ses fils", "Deux idées de la liberté", "Une « civilisation » ambiguë"], "tutelle"],
  ];
  obs.forEach(([t, ic, items, qid], i) => {
    const x = 0.6 + i * 4.15;
    card(s, x, 2.0, 3.9, 4.65);
    iconCircle(s, ic, x + 0.35, 2.3, 0.75, i === 2 ? C.accent2 : C.accent3);
    s.addText(t, { x: x + 1.3, y: 2.3, w: 2.45, h: 0.75, fontSize: 19, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: k < items.length - 1 } })), { x: x + 0.35, y: 3.3, w: 3.3, h: 1.45, ...body, fontSize: 16, paraSpaceAfter: 4, objectName: uid("l") });
    s.addText(quoteRuns(qid, 14), { x: x + 0.35, y: 4.85, w: 3.3, h: 1.65, ...body, objectName: uid("q") });
  });
  s.addNotes("Obstacles extérieurs : le père et la loi, la société des hommes (on leur jette des pierres), la colonisation. Résistances intérieures : la peur, l’angoisse, la solitude. Contradictions : libérée par ses fils, elle doit aussi refuser leur protection.");

  // 17. C3
  s = content("Une famille qui se transforme", "C · Analyse thématique", "Élève 4");
  s.addText("C3 · Comment les apprentissages modifient les rapports familiaux", { x: 0.6, y: 1.3, w: 11, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const rel = [
    ["Le père", "home", "Il l’a épousée à treize ans et décide de tout", "Il la redécouvre et se lève quand elle entre"],
    ["Les fils", "users", "Ils sont ses professeurs et la guident", "Elle refuse leur protection ; Nagib fait la cuisine"],
    ["La société", "female", "Trois personnes, une maison fermée", "Un réseau d’amies, puis un mouvement de femmes"],
  ];
  s.addText("AVANT", { x: 3.0, y: 1.85, w: 4.2, h: 0.35, fontSize: 13, bold: true, charSpacing: 3, color: C.accent3, margin: 0, isTextBox: true, objectName: uid("col") });
  s.addText("APRÈS", { x: 8.15, y: 1.85, w: 4.2, h: 0.35, fontSize: 13, bold: true, charSpacing: 3, color: C.accent1, margin: 0, isTextBox: true, objectName: uid("col") });
  rel.forEach(([t, ic, av, ap], i) => {
    const y = 2.3 + i * 1.45;
    iconCircle(s, ic, 0.6, y + 0.15, 0.85, C.text2);
    s.addText(t, { x: 1.6, y, w: 1.4, h: 1.15, fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    card(s, 3.0, y, 4.6, 1.15);
    s.addText(av, { x: 3.25, y, w: 4.15, h: 1.15, fontSize: 16, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("av") });
    s.addText("→", { x: 7.6, y, w: 0.55, h: 1.15, fontSize: 26, bold: true, color: C.accent2, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: uid("fl") });
    card(s, 8.15, y, 4.58, 1.15, C.text2);
    s.addText(ap, { x: 8.4, y, w: 4.15, h: 1.15, fontSize: 16, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("ap") });
  });
  s.addNotes("Le père passe de la domination à la reconnaissance : « c’est comme si j’avais épousé une nouvelle femme ». Les fils deviennent ses professeurs, puis elle refuse leur protection. La famille patriarcale devient une famille d’égaux.");

  // 18. C4 thèse
  s = pres.addSlide({ masterName: "Section", sectionTitle: "C · Analyse thématique" });
  star(s, 10.45, 1.45, 1.9, HEX.accent2, 55);
  s.addText("C4 · SAVOIR OU IDENTITÉ ?", { x: 0.8, y: 0.8, w: 9, h: 0.45, fontSize: 15, bold: true, charSpacing: 4, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("surtitre") });
  s.addText("Le savoir est l’instrument d’une conquête d’identité, qui se prolonge en action pour les autres.", { x: 0.8, y: 1.45, w: 9.4, h: 2.0, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.background1, valign: "top", margin: 0, isTextBox: true, objectName: uid("these") });
  ["etre", "moi", "actes"].forEach((qid, i) => {
    const x = 0.8 + i * 3.95;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 3.9, w: 3.7, h: 2.3, rectRadius: 0.12, fill: { color: C.background1, transparency: 88 }, line: { color: C.background1, width: 1, transparency: 70 }, objectName: uid("carte") });
    s.addText(quoteRuns(qid, 16, C.background1), { x: x + 0.3, y: 4.15, w: 3.1, h: 1.85, fontSize: 16, valign: "top", margin: 0, isTextBox: true, objectName: uid("q") });
  });
  s.addText("Élève 4", { x: 10.2, y: 0.8, w: 2.4, h: 0.4, fontSize: 14, bold: true, color: C.accent2, align: "center", margin: 0, isTextBox: true, objectName: uid("who") });
  s.addNotes("Notre thèse : la mère ne cherche pas seulement à acquérir des connaissances. Le roman le dit : elle cherche « à être et non à avoir ou posséder ». Le savoir est l’instrument d’une conquête d’identité. Nuance : la partie II s’intitule « Avoir », mais cet avoir sert l’être, et l’identité conquise a un prix : la solitude.");

  // 19. Enjeux
  s = content("Les enjeux du roman", "C · Analyse thématique", "Élève 4");
  const enj = [
    ["Condition des femmes", "female", "Les femmes n’ont pas voix au chapitre"],
    ["Tradition et modernité", "compass", "La vraie civilisation est celle des idées"],
    ["Colonisation", "flag", "Sa libération accompagne celle du pays"],
    ["Liberté et solitude", "heart", "« La liberté est poignante »"],
    ["Être et avoir", "gem", "Elle choisit d’abord l’être"],
  ];
  enj.forEach(([t, ic, d], i) => {
    const x = 0.6 + i * 2.48;
    card(s, x, 1.75, 2.28, 4.8);
    iconCircle(s, ic, x + 0.64, 2.15, 1.0, i % 2 ? C.accent3 : C.accent1);
    s.addText(t, { x: x + 0.2, y: 3.4, w: 1.88, h: 0.95, fontSize: 18, bold: true, color: C.text2, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.2, y: 4.45, w: 1.88, h: 1.8, fontSize: 15, color: C.text1, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: uid("d") });
  });
  s.addNotes("Cinq enjeux : la condition des femmes, tradition et modernité, colonisation et indépendance, liberté et solitude, être et avoir.");

  // 20. Section D
  pres.addSection({ title: "D · Scénette" });
  divider("D · Scénette", "D", "La scène", "L’affrontement entre la mère et le père", "Élève 5 et le groupe");

  // 21. D
  s = content("Une transformation jouée", "D · Scénette", "Élève 5");
  s.addText("Deuxième partie, chapitre 3 · la mère, le père, Nagib, le narrateur · 3 à 4 minutes", { x: 0.6, y: 1.3, w: 11, h: 0.4, fontSize: 15, color: MUTED, margin: 0, isTextBox: true, objectName: uid("question") });
  const tmp = [
    ["1", "Situation initiale", "Le père domine : il a tout payé, il l’a épousée à treize ans", "paye"],
    ["2", "Changement", "Elle lui tient tête et réclame une âme, une liberté", "ame"],
    ["3", "Conséquence", "Elle refuse même la protection de Nagib", "consciente"],
  ];
  tmp.forEach(([num, t, d, qid], i) => {
    const x = 0.6 + i * 4.15;
    card(s, x, 2.0, 3.9, 4.6, i === 2 ? C.text2 : C.background2);
    const dark = i === 2;
    s.addShape(pres.shapes.OVAL, { x: x + 0.35, y: 2.3, w: 0.8, h: 0.8, fill: { color: C.accent2 }, line: { type: "none" }, objectName: uid("num") });
    s.addText(num, { x: x + 0.35, y: 2.3, w: 0.8, h: 0.8, align: "center", valign: "middle", fontSize: 24, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: uid("num_t") });
    s.addText(t, { x: x + 1.35, y: 2.3, w: 2.4, h: 0.8, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: dark ? C.background1 : C.text2, valign: "middle", margin: 0, isTextBox: true, objectName: uid("t") });
    s.addText(d, { x: x + 0.35, y: 3.35, w: 3.25, h: 1.0, ...body, fontSize: 17, bold: true, color: dark ? C.background1 : C.text1, objectName: uid("d") });
    s.addText(quoteRuns(qid, 16, dark ? C.background1 : C.text1), { x: x + 0.35, y: 4.45, w: 3.25, h: 1.95, ...body, objectName: uid("q") });
  });
  s.addNotes("Élève 5 présente la scène en une phrase, puis le groupe la joue (script complet dans le dossier de l’Élève 5). Trois temps : le père domine ; la mère lui tient tête ; elle refuse même la protection de Nagib.");

  // 22. Synthèse
  pres.addSection({ title: "Conclusion" });
  s = content("Synthèse : ce que conquiert la mère", "Conclusion", "Élève 5");
  const syn = [
    ["A", "La langue", "D’objet à sujet : elle agit et commande", "book"],
    ["B", "L’écriture", "De la prison à la naissance, un humour tendre", "pen"],
    ["C", "Le sens", "Le savoir au service de l’identité", "compass"],
  ];
  syn.forEach(([l, t, d, ic], i) => {
    const y = 1.75 + i * 1.25;
    card(s, 0.6, y, 6.4, 1.05);
    iconCircle(s, ic, 0.85, y + 0.17, 0.7);
    s.addText([{ text: `${l} · ${t}`, options: { bold: true, color: C.text2, breakLine: true } }, { text: d, options: { color: C.text1 } }], { x: 1.8, y, w: 5.0, h: 1.05, fontSize: 16, valign: "middle", margin: 0, isTextBox: true, objectName: uid("syn") });
  });
  card(s, 7.3, 1.75, 5.43, 3.55, C.text2);
  s.addText("NOTRE RÉPONSE", { x: 7.65, y: 2.0, w: 4.8, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("lab") });
  s.addText("La mère conquiert une identité, et le savoir en est le moyen. Cette conquête a un prix, la solitude, mais elle transforme toute la famille.", { x: 7.65, y: 2.45, w: 4.8, h: 2.7, fontFace: THEME.headFontFace, fontSize: 21, bold: true, color: C.background1, valign: "top", margin: 0, isTextBox: true, objectName: uid("rep") });
  card(s, 0.6, 5.55, 12.13, 1.1);
  s.addText(quoteRuns("meleve", 17), { x: 0.95, y: 5.55, w: 11.5, h: 1.1, valign: "middle", margin: 0, isTextBox: true, objectName: uid("q") });
  s.addNotes("Trois constats : la langue change avec elle, l’écriture rend ce changement visible, et son sens est clair : elle cherche à être. La scène l’a montré. Notre réponse : la mère conquiert une identité, et le savoir en est le moyen.");

  // 23. Ouverture / merci
  s = pres.addSlide({ masterName: "Titre", sectionTitle: "Conclusion" });
  star(s, 9.4, 1.4, 3.6, HEX.accent2, 40);
  star(s, 10.35, 2.35, 1.7, HEX.lt1, 70);
  s.addText("POUR OUVRIR", { x: 0.8, y: 1.45, w: 8, h: 0.4, fontSize: 14, bold: true, charSpacing: 4, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("surtitre") });
  s.addText("La vraie civilisation, c’est la mère elle-même", { placeholder: "title" });
  s.addText([...quoteRuns("conscience", 20, C.background2)], { placeholder: "body" });
  s.addText("Merci de votre attention", { x: 0.8, y: 6.3, w: 8, h: 0.5, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true, objectName: uid("merci") });
  s.addNotes("Le titre « La Civilisation, ma Mère !… » prend tout son sens : la vraie civilisation, ce ne sont pas la radio ou le fer à repasser, c’est la mère elle-même, devenue « la conscience d’un monde inconscient ». Merci.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("ok", OUT);
}
main().catch((e) => { console.error(e); process.exit(1); });
