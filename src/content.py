# -*- coding: utf-8 -*-
"""Source unique de contenu du projet Groupe 4.

Tout ce qui apparaît dans work/*.md et output/*.pdf est défini ici.
Conventions :
- niveaux : "EXIGE", "RECO", "HYPO" (EXIGÉ / RECOMMANDÉ / HYPOTHÈSE) ;
- citations : uniquement via QUOTES, vérifiées mot à mot dans Roman.pdf par build.py ;
- pages : pagination du PDF fourni (Roman.pdf), à convertir dans l'édition de la classe.
"""

META = {
    "groupe": "Groupe 4",
    "titre": "Les péripéties : les étapes de la transformation",
    "oeuvre": "La Civilisation, ma Mère !…",
    "auteur": "Driss Chraïbi",
    "edition_pdf": "Roman.pdf (conversion calibre de l’édition Folio n° 1902, Denoël, 1972 — 122 pages PDF)",
    "version": "V1",
    "date": "20 octobre 2026",
    "jour_j": "Jour 11",
}

NIVEAUX = {
    "EXIGE": ("EXIGÉ", "Explicitement demandé par la consigne."),
    "RECO": ("RECOMMANDÉ", "Pas écrit dans la consigne, mais nécessaire pour un travail de qualité."),
    "HYPO": ("HYPOTHÈSE", "Incertain : à confirmer auprès du professeur ou dans le texte."),
}

ELEVES = {
    1: {"role": "Responsable de la recherche textuelle", "prod": "Extraits précis et preuves textuelles", "court": "Recherche textuelle", "code": "E1"},
    2: {"role": "Analyste linguistique", "prod": "Temps verbaux, lexique, énonciation, connecteurs", "court": "Analyse linguistique", "code": "E2"},
    3: {"role": "Analyste stylistique", "prod": "Procédés d’écriture et effets produits", "court": "Analyse stylistique", "code": "E3"},
    4: {"role": "Analyste thématique", "prod": "Interprétation, enjeux sociaux et philosophiques", "court": "Analyse thématique", "code": "E4"},
    5: {"role": "Metteur en scène et rapporteur", "prod": "Scénette et synthèse orale", "court": "Mise en scène et synthèse", "code": "E5"},
}

# ---------------------------------------------------------------------------
# La consigne, recopiée mot pour mot (consigne.jpeg)
# ---------------------------------------------------------------------------
CONSIGNE = {
    "titre": "Groupe 4 : Les péripéties : les étapes de la transformation",
    "intro": "Suivre l’évolution de la mère à travers ses expériences successives.",
    "axes": [
        ("AX1", "Les apprentissages et les découvertes."),
        ("AX2", "Les changements de comportement et de langage."),
        ("AX3", "Les nouvelles relations avec la famille et la société."),
    ],
    "intertitre": "Les péripéties et la transformation progressive",
    "parties": [
        {"code": "A", "titre": "Analyse linguistique", "eleve": 2, "questions": [
            ("A1", "Quels champs lexicaux accompagnent les découvertes et les apprentissages ?"),
            ("A2", "Quels verbes d’action montrent que la mère devient progressivement actrice de sa vie ?"),
            ("A3", "Comment les temps verbaux et les indicateurs temporels soulignent-ils la progression du changement ?"),
        ]},
        {"code": "B", "titre": "Analyse stylistique", "eleve": 3, "questions": [
            ("B1", "Quels procédés rendent la transformation de la mère perceptible ?"),
            ("B2", "Quelle place l’humour, l’ironie ou le décalage occupent-ils dans le passage ?"),
            ("B3", "Comment le regard du narrateur contribue-t-il à valoriser ou à interroger cette évolution ?"),
        ]},
        {"code": "C", "titre": "Analyse thématique", "eleve": 4, "questions": [
            ("C1", "Quelles sont les principales étapes de l’émancipation ?"),
            ("C2", "Quels obstacles, résistances ou contradictions apparaissent ?"),
            ("C3", "Comment les apprentissages modifient-ils les rapports familiaux ?"),
            ("C4", "La mère cherche-t-elle seulement à acquérir des connaissances ou également à conquérir une nouvelle identité ?"),
        ]},
        {"code": "D", "titre": "Scénette", "eleve": 5, "questions": [
            ("D", "Choisissez un épisode significatif qui montre une transformation concrète. La scène doit comporter une situation initiale, un changement et une conséquence identifiable."),
        ]},
    ],
}


def toutes_questions():
    for p in CONSIGNE["parties"]:
        for qid, txt in p["questions"]:
            yield qid, txt, p


# ---------------------------------------------------------------------------
# Le roman : repères vérifiés dans Roman.pdf
# ---------------------------------------------------------------------------
# (partie, chapitre) -> (page PDF début, page PDF fin). build.py vérifie que chaque
# page de début commence bien par le numéro du chapitre.
CHAPITRES = {
    ("I", 1): (9, 9), ("I", 2): (10, 17), ("I", 3): (18, 27), ("I", 4): (28, 33),
    ("I", 5): (34, 39), ("I", 6): (40, 47), ("I", 7): (48, 51), ("I", 8): (52, 57),
    ("I", 9): (58, 64), ("I", 10): (65, 66),
    ("II", 1): (68, 73), ("II", 2): (74, 83), ("II", 3): (84, 91), ("II", 4): (92, 94),
    ("II", 5): (95, 105), ("II", 6): (106, 112), ("II", 7): (113, 119),
}

REPERES_ROMAN = [
    "Deux parties : I « Être » (chapitres 1 à 10, p. 8-66) et II « Avoir » (chapitres 1 à 7, p. 67-119).",
    "Deux narrateurs : en partie I, le fils cadet (surnommé « petit loustic ») ; en partie II, le fils aîné Nagib, qui s’adresse à son frère parti en France.",
    "Le père n’est jamais nommé ; la mère non plus. Elle est « ma mère », « maman », « m’man ».",
    "Pagination : les pages citées sont celles du PDF fourni. Elles ne correspondent pas à l’édition papier. La référence fiable est le couple partie-chapitre (ex. : II-3).",
]

# Citations vérifiées automatiquement (texte exact, page PDF, partie-chapitre).
QUOTES = {
    "q01": ("Et fais-moi le plaisir d’enlever ces vêtements de païen !", 10, ("I", 2)),
    "q02": ("Personne ne lui avait rien appris depuis qu’elle était venue au monde.", 14, ("I", 2)),
    "q03": ("Elle était un arbre, cerclé dans une cour de prison", 16, ("I", 2)),
    "q04": ("C’est une boîte qui parle.", 22, ("I", 3)),
    "q05": ("Allume-éteins !… Allume-éteins !… Allume-éteins !…", 24, ("I", 3)),
    "q06": ("Elle était là, dans cette maison-tombeau, apprenant la vie.", 26, ("I", 3)),
    "q07": ("L’instinct vainquit la science, le primitif rendit des points à la civilisation métallurgique.", 33, ("I", 4)),
    "q08": ("Sans quitter sa maison, elle avait établi un réseau inextricable de liens", 39, ("I", 5)),
    "q09": ("Ce monde est à toi aussi.", 45, ("I", 6)),
    "q10": ("Jamais elle n’en avait franchi le seuil.", 46, ("I", 6)),
    "q11": ("C’était son premier secret.", 48, ("I", 7)),
    "q12": ("Elle ne cherchait pas à savoir mais à comprendre, à être et non à avoir ou posséder.", 57, ("I", 8)),
    "q13": ("Elle apprenait avec avidité", 58, ("I", 9)),
    "q14": ("Et nous la voyions naître.", 63, ("I", 9)),
    "q15": ("Elle se vit, elle – existante, toute nue dans un monde nu.", 64, ("I", 9)),
    "q16": ("La liberté est poignante, dit-elle à mi-voix. Elle fait parfois souffrir.", 66, ("I", 10)),
    "q17": ("je me demande si vous avez bien fait, Nagib et toi, d’ouvrir la porte de ma prison.", 66, ("I", 10)),
    "q18": ("Dis-lui qu’il n’y a pas que les hommes sur la terre. Il y a également les femmes et on ne nous a pas consultées.", 79, ("II", 2)),
    "q19": ("Je ne connaissais plus ma mère.", 82, ("II", 2)),
    "q20": ("Depuis quelque temps, tu as adopté un langage bizarre, un comportement insolite.", 85, ("II", 3)),
    "q21": ("mes désirs n’étaient pas exaucés. Ils étaient prévenus. Ils étaient les tiens.", 85, ("II", 3)),
    "q22": ("Mais mon âme, dis ? mon âme ?", 86, ("II", 3)),
    "q23": ("Je suis à présent consciente, entièrement responsable de ma vie, entends-tu ?", 90, ("II", 3)),
    "q24": ("Paix à vous tous, vieux compagnons d’enfance et de jeunesse, au nom de l’avenir qui commence !", 93, ("II", 4)),
    "q25": ("un mot était brodé : « MOI. »", 97, ("II", 5)),
    "q26": ("Elle disait qu’elle n’apprenait pas pour apprendre ni même pour savoir. Mais pour nourrir et régénérer son sang.", 101, ("II", 5)),
    "q27": ("c’est comme si j’avais épousé une nouvelle femme, que je commence à connaître", 103, ("II", 5)),
    "q28": ("Mes idées, mes acquisitions, mes émotions, il faut que je les traduise en actes, pour moi et pour les autres.", 110, ("II", 6)),
    "q29": ("On nous jeta des pierres, on creva les pneus de la voiture.", 110, ("II", 6)),
    "q30": ("ta mère était, à elle seule, la conscience d’un monde inconscient.", 113, ("II", 7)),
    "q31": ("Ma mère a été reçue à tous ses examens – et même au permis de conduire.", 118, ("II", 7)),
    "q32": ("j’ai besoin de faire reculer mon horizon", 118, ("II", 7)),
    "q33": ("Ça ne va pas. Ce n’est pas pour moi.", 43, ("I", 6)),
    "q34": ("Mais que va dire votre père ?", 45, ("I", 6)),
    "q35": ("Tu m’as toujours tout payé.", 85, ("II", 3)),
    "q36": ("Alors, va ouvrir cette porte, demande pardon à ton père et monte te coucher.", 91, ("II", 3)),
    "q37": ("Parfaitement. J’ai le téléphone.", 78, ("II", 2)),
    "q38": ("J’ai cru voir ton père.", 83, ("II", 2)),
}

