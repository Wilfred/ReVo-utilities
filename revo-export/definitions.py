# -*- coding: utf-8 -*-
import re
from collections import defaultdict

from utilities import clean_string
from words import get_words_from_kap
from flatten import flatten_node

class CrossReferences(object):
    def __init__(self):
        self.see = []
        self.see_also = []
        self.synonyms = []
        self.antonyms = []
        self.supernotions = []
        self.subnotions = []
        self.meronyms = [] # 'part of', e.g. branch is a meronym of tree
        self.holonyms = [] # 'has these as parts' e.g. tree is a holonym of branch

    def is_empty(self):
        if not (self.see or self.see_also or self.synonyms or
                self.antonyms or self.supernotions or
                self.subnotions):
            return True
        else:
            return False

    def add_reference(self, ref_node):
        # dif=difino i.e. this word is defined elsewhere
        if ref_node.attrib.get('tip') == 'dif':
            self.see.append(flatten_node(ref_node))

        # vid=vidu ankaŭ
        elif ref_node.attrib.get('tip') == 'vid':
            self.see_also.append(flatten_node(ref_node))

        # sin=sinonimo
        elif ref_node.attrib.get('tip') == 'sin':
            self.synonyms.append(flatten_node(ref_node))

        # ant=antonimo
        elif ref_node.attrib.get('tip') == 'ant':
            self.antonyms.append(flatten_node(ref_node))

        # super=supernocio
        elif ref_node.attrib.get('tip') == 'super':
            self.supernotions.append(flatten_node(ref_node))

        # sub=subnocio
        elif ref_node.attrib.get('tip') == 'sub':
            self.subnotions.append(flatten_node(ref_node))

        # prt=parto de
        elif ref_node.attrib.get('tip') == 'prt':
            self.meronyms.append(flatten_node(ref_node))

        # malprt=malparto de, aŭ 'konsistas el'
        elif ref_node.attrib.get('tip') == 'malprt':
            self.holonyms.append(flatten_node(ref_node))

        # hom=homonimo
        # (we ignore hononyms since we collect all the definitions together
        # so the cross-reference is unnecessary)
        elif ref_node.attrib.get('tip') == 'hom':
            pass

        # ignore unlabelled references
        elif ref_node.attrib.get('tip') is None:
            pass

        # TODO: we can probably do something useful with these.
        # "lst" and "val" refer to word lists, see vokoxml.dtd.
        elif ref_node.attrib.get('tip') in ['lst', 'val']:
            pass
        # ekz=ekzemplo presumably.
        elif ref_node.attrib.get('tip') == 'ekz':
            pass

        else:
            assert False, "Found an unknown reference type: %s" % ref_node.attrib.get('tip')

    def add_reference_group(self, refgrp_node):
        # dif=difino i.e. this word is defined elsewhere
        if refgrp_node.attrib.get('tip') == 'dif':
            for ref_node in refgrp_node.findall('ref'):
                self.see.append(flatten_node(ref_node))

        # vid=vidu ankaŭ
        elif refgrp_node.attrib.get('tip') == 'vid':
            for ref_node in refgrp_node.findall('ref'):
                self.see_also.append(flatten_node(ref_node))

        # sin=sinonimo
        elif refgrp_node.attrib.get('tip') == 'sin':
            for ref_node in refgrp_node.findall('ref'):
                self.synonyms.append(flatten_node(ref_node))

        # ant=antonimo
        elif refgrp_node.attrib.get('tip') == 'ant':
            for ref_node in refgrp_node.findall('ref'):
                self.antonyms.append(flatten_node(ref_node))

        # super=supernocio
        elif refgrp_node.attrib.get('tip') == 'super':
            for ref_node in refgrp_node.findall('ref'):
                self.supernotions.append(flatten_node(ref_node))

        # sub=subnocio
        elif refgrp_node.attrib.get('tip') == 'sub':
            for ref_node in refgrp_node.findall('ref'):
                self.subnotions.append(flatten_node(ref_node))

        # prt=parto de
        elif refgrp_node.attrib.get('tip') == 'prt':
            for ref_node in refgrp_node.findall('ref'):
                self.meronyms.append(flatten_node(ref_node))

        # malprt=malparto de, aŭ 'konsistas el'
        elif refgrp_node.attrib.get('tip') == 'malprt':
            for ref_node in refgrp_node.findall('ref'):
                self.holonyms.append(flatten_node(ref_node))

        # hom=homonimo
        # (we ignore hononyms since we collect all the definitions together
        # so the cross-reference is unnecessary)
        elif refgrp_node.attrib.get('tip') == 'hom':
            pass

        # ignore unlabelled references
        elif refgrp_node.attrib.get('tip') is None:
            pass

        else:
            assert False, "Found an unknown reference type: %s" % ref_node.attrib.get('tip')


