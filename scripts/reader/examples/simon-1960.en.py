# Outline spec for Herbert A. Simon, "The Corporation: Will It Be Managed by
# Machines?" (1960), in English. Built with --outline-only: the published map
# carries no source text, because the chapter is not ours to redistribute, and
# its locators name Simon's own section headings so that any edition will do.
#
#   python3 scripts/reader/pdf_paragraphs.py <your-copy>.pdf scripts/reader/examples/simon-1960.fi.py doc.json
#   python3 scripts/reader/build_reader.py doc.json scripts/reader/examples/simon-1960.en.py examples/simon-the-corporation-1960.html --outline-only
#
# The splitting settings (headings, running heads) live in simon-1960.fi.py;
# this file reuses the same paragraph numbers.

META = {
    "lang": "en",
    "ui": "en",
    "title": "Simon: The Corporation — outline",
    "h1": "The Corporation: Will It Be Managed by Machines?",
    "map_key": "simon-the-corporation-1960-en",
    "source_html": ("Herbert A. Simon, in M. Anshen &amp; G. L. Bach (eds.), <i>Management and Corporations 1985</i>, "
                    "McGraw-Hill, 1960. An outline without the text: each card names the section of the chapter it covers, "
                    "and together the cards cover every paragraph exactly once."),
    "first_section": "Introduction",
    "title_note": "1",
}

ROOT = ("Machines will be able to run the corporation by 1985, yet people will still do roughly the same jobs",
        "Simon forecasts the long-run equilibrium: the technical ability to replace people in every function, "
        "and comparative advantage deciding where people still work.",
        (101, 101))