# Chronologie : 12 étapes (repères factuels — l'interprétation revient à l'Élève 4)
CHRONOLOGIE = [
    {"n": 1, "titre": "La recluse", "loc": ("I", 2), "pages": "10-17", "axe": "AX2",
     "fait": "La mère vit enfermée dans la maison, fabrique tout de ses mains et rejette le français et les « vêtements de païen » de ses fils.",
     "q": ["q01", "q02", "q03"]},
    {"n": 2, "titre": "La radio et l’électricité", "loc": ("I", 3), "pages": "18-27", "axe": "AX1",
     "fait": "Arrivée de la radio. Elle croit à un magicien, « Monsieur Kteu », allume et éteint la lumière en boucle et converse avec le poste.",
     "q": ["q04", "q05", "q06"]},
    {"n": 3, "titre": "Les objets techniques et le téléphone", "loc": ("I", 4), "loc2": ("I", 5), "pages": "28-39", "axe": "AX1",
     "fait": "Elle détourne le brasero, la cuisinière et le fer à repasser. Grâce au téléphone, elle tisse un réseau d’amies dans tout le pays.",
     "q": ["q07", "q08"]},
    {"n": 4, "titre": "Robe, souliers, première sortie", "loc": ("I", 6), "loc2": ("I", 7), "pages": "40-51", "axe": "AX2",
     "fait": "Ses fils l’habillent à l’européenne et la font sortir pour la première fois : visite du parc, puis un « premier secret » gardé face au père.",
     "q": ["q33", "q34", "q09", "q10", "q11"]},
    {"n": 5, "titre": "Le cinéma", "loc": ("I", 8), "pages": "52-57", "axe": "AX1",
     "fait": "Seule femme dans la salle, elle vit le film à voix haute, le raconte aux spectateurs, puis passe une nuit d’angoisse et de questions.",
     "q": ["q12"]},
    {"n": 6, "titre": "Les apprentissages et la naissance à soi", "loc": ("I", 9), "pages": "58-64", "axe": "AX1",
     "fait": "Elle apprend la lecture, l’histoire, la géographie, son corps, la mécanique et l’argent. Monsieur Kteu est démystifié ; elle « se voit » et pleure.",
     "q": ["q13", "q14", "q15"]},
    {"n": 7, "titre": "La falaise : la liberté douloureuse", "loc": ("I", 10), "pages": "65-66", "axe": "AX3",
     "fait": "Veille du départ du fils cadet en France. Elle doute d’avoir eu raison de quitter sa « prison » et s’interroge sur l’amour.",
     "q": ["q16", "q17"]},
    {"n": 8, "titre": "L’engagement public (la guerre, Anfa)", "loc": ("II", 1), "loc2": ("II", 2), "pages": "68-83", "axe": "AX3",
     "fait": "Elle suit la guerre au téléphone, coud un drapeau des peuples et mène une foule vers la villa où loge de Gaulle.",
     "q": ["q37", "q18", "q19", "q38"]},
    {"n": 9, "titre": "L’affrontement avec le père", "loc": ("II", 3), "pages": "84-91", "axe": "AX3",
     "fait": "Elle tient tête à son mari (« mon âme ? »). Elle refuse ensuite la protection de Nagib, qui a mis le père à la porte.",
     "q": ["q20", "q35", "q21", "q22", "q23", "q36"]},
    {"n": 10, "titre": "L’enterrement du passé et la nouvelle maison", "loc": ("II", 4), "loc2": ("II", 5), "pages": "92-105", "axe": "AX2",
     "fait": "Elle enterre ses objets d’autrefois sous un oranger, vend les meubles et repeint la maison. Elle brode « MOI », s’inscrit à l’école et lit de façon critique.",
     "q": ["q24", "q25", "q26", "q27"]},
    {"n": 11, "titre": "La transmission aux femmes et les résistances", "loc": ("II", 6), "pages": "106-112", "axe": "AX3",
     "fait": "Elle organise des « déjeuners-débats » qui instruisent les femmes à travers le pays. Les maris et les villages deviennent hostiles.",
     "q": ["q28", "q29"]},
    {"n": 12, "titre": "Indépendance, conversion du père, départ", "loc": ("II", 7), "pages": "113-119", "axe": "AX3",
     "fait": "Elle interpelle les politiques. Le père reconnaît son erreur. Elle réussit ses examens, se coupe les cheveux et part pour la France avec Nagib.",
     "q": ["q30", "q31", "q32"]},
]

# Épisodes candidats pour la scénette (D), testés sur la grille exigée
EPISODES = [
    {"id": "EP-A", "titre": "La première sortie", "loc": ("I", 6), "pages": "40-47",
     "si": ("La mère n’a jamais quitté la maison depuis ses noces.", "q10"),
     "chg": ("Habillée et chaussée par ses fils, elle sort malgré sa peur et découvre la ville, puis le parc.", "q34"),
     "csq": ("Une tache d’herbe sur la robe devient son « premier secret » face au père (I-7).", "q11"),
     "roles": "La mère, Nagib, le cadet (narrateur) ; facultatif : le vendeur de chaussures.",
     "atouts": "Les trois temps sont les plus nets et faciles à jouer, la scène est visuelle (robe, talons sciés, porte).",
     "limites": "Conséquence encore intime ; l’opposition au père n’est qu’annoncée.",
     "score": [3, 3, 2, 3], "reco": "Plan B (le plus sûr si le temps de scène est court)"},
    {"id": "EP-B", "titre": "L’affrontement avec le père", "loc": ("II", 3), "pages": "84-91",
     "si": ("Le père rappelle qu’il a « tout payé » et ne reconnaît plus sa femme.", "q35"),
     "chg": ("Elle revendique une âme et une liberté (« mon âme ? »), puis refuse la protection de Nagib.", "q22"),
     "csq": ("Elle se déclare responsable de sa vie et ordonne à Nagib d’aller demander pardon au père.", "q23"),
     "roles": "La mère, le père, Nagib (narrateur) ; voix off possible pour le récit.",
     "atouts": "C’est la transformation la plus concrète et la plus forte. La scène relie directement C3 (famille) et C4 (identité), et l’humour de Nagib allège le drame.",
     "limites": "La tirade de la mère est longue et doit être coupée avec soin ; scène de colère difficile à jouer juste.",
     "score": [3, 3, 3, 2], "reco": "Recommandé (relie le mieux la scénette aux analyses)"},
    {"id": "EP-C", "titre": "La marche vers de Gaulle à Anfa", "loc": ("II", 2), "pages": "74-83",
     "si": ("Une foule menée par la mère arrive devant la villa ; la sentinelle ne bouge pas.", "q37"),
     "chg": ("Elle prend la parole au nom des femmes et des sans-voix, et dicte ses « articles » au soldat.", "q18"),
     "csq": ("Nagib ne reconnaît plus sa mère ; elle voit en de Gaulle le portrait du père.", "q19"),
     "roles": "La mère, le soldat, Nagib, le « Russe », la foule (2 à 5 rôles).",
     "atouts": "Le texte est déjà écrit en dialogue théâtral ; la scène est très comique et tous les membres peuvent jouer.",
     "limites": "La conséquence touche moins la vie de la mère ; la scène exige des accessoires (fusil, drapeau) et son contexte historique est à expliquer.",
     "score": [2, 3, 2, 3], "reco": "Variante possible si le groupe veut une scène chorale"},
]
CRITERES_EPISODE = ["Situation initiale claire", "Changement concret", "Conséquence identifiable", "Faisabilité (5 élèves, peu d’accessoires)"]
EPISODE_ECARTE = ("La radio « Monsieur Kteu » (I-3)", "C’est très drôle, mais la conséquence reste modeste et la mère y subit l’événement plus qu’elle n’agit. La consigne demande une transformation concrète.")

# ---------------------------------------------------------------------------
# Phase 1 : analyse de la consigne
# ---------------------------------------------------------------------------
QUESTION_CENTRALE = ("Comment les péripéties successives font-elles passer la mère de l’enfermement "
                     "à l’émancipation, et que conquiert-elle au bout du compte : un savoir, ou une nouvelle identité ?")