class Definition(object):
    """Every definition consists of a primary definition (either a
    non-empty string or None) and optionally subdefinitions and/or
    remarks. Note we never have subsubdefinitions.

    """
    def __init__(self, primary_definition=None):
        self.primary = primary_definition

        self.subdefinitions = []
        self.examples = []
        self.remarks = []
        self.translations = {}
        self.cross_references = CrossReferences()

    def __eq__(self, other):
        if self.primary != other.primary:
            return False
        if self.subdefinitions != other.subdefinitions:
            return False
        if self.examples != other.examples:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_empty(self):
        if (not self.primary and not self.subdefinitions and
            not self.examples and self.cross_references.is_empty()):
            return True
        return False

    def get_all(self):
        """Convenience function for JSON export."""
        # call get_all on all child definitions
        subdefinitions = [definition.get_all() for definition in
                          self.subdefinitions]
        # no subsubdefinitions (they're empty anyway
        for subdefinition in subdefinitions:
            del subdefinition['subdefinitions']

        return {'primary definition': self.primary, 
                'examples': self.examples, 
                'subdefinitions': subdefinitions,
                'remarks': self.remarks,
                'translations': self.translations}

    def to_string(self):
        return self.primary

def flatten_definition(dif_node):
    """Convert a definition node to a simple unicode string (this
    requires us to flatten it), and handle any references or
    clarifications we encounter.

    An example:

    <dif>
      <klr>(de <ref cel="polino.0o">polinomo</ref>)</klr>
      <ref tip="super" cel="nul0.0iganto.de_funkcio">Nuliganto</ref>
      de la responda <ref cel="funkci.polinoma0o">polinoma funkcio</ref>.
    </dif>
    (from radik.xml)

    """
    # skip examples, they're dealt with elsewhere
    definition = flatten_node(dif_node, skip_tags=['ekz'])

    # if this definition has examples, it ends with a colon not a full stop
    # but since we format examples separately, replace the colon
    if definition.endswith(':'):
        definition = definition[:-1].strip() + '.'

    return definition

def get_transitivity(node):
    """Return a string stating that this node represents a transitive or
    intransitive verb, if that data was found. Otherwise return None.

    """
    for gra_node in node.findall('gra'):
        if gra_node.text in ["sensubjekta", "sensubjekte"]:
            return "(sensubjekta)"

        vspec_node = gra_node.find('vspec')
        assert vspec_node is not None, 'Expected vspec inside <gra>'
        if vspec_node.text == 'tr':
            return "(transitiva)"
        elif vspec_node.text == 'ntr':
            return "(netransitiva)"
        else:
            return None # adv (presumable adverb) and so on

    return None