BRANCHES = [
 ("question", "The question and its limits", "var(--navy)", "What is forecast, and what is left out.", (1, 9), [
   ("", "A building site outside the window: mechanical elephants, their mahouts and wheelbarrows show today's division of labour.", (1, 3), []),
   ("", "Gross effects at the point of impact vs. net effects in later ripples; transient and indirect effects.", (4, 5), []),
   ("", "Transient harms are set aside; the rule: the society that gains pays for the change and compensates the losers.", (6, 7), []),
   ("highlight", "The task is to picture society in its new equilibrium, after every secondary adjustment has been made.", (8, 8), []),
   ("", "A plan in four parts: equilibrium, the new technology, the automation of management, the wider meaning.", (9, 9), []),
 ]),
 ("hammer-anvil", "The hammer and the anvil", "var(--petrol)",
  "The frame of the forecast: what changes by itself, what stays put, and how comparative advantage decides.", (10, 22), [
   ("highlight", "The forecast rests on two things: autonomous first causes (the hammer) and fixed givens (the anvil).", (10, 10), []),
   ("", "The hammer: growing knowledge sets what is feasible, growing capital what is economical; the new knowledge is how thinking works.", (11, 12), []),
   ("source", "Within far less than 25 years, machines able to substitute for “any and all human functions in organizations”.", (13, 13), []),
   ("", "The anvil: full employment and an unchanged spread of ability. Change shows in the occupational profile, not in unemployment.", (14, 17), []),
   ("", "The paradox: if machines win everywhere, are people unemployable? No: prices adjust, and comparative advantage decides.", (18, 20), []),
   ("source", "A computer 1,000× faster than a bookkeeper, 100× faster than a stenographer: fewer bookkeepers, more stenographers.", (21, 22), []),
 ]),
 ("factory-office", "The nearly automatic factory and office", "var(--slate)",
  "What automation in production and in the office already teaches.", (23, 33), [
   ("", "Automation continues the Industrial Revolution: first muscle power, now sensing, choosing and handling.", (23, 23), []),
   ("", "The workerless factory is feasible, but the typical 1985 factory will be at the level of a 1960 refinery.", (24, 24), []),
   ("", "The office automates faster than the factory; both become small groups working with large machines.", (25, 26), []),
   ("highlight", "Fewer people per unit of output does not mean fewer people in total.", (27, 30), [
      ("A warning against the same error as with comparative advantage", (27, 28)),
      ("Lesson 1: work is not dehumanised; it tends to become more pleasant", (29, 29)),
      ("Lesson 2: the profile of skill levels barely changes", (30, 30)),
   ]),
   ("", "The occupational profile also depends on income and price elasticities: the psychiatry example.", (31, 32), []),
   ("", "The cheapest automation removes a step altogether: garbage ground into the sewer, a Columbus egg.", (33, 33), []),
 ]),
 ("flexibility", "Flexibility: where people keep their edge", "var(--petrol-700)",
  "The human as a bundle of capacities, and two ways around human flexibility.", (34, 55), [
   ("", "Classify people by capacities, not occupations: eyes, brain, hands, legs, muscles; general vs. special-purpose machines.", (34, 36), []),
   ("", "Mechanisation took muscle and repetition; what remained was flexible thinking, senses, hands and moving over rough ground.", (37, 39), []),
   ("highlight", "Flexibility is the human comparative advantage. Imitate it in the machine, or remove the need for it?", (40, 43), []),
   ("", "The brain's problem solving will be automated before the eyes, hands and legs.", (44, 46), []),
   ("", "Controlling the environment substitutes for flexibility, and the effect accumulates step by step.", (47, 53), [
      ("Adapt the organism to the environment, or the environment to the organism; homeostasis", (47, 49)),
      ("The smooth road, standardised raw material, transfer machines", (50, 52)),
      ("Mechanisation has more often removed the need for flexibility than imitated it", (53, 53)),
   ]),
   ("", "Source data will be made machine-readable. High status is no shelter: physician, vice-president, college teacher.", (54, 55), []),
 ]),
 ("organisation-1985", "Man as man's environment", "var(--amber-700)",
  "Interaction, supervision and selling, and what the 1985 organisation looks like.", (56, 68), [
   ("", "Other people are the roughest part of the environment. Much interaction exists to supervise human work.", (56, 58), []),
   ("", "Work-pushing and expediting shrink from supervision once machines and schedules set the pace.", (59, 60), []),
   ("", "The salesman: if buying does not become more objective, selling takes a larger share of employment.", (61, 61), []),
   ("", "Three roles: a few in-line workers, a growing maintenance force, professionals in design and management.", (62, 65), []),
   ("", "Stressful supervisory relations decline; face-to-face personal service grows as a share of work.", (66, 67), []),
   ("highlight", "The outcome does not upend work: a more relaxed world, and perhaps more of us will be salesmen.", (68, 68), []),
 ]),
 ("management", "The automation of management", "var(--navy)",
  "Programmed decisions go first, ill-structured ones follow.", (69, 100), [
   ("", "Decision making in the broad sense: finding problems, designing courses of action, choosing. A continuum from programmed to unprogrammed.", (69, 73), [
      ("Three stages; the first two take most of the effort", (69, 70)),
      ("Programmed and unprogrammed decisions; a loose link to organisational level", (71, 72)),
      ("Two techniques: operations research and heuristic programming", (73, 73)),
   ]),
   ("highlight", "Operations research already makes middle management's repetitive decisions at least as well as managers do.", (74, 83), [
      ("Operations research as a movement and as a method", (74, 76)),
      ("Six examples: inventory, order flow, scheduling, motor design, feed mixes, an airline", (77, 82)),
      ("Middle management's share will shrink within a few years", (83, 83)),
   ]),
   ("", "Computers are not speedy morons: they handle symbols, understand compilers and can learn.", (84, 89), [
      ("They replace people without simulating them", (84, 85)),
      ("Four statements about computers", (86, 89)),
   ]),
   ("source", "Three chess programs: about a million, 2,500 and under 50 alternatives examined, all at the same weak level.", (90, 93), [
      ("What a heuristic program is, and examples", (90, 91)),
      ("Los Alamos, Bernstein, RAND-Carnegie", (92, 92)),
      ("Within ten years or less, ill-structured problems too", (93, 93)),
   ]),
   ("", "Economically, people keep their edge in physical flexibility better than in mental; middle management shrinks most.", (94, 95), []),
   ("", "The manager's job: a longer time horizon, less technical knowledge needed, programmers will not become an elite.", (96, 100), [
      ("A longer horizon: planning and redesigning systems", (96, 97)),
      ("Managers will need to know less about the machinery", (98, 98)),
      ("Programming is likelier to die out than to rule", (99, 99)),
      ("Systems thinking, for which there is no science yet", (100, 100)),
   ]),
 ]),
 ("significance", "The broader significance", "var(--petrol)",
  "Once scarcity is gone, the long-range questions remain.", (101, 110), [
   ("highlight", "Two predictions that seem to clash: machines could run the corporation, yet occupations stay familiar.", (101, 101), []),
   ("", "Scarcity stops being the first problem; the fears of technological unemployment and of robots (R.U.R.) can be dropped.", (102, 103), []),
   ("", "Three long-range problems: a science of man, goals other than work, and man's place in the universe.", (104, 104), []),
   ("", "A science of man: by 1985 psychology as successful as chemistry now, with consequences for teaching and psychiatry.", (105, 105), []),
   ("", "The problem of leisure; the corporation loses its place as a source of status and creativity.", (106, 107), []),
   ("", "Copernicus, Darwin, Freud — and now thinking machines take away the last claim to uniqueness.", (108, 110), []),
 ]),
]