EXIGENCES_IMPLICITES = [
    ("EXIGE", "Appuyer chaque réponse sur des extraits précis : c’est la « production attendue » de l’Élève 1, donc un standard pour tout le groupe."),
    ("EXIGE", "Traiter en plus l’énonciation et les connecteurs (Élève 2), même si les questions A1-A3 ne les citent pas."),
    ("EXIGE", "Toujours relier un procédé à son effet (Élève 3), et pas seulement le nommer."),
    ("EXIGE", "Dégager les enjeux sociaux et philosophiques (Élève 4), au-delà des seules questions C1-C4."),
    ("EXIGE", "Produire une synthèse orale (Élève 5), en plus de la scénette D."),
    ("RECO", "Suivre une progression : « expériences successives », « étapes », « progressivement » imposent une lecture chronologique."),
    ("RECO", "Couvrir les trois axes de la consigne (apprentissages / comportement et langage / relations), qui servent de grille de classement."),
    ("HYPO", "« Le passage » (B2) : extrait étudié en classe ou roman entier ? Le plan retient le roman entier tant que le professeur n’a pas précisé."),
    ("HYPO", "Le format de rendu (oral seul, dossier, diaporama) et les durées ne sont pas précisés."),
]

ATTRIBUTION_NOTE = ("La consigne ne relie pas les parties A-D aux élèves. La correspondance ci-dessous est déduite des "
                    "intitulés de rôle (« Analyste linguistique » → A, etc.), qui ne laissent aucun doute raisonnable.")

ROLES_SANS_QUESTION = [
    ("Élève 1", "Aucune question A-D ne lui revient. Sa mission est transversale : constituer le corpus, établir la chronologie et vérifier les citations. Il est aussi propriétaire des trois axes de la consigne, qui servent de colonnes de classement du corpus."),
    ("Élève 5", "Il possède D, ainsi que la « synthèse orale », qui n’a pas de question propre : elle doit relier A, B et C et répondre à C4 sans refaire l’analyse."),
]

FRONTIERES = [
    {"zone": "Énonciation (Élève 2) / Regard du narrateur B3 (Élève 3)",
     "regle": "L’Élève 2 repère les marques : qui parle (je / nous / elle), quel type de discours (direct, indirect, indirect libre), quel narrateur dans chaque partie. L’Élève 3 interprète l’attitude du narrateur (admiration, tendresse, ironie, distance) et ce qu’elle produit.",
     "test": "Une phrase du type « le narrateur dit… » va en A ; « le narrateur juge / met à distance… » va en B."},
    {"zone": "Champs lexicaux A1 (Élève 2) / Procédés B1 (Élève 3)",
     "regle": "Un ensemble de mots appartenant à un même thème relève de A. Une figure (comparaison, métaphore, gradation, antithèse…) relève de B, même si elle contient ces mots.",
     "test": "« comme un oiseau » est une comparaison, donc B ; « école, livres, cartable » forment un champ lexical, donc A."},
    {"zone": "Verbes d’action A2 (Élève 2) / Étapes C1 (Élève 4)",
     "regle": "A2 étudie la grammaire de l’action : qui est le sujet, quels verbes, à quelle voix. C1 interprète le sens des étapes. L’Élève 4 cite les résultats de A2 sans les refaire.",
     "test": "Le passage d’une mère complément (ses fils agissent sur elle) à une mère sujet (elle agit) s’analyse en A2 ; ce que ce passage signifie pour son émancipation s’analyse en C1."},
    {"zone": "Temps et indicateurs A3 (Élève 2) / Chronologie (Élève 1)",
     "regle": "L’Élève 1 établit QUOI et OÙ (étapes, chapitres, pages). L’Élève 2 analyse COMMENT le système des temps et les indicateurs rendent la progression.",
     "test": "Situer un épisode (II-3, p. 84) relève de l’Élève 1 ; expliquer le choix d’un temps verbal dans ce passage relève de l’Élève 2."},
    {"zone": "Humour B2 (Élève 3) / Scénette D (Élève 5)",
     "regle": "L’Élève 3 identifie les ressorts comiques ; l’Élève 5 décide de ce qui est joué. L’Élève 3 conseille sans écrire le script.",
     "test": "Un échange de 10 min (étape S09) suffit ; le script reste à l’Élève 5."},
    {"zone": "Thèse C4 (Élève 4) / Synthèse orale (Élève 5)",
     "regle": "L’Élève 4 formule la thèse. L’Élève 5 la présente et la relie aux apports de A et B, sans la réécrire.",
     "test": "Toute modification de la thèse passe par l’Élève 4."},
]

# ---------------------------------------------------------------------------
# Phase 2 : critique du plan initial (plan.md)
# ---------------------------------------------------------------------------
PLAN_INITIAL_CHARGE = {1: 6.0, 2: 5.5, 3: 6.0, 4: 6.0, 5: 6.5}  # heures annoncées dans plan.md (hors 2 h de répétitions)

CRITIQUE = {
    "forces": [
        "Les rôles imposés par la consigne sont respectés ; la mission transversale de chacun est explicite.",
        "L’idée d’un corpus commun avec une colonne « utilisée par » évite les doublons.",
        "La problématique centrale reprend C4 comme fil conducteur, ce qui est juste.",
        "Un premier tableau de risques et une checklist finale existent déjà.",
        "Les épisodes pressentis pour la scénette (sortie, radio/téléphone, affrontement avec le père) existent bien dans le texte (I-6, I-3/I-5, II-3).",
    ],
    "constats": [
        {"theme": "Équilibre de la charge",
         "constat": "Les estimations (5 h 30 à 6 h 30) ne comptent ni la relecture du roman ni les réunions. L’Élève 1 doit relire 112 pages et en extraire 25 à 35 citations : sa charge est sous-estimée et concentrée sur les jours 1 à 3. L’Élève 5 concentre son travail en fin de projet (script, synthèse, répétitions).",
         "gravite": "Forte"},
        {"theme": "Dépendances",
         "constat": "Tout le groupe attend le corpus jusqu’au jour 3. Pendant ce temps, les Élèves 2 à 4 ont une consigne vague (« relire le roman en notant ») et l’Élève 5 n’a rien à faire. La synthèse dépend de la thèse C4, qui n’arrive qu’au jour 7 : c’est trop tard.",
         "gravite": "Forte"},
        {"theme": "Contrôle qualité",
         "constat": "La vérification finale des citations tombe au jour 10, la veille de la remise : trop tard pour corriger. Personne ne relit le script ni la synthèse de l’Élève 5. L’Élève 4 écrit C tout en arbitrant la cohérence, il est donc juge et partie.",
         "gravite": "Moyenne"},
        {"theme": "Tâches vagues",
         "constat": "Plusieurs tâches n’ont pas de critère vérifiable : « relire en notant », « support visuel (si demandé) », « un rôle dans la scénette », « point écrit tous les deux jours » (à quelles dates ?).",
         "gravite": "Moyenne"},
        {"theme": "Manques",
         "constat": "Il manque une règle de frontière énonciation / regard du narrateur, la distinction entre les deux narrateurs (le cadet en I, Nagib en II), le problème de pagination (PDF ≠ édition papier), un budget de temps pour l’oral, un ordre de passage, des critères de « terminé » pour les Élèves 1 à 4 et un plan de repli si une réunion échoue.",
         "gravite": "Moyenne"},
        {"theme": "Redondances et généralités",
         "constat": "La section E répète la mission du Membre 5 déjà décrite en C. Le risque « œuvre non identifiée » est désormais levé : le PDF fourni est bien le roman de Chraïbi. Certaines formules restent génériques (« Google Drive ou équivalent ») ; la numérotation « Membre » diffère de « Élève » dans la consigne.",
         "gravite": "Faible"},
        {"theme": "Conformité à la consigne",
         "constat": "Le plan ne structure pas le corpus selon les trois axes de la consigne (apprentissages / comportement et langage / relations). Il ne mentionne pas non plus les « enjeux sociaux et philosophiques » attendus de l’Élève 4.",
         "gravite": "Moyenne"},
    ],
    "corrections": [
        ("Ajouter l’étape S03 « Repérages par angle » (jours 1-2) pour les Élèves 2 à 4.", "Personne n’attend les bras croisés, et le corpus s’enrichit de leurs repérages."),
        ("Livrer le corpus en deux lots (partie I au jour 2, partie II au jour 3).", "Cela supprime le point de blocage unique du jour 3."),
        ("Demander à l’Élève 4 sa thèse C4 en une phrase dès le jour 5.", "Cela débloque la synthèse de l’Élève 5 deux jours plus tôt."),
        ("Avancer la vérification des citations aux jours 6-7 (étape S10), avant la relecture croisée.", "Les erreurs se corrigent avant d’être répétées à l’oral."),
        ("Confier la relecture du script à l’Élève 1 (fidélité au texte) et la validation de la thèse dans la synthèse à l’Élève 4.", "Le travail de l’Élève 5 est contrôlé comme celui des autres."),
        ("Remplacer « relire en notant » par une livraison de 6 à 8 passages repérés au jour 2 à 18 h.", "La tâche devient vérifiable."),
        ("Classer le corpus selon les trois axes de la consigne (colonne « axe »).", "Le travail suit la consigne mot pour mot."),
        ("Ajouter six règles de frontière entre les rôles (voir analyse).", "Pas de doublons ni de trous à l’oral."),
        ("Noter les pages au format « p. PDF » et convertir dans l’édition de la classe au jour 10.", "Le PDF fourni n’a pas la pagination papier."),
        ("Passer à deux points de contrôle formels (CP1 corpus, CP2 répétition générale) avec un plan de repli chacun.", "Un échec au point de contrôle ne bloque plus le groupe."),
        ("Recalculer la charge (environ 12 à 13,5 h chacun, répétitions comprises) et la rééquilibrer.", "L’écart reste sous 20 % (voir tableau)."),
        ("Classer le support visuel en HYPOTHÈSE et le partager entre les Élèves 2 et 3.", "Ce support n’est pas exigé par la consigne et ne doit pas surcharger un seul élève."),
        ("Ajouter un conducteur de l’oral (ordre, minutage, transitions) à la charge de l’Élève 5.", "C’est indispensable pour une synthèse orale cohérente."),
        ("Renommer « Membre n » en « Élève n » (fichiers : E1 à E5).", "C’est le vocabulaire de la consigne, et les noms de fichiers restent sans accents."),
        ("Fusionner les sections C (mission du Membre 5) et E dans le dossier individuel de l’Élève 5.", "Supprime la redondance."),
    ],
}

