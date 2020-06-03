# -*- coding: utf-8 -*-
import re

def clean_string(string):
    r"""Discard newlines, remove multiple spaces and remove leading or
    trailing whitespace. We also replace quotation mark characters
    since we've decided to use a different style (though usually
    quotes are marked with <ctl>).

    Note since this strips leading and trailing whitespace it should
    only be applied once we have finished concatenating a string
    (since e.g. 'the '.strip() + 'dog' gives 'thedog').

    >>> clean_string(' \nfoo   bar  \n  ')
    'foo bar'

    """
    # collapse whitespace to single spaces
    string = re.sub('[\n\t ]+', ' ', string)

    # fix quotes
    string = string.replace(u'„', u'«').replace(u'“', u'»')

    # replace acronyms with their expanded versions
    # see http://www.reta-vortaro.de/revo/dok/mallongigoj.html
    string = string.replace('p.p.', 'parolante pri')
    string = string.replace('p. p.', 'parolante pri')
    string = string.replace('ktp', 'kaj tiel plu')
    string = string.replace('kp ', 'komparu ') # trailing space to avoid false positives
    string = string.replace('Kp ', 'Komparu ')
    string = string.replace('kp:', 'komparu:')
    string = string.replace('vd ', 'vidu ')
    string = string.replace('Vd ', 'Vidu ')
    string = string.replace('pp ', 'parolante pri')
    string = string.replace('vol.', 'volumo')

    # fix ; having a space before it (fixes remark in 'ankoraŭ')
    string = string.replace(' ;', ';')

    # fix ? having a space before it (fixes example in 'surda')
    string = string.replace(' ?', '?')

    # fix ! having a space before it (fixes 'mufo')
    string = string.replace(' !', '!')

    # fix . having a space before it (fixes remark in 'unu')
    string = string.replace(' .', '.')

    # get rid of leading/trailing space
    return string.strip()

def get_word_root(arbitrary_node):
    """Get the word root corresponding to this word. The XML files are
    grouped such that every word in the same file has the same word
    root. We therefore do not need any specific node for this
    function.

    A minimal example:

    <vortaro>
    <kap><rad>salut</rad></kap>
    </vortaro>

    """
    assert arbitrary_node != None
    tree = arbitrary_node.getroottree()
    return list(tree.iter('rad'))[0].text

def tld_to_string(tld_node):
    """Convert a <tld> to a string. Remarkably non-trivial.

    The lit attribute of a <tld> signifies that in this particular
    case the root starts with a different letter than normal. For
    example, 'Aglo' has root 'agl-'. I haven't seen this used for
    anything other than capitalisation (both changing to upper case
    and changing to lower case).
    
    The relevant part of the ReVo documentation is vokoxml.dtd,
    lines 340 to 344.

    """
    root = get_word_root(tld_node)

    if "lit" in tld_node.attrib:
        new_letter = tld_node.attrib['lit']
        return new_letter + root[1:]
    else:
        return root