def flatten_example(ekz_node):
    """Get the contents of an <ekz>, discarding examples sources
    (<fnt>s). Since a series of examples are often written in the form
    'foo; bar; baz.' we also discard trailing full stops or
    semicolons.

    An example:

    <ekz>
      kion vi legas mia princo? <tld/>ojn, <tld/>ojn, <tld/>ojn
      <fnt>Z</fnt>!
    </ekz>
    (from vort.xml)

    <ekz>
      <tld/>o de reno
    </ekz>;
    (from ablaci.xml)

    <ekz>
      en via decembra numero trovi&gcirc;as sub la <tld/>o <ctl>&Scirc;erco kaj
      satiro</ctl> &leftquot;publika letero&rightquot;<fnt><aut>Reinhard
      F&ouml;&szlig;meier</aut>:
      <vrk>Netrafa adreso</vrk>, <bib>Monato</bib><lok>jaro 2002a,
      numero 2a, p. 7a</lok></fnt>.
    </ekz>
    (from rubrik.xml, mixing quote types)

    """
    # klr = klarigo = clarification, ideally we'd extract this
    # and format it appropriately on the frontend (TODO)
    # <fnt> is example attribution, which we ignore
    # <uzo> indicates topic to which this examples relates
    example = flatten_node(ekz_node,
                           skip_tags=['fnt', 'klr', 'uzo', 
                                      'trd', 'trdgrp'])

    # remove trailing semicolon/full stop due to the examples being
    # written as a series
    if example.endswith(';') or example.endswith('.'):
        example = example[:-1]

    # if we didn't extract anything with letters in (e.g. only
    # references that we discarded), return an empty string
    if not re.search(u'[a-zĉĝĥĵŝ]', example,
                     flags=re.UNICODE+re.IGNORECASE):
        return ""

    source = None
    # there's probably only one <fnt>, but this loop is easy and robust
    for fnt_node in ekz_node.findall('fnt'):
        source = flatten_node(fnt_node)

    return (example, source)

def get_examples(node):
    """Get all examples from the children of a node. Examples tend to
    be in <dif>s, and take the following form:

    <ekz>
      simpla, kunmetita, dubsenca <tld/>o;
    </ekz><ekz>
      uzi la &gcirc;ustan, konvenan <tld/>on;
    </ekz><ekz>
      la bildoj elvokitaj de la <tld/>oj;
    </ekz><ekz>
      <tld/>ordo.
    </ekz>
    (from vort.xml)

    Sometimes (bizarrely) examples spread across several <ekz> nodes:

    <ekz>
      <tld/>i al si plezuron<fnt>Z</fnt>;
    </ekz><ekz>
      <tld/>i instruon<fnt>Z</fnt>,
    </ekz><ekz>
      amikecon<fnt>Z</fnt>,
    [...]
    (from sercx.xml)

    Sometimes only references, which we discard:

    <ekz>
      <ref tip="sub" cel="bier.0o">biero</ref>, 
      <ref tip="sub" cel="brand.0o">brando</ref>,
      <ref tip="sub" cel="vin.0o">vino</ref> 
    </ekz>
    (from alkoho.xml)

    <subsnc mrk="afekt.0o.sxajnigi" ref="afekt.0i.sxajnigi">
      <ekz>
        kiom a&ccirc;as la <tld/>o komplezi al duonvivul'
    (from afekt.xml)

    """
    raw_examples = []

    # examples tend to be on <dif>s
    for dif_node in node.findall('dif'):
        for ekz_node in dif_node.findall('ekz'):
            raw_example = flatten_example(ekz_node)
            if raw_example:
                raw_examples.append(raw_example)

    # but examples can also be on the <snc>/<subsnc> itself
    # (or even a <drv>!)
    for ekz_node in node.findall('ekz'):
        raw_example = flatten_example(ekz_node)
        if raw_example:
            raw_examples.append(raw_example)

    # fix examples spread over multiple <ekz>s by concatenating each
    # example that ends with a comma with the next example
    examples = []
    example_string = ""
    for (example, source) in raw_examples:
        example_string += ' ' + example

        if not example_string.endswith(','):
            examples.append((clean_string(example_string), source))
            example_string = ""

    if example_string != "":
        art_node = ekz_node.iterancestors('art').next()
        kap_node = art_node.iter('kap').next()
        word = get_words_from_kap(kap_node)[0]
        print ("Warning: example for %r ended with comma: %r" %
               (word, clean_string(example_string)))
            
    return examples