# Journal des modifications (hors corps des PDF) — tout ajout au-delà de plan.md est tagué [AJOUT]
JOURNAL = [
    ("AJOUT", "Identification confirmée de l’œuvre par le PDF fourni (métadonnées et texte) ; l’hypothèse du plan est levée."),
    ("AJOUT", "Chronologie en 12 étapes avec références partie-chapitre-page et 38 citations vérifiées automatiquement dans Roman.pdf."),
    ("AJOUT", "Trois épisodes candidats testés sur la grille situation initiale / changement / conséquence, plus un épisode écarté."),
    ("AJOUT", "Six règles de frontière entre les rôles."),
    ("AJOUT", "Étapes S03 (repérages), S10 (vérification continue), S12 (conducteur de l’oral), S13 (support visuel, en HYPOTHÈSE)."),
    ("AJOUT", "Points de contrôle CP1 et CP2 avec plans de repli."),
    ("AJOUT", "Chemin critique, diagramme de Gantt, charge recalculée par élève et par période."),
    ("AJOUT", "Niveaux EXIGÉ / RECOMMANDÉ / HYPOTHÈSE appliqués à toutes les tâches et exigences."),
    ("AJOUT", "Dossiers individuels avec fiches méthode, entrées / sorties et définition de « terminé »."),
    ("AJOUT", "Probabilité et impact qualitatifs dans le tableau des risques, et 5 nouveaux risques."),
    ("AJOUT", "Budget de temps de l’oral (HYPOTHÈSE) et ordre de passage."),
    ("AJOUT", "Tableau de suivi Kanban prêt à imprimer."),
    ("MODIF", "« Membre n » devient « Élève n » ; nommage des fichiers en G4_[Partie]_E[n]_V[n]."),
    ("MODIF", "Vérification des citations avancée du jour 10 aux jours 6-7 ; jour 10 devenu tampon et contrôle final."),
    ("MODIF", "Thèse C4 livrée au jour 5 (au lieu du jour 7)."),
    ("MODIF", "Corpus livré en deux lots (jour 2 et jour 3)."),
    ("MODIF", "Support visuel : de « Membre 3 » à « Élèves 2 et 3, si exigé »."),
    ("SUPPR", "Section E fusionnée dans le dossier de l’Élève 5 ; risque « œuvre non identifiée » retiré."),
    ("MODIF", "Partie D (scénette) mise en attente à la demande du groupe : S05, S09 et S14 sont retirées du calendrier actif ; décision au plus tard au jour 6."),
    ("MODIF", "Rééquilibrage après la mise en attente : l’Élève 5 relève II-6 et II-7 (S04), écrit l’introduction et les transitions (S12) et assemble le support visuel (S13)."),
    ("NOTE", "La section G de plan.md était déjà d’un seul tenant dans le fichier reçu : il n’y avait rien à fusionner."),
    ("NOTE", "infos.md est absent : il n’y a ni date limite, ni durée d’oral, ni noms. Le calendrier est donc relatif (Jour 1 à Jour 11) et les noms sont laissés en blanc."),
]

# ---------------------------------------------------------------------------
# Phase 3 : feuille de route
# ---------------------------------------------------------------------------
JOURS = [f"J{i}" for i in range(1, 12)]  # J11 = Jour J (présentation)

ETAPES = [
    {"code": "S01", "titre": "Cadrage et lancement", "j": (1, 1), "h": {5: 2.0, 1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5},
     "niveau": "RECO", "critique": True, "prereq": [],
     "actions": ["Créer le dossier partagé et le groupe de discussion", "Confirmer les rôles et les règles de frontière", "Envoyer les questions de cadrage au professeur", "Fixer la date du Jour J", "Afficher le tableau de suivi"],
     "livrable": "Fiche de cadrage (G4_Cadrage_E5_V1)", "validation": "Les 5 élèves confirment par écrit ; questions envoyées ; Jour J noté.",
     "debloque": ["S02", "S03"]},
    {"code": "S02", "titre": "Corpus, lot 1 (partie I) et chronologie V1", "j": (1, 2), "h": {1: 3.0},
     "niveau": "EXIGE", "critique": True, "prereq": ["S01"],
     "actions": ["Relire la partie I « Être » (ch. 1-10)", "Vérifier les 12 étapes de la chronologie de référence", "Relever au moins 15 citations exactes avec page et chapitre", "Classer chaque citation par étape et par axe"],
     "livrable": "G4_Corpus_E1_V1", "validation": "Chaque étape de la partie I a au moins 1 citation recopiée mot à mot et référencée.",
     "debloque": ["S04"]},
    {"code": "S03", "titre": "Repérages par angle d’analyse", "j": (1, 2), "h": {2: 1.5, 3: 1.5, 4: 1.5},
     "niveau": "RECO", "critique": False, "prereq": ["S01"],
     "actions": ["Relire le roman avec sa propre grille (A, B ou C)", "Proposer 6 à 8 passages (partie-chapitre + page) à l’Élève 1", "Signaler à l’Élève 5 les passages jouables"],
     "livrable": "Liste de repérages (G4_Reperages_E[n]_V1)", "validation": "Liste déposée au jour 2 avant 18 h.",
     "debloque": ["S04"]},
    {"code": "S04", "titre": "Corpus V2 complet (partie II et fusion)", "j": (2, 3), "h": {1: 2.0, 5: 1.0},
     "niveau": "EXIGE", "critique": True, "prereq": ["S02", "S03"],
     "actions": ["Relever la partie II « Avoir » (ch. 1-5) ; l’Élève 5 relève II-6 et II-7, l’Élève 1 vérifie", "Intégrer les repérages des Élèves 2 à 4", "Numéroter les citations et laisser la colonne « utilisée par » vide", "Vérifier chaque citation mot à mot"],
     "livrable": "G4_Corpus_E1_V2 (25 à 35 citations)", "validation": "25 citations ou plus, 12 étapes couvertes, 3 axes représentés.",
     "debloque": ["CP1"]},
    {"code": "CP1", "titre": "Point de contrôle 1 : validation du corpus", "j": (3, 3), "h": {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5, 5: 0.5},
     "niveau": "RECO", "critique": True, "prereq": ["S04"], "checkpoint": True,
     "actions": ["Réunion de 30 min", "Chaque analyste réserve ses citations (colonne « utilisée par »)", "L’Élève 5 rappelle la date limite de décision sur la partie D (jour 6)"],
     "livrable": "Corpus validé (G4_Corpus_E1_V3)", "validation": "Accord des 5 élèves ; aucune étape sans citation.",
     "debloque": ["S06", "S07", "S08"]},
    {"code": "S05", "titre": "Choix de l’épisode de la scénette", "j": (3, 4), "h": {5: 1.5},
     "niveau": "EXIGE", "critique": False, "partie_d": True, "prereq": ["CP1"],
     "actions": ["Tester les 3 candidats sur la grille SI / changement / conséquence", "Faire voter le groupe (vote par message)", "Obtenir de l’Élève 1 les citations de l’épisode"],
     "livrable": "Fiche de choix d’épisode", "validation": "Les 3 temps sont identifiés, chacun avec une citation et sa page.",
     "debloque": ["S09"]},
    {"code": "S06", "titre": "Analyse linguistique A1-A3", "j": (4, 6), "h": {2: 4.0},
     "niveau": "EXIGE", "critique": True, "prereq": ["CP1"],
     "actions": ["Remplir la grille relevé → analyse → effet", "Traiter aussi l’énonciation et les connecteurs", "Utiliser uniquement des citations du corpus"],
     "livrable": "G4_FicheA_E2_V1 (1 à 2 pages)", "validation": "Au moins 3 relevés analysés par question, tous issus du corpus.",
     "debloque": ["S10", "S11"]},
    {"code": "S07", "titre": "Analyse stylistique B1-B3", "j": (4, 6), "h": {3: 4.0},
     "niveau": "EXIGE", "critique": True, "prereq": ["CP1"],
     "actions": ["Remplir la grille procédé → citation → effet", "Distinguer humour, ironie et décalage (B2)", "Comparer le regard des deux narrateurs (B3)"],
     "livrable": "G4_FicheB_E3_V1 (1 à 2 pages)", "validation": "Chaque procédé est nommé, cité et suivi de son effet ; au moins 3 par question.",
     "debloque": ["S10", "S11"]},
    {"code": "S08", "titre": "Analyse thématique C1-C4", "j": (4, 6), "h": {4: 4.5},
     "niveau": "EXIGE", "critique": True, "prereq": ["CP1"],
     "actions": ["Envoyer la thèse C4 en une phrase à l’Élève 5 au jour 5", "Rédiger les réponses argumentées C1-C4", "Dégager les enjeux sociaux et philosophiques"],
     "livrable": "G4_FicheC_E4_V1 (2 pages)", "validation": "Chaque réponse a une idée directrice et 2 preuves ; la thèse C4 est formulée en une phrase.",
     "debloque": ["S10", "S11", "S12"]},
    {"code": "S09", "titre": "Script de la scénette V1", "j": (4, 6), "h": {5: 2.5, 1: 0.5, 2: 0.5, 3: 0.5},
     "niveau": "EXIGE", "critique": False, "partie_d": True, "prereq": ["S05"],
     "actions": ["Écrire le script en 3 temps à partir du texte", "Conseil de 10 min : langage avant / après (Élève 2) et ressorts comiques (Élève 3)", "Distribuer les rôles et prévoir les coupes"],
     "livrable": "G4_Script_E5_V1", "validation": "3 temps identifiables, chaque réplique clé sourcée, durée cible respectée à la lecture.",
     "debloque": ["S14"]},
    {"code": "S10", "titre": "Vérification des citations", "j": (6, 7), "h": {1: 1.5},
     "niveau": "RECO", "critique": True, "prereq": ["S06", "S07", "S08"],
     "actions": ["Comparer chaque citation des fiches A, B et C au texte", "Signaler les écarts à l’auteur", "Tenir le rapport de vérification"],
     "livrable": "G4_Verif_E1_V1", "validation": "100 % des citations conformes ou corrigées.",
     "debloque": ["S11"]},
    {"code": "S11", "titre": "Relecture croisée et corrections", "j": (7, 8), "h": {1: 1.0, 2: 2.0, 3: 2.0, 4: 2.0, 5: 1.0},
     "niveau": "RECO", "critique": True, "prereq": ["S10"],
     "actions": ["L’Élève 2 relit B, l’Élève 3 relit C, l’Élève 4 relit A", "Chaque auteur corrige sa fiche (V2) ; l’Élève 1 vérifie les citations modifiées", "L’Élève 5 relit les trois fiches et en extrait une idée clé chacune"],
     "livrable": "Fiches A, B, C en V2", "validation": "Plus aucune contradiction ni doublon signalé.",
     "debloque": ["S12"]},
    {"code": "S12", "titre": "Synthèse orale et conducteur de l’oral", "j": (7, 8), "h": {5: 3.0, 4: 0.5},
     "niveau": "EXIGE", "critique": True, "prereq": ["S08", "S11"],
     "actions": ["Rédiger la synthèse : thèse C4 + 1 apport de A, B et C", "Écrire l’introduction et les phrases de transition", "Fixer l’ordre de passage, le minutage et les transitions", "L’Élève 4 valide la formulation de la thèse"],
     "livrable": "G4_Synthese_E5_V1 et conducteur de l’oral", "validation": "Elle répond à C4, cite A, B et C et tient dans le temps imparti.",
     "debloque": ["CP2"]},
    {"code": "S13", "titre": "Support visuel (si exigé)", "j": (8, 8), "h": {2: 1.0, 3: 1.0, 5: 1.0},
     "niveau": "HYPO", "critique": False, "prereq": ["S11"],
     "actions": ["Uniquement si le professeur le demande", "Chronologie visuelle + 1 diapositive par partie", "L’Élève 5 assemble le support et l’intègre au conducteur"],
     "livrable": "G4_Support_E5_V1", "validation": "Lisible du fond de la salle ; aucun texte long.",
     "debloque": ["CP2"]},
    {"code": "S14", "titre": "Répétition de la scénette", "j": (8, 8), "h": {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.5},
     "niveau": "RECO", "critique": False, "partie_d": True, "prereq": ["S09"],
     "actions": ["Lecture à la table, puis mise en place", "Chronométrer", "Noter les coupes nécessaires"],
     "livrable": "Script V3 annoté", "validation": "La scène est jouée en entier sans texte en main pour les répliques clés.",
     "debloque": ["CP2"]},
    {"code": "CP2", "titre": "Point de contrôle 2 : répétition générale", "j": (9, 9), "h": {1: 1.5, 2: 1.5, 3: 1.5, 4: 1.5, 5: 1.5},
     "niveau": "RECO", "critique": True, "prereq": ["S12"], "checkpoint": True,
     "actions": ["Oral complet, dans l’ordre, chronométré", "Un élève note les écarts de temps", "Débriefing de 10 min"],
     "livrable": "Fiche de répétition (temps réel par partie)", "validation": "L’oral entier tient dans le temps imparti à ±10 %, sans trou ni doublon.",
     "debloque": ["S15"]},
    {"code": "S15", "titre": "Contrôle final et tampon", "j": (10, 10), "h": {1: 1.0, 4: 0.5, 5: 1.0},
     "niveau": "RECO", "critique": True, "prereq": ["CP2"],
     "actions": ["Convertir les pages dans l’édition de la classe (Élève 1)", "Vérifier la cohérence de fond (Élève 4)", "Cocher la checklist finale et imprimer (Élève 5)"],
     "livrable": "Checklist finale cochée", "validation": "Toutes les cases sont cochées et le dossier est imprimé ou envoyé.",
     "debloque": ["JJ"]},
    {"code": "JJ", "titre": "Jour J : présentation", "j": (11, 11), "h": {},
     "niveau": "EXIGE", "critique": True, "prereq": ["S15"],
     "actions": ["Arriver 15 min en avance", "Conducteur de l’oral en main"],
     "livrable": "Présentation orale (scénette : selon la décision sur la partie D)", "validation": "—", "debloque": []},
]

