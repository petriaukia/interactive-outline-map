# Reader-map spec for Virginia Woolf, A Room of One's Own (1929). The text is in
# the public domain in the EU and the UK (Woolf died in 1941) and in the US
# (published 1929), so the published map carries it in full.
#
#   curl -sLo woolf.html https://www.gutenberg.ca/ebooks/woolfv-aroomofonesown/woolfv-aroomofonesown-00-h.html
#   python3 scripts/reader/html_paragraphs.py woolf.html scripts/reader/examples/a-room-of-ones-own.py doc.json
#   python3 scripts/reader/build_reader.py doc.json scripts/reader/examples/a-room-of-ones-own.py examples/a-room-of-ones-own-reader.html
#
# Branches follow the chapters, because a reader map has to: every branch is
# one contiguous run of paragraphs. The thematic map of the same essay is
# examples/a-room-of-ones-own.html.

META = {
    "lang": "en",
    "ui": "en",
    "title": "A Room of One's Own — reader map",
    "h1": "A Room of One's Own",
    "map_key": "a-room-of-ones-own-reader",
    "source_html": ("Virginia Woolf, 1929. Full text from "
                    "<a href=\"https://www.gutenberg.ca/ebooks/woolfv-aroomofonesown/woolfv-aroomofonesown-00-h.html\">Project Gutenberg Canada</a> "
                    "(Hogarth Press edition), public domain. Each card opens the text at its own paragraphs; "
                    "together the cards cover all {paras} paragraphs, verse included, exactly once."),
    "reader_title_html": ("<h2>A Room of One's Own{note1}</h2>"
                          "<p>Virginia Woolf. London: Hogarth Press, 1929.</p>"),
    "title_note": "1",
    "html_start": r'<h2 id="chapter01">',
    "html_end": r'THE END',
}

ROOT = ("A woman must have money and a room of her own if she is to write fiction",
        "Woolf's lecture told as two days of a fictional narrator: Oxbridge, the British Museum, "
        "the history of women writing, a first novel, and the androgynous mind.",
        (130, 130))

