# Reader-map spec for Herbert A. Simon, "The Corporation: Will It Be Managed by
# Machines?" (1960). Contains the outline only, never the source text: the text
# is extracted from the reader's own PDF at build time.
#
#   python3 scripts/reader/pdf_paragraphs.py Simon_The_Corporation_clean.pdf scripts/reader/examples/simon-1960.py doc.json
#   python3 scripts/reader/build_reader.py doc.json scripts/reader/examples/simon-1960.py simon-runko.html

META = {
    "lang": "fi",
    "text_lang": "en",
    "title": "Simon: The Corporation – runko",
    "h1": "The Corporation: Will It Be Managed by Machines?",
    "map_key": "simon-the-corporation-1960",
    "source_html": ("Herbert A. Simon 1960, teoksessa Anshen &amp; Bach (toim.), <i>Management and Corporations 1985</i>, McGraw-Hill. "
                    "Rungon ¶-numerot viittaavat koko tekstin {paras} kappaleeseen ja s.-numerot <a href=\"{pdf}\">PDF:n</a> sivuihin. "
                    "Jokainen kappale kuuluu täsmälleen yhteen korttiin."),
    "pdf_href": "Simon_The_Corporation_clean.pdf",
    "reader_title_html": ("<h2>The Corporation: Will It Be Managed by Machines?{note1}</h2>"
                          "<p>Herbert A. Simon. In M. Anshen &amp; G. L. Bach (Eds.), <i>Management and Corporations 1985.</i> "
                          "New York: McGraw-Hill, 1960.</p>"),
    "title_note": "1",
    # Lines dropped wherever they occur: title block and running header.
    "skip_lines": [r"^The Corporation: Will It$", r"^Be Managed by Machines\?1$", r"^Herbert A\. Simon$",
                   r"^In M\. Anshen", r"^New York: McGraw", r"^Herbert A\. Simon\s{5,}The Corporation$"],
    "heads_h1": ["PREDICTING LONG-RUN EQUILIBRIUM", "THE NEW TECHNOLOGY OF INFORMATION PROCESSING",
                 "THE AUTOMATION OF MANAGEMENT", "THE BROADER SIGNIFICANCE OF AUTOMATION"],
    "heads_h2": ["The Causes of Change", "The Invariants", "The Nearly Automatic Factory and Office",
                 "The Occupational Profile", "Another Approach to Prediction", "Flexibility in Automata",
                 "Environmental Control a Substitute for Flexibility", "Man as Man’s Environment",
                 "Summary: Blue-collar and Clerical Automation", "Operations Research", "Heuristic Programing8",
                 "A Summary: The Automation of Management", "Some Other Dimensions of Change in Management",
                 "A Science of Man", "Social Goals", "Man in the Universe"],
    "word_fixes": {"Bern-stein": "Bernstein", "Inter-acting": "Interacting"},
}

ROOT = ("Koneet pystyvät johtamaan yritystä vuonna 1985, mutta ihmiset tekevät silti suunnilleen samoja töitä",
        "Simon ennustaa pitkän aikavälin tasapainon: tekninen kyky korvata ihminen kaikessa, ja suhteellinen etu ratkaisee, missä ihminen silti työskentelee.",
        (101,101))