def get_translations(node):
    """Get all translations attached directly to this node.

    """
    assert node.tag in ['snc', 'subsnc', 'drv', 'subdrv']

    # a dict that defaults to empty list if that key isn't present
    translations = defaultdict(list)

    for trd_node in node.findall('trd'):
        language_code = trd_node.attrib['lng']
        foreign_word = flatten_node(trd_node)
        translations[language_code].append(foreign_word)

    for trdgrp_node in node.findall('trdgrp'):
        language_code = trdgrp_node.attrib['lng']

        for trd_node in trdgrp_node.findall('trd'):
            foreign_word = flatten_node(trd_node)
            if foreign_word.endswith(';'):
                foreign_word = foreign_word[:-1]

            translations[language_code].append(foreign_word)

    return translations

def get_subdefinition(subsnc_node):
    """Get a Definition object representing this subdefinition, including
    any examples and/or translations present.

    """
    subdefinition = Definition()

    # either a dif or a ref to another word
    dif_node = subsnc_node.find('dif')
    if dif_node is not None:
        subdefinition.primary = flatten_definition(dif_node)

    # cross-references
    for child in subsnc_node.getchildren():
        # we avoid grandchildren to make sure add_reference_group handles them
        if child.tag == 'ref':
            subdefinition.cross_references.add_reference(child)
        elif child.tag == 'refgrp':
            subdefinition.cross_references.add_reference_group(child)

    subdefinition.examples = get_examples(subsnc_node)
    subdefinition.translations = get_translations(subsnc_node)

    return subdefinition

def get_definition_notes(node):
    """Whether a word is figurative or not, and whether or not it is
    transitive are both written outside the <dif>. Here we get this
    data and return a string.

    """
    assert node.tag in ['drv', 'snc']

    notes = ''

    # add figurative note if present
    uzo_node = node.find('uzo')
    if uzo_node is not None:
        if uzo_node.text.strip().lower() == 'fig':
            notes = '(figure) '

    # add transitivity notes if present, could be on <snc> or on <drv>
    transitivity = get_transitivity(node)
    if not transitivity:
        transitivity = get_transitivity(node.getparent())
    if transitivity:
        notes = transitivity + ' ' + notes

    return notes