# Partie D (scénette) mise en attente par le groupe. Passer à False pour la réactiver :
# les étapes marquées "partie_d" reviennent alors dans le calendrier, le Gantt et le Kanban.
PARTIE_D_EN_ATTENTE = True
ATTENTE_D = {
    "statut": "La partie D (scénette) est en attente : le groupe a reporté la décision.",
    "exige": "Elle reste exigée par la consigne. La mettre en attente ne la rend pas facultative.",
    "reprise": "Jour 6",
    "pourquoi": "Choisir l’épisode, écrire le script et répéter demandent environ 3 jours. Au-delà du jour 6, la scénette ne peut plus être prête pour la répétition générale (CP2, jour 9).",
    "pret": "Ce qui est déjà prêt pour la reprise : les trois épisodes candidats analysés et notés (section 5), avec leurs citations vérifiées, et la grille de choix.",
}

CHEMIN_CRITIQUE = ["S01", "S02", "S04", "CP1", "S06/S07/S08", "S10", "S11", "S12", "CP2", "S15", "JJ"]

CHECKPOINTS = {
    "CP1": {"quand": "Jour 3, réunion de 30 min",
            "reussite": "Corpus de 25 citations ou plus, 12 étapes couvertes, 3 axes représentés, accord des 5 élèves.",
            "echec": [
                "Si le corpus compte moins de 20 citations ou qu’une étape n’en a aucune, les analyses démarrent quand même sur la partie validée.",
                "Chaque analyste complète lui-même 5 citations pour son angle avant le jour 4 à midi ; l’Élève 1 les vérifie le soir.",
                "Le choix de l’épisode (S05) se limite aux étapes déjà couvertes.",
                "Si le désaccord porte sur l’interprétation, on tranche par le texte, puis par vote majoritaire.",
            ]},
    "CP2": {"quand": "Jour 9, répétition générale de 1 h 30",
            "reussite": "Oral complet à ±10 % du temps imparti, transitions fluides.",
            "echec": [
                "En cas de dépassement de plus de 10 %, appliquer les coupes déjà marquées dans le script et la synthèse (jamais dans la réponse à C4).",
                "Si une partie est faible, son auteur la corrige le jour 10 au matin ; seconde répétition partielle le jour 10 à 17 h.",
                "Si un élève est absent, sa doublure prend le relais (voir tableau des doublures) ; la répétition a lieu quand même.",
                "Si la partie D a été reprise, la scénette est intégrée à cette répétition ; si elle n’est pas prête, on bascule sur l’épisode le plus simple (EP-A).",
            ]},
}

BUDGET_ORAL = {  # HYPOTHÈSE : durée totale inconnue — 15 min retenues par défaut
    "total": "15 min",
    "lignes": [
        ("Introduction : problématique et repères du roman", 5, "1 min"),
        ("A. Analyse linguistique", 2, "2 min 30"),
        ("B. Analyse stylistique", 3, "2 min 30"),
        ("C. Analyse thématique", 4, "3 min"),
        ("D. Scénette (en attente)", 5, "3 à 4 min réservées"),
        ("Synthèse orale : réponse à C4", 5, "2 min"),
    ],
    "note": "Une introduction rapide, la chronologie projetée (ou au tableau) par l’Élève 1, puis A, B, C, la scénette en point d’orgue et la synthèse pour conclure. Les durées sont à ajuster dès que le professeur donne le temps imparti.",
}

DOUBLURES = [(1, 4), (2, 3), (3, 2), (4, 1), (5, 2)]  # (titulaire, doublure) : la doublure connaît la partie

