# -*- coding: utf-8 -*-
import re

from words import get_words_from_kap, tld_to_string
from utilities import clean_string
from flatten import flatten_node

class Definition:
    """Every definition consists of a primary definition (either a
    non-empty string or None) and optionally subdefinitions and/or
    remarks. Note we never have subsubdefinitions.

    """
    def __init__(self, primary_definition=None):
        self.primary = primary_definition

        self.subdefinitions = []
        self.examples = []
        self.remarks = []

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
        if not self.primary and not self.subdefinitions == [] and \
                not self.examples:
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
                'remarks': self.remarks}

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

    An example which tests adding full stops:

    <dif>
      Io, kio <tld/>as <sncref ref="sekv.0i.rezulti"/>:
      <ekz>
        tio estas tute natura <tld/>o<fnt>Z</fnt>;
      </ekz>
      <ekz>
        li ne povis distingi, &ccirc;u <klr>[la varmego]</klr>
        estas <tld/>o de la efektiva fajro, &ccirc;u de lia tro
        granda ardo de amo
        <fnt><bib>Fab1</bib><lok>Persista stana soldato</lok></fnt>;
      </ekz>
      <ekz>
        <ind><tld/>ori&ccirc;a</ind> sukceso.
        <trd lng="fr">riche de <ind>cons&eacute;quences</ind></trd>
      </ekz>
    </dif>
    (from sekv.xml)

    """
    definition = ""

    if dif_node.text is not None:
        definition += dif_node.text
    for node in dif_node:
        if node.tag == 'ekz':
            # skip examples, they're dealt with elsewhere
            continue

        if node.tag == 'tld':
            definition += tld_to_string(node)
        elif node.tag == 'refgrp':
            definition += flatten_node(node)
        elif node.tag == 'ref' and node.attrib.get('tip') == 'dif':
            definition += flatten_node(node)
        elif node.tag == 'klr':
            definition += flatten_node(node)
        else:
            if node.text is not None:
                definition += node.text

        if node.tail is not None:
            definition += node.tail
    
    final_string = clean_string(definition)

    # if this definition has examples, it ends with a colon not a full stop
    # however we don't want those as we deal with examples separately
    if final_string.endswith(':'):
        final_string = final_string[:-1].strip() + '.'

    return final_string

def get_transitivity(node):
    """Return a string stating that this node represents a transitive
    or intransitive verb, if that data found. Otherwise return None.

    """
    for child in node.getchildren():
        if child.tag == 'gra':
            vspec_node = child.getchildren()[0]
            assert vspec_node.tag == 'vspec', 'Expected vspec inside <gra>'
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
    flat_string = flatten_node(ekz_node, skip_tags=['fnt', 'klr', 'uzo'])

    # remove trailing semicolon/full stop due to the examples being
    # written as a series
    if flat_string.endswith(';') or flat_string.endswith('.'):
        flat_string = flat_string[:-1]

    # if we didn't extract anything with letters in (e.g. only
    # references that we discarded), return an empty string
    if not re.search(u'[a-zĉĝĥĵŝ]', flat_string,
                     flags=re.UNICODE+re.IGNORECASE):
        return ""

    return flat_string

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
    for ekz_node in node.findall('ekz'):
        raw_example = flatten_example(ekz_node)
        if raw_example:
            raw_examples.append(raw_example)

    # fix examples spread over multiple <ekz>s by concatenating each
    # example that ends with a comma with the next example
    examples = []
    example_string = ""
    for example in raw_examples:
        example_string += ' ' + example

        if not example_string.endswith(','):
            examples.append(clean_string(example_string))
            example_string = ""

    if example_string != "":
        print "Warning: example ended with comma."
            
    return examples

def get_subdefinition(subsnc_node):
    """Get a Definition object representing this subdefinition, including
    any examples found.

    """
    subdefinition = Definition()

    # either a dif or a ref to another word
    dif_node = subsnc_node.find('dif')
    if dif_node is not None:
        subdefinition.primary = flatten_definition(dif_node)
    else:
        for child in subsnc_node.getchildren():
            if child.tag == 'ref' and child.attrib.get('tip') == 'dif':
                subdefinition.primary = flatten_node(child)
                break

    subdefinition.examples = get_examples(subsnc_node)

    return subdefinition

def get_definition_notes(node):
    """Whether a word is figurative or not, and whether or not it is
    transitive are both written outside the <dif>. Here we get this
    data and return a string.

    """
    assert node.tag == 'drv' or node.tag == 'snc'

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

def get_remark(rim_node):
    """Get a string representing the remark in this node.

    Example input:

    <rim>
      La vorto aperas en la Fundamento nur en la formo
      <ctl>L. L. Zamenhof</ctl>.
    </rim>
    (from zamenhof.xml)

    """
    assert rim_node is not None

    remark = "Rimarko: "
    for child in rim_node.iterdescendants():
        if child.tag == 'ctl':
            remark += u'«' + child.text + u'»'
        if child.text:
            remark += child.text
        if child.tail:
            remark += child.tail

    return clean_string(remark)

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
    # TODO: use generic flattener instead

    # we gradually populate the Definition
    definition = Definition()

    # get the primary definition itself
    for dif_node in snc_node.findall('dif'):
        definition.primary = flatten_definition(dif_node)

    # get examples of this definition, regardless of position
    definition.examples = get_examples(snc_node)

    # may have a <ref> that points to another word
    for ref_node in snc_node.findall('ref'):
        if definition.primary:
            definition.primary += ' ' + flatten_node(ref_node)
        else:
            definition.primary = flatten_node(ref_node)

    # may have <ref>s in a group
    for refgrp_node in snc_node.findall('refgrp'):
        if definition.primary:
            definition.primary += ' ' + flatten_node(refgrp_node)
        else:
            definition.primary = flatten_node(refgrp_node)

    # note: may have only <subsnc>, no <dif> or <ref>
    # (e.g. sxilin.xml)

    notes = get_definition_notes(snc_node)
    if notes and definition.primary:
        definition.primary = notes + definition.primary

    # get any subdefinitions
    for child in snc_node.findall('subsnc'):
        definition.subdefinitions.append(get_subdefinition(child))

    # get any remarks
    for rim_node in snc_node.findall('rim'):
        definition.remarks.append(flatten_node(rim_node))

    # final sanity check: do we have *something* for this word?
    if definition.primary == '' and definition.subdefinitions == [] \
            and definition.examples == []:
        kap_node = snc_node.getparent().find('kap')
        print "Warning: no data found for " + get_words_from_kap(kap_node)[0]

    return definition

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
    assert drv_node.tag == 'drv'

    definitions = []

    # if <dif> is outside <snc>, treat <snc>s as subsenses
    # there may be a definition outside of a <snc> (yes, this isn't simple)
    for dif_node in drv_node.findall('dif'):
        # outside a <snc> we do not have subdefinitions
        definition_string = flatten_definition(dif_node)
        definition_string = get_definition_notes(drv_node) + definition_string
        definitions.append(Definition(definition_string))

    # the common case, get definitions on <snc>s
    for snc_node in drv_node.findall('snc'):
        definitions.append(get_definition(snc_node))

    # there may just be a <ref> (normally these are inside <snc>s)
    # TODO: make this work, handling all the <refgrp> types

    # get any remarks which aren't on <dif>s and assign them
    # (arbitrarily) to the first definition. This happens so rarely
    # (e.g. abdiko) that the loss of clarity is negligible.
    rim_nodes = []
    for rim_node in drv_node.findall('rim'):
        rim_nodes.append(rim_node)

    # TODO: we won't need to check once we are extracting references reliably
    if len(definitions) < 0:
        definitions[0].remarks = rim_nodes

    # remove any duplicates (happens with multiple <ref>s
    # e.g. direkt3.xml) or empty definitions (happens with example
    # only senses, such as purigi in pur.xml)
    no_duplicates = []
    for definition in definitions:
        if definition not in no_duplicates and not definition.is_empty():
            no_duplicates.append(definition)
    
    return no_duplicates