def expand_bibliography_abbreviation(abbrev):
    """Replace any abbreviations used for example sources with their
    expansions.

    """
    bibliography_abbrevs = {
        u'Z': u'Zamenhof',
        u'9OA': u'Naŭa Oficiala Aldono al la Universala Vortaro',
        u'Aventuroj': u'Aventuroj de pioniro',
        u'BazRad': u'Bazaj Radikoj Esperanto-Esperanto',
        u'Bird': u'Oklingva nomaro de eŭropaj birdoj',
        u'BoE': u'Entrepreno. Entreprenistaj Strategioj: Priskribo de la entrepreno',
        u'BoER': u'Esperanta-rusa vortaro',
        u'BoM': u'Mondkomerco kaj Lingvo',
        u'BonaLingvo': u'La bona lingvo',
        u'BonaS-ino': u'La bona sinjorino',
        u'BoRE': u'Rusa-esperanta vortaro',
        u'BoT': u'La Merkato de Trafikservoj',
        u'BT': u'Biblioteka terminaro',
        u'ĈA': u'Ĉina Antologio (1919-1949)',
        u'CCT': u'Common Commercial Terms in English and Esperanto',
        u'CEE': u'Comprehensive English-Esperanto Dictionary',
        u'ChP': u'Profesia uzo de Esperanto kaj ĝiaj specifaj trajtoj',
        u'Ĉukĉoj': u'El vivo de ĉukĉoj',
        u'ĉuSn': u'Ĉu ili estas sennaciistoj?',
        u'DanĝLng': u'La danĝera lingvo, studo pri la persekutoj kontraŭ Esperanto',
        u'DdH': u'Aldono al la «Dogmoj de Hilelismo»',
        u'Deneva': u'Esperanta-Bulgara-Rusa Matematika Terminaro',
        u'DonKihxoto': u'La inĝenia hidalgo Don Quijote de la Mancha',
        u'DOz': u'Doroteo kaj la Sorĉisto en Oz',
        u'EBV': u'Esperanta Bildvortaro',
        u'EdE': u'Enciklopedio de Esperanto',
        u'EE': u'Esenco kaj Estonte',
        u'Eek': u'Esperanto en Komerco. Esperanto in Commerce',
        u'EFM': u'Economie, finance, monnaie. Glosaro de la komisiono de la Eŭropaj Komunumoj. Versio esperanto ― français ― english',
        u'EKV': u'EK-Vortaro de matematikaj terminoj',
        u'ElektFab': u'Elektitaj Fabeloj de Fratoj Grimm',
        u'EncCxi': u'Enciklopedieto de Ĉinio',
        u'EncJap': u'Enciklopedieto japana',
        u'Esperanto': u'Esperanto',
        u'F': u'Fundamento de Esperanto',
        u'Fab1': u'Fabeloj, vol. 1',
        u'Fab2': u'Fabeloj, vol. 2',
        u'Fab3': u'Fabeloj, vol. 3',
        u'Fab4': u'Fabeloj, vol. 4',
        u'Far1': u'La Faraono, vol. 1',
        u'Far2': u'La Faraono, vol. 2',
        u'Far3': u'La Faraono, vol. 3',
        u'FIL': u"Pri la solvo de l'problemo de internacia lingvo por komerco kaj trafiko. Zur Lösung der Frage einer internationalen Handels- und Verkehrssprache. Amtlicher Sitzungsbericht der Internationalen Konferenz für eine gemeinsame Hilfssprache des Handels und Verkehrs, Venedig, 2.-4. April 1923",
        u'FK': u'Fundamenta Krestomatio de la lingvo Esperanto',
        u'FT': u'Fervoja Terminaro (UIC Railway Dictionary)',
        u'FzT': u'Esperanta terminaro de fiziko, Esperanto ― japana ― angla. Reviziita',
        u'GDFE': u'Grand dictionnaire français espéranto',
        u'Gerda': u'Gerda malaperis',
        u'Gv': u'La Gunkela vortaro de vortoj mankantaj en PIV 2002',
        u'HejmVort': u'Hejma Vortaro',
        u'HomojManĝantaj': u'Homoj manĝantaj',
        u'Homaranismo': u'Homoranismo',
        u'IKEV': u'Internacia komerca-ekonomika vortaro en 11 lingvoj',
        u'InfanTorent2': u'Infanoj en Torento, dua libro en la Torento-trilogio',
        u'IntArkeol': u'Interesa arkeologio',
        u'IntKui': u'Internacie kuiri',
        u'Iŝtar': u'Pro Iŝtar',
        u'ItEsp': u'Vocabolario Italiano-Esperanto',
        u'Jamburg': u'Oni ne pafas en Jamburg',
        u'JuanReg': u'Serta gratulatoria in honorem Juan Régulo',
        u'JV': u'Jura Vortaro esperante-ruse-ukraine-angla',
        u'Kalendaro': u'La kalendaro tra la tempo, tra la spaco',
        u'KelS': u'Kajeroj el la Sudo',
        u'KielAkvo': u"Kiel akvo de l' rivero",
        u'Kiso': u'La Kiso kaj dek tri aliaj noveloj',
        u'KompLeks': u'Komputada Leksiko',
        u'Kosmo': u'La kosmo kaj ni ― Galaksioj, planedoj kaj vivo en la universo',
        u'KrDE': u'Wörterbuch Deutsch-Esperanto',
        u'KrED': u'Großes Wörterbuch Esperanto-Deutsch',
        u'Kukobak': u'Kukobakado',
        u'KVS': u'Komerca Vortaro Seslingva. Germana ― Angla ― Franca ― Itala ― Hispana ― Esperanta',
        u'LaFamilio': u'La Familio',
        u'LanLin': u'Landoj kaj lingvoj de la mon',
        u'Lanti': u'Vortoj de k-do Lanti',
        u'Lasu': u'Lasu min paroli plu!',
        u'LF': u'Literatura Foiro',
        u'Lkn': u'Leksara kolekto de ofte uzataj propraj nomoj',
        u'LOdE': u'La Ondo de Esperanto',
        u'LR': u'Lingvaj Respond',
        u'LSF': u'Lingvo, Stilo, Formo',
        u'LSV': u'„Liberiga Stelo“ al la Verdruĝul',
        u'LtE': u'La tuta Esperanto',
        u'Lusin': u'Noveloj de Lusin',
        u'Malben': u'Malbeno Kara',
        u'ManPol': u'Deklingva manlibro pri politiko',
        u'Marta': u'Marta',
        u'Mary': u'Princidino Mary',
        u'MatStokTerm': u'Matematika kaj Stokastika Terminaro Esperanta',
        u'MatTerm': u'Matematika Terminaro kaj Krestomatio',
        u'MatVort': u'Matematika Vortaro, Esperanta-Ĉeĥa-Germana',
        u'MB': u'Malbabelo',
        u'MemLapenna': u'Memore al Ivo Lapennaexample',
        u'Metrop': u'Metropoliteno',
        u'MEV': u'Maŝinfaka Esperanto-vortaro',
        u'MkM': u'La majstro kaj Margarita',
        u'Monato': u'Monato',
        u'MortulŜip': u'Mortula Ŝipo, Rakonto de usona maristo',
        u'MT': u'La Malnova Testamento',
        u'Munchhausen': u'[La Vojaĝoj kaj] Mirigaj Aventuroj de Barono Münchhausen',
        u'MuzTerm': u'Muzika terminaro (represo de la eldono fare de Internacia Esperanto-Ligo, 1944)',
        u'NeĝaBlovado': u'La neĝa blovado',
        u'NeoGlo': u'Neologisma glosaro, postrikolto al PIV',
        u'NePiv': u'Nepivaj vortoj',
        u'NT': u'La Nova Testamento',
        u'Oomoto': u'Oficiala organo de Oomoto kaj UHA',
        u'OriginoDeSpecioj': u'La Origino de Speci',
        u'OV': u'Originala Verka',
        u'Paroloj': u'Paroloj',
        u'PatrojFiloj': u'Patroj kaj filoj',
        u'PGl': u'Parnasa Gvidlibro',
        u'PIV1': u'Plena Ilustrita Vortaro',
        u'PIV2': u'La Nova Plena Ilustrita Vortaro',
        u'PIV3': u'Plena Ilustrita Vortaro de Esperanto 2005',
        u'Plumamikoj': u'Ne nur leteroj de plum-amikoj',
        u'PMEG': u'Plena Manlibro de Esperanta Gramati',
        u'PoŝAtlas': u'Poŝatlaso de la mondo',
        u'PrV': u'Proverbaro esperanta',
        u'PV': u'Plena Vortaro de Esperanto',
        u'RabistFab': u'La unua rabista fabe',
        u'Revadoj': u'La revadoj de soleca promenanto',
        u'Revizoro': u'La Revizo',
        u'RokPop': u'Roko kaj Popo, Popularmuzika Terminaro en Esperan',
        u'RugxDom': u'Ruĝdoma sonĝo',
        u'Salamandroj': u'Milito kontraŭ salamandr',
        u'SatirRak': u'Satiraj rakontoj',
        u'ScTerm': u'Scienca Fundamenta Esperanta Terminaro',
        u'SkandalJozef': u'La skandalo pro Jozefo',
        u'SPIV': u'Plena Vortaro de Esperanto, Suplemento',
        u'Ŝtalrato': u'Naskiĝo de la rustimuna ŝtalrato',
        u'Studoj': u'Studoj pri la Esperanta Literaturo',
        u'TermKurs': u'Terminologia Kurso',
        u'TK': u'Ilustrita terminaro de kombinita transporto, franca, angla, germana, esperanta, serba',
        u'TW': u'Technisches Wörterbuch Deutsch-Esperanto',
        u'UrdHadda': u'Urd Hadda murdita!',
        u'VdE': u'Vortaro de Esperanto',
        u'Vetero': u'Vetero kaj klimato de la mondo',
        u'Viki': u'Vikipedio',
        u'viki': u'Vikipedio',
        u'VivZam': u'Vivo de Zamenhof',
        u'VojaĝImp': u'Vojaĝimpresoj',
        u'Vojaĝo': u'Vojaĝo en Esperanto-lando',
        u'WAPS': u'Pajleroj kaj stoploj',
        u'WED': u'Esperanto Dictionary Esperanto-English, English-Esperanto',
        u'ZR': u'Zamenhof-radikaro'}

    if abbrev in bibliography_abbrevs:
        expansion = bibliography_abbrevs[abbrev]
    else:
        expansion = abbrev
        print "Warning: no expansion found for '%s'" % abbrev

    return clean_string(expansion)  # clean string to fix quotation marks and generic abbreviations