# ---------------------------------------------------------------------------
# Sections F, G, H (améliorées)
# ---------------------------------------------------------------------------
ORGANISATION = {
    "outils": [
        ("Dossier partagé", "Un dossier « G4_Chraibi » avec 4 sous-dossiers : 1_Corpus, 2_Fiches, 3_Scenette, 4_Oral. Les versions finales vont dans 4_Oral."),
        ("Messagerie", "Un groupe réservé au projet. Un message = un sujet ; pas de vocal pour une décision (il ne laisse pas de trace écrite)."),
        ("Tableau de suivi", "Le Kanban (G4_Tableau_Suivi) : chaque élève déplace lui-même ses cartes."),
    ],
    "nommage": "G4_[Partie]_E[n]_V[n], par exemple G4_Corpus_E1_V2 ou G4_FicheB_E3_V1. Pas d’accents ni d’espaces. On incrémente V à chaque envoi.",
    "rythme": [
        ("Comptes rendus écrits", "Jours 2, 4, 6 et 8 avant 20 h, selon le modèle (5 lignes suffisent)."),
        ("Réunions", "Deux seulement : CP1 (jour 3, 30 min) et CP2 (jour 9, 1 h 30). Le reste se fait par écrit."),
        ("Échéances", "Toute échéance tombe à 18 h le jour indiqué."),
        ("Délai de réponse", "Moins de 12 h pour une question bloquante."),
    ],
    "regles": [
        ("Doublons", "Une citation n’est analysée qu’une fois par angle. Le corpus indique qui l’utilise (colonne « utilisée par »)."),
        ("Retard", "On prévient au moins 24 h avant l’échéance ; la doublure aide en priorité."),
        ("Désaccord", "On tranche par le texte, puis par vote majoritaire. L’Élève 4 tranche sur le fond (interprétation), l’Élève 5 sur la forme (temps, ordre)."),
        ("Citations", "Toujours recopiées du corpus, jamais de mémoire, avec chapitre et page."),
    ],
    "compte_rendu": ["Élève :", "Date :", "Tâches terminées :", "Travail en cours :", "Prochaines actions :", "Difficultés rencontrées :", "Aide nécessaire (de qui ?) :", "Date prévue de livraison :"],
}

RISQUES = [
    # (risque, cause, conséquence, proba, impact, prévention, correction, propriétaire, nouveau?)
    ("Corpus en retard", "Relecture longue du roman", "Analyses bloquées", "Moyenne", "Fort", "Livraison en deux lots (J2, J3) et repérages S03", "Plan de repli de CP1 : chaque analyste complète 5 citations", 1, False),
    ("Chevauchement A / B", "Frontière floue entre lexique et procédés", "Répétitions à l’oral", "Forte", "Moyen", "Règles de frontière n° 1 et n° 2", "Fusion lors de la relecture croisée S11", 3, False),
    ("Scénette hors sujet", "Épisode choisi parce qu’il est « drôle », pas parce qu’il transforme", "Partie D non conforme", "Faible", "Fort", "Grille en 3 temps imposée (S05)", "Bascule sur l’épisode de repli avant S14", 5, False),
    ("Partie D reprise trop tard", "Décision sur la scénette reportée", "Partie exigée absente ou bâclée", "Moyenne", "Fort", "Date limite de décision : jour 6 ; épisodes déjà analysés", "Reprendre avec l’épisode le plus simple (EP-A)", 5, True),
    ("Citations inexactes", "Citations de mémoire", "Perte de crédibilité", "Moyenne", "Fort", "Toute citation vient du corpus", "Vérification S10 aux jours 6-7", 1, False),
    ("Analyse trop narrative", "On raconte au lieu d’analyser", "Analyse superficielle", "Forte", "Fort", "Règle relevé → analyse → effet", "Réécriture en S11", 4, False),
    ("Contradictions entre parties", "Rédaction en parallèle", "Discours incohérent", "Moyenne", "Moyen", "La thèse C4 est envoyée au jour 5 à tous", "Arbitrage par l’Élève 4 (fond)", 4, False),
    ("Dépassement du temps", "Scénette ou synthèse trop longues", "Pénalité ou coupure", "Forte", "Moyen", "Budget de l’oral et coupes marquées à l’avance", "Plan de repli de CP2", 5, False),
    ("Élève absent le Jour J", "Imprévu", "Partie ou rôle manquant", "Faible", "Fort", "Doublures désignées", "La doublure prend le relais", 5, False),
    ("Pagination fausse", "Pages du PDF ≠ édition papier", "Références introuvables pour le professeur", "Forte", "Moyen", "Citer partie-chapitre + page PDF", "Conversion des pages en S15", 1, True),
    ("Confusion des narrateurs", "Deux narrateurs différents (cadet en I, Nagib en II)", "Erreurs en B3 et sur l’énonciation", "Moyenne", "Moyen", "Repère affiché dans tous les dossiers", "Correction en S11", 2, True),
    ("Synthèse qui répète", "La synthèse refait l’analyse", "Conclusion longue et faible", "Moyenne", "Moyen", "Plan imposé : thèse + 1 apport A/B/C", "Coupes à CP2", 5, True),
    ("« Le passage » mal compris", "Consigne ambiguë (B2)", "Hors sujet partiel en B", "Moyenne", "Moyen", "Question posée au professeur au jour 1", "Recentrer B2 sur l’extrait indiqué", 3, True),
    ("Surcharge de l’Élève 1 en début de projet", "Corpus et chronologie aux jours 1-3", "Retard en chaîne", "Moyenne", "Fort", "Repérages S03 par les Élèves 2 à 4", "La doublure (Élève 4) prend un chapitre", 1, True),
]

CHECKLIST_FINALE = [
    ("EXIGE", "Les parties A, B, C, D et la synthèse orale sont présentes."),
    ("EXIGE", "Chaque question A1 à C4 a une réponse appuyée sur au moins une citation."),
    ("EXIGE", "La scénette montre une situation initiale, un changement et une conséquence identifiables (partie D : en attente, décision au jour 6)."),
    ("EXIGE", "La synthèse répond clairement à C4 (savoir ou identité ?)."),
    ("RECO", "Toutes les citations sont exactes et référencées (partie-chapitre + page de l’édition de la classe)."),
    ("RECO", "Aucun doublon ni contradiction entre A, B et C."),
    ("RECO", "Les trois axes de la consigne sont couverts."),
    ("RECO", "L’énonciation, les connecteurs et les enjeux sociaux et philosophiques sont traités."),
    ("RECO", "L’oral complet a été répété et chronométré (CP2)."),
    ("RECO", "Chaque élève sait expliquer sa partie et celle de son binôme de doublure."),
    ("HYPO", "Le format et les durées respectent les précisions obtenues du professeur."),
    ("HYPO", "Le support visuel est prêt, si le professeur l’a demandé."),
]

ACTIONS_IMMEDIATES = [
    (5, "Jour 1, 12 h", "Créer le dossier partagé et le groupe ; y déposer la consigne, Roman.pdf, ce plan et les 5 dossiers."),
    (5, "Jour 1, 18 h", "Envoyer au professeur les questions de cadrage (liste ci-dessous)."),
    ("Tous", "Jour 1, 20 h", "Confirmer par écrit son rôle, les règles de frontière et sa doublure."),
    (1, "Jour 1", "Commencer la relecture de la partie I et la vérification de la chronologie de référence."),
    ("2, 3, 4", "Jour 2, 18 h", "Déposer 6 à 8 repérages (partie-chapitre + page) pour l’Élève 1."),
    (1, "Jour 2, 18 h", "Livrer le corpus lot 1 (partie I)."),
    ("Tous", "Jour 2, 20 h", "Envoyer le premier compte rendu écrit."),
    (5, "Jour 3, 12 h", "Livrer à l’Élève 1 le relevé des chapitres II-6 et II-7."),
    ("Tous", "Jour 3", "Réunion CP1 : valider le corpus."),
    (4, "Jour 5, 18 h", "Envoyer la thèse C4 en une phrase à l’Élève 5."),
]

QUESTIONS_PROF = [
    ("Œuvre et passage", "Travaille-t-on sur l’ensemble de La Civilisation, ma Mère !… ou sur un passage précis ? À quoi renvoie « le passage » dans la question B2 ?"),
    ("Date", "Quelle est la date de présentation ?"),
    ("Durées", "Quelle est la durée totale de l’oral, et celle de la scénette ?"),
    ("Livrables", "Faut-il rendre un document écrit ou un diaporama en plus de l’oral ?"),
    ("Scénette", "Tous les élèves doivent-ils jouer ? Peut-on adapter et couper le texte, ou faut-il le respecter à la lettre ?"),
    ("Édition", "Quelle édition sert de référence pour les numéros de page ?"),
    ("Évaluation", "Quels sont les critères d’évaluation et la note est-elle individuelle ou collective ?"),
]

HYPOTHESES = [
    "Le roman fourni est l’œuvre étudiée et on travaille sur l’ensemble du roman (pas seulement un extrait).",
    "Le travail se fait en 10 jours ouvrés plus le Jour J (J11), à raison de 1 à 2 h par jour et par élève.",
    "L’oral dure 15 min au total, dont 3 à 4 min de scénette.",
    "Tous les élèves ont déjà lu le roman une première fois ; cette lecture n’est pas comptée dans la charge.",
    "Le support visuel n’est pas exigé ; il est prévu en option (S13).",
    "Les pages citées sont celles de Roman.pdf ; elles devront être converties dans l’édition de la classe.",
    "La correspondance parties A-D ↔ élèves est déduite des intitulés de rôle.",
]