def get_definition(snc_node):
    """Build a Definition from this <snc> and add any subdefinitions if
    present, any examples if present and any remarks if present.

    Every <snc> contains a primary definition (a <dif>), a reference
    (i.e. a 'see foo' definition, a <ref>) or subdefinitions (<dif>s
    inside <subsnc>s).

    Worth testing pur.xml, since <snc> may have <dif> as a sibling
    rather than a child.

    An example:

    <dif>
      <ekz>
        lingva <tld/>a&jcirc;o<fnt>Z</fnt>;
      </ekz>
      <ekz>
        rimaj <tld/>a&jcirc;oj.
      </ekz>
    </dif>
    (from akroba.xml)

    <snc mrk="sekv.0i.dividi_opinion">
      <uzo tip="stl">FIG</uzo>
      <dif>
        Dividi ies opinion, morojn, konduton; alpreni kiel modelon,
        mastron:
        <ekz>
          kaj Barak vokis la Zebulunidojn kaj la Naftaliidojn al Kede&scirc;,
          kaj lin <tld/>is dek mil viroj
          <fnt><bib>MT</bib><lok>&Jug; 4:10</lok></fnt>;
        </ekz>
        <ekz>
          ne <tld/>u aliajn diojn el la dioj de la popoloj,
          kiuj estas &ccirc;irka&ubreve; vi
          <fnt><bib>MT</bib><lok>&Rea; 6:14</lok></fnt>;
        </ekz>
        <ekz>
          ne <tld/>u malbonajn homojn, kaj ne deziru esti kun ili
          <fnt><bib>MT</bib><lok>&Sen; 24:1</lok></fnt>.
        </ekz>
      </dif>
    </snc>
    (from sekv.xml)

    <snc>
      <dif>
        Neoficiala sufikso, uzata por nomi
        <ref tip="vid" cel="famili.0o.BIO">familiojn</ref>
        la&ubreve; la botanika nomenklaturo.
        La sufikso apliki&gcirc;as al genro el la familio
        por formi la familinomon:
        <ekz>
          La rozo apartenas al la familio rozacoj.
        </ekz>
      </dif>
      <rim num="1">
        Al kiu genro apliki&gcirc;as la sufikso por nomi la
        familion, estas difinite de la internacia botanika
        nomenklaturo.
      </rim>
      <rim num="2">
        Povas okazi, ke tiu genro ne plu ekzistas, &ccirc;ar
        pro novaj esploroj &gcirc;iaj specioj estas ordigitaj
        sub aliaj genroj.
        <refgrp tip="vid">
          <ref cel="fabac.0oj">fabacoj</ref>,
          <ref cel="kaprif1.0oj">kaprifoliacoj</ref> k.a.
        </refgrp>
      </rim>
      [...]
    </snc>
    (from ac.xml)

    """
    # we gradually populate the Definition
    definition = Definition()

    # get the primary definition itself
    for dif_node in snc_node.findall('dif'):
        definition.primary = flatten_definition(dif_node)

    # get examples of this definition, regardless of position
    definition.examples = get_examples(snc_node)

    # may have a <ref> that points to another word
    for ref_node in snc_node.findall('ref'):
        definition.cross_references.add_reference(ref_node)
    for refgrp_node in snc_node.findall('refgrp'):
        definition.cross_references.add_reference(refgrp_node)

    # note: may have only <subsnc>, no <dif> or <ref>
    # (e.g. sxilin.xml)

    # prepend any notes (transitivity etc)
    notes = get_definition_notes(snc_node)
    if notes and definition.primary:
        definition.primary = notes + definition.primary

    # get any subdefinitions
    for child in snc_node.findall('subsnc'):
        definition.subdefinitions.append(get_subdefinition(child))

    # get any remarks
    for rim_node in snc_node.findall('rim'):
        definition.remarks.append(flatten_node(rim_node,
                                               skip_tags=['aut', 'fnt']))

    # get all translations
    definition.translations = get_translations(snc_node)

    # final sanity check: do we have *something* for this word?
    if definition.is_empty():
        kap_node = snc_node.getparent().find('kap')
        print "Warning: no data found for %r" % (get_words_from_kap(kap_node)[0],)

    return definition

def get_definition_from_subdrvs(subdrv_nodes):
    """For a given <subdrv>, which seems to represent a single
    definition with children, get a definition.

    """
    assert len(subdrv_nodes) > 0

    definition = Definition()

    subdrv_node = subdrv_nodes[0]
    assert len(subdrv_node.findall('dif')) <= 1, "Expected at most one <dif> on a <subdrv>"

    if subdrv_node.findall('dif'):
        definition.primary = flatten_definition(subdrv_node.findall('dif')[0])

    # the rest should be normal <snc>s
    for subdrv_node in subdrv_nodes:
        for snc_node in subdrv_node.findall('snc'):
            subdefinition = get_definition(snc_node)
            subdefinition.translations = get_translations(subdrv_node)
            definition.subdefinitions.append(subdefinition)

    return definition

def get_subdefinitions_from_subdrv(subdrv_node):
    """Sometimes, frustratingly, we have a <snc>s with <dif>s and
    <subsnc>s which themselves have <dif>s. We use a heuristic where
    we only use the leaf nodes of this crazy structure.

    """
    subdefinitions = []

    for snc_node in subdrv_node.findall('snc'):
        subsenses = snc_node.findall('subsnc')
        if not subsenses:
            subdefinitions.append(get_definition(snc_node))
        else:
            for subsnc_node in subsenses:
                subdefinitions.append(get_subdefinition(subsnc_node))

    return subdefinitions

