# -*- coding: utf-8 -*-
"""Réponses rédigées, par élève (partie D en attente : non traitée).

Dans les textes, [[id]] insère la citation id de CORPUS ; build.py la vérifie mot à mot
dans Roman.pdf, calcule sa page, son chapitre, son étape et son numéro de corpus.
"""

# id -> (texte exact, axe)
CORPUS = {
    "paien": ("Et fais-moi le plaisir d’enlever ces vêtements de païen !", "AX2"),
    "revenais": ("Je revenais de l’école, jetais mon cartable dans le vestibule", "AX2"),
    "personne": ("Personne ne lui avait rien appris depuis qu’elle était venue au monde.", "AX1"),
    "bibliotheque": ("Je l’ai là, devant moi, dans ma bibliothèque vitrée.", "AX2"),
    "arbre": ("Elle était un arbre, cerclé dans une cour de prison, mais que le moindre souffle de printemps pouvait faire bourgeonner et fleurir avec luxuriance.", "AX2"),
    "soleil": ("j’ai assisté à un lever de soleil sur sa solitude quotidienne et profonde", "AX3"),
    "fakirs": ("Ah bon ! a dit ma mère, soulagée et joyeuse tout à coup. Comme les fakirs et les charmeurs de serpents ?", "AX1"),
    "magicien": ("Il est là !… Le magicien est venu !", "AX1"),
    "lumiere": ("et la lumière fut dans la chambre, le soleil sur son visage.", "AX1"),
    "bonsoir": ("Bonsoir, monsieur le magicien, lui répondit ma mère.", "AX2"),
    "ainsi": ("C’est ainsi que le « magicien » s’installa dans la maison", "AX1"),
    "tombeau": ("Elle était là, dans cette maison-tombeau, apprenant la vie.", "AX1"),
    "assoiffee": ("assoiffée d’eau, assoiffée de liberté et de vérité", "AX1"),
    "objets": ("Moderniste d’objets, non d’idées.", "AX3"),
    "juger": ("C’est un crime de juger, je le sais. Mais déjà je jugeais.", "AX3"),
    "instinct": ("L’instinct vainquit la science, le primitif rendit des points à la civilisation métallurgique.", "AX1"),
    "europeens": ("Ces Européens sont malins, ma foi, oui.", "AX2"),
    "meryem": ("Allô, Meryem ? Tu as changé de voix…", "AX2"),
    "reseau": ("Sans quitter sa maison, elle avait établi un réseau inextricable de liens", "AX3"),
    "habillames": ("Nous réveillâmes maman, lui préparâmes son petit déjeuner, la coiffâmes, l’habillâmes, la chaussâmes.", "AX2"),
    "entrainames": ("Nous l’entraînâmes le long du vestibule.", "AX2"),
    "votrepere": ("Mais que va dire votre père ?", "AX3"),
    "fumes": ("Nous ouvrîmes la porte et fûmes dehors d’un bond", "AX2"),
    "monde": ("Ce monde est à toi aussi.", "AX1"),
    "loi": ("n’avait fait qu’appliquer la loi. Religieusement.", "AX3"),
    "seuil": ("Jamais elle n’en avait franchi le seuil.", "AX2"),
    "tache": ("une tache verte, imprimée par l’herbe où elle s’était assise.", "AX2"),
    "secret": ("C’était son premier secret.", "AX3"),
    "immobile": ("Un être libre est un être immobile comme un arbre, ma foi oui…", "AX1"),
    "lendemain": ("Dès le lendemain matin, elle téléphona à sa cousine.", "AX3"),
    "bruler": ("Il fallait brûler les étapes.", "AX1"),
    "deluge": ("Alors, brusquement et tous ensemble, le monde extérieur et la violence de la liberté s’étaient abattus devant et sur elle comme un déluge d’équinoxe", "AX1"),
    "etre": ("Elle ne cherchait pas à savoir mais à comprendre, à être et non à avoir ou posséder.", "AX1"),
    "mots": ("Non, non, je n’ai pas trouvé de mots humains pour répondre à cet être humain qui était ma mère", "AX3"),
    "avidite": ("Elle apprenait avec avidité", "AX1"),
    "corps": ("Je lui appris son corps.", "AX1"),
    "mollusque": ("Un mollusque sort de sa coquille au cours de sa mutation. Pourquoi pas elle ?", "AX1"),
    "jourapres": ("Jour après jour, je l’amenais à remettre en cause son propre passé.", "AX1"),
    "importaient": ("Peu m’importaient les conséquences : je l’aimais.", "AX3"),
    "maitres": ("Mais pourquoi sont-ils nos maîtres ? Ici ? Chez nous ?", "AX3"),
    "nid": ("Petit à petit le nid fait son oiseau, lui dit Nagib.", "AX1"),
    "naitre": ("Et nous la voyions naître.", "AX1"),
    "decouvrit": ("Elle nous découvrit, nous. Ses enfants.", "AX3"),
    "vit": ("Elle se vit, elle – existante, toute nue dans un monde nu.", "AX1"),
    "vieille": ("Je suis vieille, vieille !", "AX2"),
    "falaise": ("Nous sommes assis en haut de la falaise, sous l’ombre d’un cèdre hérissé.", "AX3"),
    "poignante": ("La liberté est poignante, dit-elle à mi-voix. Elle fait parfois souffrir.", "AX3"),
    "solitude": ("Elle ne résout pas le problème de la solitude.", "AX3"),
    "prison": ("je me demande si vous avez bien fait, Nagib et toi, d’ouvrir la porte de ma prison.", "AX3"),
    "maintenant": ("Je ne me posais pas de questions, je ne savais pas qui j’étais. Tandis que maintenant !…", "AX2"),
    "parti": ("Donc, tu es parti et elle a tourné en rond.", "AX3"),
    "interprete": ("Je me fais l’interprète de maman", "AX3"),
    "debout": ("Debout ! Direction : sud-sud-est ! Au marché ! Debout, fainéant !", "AX2"),
    "telephona": ("Elle a téléphoné à Meknès, Fès, Marrakech, Rabat, Tanger.", "AX2"),
    "professeur": ("C’était un professeur acharné", "AX3"),
    "telephone": ("Parfaitement. J’ai le téléphone.", "AX2"),
    "femmes": ("Dis-lui qu’il n’y a pas que les hommes sur la terre. Il y a également les femmes et on ne nous a pas consultées.", "AX3"),
    "connaissais": ("Je ne connaissais plus ma mère.", "AX3"),
    "tete": ("Elle tint tête à mon père.", "AX3"),
    "langage": ("Depuis quelque temps, tu as adopté un langage bizarre, un comportement insolite.", "AX2"),
    "paye": ("Tu m’as toujours tout payé.", "AX3"),
    "peux": ("Peut-être, mais je peux le faire. Je peux tout faire.", "AX2"),
    "treize": ("Quand je t’ai épousée, tu avais treize ans.", "AX3"),
    "ame": ("Dis ? mon âme ? où est-elle ? qui est-elle ? que fait-elle ?", "AX2"),
    "trentesept": ("Me voici à l’âge de trente-sept ans – et je vais te dire : je ne sais rien.", "AX1"),
    "consciente": ("Je suis à présent consciente, entièrement responsable de ma vie, entends-tu ?", "AX2"),
    "tutelle": ("Je ne suis pas en train de me libérer de la tutelle de ton père pour venir te demander ta protection, tout grand gaillard que tu es.", "AX3"),
    "poils": ("Mais, m’man, ce n’est pas une peau de bête. Ce sont mes poils.", "AX3"),
    "paix": ("Paix à vous tous, vieux compagnons d’enfance et de jeunesse, au nom de l’avenir qui commence !", "AX2"),
    "peint": ("Elle a peint toute la maison. Elle-même.", "AX2"),
    "moi": ("un mot était brodé : « MOI. »", "AX2"),
    "inscrite": ("Et elle s’est inscrite dans une école spéciale.", "AX1"),
    "tablier": ("C’est ainsi que j’ai ceint un tablier de cuisine – oui –", "AX3"),
    "soif": ("Elle avait une soif d’apprendre d’assoiffé en plein désert", "AX1"),
    "mahometans": ("Les Mahométans se font raser le crâne, à l’exception d’une frange médiane", "AX1"),
    "sang": ("Elle disait qu’elle n’apprenait pas pour apprendre ni même pour savoir. Mais pour nourrir et régénérer son sang.", "AX1"),
    "tolstoi": ("A la porte, Tolstoï !", "AX1"),
    "nouvelle": ("c’est comme si j’avais épousé une nouvelle femme, que je commence à connaître", "AX3"),
    "ruche": ("Maître d’œuvre de la ruche, ma mère fait écourter le repas, mobilise les femmes en groupes d’études", "AX3"),
    "pierres": ("On nous jeta des pierres, on creva les pneus de la voiture.", "AX3"),
    "actes": ("Mes idées, mes acquisitions, mes émotions, il faut que je les traduise en actes, pour moi et pour les autres.", "AX3"),
    "conscience": ("ta mère était, à elle seule, la conscience d’un monde inconscient.", "AX3"),
    "meleve": ("Quand elle entre maintenant dans cette maison, je me lève aussitôt", "AX3"),
    "locomotive": ("A l’heure de l’indépendance, ma mère était à bord de la locomotive", "AX3"),
    "examens": ("Ma mère a été reçue à tous ses examens – et même au permis de conduire.", "AX1"),
    "souvenir": ("En souvenir du passé, m’a-t-elle dit.", "AX2"),
    "horizon": ("j’ai besoin de faire reculer mon horizon", "AX1"),
}