# ---------------------------------------------------------------------------
# Phase 4 : dossiers individuels
# ---------------------------------------------------------------------------
MEMBRES = {
    1: {
        "mission": [
            "Tu construis la base de preuves de tout le groupe : la chronologie de la transformation en 12 étapes et un corpus de 25 à 35 citations exactes et référencées.",
            "Tu classes chaque citation par étape et par axe de la consigne, puis tu vérifies toutes les citations utilisées par les autres.",
            "En fin de projet, tu convertis les pages dans l’édition de la classe.",
        ],
        "pourquoi": "Sans preuve, une analyse n’est qu’une opinion. Chaque fiche, la scénette et la synthèse reposent sur ton corpus : une citation fausse décrédibilise tout le groupe.",
        "possede_axes": True,
        "possede": [],
        "frontieres": ["Tu dis QUOI et OÙ (étapes, chapitres, pages) ; tu n’analyses pas les temps ni les procédés (Élèves 2 et 3).", "Partie D (scénette) en attente : si elle reprend, tu fourniras à l’Élève 5 les citations de l’épisode choisi."],
        "entrees": [("Élève 5", "Fiche de cadrage, règles du corpus", "Jour 1"), ("Élèves 2, 3, 4", "Repérages (6 à 8 passages chacun)", "Jour 2, 18 h"), ("Élève 5", "Relevé des chapitres II-6 et II-7", "Jour 3, 12 h"), ("Élèves 2, 3, 4", "Fiches A, B, C V1 à vérifier", "Jour 6, 18 h")],
        "sorties": [("Élèves 2 à 5", "Corpus lot 1 (partie I) et chronologie V1", "Jour 2, 18 h"), ("Tous", "Corpus V2 complet (25 à 35 citations)", "Jour 3, avant CP1"), ("Élèves 2 à 5", "Rapport de vérification des citations", "Jour 7, 12 h"), ("Élève 5", "Vérification des citations de la synthèse", "Jour 8, 18 h"), ("Tous", "Pages converties dans l’édition de la classe", "Jour 10, 18 h")],
        "termine": ["La chronologie a 12 étapes, chacune avec au moins 1 citation.", "Le corpus contient 25 à 35 citations, recopiées mot à mot et numérotées.", "Chaque citation a : partie-chapitre, page, étape, axe.", "Les trois axes de la consigne sont représentés (au moins 6 citations chacun).", "Le rapport de vérification couvre 100 % des citations utilisées.", "Les pages sont converties dans l’édition de la classe.", "Tu peux expliquer la chronologie en 1 minute à l’oral."],
    },
    2: {
        "mission": [
            "Tu montres, mot à mot, COMMENT la langue du roman fait sentir la transformation de la mère.",
            "Tu réponds aux questions A1 à A3 et tu traites aussi l’énonciation et les connecteurs (ta « production attendue »).",
            "Tu fournis à l’Élève 5 l’idée clé de ta partie pour la synthèse orale.",
        ],
        "pourquoi": "La consigne parle de « changements de comportement et de langage ». C’est toi qui prouves que le changement est visible dans les mots eux-mêmes et pas seulement dans l’intrigue.",
        "possede": ["A1", "A2", "A3"],
        "frontieres": ["Lexique, verbes, temps, énonciation et connecteurs sont à toi ; les figures de style sont à l’Élève 3 (règles 1 et 2).", "Tu repères les marques de l’énonciation ; l’Élève 3 interprète le regard du narrateur.", "Tu analyses COMMENT les temps rendent la progression ; l’Élève 1 établit la chronologie."],
        "entrees": [("Élève 1", "Corpus V2 validé", "Jour 3 (CP1)"), ("Élève 4", "Thèse C4 en une phrase", "Jour 5, 18 h"), ("Élève 4", "Relecture de ta fiche A", "Jour 7")],
        "sorties": [("Élève 1", "Repérages (6 à 8 passages)", "Jour 2, 18 h"), ("Élève 1", "Fiche A V1 pour vérification", "Jour 6, 18 h"), ("Élève 3", "Relecture de la fiche B", "Jour 7, 18 h"), ("Élève 5", "Fiche A V2 (une idée clé pour la synthèse)", "Jour 8, 12 h")],
        "termine": ["A1, A2 et A3 ont chacune au moins 3 relevés analysés.", "Chaque relevé suit relevé → analyse → effet.", "L’énonciation est traitée et les deux narrateurs (I et II) sont distingués.", "Au moins 3 connecteurs ou indicateurs sont analysés.", "Toutes les citations viennent du corpus (n° indiqué).", "La fiche tient sur 1 à 2 pages et tu peux la présenter en 2 min 30.", "Tu as relu la fiche B et transmis tes remarques."],
    },
    3: {
        "mission": [
            "Tu montres par quels procédés d’écriture la transformation de la mère devient visible et quel effet ils produisent.",
            "Tu réponds aux questions B1 à B3 : procédés, humour, ironie et décalage, regard du narrateur.",
            "Tu fournis à l’Élève 5 l’idée clé de ta partie pour la synthèse orale.",
        ],
        "pourquoi": "Le roman est souvent drôle, et ce rire n’est pas gratuit. Tu expliques ce qu’il fait voir de la mère et des personnages : c’est ce qui distingue une analyse d’un résumé.",
        "possede": ["B1", "B2", "B3"],
        "frontieres": ["Les figures et leurs effets sont à toi ; les champs lexicaux et les temps sont à l’Élève 2.", "Tu interprètes le regard du narrateur ; l’Élève 2 en repère les marques.", "Partie D en attente : si elle reprend, tu conseilleras l’Élève 5 sur les ressorts comiques, sans écrire le script."],
        "entrees": [("Élève 1", "Corpus V2 validé", "Jour 3 (CP1)"), ("Élève 4", "Thèse C4 en une phrase", "Jour 5, 18 h"), ("Élève 2", "Relecture de ta fiche B", "Jour 7"), ("Professeur (via Élève 5)", "Sens de « le passage » (B2)", "Dès que possible")],
        "sorties": [("Élève 1", "Repérages (6 à 8 passages)", "Jour 2, 18 h"), ("Élève 1", "Fiche B V1 pour vérification", "Jour 6, 18 h"), ("Élève 4", "Relecture de la fiche C", "Jour 7, 18 h"), ("Élève 5", "Fiche B V2 (une idée clé pour la synthèse)", "Jour 8, 12 h")],
        "termine": ["B1 à B3 ont chacune au moins 3 procédés nommés, cités et commentés.", "Chaque procédé est suivi de son effet (pas seulement de son nom).", "Humour, ironie et décalage sont distingués en B2.", "Le regard des deux narrateurs est comparé en B3.", "Toutes les citations viennent du corpus.", "La fiche tient sur 1 à 2 pages ; présentation en 2 min 30.", "Tu as relu la fiche C et transmis tes remarques."],
    },
    4: {
        "mission": [
            "Tu interprètes la transformation : étapes, obstacles, effets sur la famille, enjeux sociaux et philosophiques.",
            "Tu réponds aux questions C1 à C4 et tu formules la thèse du groupe sur C4 : savoir ou identité ?",
            "Tu es le garant de la cohérence de fond entre les parties.",
        ],
        "pourquoi": "C4 est la question à laquelle tout l’oral doit répondre. Ta thèse devient la conclusion du groupe : elle doit être claire, prouvée et nuancée.",
        "possede": ["C1", "C2", "C3", "C4"],
        "frontieres": ["Tu interprètes ; tu reprends les résultats des Élèves 2 et 3 sans refaire leurs analyses.", "Tu formules la thèse ; l’Élève 5 la présente sans la réécrire.", "Tu tranches les désaccords de fond ; l’Élève 5 tranche la forme (temps, ordre)."],
        "entrees": [("Élève 1", "Corpus V2 validé et chronologie", "Jour 3 (CP1)"), ("Élève 3", "Relecture de ta fiche C", "Jour 7"), ("Élève 5", "Projet de synthèse à valider", "Jour 8")],
        "sorties": [("Élève 1", "Repérages (6 à 8 passages)", "Jour 2, 18 h"), ("Tous", "Thèse C4 en une phrase", "Jour 5, 18 h"), ("Élève 1", "Fiche C V1 pour vérification", "Jour 6, 18 h"), ("Élève 2", "Relecture de la fiche A", "Jour 7, 18 h"), ("Élève 5", "Validation de la thèse dans la synthèse", "Jour 8, 18 h"), ("Tous", "Contrôle de cohérence final", "Jour 10")],
        "termine": ["C1 à C4 ont chacune une idée directrice et au moins 2 preuves du corpus.", "C2 distingue obstacles extérieurs et contradictions intérieures.", "C3 montre l’évolution d’au moins 2 relations (père, fils).", "La thèse C4 tient en une phrase et a été envoyée au jour 5.", "Les enjeux sociaux et philosophiques sont nommés.", "La fiche tient sur 2 pages ; présentation en 3 min.", "Tu as relu la fiche A et contrôlé la cohérence finale."],
    },
    5: {
        "mission": [
            "Tu rédiges et présentes la synthèse orale qui relie A, B et C et donne la réponse du groupe à C4, avec l’introduction et les transitions.",
            "Tu coordonnes le calendrier, le tableau de suivi et le conducteur de l’oral, et tu aides l’Élève 1 sur le corpus de la partie II.",
            "La partie D (scénette) est en attente : tu la tiens prête à redémarrer et tu fais trancher le groupe au plus tard au jour 6.",
        ],
        "pourquoi": "Tu produis la conclusion que le public retient : la réponse du groupe. Tu fais de cinq travaux un seul exposé, et tu es le garant de la partie D, que la consigne exige toujours.",
        "possede": ["D"],
        "frontieres": ["Partie D en attente : tu ne lances ni le choix de l’épisode ni le script avant la décision du groupe.", "Tu présentes la thèse C4 de l’Élève 4 sans la réécrire.", "Tu tranches la forme (temps, ordre de passage) ; l’Élève 4 tranche le fond."],
        "entrees": [("Élève 1", "Consignes de relevé pour II-6 et II-7", "Jour 2"), ("Élève 1", "Corpus validé", "Jour 3 (CP1)"), ("Élève 4", "Thèse C4 en une phrase", "Jour 5, 18 h"), ("Élèves 2, 3, 4", "Fiches V2 (une idée clé chacune)", "Jour 8, 12 h"), ("Élève 1", "Vérification des citations de la synthèse", "Jour 8, 18 h")],
        "sorties": [("Tous", "Fiche de cadrage, dossier partagé, questions au professeur", "Jour 1"), ("Élève 1", "Relevé des chapitres II-6 et II-7", "Jour 3, 12 h"), ("Tous", "Décision sur la partie D (reprise ou report)", "Jour 6"), ("Tous", "Synthèse, introduction et conducteur de l’oral", "Jour 8, 18 h"), ("Tous", "Répétition générale CP2", "Jour 9"), ("Tous", "Checklist finale cochée", "Jour 10")],
        "termine": ["Le relevé des chapitres II-6 et II-7 est livré et vérifié par l’Élève 1.", "La synthèse cite au moins un apport de A, de B et de C et répond à C4.", "L’introduction et les phrases de transition sont écrites.", "Le conducteur indique l’ordre, le minutage et les transitions.", "La répétition générale (CP2) a eu lieu et l’oral tient dans le temps.", "La décision sur la partie D est prise et notée (jour 6 au plus tard).", "La checklist finale est cochée."],
    },
}

