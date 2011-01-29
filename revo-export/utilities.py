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
    string = string.replace('p.p.', 'parolante pri')
    string = string.replace('p. p.', 'parolante pri')
    string = string.replace('ktp', 'kaj tiel plu')
    string = string.replace('kp ', 'komparu ') # trailing space to avoid false positives
    string = string.replace('Kp ', 'Komparu ')
    string = string.replace('kp:', 'komparu:')
    string = string.replace('vd ', 'vidu ')
    string = string.replace('Vd ', 'Vidu ')

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

def expand_source_abbreviations(example_source):
    """Replace any abbreviations used for example sources with their
    exapdnsions.

    """
    if example_source == 'Z':
        example_source = 'Zamenhof'

    # trailing spaces to avoid false positives
    example_source = example_source.replace(u'Z ', u'Zamenhof')
    example_source = example_source.replace(u'90A', u'Naŭa Oficiala Aldono al la Universala Vortaro')
    example_source = example_source.replace(u'Aventuroj', u'Aventuroj de pioniro')
    example_source = example_source.replace(u'BazRad', u'Bazaj Radikoj Esperanto-Esperanto')
    example_source = example_source.replace(u'Bird', u'Oklingva nomaro de eŭropaj birdoj')
    example_source = example_source.replace(u'BoE', u'Entrepreno. Entreprenistaj Strategioj: Priskribo de la entrepreno')
    example_source = example_source.replace(u'BoER', u'Esperanta-rusa vortaro')
    example_source = example_source.replace(u'BoM', u'Mondkomerco kaj Lingvo')
    example_source = example_source.replace(u'BonaLingvo', u'La bona lingvo')
    example_source = example_source.replace(u'BonaS-ino', u'La bona sinjorino')
    example_source = example_source.replace(u'BoRE', u'Rusa-esperanta vortaro')
    example_source = example_source.replace(u'BoT', u'La Merkato de Trafikservoj')
    example_source = example_source.replace(u'BT', u'Biblioteka terminaro')
    example_source = example_source.replace(u'ĈA', u'Ĉina Antologio (1919-1949)')
    example_source = example_source.replace(u'CCT', u'Common Commercial Terms in English and Esperanto')
    example_source = example_source.replace(u'CEE', u'Comprehensive English-Esperanto Dictionary')
    example_source = example_source.replace(u'ChP', u'Profesia uzo de Esperanto kaj ĝiaj specifaj trajtoj')
    example_source = example_source.replace(u'Ĉukĉoj', u'El vivo de ĉukĉoj')
    example_source = example_source.replace(u'ĉuSn', u'Ĉu ili estas sennaciistoj?')
    example_source = example_source.replace(u'DanĝLng', u'La danĝera lingvo, studo pri la persekutoj kontraŭ Esperanto')
    example_source = example_source.replace(u'DdH', u'Aldono al la «Dogmoj de Hilelismo»')
    example_source = example_source.replace(u'Deneva', u'Esperanta-Bulgara-Rusa Matematika Terminaro')
    example_source = example_source.replace(u'DonKihxoto', u'La inĝenia hidalgo Don Quijote de la Mancha')
    example_source = example_source.replace(u'DOz', u'Doroteo kaj la Sorĉisto en Oz')
    example_source = example_source.replace(u'EBV', u'Esperanta Bildvortaro')
    example_source = example_source.replace(u'EdE', u'Enciklopedio de Esperanto')
    example_source = example_source.replace(u'EE', u'Esenco kaj Estonte')
    example_source = example_source.replace(u'Eek', u'Esperanto en Komerco. Esperanto in Commerce')
    example_source = example_source.replace(u'EFM', u'Economie, finance, monnaie. Glosaro de la komisiono de la Eŭropaj Komunumoj. Versio esperanto ― français ― english')
    example_source = example_source.replace(u'EKV', u'EK-Vortaro de matematikaj terminoj')
    example_source = example_source.replace(u'ElektFab', u'Elektitaj Fabeloj de Fratoj Grimm')
    example_source = example_source.replace(u'EncCxi', u'Enciklopedieto de Ĉinio')
    example_source = example_source.replace(u'EncJap', u'Enciklopedieto japana')
    example_source = example_source.replace(u'F', u'Fundamento de Esperanto')
    example_source = example_source.replace(u'Fab1', u'Fabeloj, vol. 1')
    example_source = example_source.replace(u'Fab2', u'Fabeloj, vol. 2')
    example_source = example_source.replace(u'Fab3', u'Fabeloj, vol. 3')
    example_source = example_source.replace(u'Fab4', u'Fabeloj, vol. 4')
    example_source = example_source.replace(u'Far1', u'La Faraono, vol. 1')
    example_source = example_source.replace(u'Far2', u'La Faraono, vol. 2')
    example_source = example_source.replace(u'Far3', u'La Faraono, vol. 3')
    example_source = example_source.replace(u'FIL', u"Pri la solvo de l'problemo de internacia lingvo por komerco kaj trafiko. Zur Lösung der Frage einer internationalen Handels- und Verkehrssprache. Amtlicher Sitzungsbericht der Internationalen Konferenz für eine gemeinsame Hilfssprache des Handels und Verkehrs, Venedig, 2.-4. April 1923")
    example_source = example_source.replace(u'FK', u'Fundamenta Krestomatio de la lingvo Esperanto')
    example_source = example_source.replace(u'FT', u'Fervoja Terminaro (UIC Railway Dictionary)')
    example_source = example_source.replace(u'FzT', u'Esperanta terminaro de fiziko, Esperanto ― japana ― angla. Reviziita')
    example_source = example_source.replace(u'GDFE', u'Grand dictionnaire français espéranto')
    example_source = example_source.replace(u'Gerda', u'Gerda malaperis')
    example_source = example_source.replace(u'Gv', u'La Gunkela vortaro de vortoj mankantaj en PIV 2002')
    example_source = example_source.replace(u'HejmVort', u'Hejma Vortaro')
    example_source = example_source.replace(u'IKEV', u'Internacia komerca-ekonomika vortaro en 11 lingvoj')
    example_source = example_source.replace(u'InfanTorent2', u'Infanoj en Torento, dua libro en la Torento-trilogio')
    example_source = example_source.replace(u'IntArkeol', u'Interesa arkeologio')
    example_source = example_source.replace(u'IntKui', u'Internacie kuiri')
    example_source = example_source.replace(u'Iŝtar', u'Pro Iŝtar')
    example_source = example_source.replace(u'ItEsp', u'Vocabolario Italiano-Esperanto')
    example_source = example_source.replace(u'Jamburg', u'Oni ne pafas en Jamburg')
    example_source = example_source.replace(u'JuanReg', u'Serta gratulatoria in honorem Juan Régulo')
    example_source = example_source.replace(u'JV', u'Jura Vortaro esperante-ruse-ukraine-angla')
    example_source = example_source.replace(u'Kalendaro', u'La kalendaro tra la tempo, tra la spaco')
    example_source = example_source.replace(u'KelS', u'Kajeroj el la Sudo')
    example_source = example_source.replace(u'KielAkvo', u"Kiel akvo de l' rivero")
    example_source = example_source.replace(u'Kiso', u'La Kiso kaj dek tri aliaj noveloj')
    example_source = example_source.replace(u'KompLeks', u'Komputada Leksiko')
    example_source = example_source.replace(u'Kosmo', u'La kosmo kaj ni ― Galaksioj, planedoj kaj vivo en la universo')
    example_source = example_source.replace(u'KrDE', u'Wörterbuch Deutsch-Esperanto')
    example_source = example_source.replace(u'KrED', u'Großes Wörterbuch Esperanto-Deutsch')
    example_source = example_source.replace(u'Kukobak', u'Kukobakado')
    example_source = example_source.replace(u'KVS', u'Komerca Vortaro Seslingva. Germana ― Angla ― Franca ― Itala ― Hispana ― Esperanta')
    example_source = example_source.replace(u'LaFamilio', u'La Familio')
    example_source = example_source.replace(u'LanLin', u'Landoj kaj lingvoj de la mon')
    example_source = example_source.replace(u'Lanti', u'Vortoj de k-do Lanti')
    example_source = example_source.replace(u'Lasu', u'Lasu min paroli plu!')
    example_source = example_source.replace(u'LF', u'Literatura Foiro')
    example_source = example_source.replace(u'Lkn', u'Leksara kolekto de ofte uzataj propraj nomoj')
    example_source = example_source.replace(u'LOdE', u'La Ondo de Esperanto')
    example_source = example_source.replace(u'LR', u'Lingvaj Respond')
    example_source = example_source.replace(u'LSF', u'Lingvo, Stilo, Formo')
    example_source = example_source.replace(u'LSV', u'„Liberiga Stelo“ al la Verdruĝul')
    example_source = example_source.replace(u'LtE', u'La tuta Esperanto')
    example_source = example_source.replace(u'Lusin', u'Noveloj de Lusin')
    example_source = example_source.replace(u'Malben', u'Malbeno Kara')
    example_source = example_source.replace(u'ManPol', u'Deklingva manlibro pri politiko')
    example_source = example_source.replace(u'Mary', u'Princidino Mary')    
    example_source = example_source.replace(u'MatStokTerm', u'Matematika kaj Stokastika Terminaro Esperanta')
    example_source = example_source.replace(u'MatTerm', u'Matematika Terminaro kaj Krestomatio')
    example_source = example_source.replace(u'MatVort', u'Matematika Vortaro, Esperanta-Ĉeĥa-Germana')
    example_source = example_source.replace(u'MB', u'Malbabelo')
    example_source = example_source.replace(u'MemLapenna', u'Memore al Ivo Lapennaexample')
    example_source = example_source.replace(u'Metrop', u'Metropoliteno')
    example_source = example_source.replace(u'MEV', u'Maŝinfaka Esperanto-vortaro')
    example_source = example_source.replace(u'MkM', u'La majstro kaj Margarita')
    example_source = example_source.replace(u'MortulŜip', u'Mortula Ŝipo, Rakonto de usona maristo')
    example_source = example_source.replace(u'MT', u'La Malnova Testamento')
    example_source = example_source.replace(u'Munchhausen', u'[La Vojaĝoj kaj] Mirigaj Aventuroj de Barono Münchhausen')
    example_source = example_source.replace(u'MuzTerm', u'Muzika terminaro (represo de la eldono fare de Internacia Esperanto-Ligo, 1944) ')
    example_source = example_source.replace(u'NeĝaBlovado', u'La neĝa blovado')
    example_source = example_source.replace(u'NeoGlo', u'Neologisma glosaro, postrikolto al PIV')
    example_source = example_source.replace(u'NePiv', u'Nepivaj vortoj')
    example_source = example_source.replace(u'NT', u'La Nova Testamento')
    example_source = example_source.replace(u'OriginoDeSpecioj', u'La Origino de Speci')
    example_source = example_source.replace(u'OV', u'Originala Verka')
    example_source = example_source.replace(u'PatrojFiloj', u'Patroj kaj filoj')
    example_source = example_source.replace(u'PGl', u'Parnasa Gvidlibro')
    example_source = example_source.replace(u'PIV1', u'Plena Ilustrita Vortaro')
    example_source = example_source.replace(u'PIV2', u'La Nova Plena Ilustrita Vortaro')
    example_source = example_source.replace(u'PIV3', u'Plena Ilustrita Vortaro de Esperanto 2005')
    example_source = example_source.replace(u'Plumamikoj', u'Ne nur leteroj de plum-amikoj')
    example_source = example_source.replace(u'PMEG', u'Plena Manlibro de Esperanta Gramati')
    example_source = example_source.replace(u'PoŝAtlas', u'Poŝatlaso de la mondo')
    example_source = example_source.replace(u'PrV', u'Proverbaro esperanta')
    example_source = example_source.replace(u'PV', u'Plena Vortaro de Esperanto')
    example_source = example_source.replace(u'RabistFab', u'La unua rabista fabe')
    example_source = example_source.replace(u'Revadoj', u'La revadoj de soleca promenanto')
    example_source = example_source.replace(u'Revizoro', u'La Revizo')
    example_source = example_source.replace(u'RokPop', u'Roko kaj Popo, Popularmuzika Terminaro en Esperan')
    example_source = example_source.replace(u'RugxDom', u'Ruĝdoma sonĝo')
    example_source = example_source.replace(u'Salamandroj', u'Milito kontraŭ salamandr')
    example_source = example_source.replace(u'SatirRak', u'Satiraj rakontoj')
    example_source = example_source.replace(u'ScTerm', u'Scienca Fundamenta Esperanta Terminaro')
    example_source = example_source.replace(u'SkandalJozef', u'La skandalo pro Jozefo')
    example_source = example_source.replace(u'SPIV', u'Plena Vortaro de Esperanto, Suplemento')
    example_source = example_source.replace(u'Ŝtalrato', u'Naskiĝo de la rustimuna ŝtalrato')
    example_source = example_source.replace(u'Studoj', u'Studoj pri la Esperanta Literaturo')
    example_source = example_source.replace(u'TermKurs', u'Terminologia Kurso')
    example_source = example_source.replace(u'TK', u'Ilustrita terminaro de kombinita transporto, franca, angla, germana, esperanta, serba')
    example_source = example_source.replace(u'TW', u'Technisches Wörterbuch Deutsch-Esperanto')
    example_source = example_source.replace(u'UrdHadda', u'Urd Hadda murdita!')
    example_source = example_source.replace(u'VdE', u'Vortaro de Esperanto')
    example_source = example_source.replace(u'Vetero', u'Vetero kaj klimato de la mondo')
    example_source = example_source.replace(u'Viki ', u'Vikipedio')
    example_source = example_source.replace(u'VojaĝImp', u'Vojaĝimpresoj')
    example_source = example_source.replace(u'Vojaĝo', u'Vojaĝo en Esperanto-lando')
    example_source = example_source.replace(u'WAPS', u'Pajleroj kaj stoploj')
    example_source = example_source.replace(u'WED', u'Esperanto Dictionary Esperanto-English, English-Esperanto')
    example_source = example_source.replace(u'ZR', u'Zamenhof-radikaro')

    return clean_string(example_source)  # clean string to fix quotation marks