# Chapitre -> étape de la chronologie (content.CHRONOLOGIE)
ETAPE_DE_CHAPITRE = {
    ("I", 1): 1, ("I", 2): 1, ("I", 3): 2, ("I", 4): 3, ("I", 5): 3, ("I", 6): 4, ("I", 7): 4,
    ("I", 8): 5, ("I", 9): 6, ("I", 10): 7, ("II", 1): 8, ("II", 2): 8, ("II", 3): 9,
    ("II", 4): 10, ("II", 5): 10, ("II", 6): 11, ("II", 7): 12,
}

# Blocs : ("p", texte) paragraphe · ("ul", [textes]) liste · ("cle", texte) idée clé · ("say", texte) texte à dire
REPONSES = {
    2: {
        "titre": "Analyse linguistique",
        "sections": [
            {"code": "A1", "blocs": [
                ("cle", "Le vocabulaire passe de l’enfermement et de la magie au vocabulaire de la naissance et du savoir."),
                ("ul", [
                    "**L’enfermement.** Au départ, la maison est décrite comme une prison et un tombeau : [[arbre]] ; [[tombeau]]. Le mot « prison » revient encore quand la mère fait le bilan : [[prison]]. La mère est d’abord définie par un espace clos.",
                    "**Le merveilleux.** Les premières découvertes techniques sont dites avec le vocabulaire des contes : magie, magicien, génie, fakirs. [[fakirs]] ; [[magicien]]. La technique moderne est traduite dans l’univers de la mère ; son savoir n’est pas encore rationnel.",
                    "**La naissance et l’éclosion.** Les apprentissages s’accompagnent des mots naître, nid, oiseau, coquille : [[nid]] ; [[naitre]] ; [[mollusque]]. Apprendre, c’est naître une seconde fois : la transformation est présentée comme vitale et naturelle.",
                    "**Le savoir scolaire.** En partie II, le lexique de l’école envahit le texte : école, cahiers, examens, soif d’apprendre. [[inscrite]] ; [[soif]] ; [[examens]]. Le merveilleux cède la place au savoir méthodique et reconnu.",
                ]),
                ("p", "**Bilan.** Le lexique de la soif relie les deux parties ([[assoiffee]]) : le besoin de savoir existait depuis toujours, il manquait seulement les moyens de le satisfaire."),
            ]},
            {"code": "A2", "blocs": [
                ("cle", "La mère passe du rôle de complément d’objet à celui de sujet des verbes d’action, puis à celui de personne qui donne des ordres."),
                ("ul", [
                    "**La mère objet (partie I).** Ce sont les fils qui agissent sur elle : [[habillames]]. Cinq verbes au passé simple, tous avec « nous » pour sujet et la mère en complément (la, lui). Même sa première sortie est subie : [[entrainames]].",
                    "**La transition.** Avec les apprentissages, la mère devient sujet, mais d’un verbe encore intérieur : [[avidite]].",
                    "**La mère sujet (partie II).** Elle est sujet de verbes concrets et publics : acheter, téléphoner, peindre, s’inscrire, mobiliser. [[telephona]] ; [[peint]] ; [[inscrite]] ; [[ruche]]. Dans la dernière citation, l’accumulation des verbes au présent (fait écourter, mobilise) montre qu’elle organise désormais les autres.",
                    "**L’impératif et la modalité.** Elle donne des ordres à son fils et affirme sa capacité avec le verbe pouvoir : [[debout]] ; [[peux]].",
                    "**L’action contre le père.** Une phrase brève, un sujet, un verbe d’opposition : [[tete]].",
                ]),
                ("p", "**Bilan.** Le renversement grammatical (objet → sujet → donneuse d’ordres) prouve que la mère devient « actrice de sa vie »."),
            ]},
            {"code": "A3", "blocs": [
                ("cle", "Les temps verbaux et les indicateurs temporels font passer d’un temps immobile à un temps qui s’accélère."),
                ("ul", [
                    "**L’imparfait d’habitude** installe la répétition de la vie d’avant : [[revenais]]. Chaque jour ressemble au précédent ; rien ne change.",
                    "**Le passé simple** marque les ruptures et les premières fois : [[lumiere]] ; [[fumes]]. Chaque découverte devient un événement unique.",
                    "**Le plus-que-parfait et la négation** mesurent tout ce qui a manqué avant : [[personne]] ; [[seuil]].",
                    "**Les indicateurs temporels** signalent l’accélération : [[lendemain]] ; [[bruler]] ; [[jourapres]]. Le rythme du changement devient de plus en plus rapide.",
                    "**L’opposition avant / maintenant** : [[maintenant]]. L’âge sert aussi de repère : 35 ans en partie I, puis [[trentesept]]",
                    "**Le changement de temps avec le changement de narrateur.** La partie II, racontée par Nagib dans une lettre, est au passé composé, temps de l’oral : [[parti]]. La scène de la falaise est au présent, qui fige un moment de bilan : [[falaise]].",
                ]),
            ]},
            {"code": "Énonciation", "titre": "Énonciation", "blocs": [
                ("ul", [
                    "**Deux narrateurs, deux fils.** En partie I, le fils cadet raconte en adulte qui se souvient ; le présent d’énonciation le montre : [[bibliotheque]]. En partie II, Nagib écrit à son frère, et la mère lit par-dessus son épaule : [[interprete]]. La mère est toujours vue par ses fils ; elle n’est jamais narratrice.",
                    "**La parole de la mère prend de la place.** D’abord des répliques courtes et des questions ; en partie II, de longues tirades ([[ame]]) et même une scène écrite comme du théâtre (la scène devant le soldat, à Anfa). Elle prend la parole en public.",
                    "**Le père remarque lui-même le changement de langage** : [[langage]].",
                ]),
            ]},
            {"code": "Connecteurs", "titre": "Connecteurs", "blocs": [
                ("ul", [
                    "**« Mais » (opposition)** : il marque l’obstacle puis son dépassement. [[peux]]",
                    "**« C’est ainsi que » (conséquence)** : il enchaîne les étapes comme des causes et des effets. [[ainsi]] ; [[tablier]]",
                    "**« Alors » (basculement)** : [[deluge]]",
                    "**« Tandis que » (opposition temporelle)** : [[maintenant]]",
                ]),
                ("p", "**Bilan.** Le récit est construit comme une suite d’étapes liées logiquement : la transformation n’est pas un hasard, c’est un enchaînement."),
            ]},
        ],
    },
    3: {
        "titre": "Analyse stylistique",
        "sections": [
            {"code": "B1", "blocs": [
                ("cle", "Images, symboles et rythme rendent la transformation visible."),
                ("ul", [
                    "**Métaphore et antithèse de l’arbre.** [[arbre]] L’opposition entre la prison et le printemps annonce toute l’évolution : la mère est enfermée mais vivante.",
                    "**Métaphore filée de la naissance.** [[nid]] ; [[naitre]] ; [[mollusque]] La question rhétorique « Pourquoi pas elle ? » fait de la transformation une évidence naturelle.",
                    "**Allusion biblique.** [[lumiere]] La formule rappelle la Genèse : l’éveil de la mère est présenté comme une création du monde.",
                    "**Symboles concrets.** La tache verte sur la robe ([[tache]]), les objets enterrés sous un oranger ([[paix]]), la serviette brodée ([[moi]]), les cheveux coupés ([[souvenir]]). Chaque étape est rendue visible par un objet ou un geste.",
                    "**Personnification.** Au moment de l’enterrement, la mère parle à ses objets comme à des amis : c’est un véritable discours funèbre pour son passé ([[paix]]).",
                    "**Accumulation de questions.** [[ame]] Le rythme haletant fait entendre une parole longtemps retenue qui explose.",
                    "**Antithèse des deux titres.** « Être » et « Avoir » structurent le roman ; la mère elle-même choisit : [[etre]]",
                ]),
            ]},
            {"code": "B2", "blocs": [
                ("cle", "L’humour est partout, mais il sert l’émancipation : il rend la mère attachante, désamorce le drame et critique la société sans violence."),
                ("ul", [
                    "**Le décalage comique (partie I).** La mère interprète la technique avec ses propres repères : [[bonsoir]] ; [[europeens]] ; [[meryem]]. Le rire est tendre, jamais méprisant : il montre sa logique propre et son intelligence pratique.",
                    "**L’ironie contre le père et la « civilisation ».** [[objets]] ; [[instinct]] ; [[loi]]. Le progrès matériel n’est pas un progrès des idées : l’ironie vise le titre même du roman.",
                    "**L’ironie contre les clichés occidentaux.** La mère rit des préjugés des livres ([[mahometans]]) et « met à la porte » les auteurs ([[tolstoi]]).",
                    "**Le décalage politique.** Devant le soldat qui garde de Gaulle : [[telephone]]. Le comique naît de l’écart entre son assurance et la situation.",
                    "**L’humour de Nagib dans les scènes graves.** Juste après l’affrontement avec le père : [[poils]]. Le rire désamorce la tension.",
                ]),
            ]},
            {"code": "B3", "blocs": [
                ("cle", "Les narrateurs valorisent l’évolution de la mère, mais restent lucides sur son prix."),
                ("ul", [
                    "**Partie I, le fils cadet : un regard admiratif et engagé.** [[soleil]] ; [[juger]]. Il est lyrique et prend parti contre le père.",
                    "**Mais un regard qui s’interroge.** Il reconnaît la violence de sa méthode et ses limites : [[importaient]] ; [[mots]].",
                    "**Partie II, Nagib : un regard humoristique et étonné.** [[connaissais]]. Il accepte d’être dépassé et d’inverser les rôles : [[tablier]].",
                    "**Le regard du père finit par rejoindre celui des fils** : [[conscience]].",
                    "**Une évolution qui a un prix.** La mère elle-même le dit ([[poignante]]), et les narrateurs montrent l’hostilité qu’elle rencontre ([[pierres]]).",
                ]),
                ("p", "**Bilan.** Le regard des narrateurs valorise l’émancipation tout en l’interrogeant : la liberté conquise est belle, mais elle coûte."),
            ]},
        ],
    },
    4: {
        "titre": "Analyse thématique",
        "sections": [
            {"code": "C1", "blocs": [
                ("cle", "L’émancipation progresse en cercles de plus en plus larges : de l’intime à la famille, puis à la société et au monde."),
                ("ol", [
                    "**L’enfermement.** [[personne]] ; [[seuil]]",
                    "**L’éveil par les objets.** Radio, électricité, téléphone : la découverte passe par les sens, et le téléphone ouvre déjà un premier réseau. [[reseau]]",
                    "**La sortie et le premier secret.** [[monde]] ; [[secret]]",
                    "**Le savoir et la naissance à soi.** [[avidite]] ; [[vit]]",
                    "**Le doute.** [[poignante]]",
                    "**L’affirmation, publique puis privée.** Devant le soldat à Anfa ([[femmes]]), puis face au mari ([[consciente]]).",
                    "**La rupture avec le passé.** [[paix]] ; [[moi]] ; [[inscrite]]",
                    "**La transmission, l’engagement et le départ.** [[actes]] ; [[locomotive]] ; [[horizon]]",
                ]),
                ("p", "**Sens de la progression.** Le parcours suit les titres des deux parties : « Être » (devenir soi), puis « Avoir » (prendre sa place dans le monde)."),
            ]},
            {"code": "C2", "blocs": [
                ("cle", "Les obstacles sont à la fois extérieurs (le père, la société, la colonisation) et intérieurs (la peur, la solitude) ; l’émancipation elle-même contient des contradictions."),
                ("h", "Obstacles extérieurs"),
                ("ul", [
                    "**Le père et la loi.** [[loi]] ; [[treize]] ; [[paye]]",
                    "**La société des hommes.** Les maris des amies deviennent hostiles : [[pierres]]",
                    "**La colonisation.** [[maitres]]",
                ]),
                ("h", "Résistances intérieures"),
                ("ul", [
                    "**La peur.** [[votrepere]]",
                    "**L’angoisse et le sentiment d’avoir perdu sa vie.** [[vieille]]",
                    "**La solitude.** [[solitude]] ; [[prison]]",
                ]),
                ("h", "Contradictions"),
                ("ul", [
                    "**Libérée par des hommes.** Ce sont ses fils qui la libèrent ; elle doit donc refuser aussi leur protection : [[tutelle]]",
                    "**Deux idées de la liberté.** Au début, elle la conçoit comme une immobilité ([[immobile]]) ; à la fin, elle part voyager.",
                    "**Une « civilisation » ambiguë.** Elle adopte les objets de l’Occident, mais refuse ses préjugés : [[mahometans]] ; [[tolstoi]]",
                ]),
            ]},
            {"code": "C3", "blocs": [
                ("cle", "Les apprentissages transforment la famille patriarcale en une famille d’égaux."),
                ("ul", [
                    "**Avec le père : de la soumission à la reconnaissance.** Il l’a épousée enfant ([[treize]]). Elle l’affronte ([[ame]]), puis il la redécouvre ([[nouvelle]]) et finit par se lever devant elle ([[meleve]]). Le père change lui aussi : [[conscience]]",
                    "**Avec les fils : l’inversion des rôles.** Au début, c’est elle qui corrige ses fils et rejette leur monde ([[paien]]). Puis les fils deviennent ses professeurs ([[corps]]). Elle les découvre adultes ([[decouvrit]]), puis devient elle-même professeur ([[professeur]]). Elle refuse la protection de Nagib ([[tutelle]]), qui finit par faire la cuisine ([[tablier]]).",
                    "**Avec la société : d’un cercle de trois personnes à un mouvement.** [[reseau]] ; [[ruche]]",
                ]),
            ]},
            {"code": "C4", "blocs": [
                ("these", "La mère ne cherche pas seulement à acquérir des connaissances : le savoir est pour elle l’instrument d’une conquête d’identité, qui se prolonge en action pour les autres."),
                ("ul", [
                    "**Le texte le dit explicitement.** [[etre]] ; [[sang]]",
                    "**Les signes d’une identité conquise.** [[vit]] ; [[moi]] ; [[consciente]]",
                    "**Un savoir critique, pas une accumulation.** Elle trie les livres et chasse les auteurs qui la déçoivent : [[tolstoi]]",
                    "**Une identité tournée vers les autres.** [[actes]]",
                ]),
                ("p", "**Nuance.** La partie II s’intitule « Avoir » : la mère acquiert bien des diplômes ([[examens]]). Mais cet « avoir » sert l’« être ». Et l’identité conquise a un prix : [[solitude]]"),
            ]},
            {"code": "Enjeux", "titre": "Enjeux sociaux et philosophiques", "blocs": [
                ("ul", [
                    "**La condition des femmes.** Les femmes n’ont pas voix au chapitre, et la mère réclame cette voix : [[femmes]]",
                    "**Tradition et modernité.** La vraie civilisation est celle des idées, pas celle des objets : [[objets]]",
                    "**Colonisation et indépendance.** La libération de la mère accompagne celle du pays : [[maitres]] ; [[locomotive]]",
                    "**Liberté et solitude.** [[poignante]]",
                    "**Être et avoir.** Les titres des deux parties posent la question ; la mère choisit d’abord l’être : [[etre]]",
                ]),
            ]},
        ],
    },
    5: {
        "titre": "Synthèse orale",
        "sections": [
            {"code": "Synthèse", "titre": "Synthèse orale", "blocs": [
                ("say", "Au terme de cette étude, trois constats se rejoignent. D’abord, la langue elle-même change avec la mère : au début, elle est le complément des verbes de ses fils, qui l’habillent et l’entraînent dehors ; à la fin, elle est sujet de verbes d’action et donne des ordres. Ensuite, l’écriture rend cette transformation visible : les images de la prison laissent place à celles de la naissance, et l’humour, toujours tendre, désamorce le drame tout en critiquant une « civilisation » qui modernise les objets sans moderniser les idées. Enfin, le sens de ce parcours est clair : la mère ne veut pas seulement savoir. Le roman le dit lui-même : elle cherche « à être et non à avoir ou posséder ». Le savoir est pour elle l’instrument d’une conquête d’identité, qui se prolonge en action pour les autres femmes et pour son pays."),
                ("say", "Notre réponse est donc la suivante : la mère conquiert une identité, et le savoir en est le moyen. Cette conquête a un prix, la solitude, mais elle transforme toute la famille, jusqu’au père, qui finit par se lever quand elle entre."),
                ("say", "Pour ouvrir : le titre, « La Civilisation, ma Mère !… », prend alors tout son sens. La vraie civilisation, dans ce roman, ce ne sont pas la radio ou le fer à repasser : c’est la mère elle-même, devenue, selon le mot du père, « la conscience d’un monde inconscient »."),
            ]},
        ],
    },
}