FICHE_METHODE = {
    1: {
        "titre": "Construire un tableau de citations référencées",
        "etapes": [
            "Recopie la citation mot à mot depuis le texte, jamais de mémoire. Garde la ponctuation et les guillemets d’origine.",
            "Coupe avec « […] » ; si tu modifies un mot pour l’accord, mets-le entre crochets [ ].",
            "Note la référence au format « II-3, p. 85 » (partie-chapitre, page PDF), puis ajoute la page de l’édition de la classe au jour 10.",
            "Rattache la citation à UNE étape (1 à 12) et à UN axe (AX1, AX2, AX3). Si tu hésites, choisis l’axe principal.",
            "Laisse la colonne « utilisée par » vide : chaque analyste y inscrit son code (E2, E3…) au point de contrôle CP1.",
            "Vise des citations courtes (1 à 2 lignes) : elles se lisent mieux à l’oral et se vérifient plus vite.",
        ],
        "colonnes": ["N°", "Citation (mot à mot)", "Partie-ch. / page", "Étape", "Axe", "Utilisée par"],
        "lignes": 12,
        "verif_colonnes": ["N°", "Utilisée dans (fiche, ligne)", "Conforme ?", "Correction apportée"],
    },
    2: {
        "titre": "Grille d’analyse linguistique : relevé → analyse → effet",
        "rubriques": [
            ("Champs lexicaux (A1)", "Regroupe les mots d’un même thème : découverte, savoir, enfermement, liberté… Compare leur présence en partie I et en partie II."),
            ("Verbes d’action (A2)", "Qui est le sujet des verbes : la mère, ou les autres qui agissent sur elle ? Observe comment cela évolue d’une étape à l’autre. Regarde aussi la voix (active, passive) et la modalité (pouvoir, vouloir, devoir)."),
            ("Temps verbaux (A3)", "Repère les temps dominants dans chaque partie (imparfait, passé simple, passé composé, présent). Quand change-t-on de temps, et à quoi sert chaque temps ?"),
            ("Indicateurs temporels (A3)", "Relève les expressions de temps (dates, durées, adverbes comme désormais ou à présent). Que disent-elles du rythme du changement : lent, brutal, par paliers ?"),
            ("Énonciation", "Qui raconte ? Le cadet en partie I, Nagib en partie II. Repère aussi le discours direct ou rapporté et la place de la parole de la mère."),
            ("Connecteurs", "Relève les connecteurs logiques et temporels (opposition, conséquence, succession). Comment articulent-ils les étapes ?"),
        ],
        "colonnes": ["Relevé (citation + n° du corpus)", "Analyse (ce que l’on observe)", "Effet (ce que cela montre de la transformation)"],
        "lignes_par_rubrique": 2,
    },
    3: {
        "titre": "Procédés d’écriture : procédé → citation → effet",
        "procedes": [
            ("Comparaison / métaphore", "Rapproche la mère d’une autre réalité (animal, arbre, enfant…)."),
            ("Gradation", "Une suite de termes d’intensité croissante."),
            ("Antithèse", "L’opposition de deux idées (prison / liberté, avant / maintenant)."),
            ("Hyperbole", "Une exagération, souvent comique."),
            ("Énumération / accumulation", "Une liste qui crée un effet d’abondance ou de vitesse."),
            ("Anaphore / répétition", "La reprise d’un mot ou d’une formule en début de phrase."),
            ("Ironie", "Dire le contraire de ce que l’on pense, ou laisser entendre un jugement."),
            ("Décalage", "Un écart entre la situation et la réaction (comique de situation ou de langage)."),
            ("Personnification", "Donner vie aux objets (radio, brasero, machine à coudre…)."),
            ("Point de vue / focalisation", "Ce que le narrateur voit, sait et choisit de montrer."),
            ("Discours rapporté", "Direct, indirect ou indirect libre : qui a la parole ?"),
            ("Symbole", "Un objet ou un geste qui porte un sens au-delà de lui-même."),
        ],
        "colonnes": ["Procédé", "Citation (n° du corpus)", "Effet produit"],
        "b2": ["Humour (rire bienveillant)", "Ironie (jugement implicite)", "Décalage (écart situation / réaction)"],
        "b3": ["Narrateur de la partie I (le cadet)", "Narrateur de la partie II (Nagib)"],
    },
    4: {
        "titre": "Structure d’une réponse argumentée (C1 à C4)",
        "structure": [
            ("Idée directrice", "Une phrase qui répond directement à la question."),
            ("Argument 1 + preuve", "Une idée et une citation du corpus (n°), puis ce qu’elle montre."),
            ("Argument 2 + preuve", "Une deuxième idée avec une autre étape du roman, de préférence dans l’autre partie."),
            ("Nuance / limite", "Ce qui résiste, contredit ou complique l’idée."),
            ("Mini-conclusion", "Une phrase qui prépare la question suivante."),
        ],
        "c1_colonnes": ["Étape (n°)", "Ce que la mère gagne", "Ce qu’elle perd ou risque", "Obstacle rencontré"],
        "c4_positions": [
            ("Savoir", "Elle cherche surtout à apprendre : lire, comprendre le monde."),
            ("Identité", "Le savoir n’est qu’un moyen : elle cherche à exister par elle-même."),
            ("Les deux, liés", "Le savoir est l’instrument d’une conquête d’identité, qui se prolonge en action pour les autres."),
        ],
        "enjeux": ["Condition des femmes", "Tradition et modernité (« civilisation »)", "Colonisation et indépendance", "Liberté et solitude", "Être et avoir (titres des deux parties)"],
    },
    5: {
        "titre": "Synthèse orale et conducteur (partie D en attente)",
        "script_entete": ["Épisode retenu", "Référence (partie-chapitre, pages)", "Durée cible", "Rôles et interprètes", "Accessoires", "Coupes prévues si dépassement"],
        "temps": [
            ("Temps 1 : situation initiale", "Montrer la mère « avant » : gestes, langage, place dans la maison."),
            ("Temps 2 : changement", "Le moment où quelque chose bascule : une parole, un acte, une décision."),
            ("Temps 3 : conséquence", "Ce qui a changé de façon visible et durable ; le public doit pouvoir le nommer."),
        ],
        "temps_colonnes": ["Durée", "Didascalies (déplacements, ton, gestes)", "Répliques (citation n° ou adaptation)"],
        "repetitions": [
            ("R1 : lecture à la table", "Jour 6 ou 7, 30 min", "Chacun lit son rôle ; on chronomètre ; on repère les passages trop longs."),
            ("R2 : mise en place (S14)", "Jour 8, 1 h", "Déplacements, accessoires, entrées et sorties ; répliques clés sues par cœur."),
            ("R3 : générale (CP2)", "Jour 9, 1 h 30", "Oral complet dans l’ordre, chronométré, sans interruption ; débriefing de 10 min."),
        ],
        "synthese": [
            ("Accroche", "Une image forte du roman (objet, geste, phrase)."),
            ("Rappel de la question", "La problématique centrale, en une phrase."),
            ("Apport de A", "Une idée clé de l’Élève 2 (comment la langue montre le changement)."),
            ("Apport de B", "Une idée clé de l’Élève 3 (ce que l’écriture fait voir)."),
            ("Apport de C", "Une idée clé de l’Élève 4 (le sens de l’émancipation)."),
            ("Réponse à C4", "La thèse de l’Élève 4, telle quelle."),
            ("Ouverture", "Un lien avec aujourd’hui ou avec une autre œuvre."),
        ],
    },
}

REGLES_COMMUNES = [
    ("Nommage", ORGANISATION["nommage"]),
    ("Échéances", "Toujours à 18 h le jour indiqué. En cas de retard, prévenir au moins 24 h avant ; ta doublure aide en priorité."),
    ("Comptes rendus", "Jours 2, 4, 6 et 8 avant 20 h, avec le modèle (page suivante)."),
    ("Citations", "Toujours recopiées du corpus (avec son n°), jamais de mémoire."),
    ("Désaccord", "On tranche par le texte, puis par vote. Le fond revient à l’Élève 4, la forme à l’Élève 5."),
    ("Tableau de suivi", "Déplace toi-même tes cartes : À faire → En cours → À vérifier → Terminé."),
]
