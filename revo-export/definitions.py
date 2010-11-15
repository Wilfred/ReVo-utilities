# -*- coding: utf-8 -*-
import re

from utilities import clean_string
from words import get_word_root, get_words_from_kap, tld_to_string

class Definition:
    """Every definition consists of a primary definition (either a
    non-empty string or None) and optionally subdefinitions. Note we
    never have subsubdefinitions.

    """
    def __init__(self, primary_definition=None, subdefinitions=None,
                 examples=None):
        self.primary = primary_definition

        if subdefinitions is None:
            self.subdefinitions = []
        else:
            self.subdefinitions = subdefinitions

        if examples is None:
            self.examples = []
        else:
            self.examples = examples

    def __eq__(self, other):
        if self.primary != other.primary:
            return False
        if self.subdefinitions != other.subdefinitions:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_empty(self):
        if self.primary is None and self.subdefinitions == []:
            return True
        return False

    def get_all(self):
        """Convenience function for JSON export."""
        subdefinitions = [definition.get_all() for definition in
                          self.subdefinitions]
        for subdefinition in subdefinitions:
            del subdefinition['subdefinitions'] # no subsubdefinitions

        return {'primary definition': self.primary, 
                'examples': self.examples, 
                'subdefinitions': subdefinitions}

def get_reference_to_another(ref_node):
    """If a word is only defined by a reference to another (a <ref>),
    return a string that describes the reference. Note that there are other
    ways in which <ref> are used which are not relevant here.

    """
    assert ref_node.attrib['tip'] == 'dif' or ref_node.tag == 'refgrp'
    
    reference = ""

    if ref_node.text:
        reference += ref_node.text
    for node in ref_node:
        if node.tag == 'tld':
            reference += get_word_root(node)
        if node.text is not None:
            reference += node.text
        if node.tail is not None:
            reference += node.tail

    reference = "Vidu: " + reference.strip()
    if not reference.endswith('.'):
        reference += '.'

    return reference

def flatten_clarification(klr_node):
    """Convert a <klr> (klarigo = clarification) to a flat piece of
    text. This may contain <ref>s.

    An example:

    <klr>(de <ref cel="polino.0o">polinomo</ref>)</klr>

    """
    flat_text = ""

    if klr_node.text:
        flat_text += klr_node.text

    for child in klr_node:
        if child.text:
            flat_text += child.text
        if child.tail:
            flat_text += child.tail

    return clean_string(flat_text)

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
            definition += get_word_root(node)
        elif node.tag == 'refgrp':
            definition += get_reference_to_another(node)
        elif node.tag == 'ref' and 'tip' in node.attrib \
                and node.attrib['tip'] == 'dif':
            definition += get_reference_to_another(node)
        elif node.tag == 'klr':
            definition += flatten_clarification(node)
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
    assert node.tag == 'drv' or node.tag == 'snc'

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
    """Get the contents of an <ekz>, discarding <fnt> but replacing
    <tld>. Since a series of examples are often written in the form
    'foo; bar; baz.' we also discard trailing full stops or
    semicolons.

    An example:

    <ekz>
      kion vi legas mia princo? <tld/>ojn, <tld/>ojn, <tld/>ojn
      <fnt>Z</fnt>!
    </ekz>

    <ekz>
      <ctl>popolo</ctl>, <ctl>foliaro</ctl>, <ctl>herbo</ctl>,
      <ctl>armeo</ctl> estas ar<tld/>oj.
    </ekz>
    (both from vort.xml)

    <ekz>
      <tld/>o de reno
    </ekz>;
    (from ablaci.xml)

    <ekz>
      <ind>saluton!</ind>
      [...]
    </ekz>
    (from salut.xml)

    <ekz>
      en via decembra numero trovi&gcirc;as sub la <tld/>o <ctl>&Scirc;erco kaj
      satiro</ctl> &leftquot;publika letero&rightquot;<fnt><aut>Reinhard
      F&ouml;&szlig;meier</aut>:
      <vrk>Netrafa adreso</vrk>, <bib>Monato</bib><lok>jaro 2002a,
      numero 2a, p. 7a</lok></fnt>.
    </ekz>
    (from rubrik.xml, mixing quote types)

    """
    flat_string = ""

    if ekz_node.text:
        flat_string += ekz_node.text

    # get example data from relevant nodes
    for child in ekz_node.getchildren():
        if child.tag == 'tld':
            flat_string += tld_to_string(child)
        if child.tag == 'ctl':
            # ctl = citilo = quotation mark, we use the same as vikipedio
            flat_string += u"«%s»" % child.text

        if child.tag == 'ind':
            # relates to a ReVo index somehow, purpose is not relevant
            # but contains part of the example and can contain <tld>s
            # and other stuff (<fnt>, <trd>)
            if child.text:
                flat_string += child.text
            for grandchild in child.getchildren():
                if grandchild.tag == 'tld':
                    flat_string += tld_to_string(grandchild)
                    if grandchild.tail:
                        flat_string += grandchild.tail

        if child.tag == 'klr':
            # klr = klarigo = clarification, ideally we'd extract this
            # and format it appropriately on the frontend (TODO)
            pass

        if child.tail:
            flat_string += child.tail

    flat_string = clean_string(flat_string)

    # remove trailing semicolon/full stop due to the examples being
    # written as a series
    if flat_string.endswith(';') or flat_string.endswith('.'):
        flat_string = flat_string[:-1]

    # sometimes quotes are put in as literals, make consistent
    flat_string = flat_string.replace(u'„', u'«').replace(u'“', u'»')

    # if we didn't extract anything with letters in (e.g. only
    # references that we discarded), return an empty string
    if not re.search(u'[a-zĉĝĥĵŝ]', flat_string,
                     flags=re.UNICODE+re.IGNORECASE):
        return ""

    return flat_string