BRANCHES = [
 ("oxbridge", "I · Oxbridge: lunch and dinner", "var(--navy)",
  "A day at a men's college and a women's college, and the money beneath each.", (1, 31), [
   ("highlight", "Her one opinion on a minor point: a woman needs money and a room of her own to write fiction.", (1, 1), []),
   ("", "A thought like a fish on a line; a Beadle turns her off the turf, the library turns her away.", (2, 4), []),
   ("", "Centuries of gold and silver from kings, then merchants, built the men's college.", (5, 5), []),
   ("", "A rich lunch, a Manx cat, and the humming that men and women no longer hear since the war.", (6, 25), [
      ("The lunch itself: soles, partridges, wine", (6, 6)),
      ("The tailless cat; Tennyson and Christina Rossetti as what people once hummed", (7, 12)),
      ("Walking to Fernham: why the poets of then cannot be matched now", (13, 22)),
      ("Fernham's garden in a spring fancy", (23, 25)),
   ]),
   ("source", "A plain dinner at Fernham, built on £30,000 raised with difficulty: “The amenities will have to wait.”", (26, 27), []),
   ("", "Why were our mothers poor? They could not earn, and until recently could not own; locked out, or locked in.", (28, 31), []),
 ]),
 ("museum", "II · The British Museum", "var(--petrol)",
  "The search for facts about women ends in the discovery of anger.", (32, 47), [
   ("", "In the catalogue, women are the most discussed animal in the universe, and almost entirely by men.", (32, 33), []),
   ("", "Notes headed Women and Poverty turn into fifty questions; the sages contradict each other.", (34, 41), [
      ("The notebook page", (34, 35)),
      ("Pope against La Bruyère, Napoleon against Johnson", (36, 40)),
      ("Nothing worth taking home", (41, 41)),
   ]),
   ("", "Her sketch of Professor von X shows the professor's anger, and her own.", (42, 42), []),
   ("source", "Women “as looking-glasses … reflecting the figure of man at twice its natural size.”", (43, 43), []),
   ("highlight", "Her aunt's legacy of £500 a year mattered more than the vote: fear and bitterness gave way to freedom.", (44, 45), []),
   ("", "In a century women may cease to be the protected sex, and all assumptions built on that will go.", (46, 47), []),
 ]),
 ("shakespeares-sister", "III · Shakespeare's sister", "var(--slate)",
  "Why no woman wrote in the age of Elizabeth, and what a writing mind needs.", (48, 64), [
   ("", "History has nothing on the Elizabethan woman: supreme in poetry, locked up and beaten in fact.", (48, 53), [
      ("Trevelyan's History of England", (48, 50)),
      ("A worm winged like an eagle", (51, 52)),
      ("A supplement to history is wanted", (53, 53)),
   ]),
   ("highlight", "Judith Shakespeare, as gifted as her brother: no school, flight to London, and death at the cross-roads.", (54, 54), []),
   ("", "Lost genius shows in witches and wise women; Anon was often a woman; chastity demanded anonymity.", (55, 56), []),
   ("", "Even for men, writing a work of genius is a feat of prodigious difficulty against an indifferent world.", (57, 58), []),
   ("", "For women the world's indifference was hostility: Oscar Browning, Mr. Greg, a dog on its hind legs.", (59, 62), [
      ("No room of her own, and open contempt", (59, 59)),
      ("Johnson's dog dictum, repeated of women composers in 1928", (60, 60)),
      ("Men's opposition to emancipation; tears that were real", (61, 62)),
   ]),
   ("", "Shakespeare's mind was incandescent: every grievance consumed, so the work came out whole.", (63, 64), []),
 ]),
 ("forerunners", "IV · The women who wrote anyway", "var(--petrol-700)",
  "From aristocratic poets to Aphra Behn to the novelists of the sitting-room.", (65, 100), [
   ("", "Lady Winchilsea had a true gift, but her poems are torn by anger at the “opposing faction”.", (65, 79), [
      ("Her outburst against the position of women", (65, 68)),
      ("Writing for no audience; lines of pure poetry", (69, 74)),
      ("Melancholy, rambling in the fields, and dubious gossip", (75, 79)),
   ]),
   ("", "Margaret of Newcastle runs riot; Dorothy Osborne, a born writer, thinks writing books ridiculous.", (80, 83), [
      ("The crazy Duchess as a bogey for clever girls", (80, 80)),
      ("Dorothy Osborne's letters", (81, 83)),
   ]),
   ("highlight", "Aphra Behn earned her living by her pen; that, more than anything she wrote, freed the mind.", (84, 85), []),
   ("", "Austen, the Brontës and Eliot wrote novels in the common sitting-room; Austen without hate, Charlotte Brontë in a rage.", (86, 92), [
      ("Why novels: the one sitting-room, and training in observing character", (86, 86)),
      ("Jane Eyre on the roof, longing for the world", (87, 90)),
      ("The awkward break, and what experience would have given her", (91, 92)),
   ]),
   ("", "A novel's integrity: most women bent their values towards men's; only Austen and Emily Brontë did not.", (93, 97), [
      ("Integrity as the conviction that this is the truth", (93, 94)),
      ("Men's values prevail in life and in fiction", (95, 95)),
      ("No lock upon the freedom of the mind", (96, 97)),
   ]),
   ("", "No tradition: the man's sentence did not fit her; only the novel was young enough to shape.", (98, 100), []),
 ]),
 ("mary-carmichael", "V · Mary Carmichael's first novel", "var(--amber-700)",
  "Reading a living woman novelist as the heir of all the others.", (101, 119), [
   ("", "Women now write on every subject; Mary Carmichael has broken the expected sentence.", (101, 103), []),
   ("highlight", "“Chloe liked Olivia”: perhaps the first time in literature that women are seen apart from men.", (104, 106), []),
   ("", "Two women sharing a laboratory; the writer must catch what women do when they are alone.", (107, 108), []),
   ("", "Women's creative power is unmeasured and different; it would be a pity if women wrote like men.", (109, 111), []),
   ("", "Still to record: obscure lives, and the spot the size of a shilling at the back of a man's head.", (112, 114), []),
   ("", "She breaks the sequence too; no genius, but free of fear and hatred. Give her a room, £500, a century.", (115, 119), []),
 ]),
 ("androgynous-mind", "VI · The androgynous mind", "var(--navy)",
  "Two sexes in the mind, and why the age's sex-consciousness spoils writing.", (120, 129), [
   ("", "A man and a woman meet and take a taxi; the mind, divided for two days, comes together.", (120, 121), []),
   ("highlight", "Two powers in every mind, male and female; Coleridge: a great mind is androgynous.", (122, 122), []),
   ("", "A sex-conscious age: Mr. A's shadow of the letter “I”; Mr. B's sentences fall dead.", (123, 124), []),
   ("", "Galsworthy and Kipling lack suggestive power; a Fascist call for a poet from an incubator.", (125, 126), []),
   ("source", "Shakespeare, Keats and Proust were androgynous: “it is fatal for anyone who writes to think of their sex.”", (127, 129), []),
 ]),
 ("ceases-to-speak", "Mary Beton ceases to speak", "var(--petrol)",
  "Woolf in her own person: two objections answered, and the peroration.", (130, 143), [
   ("", "No ranking of the sexes as writers: measuring is futile; write what you wish to write.", (130, 131), []),
   ("source", "Quiller-Couch: the poor poet has not “a dog's chance”; intellectual freedom depends on material things.", (132, 134), []),
   ("", "Write every kind of book; to have money and a room is to live in the presence of reality.", (135, 136), []),
   ("", "The peroration: be yourself; colleges since 1866, property since 1880, the vote since 1919.", (137, 141), []),
   ("highlight", "Shakespeare's sister will be born if we have money, rooms of our own and the habit of freedom.", (142, 143), []),
 ]),
]
