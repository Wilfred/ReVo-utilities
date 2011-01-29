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
    example_source = example_source.replace(u'MT', u'La Malnova Testamento')
    example_source = example_source.replace(u'LOdE', u'La Ondo de Esperanto')
    example_source = example_source.replace(u'Viki ', u'Vikipedio')
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

    return example_source