BRANCHES = [
 ("kysymys","Kysymys ja rajaus","var(--navy)","Mitä ennustetaan ja mitä jätetään pois.",(1,9),[
   ("", "Rakennustyömaa ikkunan takana: koneelefantit, kuljettajat ja kottikärryt näyttävät nykyisen työnjaon.",(1,3),[]),
   ("", "Bruttovaikutus iskukohdassa vs. nettovaikutus jälkiaaltoina; ohimenevät ja välilliset vaikutukset (sepät, esikaupungit).",(4,5),[]),
   ("", "Ohimenevät haitat rajataan pois; sääntö: hyötyvä yhteiskunta maksaa muutoksen ja korvaa kärsijöille.",(6,7),[]),
   ("highlight", "Tehtävä on kuvata yhteiskunta uudessa tasapainossa, kun kaikki toissijaiset sopeutumiset on tehty.",(8,8),[]),
   ("", "Neljän osan suunnitelma: tasapaino, uusi tekniikka, johtamisen automaatio, laajempi merkitys.",(9,9),[]),
 ]),
 ("vasara-alasin","Vasara ja alasin","var(--petrol)","Ennusteen kehys: mikä muuttuu itsestään, mikä pysyy, ja miten suhteellinen etu ratkaisee.",(10,22),[
   ("highlight", "Ennuste lepää kahdella: itsestään muuttuvat ensimmäiset syyt (vasara) ja muuttumattomat reunaehdot (alasin).",(10,10),[]),
   ("", "Vasara: tiedon kasvu rajaa mahdollisen, pääoman kasvu taloudellisen. Uusi tieto on ajattelun ja oppimisen ymmärtäminen.",(11,12),[]),
   ("source", "Alle 25 vuodessa koneet voivat korvata ”any and all human functions in organizations”.",(13,13),[]),
   ("", "Alasin: täystyöllisyys ja ennallaan pysyvä kykyjakauma. Muutos näkyy ammattirakenteessa, ei työttömyytenä.",(14,17),[]),
   ("", "Paradoksi: jos kone voittaa kaikessa, jääkö ihminen työttömäksi? Ei, hinnat sopeutuvat ja suhteellinen etu ratkaisee.",(18,20),[]),
   ("source", "Kone 1000× kirjanpitäjää ja 100× pikakirjoittajaa nopeampi: kirjanpitäjiä vähemmän, pikakirjoittajia enemmän.",(21,22),[]),
 ]),
 ("tehdas-toimisto","Lähes automaattinen tehdas ja toimisto","var(--slate)","Mitä tuotannon ja toimiston automaatio jo opettaa.",(23,33),[
   ("", "Automaatio jatkaa teollista vallankumousta: ensin lihasvoima, nyt aistiminen, valinta ja käsittely.",(23,23),[]),
   ("", "Työntekijätön tehdas on mahdollinen, mutta tyypillinen vuoden 1985 tehdas on vuoden 1960 jalostamon tasolla.",(24,24),[]),
   ("", "Toimisto automatisoituu tehdasta nopeammin; molemmista tulee pienen ryhmän ja ison koneen yhteistyötä.",(25,26),[]),
   ("highlight", "Vähemmän ihmisiä tuotosyksikköä kohden ei tarkoita vähemmän ihmisiä yhteensä.",(27,30),[
      ("Varoitus samasta virheestä kuin suhteellisessa edussa",(27,28)),
      ("Opetus 1: työ ei epäinhimillisty, vaan muuttuu mielekkäämmäksi",(29,29)),
      ("Opetus 2: taitotasojen jakauma ei juuri muutu",(30,30)),
   ]),
   ("", "Ammattirakenne riippuu myös tulo- ja hintajoustoista: psykiatrian esimerkki.",(31,32),[]),
   ("", "Halvin automaatio poistaa vaiheen kokonaan: jätteet jauhetaan viemäriin, ”Kolumbuksen muna”.",(33,33),[]),
 ]),
 ("joustavuus","Joustavuus: missä ihminen pitää etunsa","var(--petrol-700)","Ihminen kykyjen kimppuna, ja kaksi tietä ohittaa hänen joustavuutensa.",(34,55),[
   ("", "Luokittele ihminen kykyinä, ei ammatteina: silmät, aivot, kädet, jalat, lihakset; yleis- vs. erikoiskone.",(34,36),[]),
   ("", "Mekanisaatio vei lihasvoiman ja toistot; jäljelle jäi joustava ajattelu, aistit, kädet ja liikkuminen maastossa.",(37,39),[]),
   ("highlight", "Joustavuus on ihmisen suhteellinen etu. Jäljitelläänkö sitä koneessa, vai poistetaanko sen tarve?",(40,43),[]),
   ("", "Aivojen ongelmanratkaisu automatisoituu ennen silmiä, käsiä ja jalkoja.",(44,46),[]),
   ("", "Ympäristön vakiointi korvaa joustavuuden, ja se kumuloituu vaiheesta toiseen.",(47,53),[
      ("Sopeuta organismi ympäristöön tai ympäristö organismiin; homeostaasi",(47,49)),
      ("Sileä tie, raaka-aineen yhdenmukaistus, siirtolinjat",(50,52)),
      ("Mekanisaatio on useammin poistanut joustavuuden tarpeen kuin jäljitellyt sitä",(53,53)),
   ]),
   ("", "Lähdedata tehdään koneluettavaksi. Korkea status ei suojaa: lääkäri, varatoimitusjohtaja, opettaja.",(54,55),[]),
 ]),
 ("organisaatio-1985","Ihminen ihmisen ympäristönä","var(--amber-700)","Vuorovaikutus, esimiestyö ja myynti – ja millainen organisaatio vuonna 1985 on.",(56,68),[
   ("", "Toinen ihminen on työn karkein ympäristö. Suuri osa vuorovaikutuksesta syntyy ihmistyön valvonnasta.",(56,58),[]),
   ("", "Hoputus ja kiirehtiminen kutistuvat esimiestyöstä, kun tahdin määräävät kone ja aikataulu.",(59,60),[]),
   ("", "Myyjä: jos ostopäätökset eivät objektivoidu, myynnin osuus työllisyydestä kasvaa.",(61,61),[]),
   ("", "Kolme roolia: muutama linjatyöntekijä, kasvava kunnossapito, ammattilaiset suunnittelussa ja johdossa.",(62,65),[]),
   ("", "Stressaavat esimiessuhteet vähenevät; kasvokkain tehtävän palvelutyön osuus kasvaa.",(66,67),[]),
   ("highlight", "Lopputulos ei mullista työtä: maailma on rennompi, ja ehkä useampi meistä on myyjä.",(68,68),[]),
 ]),
 ("johtaminen","Johtamisen automatisointi","var(--navy)","Ohjelmoidut päätökset menevät ensin, huonosti jäsennellyt perässä.",(69,100),[
   ("", "Päätöksenteko laajasti: ongelman havaitseminen, vaihtoehtojen kehittely, valinta. Jatkumo ohjelmoidusta ohjelmoimattomaan.",(69,73),[
      ("Kolme vaihetta; kaksi ensimmäistä vievät eniten työtä",(69,70)),
      ("Ohjelmoidut ja ohjelmoimattomat päätökset; korrelaatio organisaatiotasoon",(71,72)),
      ("Kaksi tekniikkaa: operaatiotutkimus ja heuristinen ohjelmointi",(73,73)),
   ]),
   ("highlight", "Operaatiotutkimus tekee keskijohdon toistuvat päätökset jo nyt vähintään yhtä hyvin kuin johtajat.",(74,83),[
      ("Operaatiotutkimus liikkeenä ja menetelmänä",(74,76)),
      ("Kuusi esimerkkiä: varasto, tilausvirta, aikataulutus, moottorisuunnittelu, rehuseokset, lentoyhtiö",(77,82)),
      ("Keskijohdon osuus kutistuu muutamassa vuodessa",(83,83)),
   ]),
   ("", "Tietokoneet eivät ole nopeita idiootteja: ne käsittelevät symboleja, ymmärtävät kääntäjiä ja oppivat.",(84,89),[
      ("Korvaa ihmisen, mutta ei jäljittele häntä",(84,85)),
      ("Neljä väitettä tietokoneista",(86,89)),
   ]),
   ("source", "Kolme shakkiohjelmaa: noin miljoona, 2 500 ja alle 50 tutkittua vaihtoehtoa, sama heikko taso.",(90,93),[
      ("Heuristisen ohjelman määritelmä ja esimerkit",(90,91)),
      ("Los Alamos, Bernstein, RAND-Carnegie",(92,92)),
      ("Kymmenessä vuodessa tai alle myös huonosti jäsennellyt ongelmat",(93,93)),
   ]),
   ("", "Taloudessa ihminen pitää etunsa fyysisessä joustavuudessa paremmin kuin henkisessä; keskijohto kutistuu eniten.",(94,95),[]),
   ("", "Johtajan työ: aikajänne pitenee, teknistä osaamista tarvitaan vähemmän, ohjelmoijista ei tule eliittiä.",(96,100),[
      ("Aikajänne pitenee: suunnittelu ja järjestelmien muutos",(96,97)),
      ("Johtaja tarvitsee vähemmän tietoa koneen sisuksista",(98,98)),
      ("Ohjelmoijan ammatti kuolee ennemmin kuin nousee valtaan",(99,99)),
      ("Systeemiajattelu, jolle ei vielä ole tiedettä",(100,100)),
   ]),
 ]),
 ("merkitys","Laajempi merkitys","var(--petrol)","Kun niukkuus poistuu, jäljelle jäävät pitkän aikavälin kysymykset.",(101,110),[
   ("highlight", "Kaksi näennäisesti ristiriitaista ennustetta: kone voi johtaa yritystä, mutta ammatit pysyvät tuttuina.",(101,101),[]),
   ("", "Niukkuus lakkaa olemasta ensimmäinen ongelma; teknologisen työttömyyden ja R.U.R.-pelon voi haudata.",(102,103),[]),
   ("", "Kolme pitkän aikavälin ongelmaa: ihmistiede, työn korvaavat tavoitteet ja ihmisen paikka maailmankaikkeudessa.",(104,104),[]),
   ("", "Ihmistiede: vuonna 1985 psykologia on yhtä onnistunutta kuin kemia nyt; seuraukset opetukseen ja psykiatriaan.",(105,105),[]),
   ("", "Vapaa-ajan ongelma; yritys menettää asemaansa statuksen ja luovuuden lähteenä.",(106,107),[]),
   ("", "Kopernikus, Darwin, Freud – ja nyt ajattelevat koneet vievät ihmiseltä viimeisen ainutlaatuisuuden.",(108,110),[]),
 ]),
]