def get_examples(node):
    """Get all examples from a <dif> or <subsnc>. Examples tend to be in
    <dif>s, but can also be in <subsnc>s and take the following form:

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
    for child in node.iterdescendants():
        if child.tag == 'ekz':
            raw_example = flatten_example(child)
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
            if child.tag == 'ref' and 'tip' in child.attrib and \
                    child.attrib['tip'] == 'dif':
                subdefinition.primary = get_reference_to_another(child)
                break

    subdefinition.examples = get_examples(subsnc_node)

    return subdefinition

def get_definition(snc_node):
    """Build a Definition from this <snc> and add any subdefinitions if
    present and any examples if present.

    Every <snc> contains a primary definition (a <dif>), a reference
    (i.e. a 'see foo' definition, a <ref>) or a subdefinitions (<dif>s
    inside <subsnc>s).

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
    (sekv.xml)

    """
    # we gradually populate the Deifinition
    definition = Definition()

    for child in snc_node.getchildren():
        if child.tag == 'dif':
            definition.primary = flatten_definition(child)
            definition.examples = get_examples(child)

    # if no <dif>, may have a <ref> that points to another word
    if definition.primary is None:
        for child in snc_node.getchildren():
            if child.tag == 'ref' and 'tip' in child.attrib and \
                    child.attrib['tip'] == 'dif':
                definition.primary = get_reference_to_another(child)
            elif child.tag == 'refgrp':
                definition.primary = get_reference_to_another(child)
            
    # note: may have only <subsnc>, no <dif> or <ref>
    # (e.g. sxilin.xml)

    # add figurative note if present
    uzo_node = snc_node.find('uzo')
    if uzo_node is not None:
        if uzo_node.text.strip().lower() == 'fig' and definition.primary:
            definition.primary = '(figure) ' + definition.primary

    # add transitivity notes if present, could be on <snc> or on <drv>
    transitivity = get_transitivity(snc_node)
    if not transitivity:
        transitivity = get_transitivity(snc_node.getparent())
    if definition.primary and transitivity:
        definition.primary = transitivity + ' ' + definition.primary

    # get any subdefinitions
    for child in snc_node.getchildren():
        if child.tag == 'subsnc':
            definition.subdefinitions.append(get_subdefinition(child))

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
    jakobi1.xml only <ref>, no <dif> node
    frakci.xml only <ref> but huge and complex
    ad.xml has a load of stuff, some of which is not documented
    
    """
    definitions = []

    # there may be a definition outside of a <snc> (yes, this isn't simple)
    for node in drv_node.getchildren():
        if node.tag == 'dif':
            # outside a <snc> we do not have subdefinitions
            definitions.append(Definition(flatten_definition(node)))

    for sense in drv_node.findall('snc'):
        definitions.append(get_definition(sense))

    # remove any duplicates (happens with multiple <ref>s
    # e.g. direkt3.xml) or empty definitions (happens with example
    # only senses, such as purigi in pur.xml)
    no_duplicates = []
    for definition in definitions:
        if definition not in no_duplicates and not definition.is_empty():
            no_duplicates.append(definition)
    
    return no_duplicates