def get_all_definitions(drv_node):
    """For a given entry (which is a single <drv> node), get all its
    definitions. I have tested this as far as possible but bugs may
    remain given the complexity and variability of the XML.

    Generally, a primary definition is a <dif> inside a <snc> and a
    subdefinition is a <dif> inside a <subsnc> inside a <snc>.

    Some representative examples are:
    sxiling.xml and vort.xml for subsenses
    apetit.xml for notes that the term is figurative
    jakobi1.xml only <ref> inside <snc>, no <dif> node
    frakci.xml only <ref> inside <snc> but huge and complex
    ad.xml has a load of stuff, some of which is not documented by ReVo
    akusx.xml has <ref> and no <snc> on akusxigisistino

    """
    assert drv_node.tag in ['drv', 'subdrv']

    definitions = []

    # if <dif> is outside <snc>, treat <snc>s as subsenses
    # (yes, this isn't simple)
    for dif_node in drv_node.findall('dif'):
        # outside a <snc> we do not have subdefinitions
        definition_string = flatten_definition(dif_node)
        definition_string = get_definition_notes(drv_node) + definition_string
        definitions.append(Definition(definition_string))

    # the common case, get definitions on <snc>s
    for snc_node in drv_node.findall('snc'):
        definitions.append(get_definition(snc_node))

    # there may just be a <ref> (normally these are inside <snc>s)
    for ref_node in drv_node.findall('ref'):
        # ignore malprt which (e.g. saluti, pluralo) just comes in awkward places
        if not ref_node.attrib.get('tip') in ['malprt', 'sub']:
            definition_string = flatten_node(ref_node)
            definitions.append(Definition(definition_string))

    # or similarly may be just a <refgrp>
    for refgrp_node in drv_node.findall('refgrp'):
        # ignore malprt which (e.g. saluti, pluralo) just comes in awkward places
        if not refgrp_node.attrib.get('tip') in ['malprt', 'sub']:
            definition_string = flatten_node(refgrp_node)
            definitions.append(Definition(definition_string))

    # get any remarks which aren't on <dif>s and assign them
    # (arbitrarily) to the first definition. This happens so rarely
    # (e.g. abdiko) that the loss of clarity is negligible.
    rim_nodes = []
    for rim_node in drv_node.findall('rim'):
        rim_nodes.append(flatten_node(rim_node, skip_tags=['aut', 'fnt']))

    if rim_nodes:
        definitions[0].remarks = rim_nodes

    # get any examples which are just on the <drv> (rare, e.g. 'pluralo')
    examples = get_examples(drv_node)
    if examples:
        definitions[0].examples.extend(examples)

    # get any translations which are just on the <drv>
    translations = get_translations(drv_node)
    if translations and definitions:
        definitions[0].translations.update(translations)

    # get any definitions which are in a subdrv:
    # if we've already started on a definition, we add to it
    if definitions:
        for subdrv_node in drv_node.findall('subdrv'):
            subdefinitions = get_subdefinitions_from_subdrv(subdrv_node)
            definitions[0].subdefinitions.extend(subdefinitions)
    else:
        subdrv_nodes = drv_node.findall('subdrv')
        if subdrv_nodes:
            definitions.append(get_definition_from_subdrvs(subdrv_nodes))

    # remove any duplicates (happens with multiple <ref>s
    # e.g. direkt3.xml) or empty definitions (happens with example
    # only senses, such as purigi in pur.xml)
    no_duplicates = []
    for definition in definitions:
        if definition not in no_duplicates and not definition.is_empty():
            no_duplicates.append(definition)
    
    return no_duplicates
