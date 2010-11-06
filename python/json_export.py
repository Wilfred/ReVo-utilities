# -*- coding: utf-8 -*-
import os
import lxml.etree
import re
import json

from esperanto_sort import compare_esperanto_strings

class Entry:
    """Every entry consists of a word (a string), a root (a string)
    and a list of definitions.

    """
    def __init__(self, word, root, definitions, primary=False):
        self.word = word
        self.root = root
        self.definitions = definitions
        self.primary = primary

    def __eq__(self, other):
        if self.word != other.word:
            return False
        if self.root != other.root:
            return False
        if self.definitions != other.definitions:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_all(self):
        """A convenience function used for JSON export."""
        return {"root": self.root, "primary": self.primary,
                "definitions": [definition.get_all() for definition in self.definitions]}

class Definition:
    """Every definition consists of a primary definition (either a
    non-empty string or None) and optionally subdefinitions. Note we
    never have subsubdefinitions.

    """
    def __init__(self, primary_definition, subdefinitions):
        self.primary = primary_definition
        self.subdefinitions = subdefinitions

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
        return (self.primary, self.subdefinitions)

def clean_string(string):
    r"""Discard newlines, remove multiple spaces and remove leading or
    trailing whitespace.

    >>> clean_string(' \nfoo   bar  \n  ')
    'foo bar'

    """

    return re.sub('[\n\t ]+', ' ', string).strip()

def get_words_from_kap(node):
    """Return a list of all the terms in a kap node. This is not
    necessarily single words, since ReVo includes entries such as
    'brazila nukso'.

    The heavy lifting is done in flatten_kap, all we do here is
    separate out terms and remove extraneous whitespace.

    Possible formats encountered:
    'foo'
    'foo, bar'
    'foo,\n   bar'
    '(n,p)-matrico' (only term in ReVo with an internal comma)

    """
    flat_string = flatten_kap(node)

    if flat_string == '(n,p)-matrico':
        words = ['(n,p)-matrico']
    else:
        words = flat_string.split(',')
    if len(words) > 1:
        for i in range(len(words)):
            # remove trailing/leading space and awkard newlines
            words[i] = clean_string(words[i])

    return words

def flatten_kap(kap):
    """Take everything between <kap> and </kap> and return a naked
    string. This will either be one word or multiple (usually
    separated by commas but I haven't checked whether this is
    universally true).

    For the interested reader, some examples:

    <kap><ofc>*</ofc><tld/>o</kap>
    <kap>brazil<tld/>arbo, <var><kap>brazila <tld/>arbo</kap></var></kap>
    (from nuks.xml)

    <kap><tld lit="A"/>o</kap>
    (from agl.xml)

    <kap><tld/>ino<fnt>Z</fnt></kap>
    (from hom.xml)

    <kap>
      <tld lit="S"/>lando
      <fnt>
        <vrk>Oficiala Informo de AdE</vrk>,
        <lok>numero 12</lok>
      </fnt>
    </kap>
    (from skot.xml)

    """
    assert kap != None and kap.tag == 'kap', "Cannot call flatten_kap without a <kap>"
    root = get_word_root(kap)
    
    flat_string = ""
    if kap.text != None:
        flat_string += kap.text

    # flatten, get all the text, throw away ofc and fnt tags
    # this is not simple, but the xml structure is a pain
    for child in kap.getchildren():
        if child.tag == 'tld':
            """The lit attribute of a tld tag signifies that in this
            particular case the root starts with a different letter
            than normal. For example, 'Aglo' has root 'agl-'. I
            haven't seen this used for anything other than
            capitalisation (both changing to upper case and changing
            to lower case).

            The relevant part of the ReVo documentation is vokoxml.dtd,
            lines 340 to 344.

            """
            if "lit" in child.attrib:
                new_letter = child.attrib['lit']
                flat_string += new_letter + root[1:]
            else:
                flat_string += root

            if child.text != None:
                flat_string += child.text
        elif child.tag == 'fnt':
            # we throw away source of word, not interested right now
            pass
        elif child.tag == 'ofc':
            # also throw away oficialness, not interested
            pass
        elif child.tag == 'var':
            # recurse -- egads! Why isn't the xml simpler?
            child_kap = child.getchildren()[0]
            flat_string += flatten_kap(child_kap)
        else:
            # shouldn't get here
            assert False
        if child.tail != None:
            flat_string += child.tail

    return clean_string(flat_string)

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
            definitions.append(Definition(get_definition_string(node), []))

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

def get_definition(snc_node):
    """Build a Definition from this <snc> and add any subdefitions if
    present.

    Every <snc> contains a primary definition (a <dif>), a reference
    (i.e. a 'see foo' definition, a <ref>) or a subdefinitions (<dif>s
    inside <subsnc>s).

    """
    # get primary definition
    primary_definition = Definition(None, [])
    for child in snc_node.getchildren():
        if child.tag == 'dif':
            primary_definition.primary = get_definition_string(child)

    # if no <dif>, may have a <ref> that points to another word
    if primary_definition.primary is None:
        for child in snc_node.getchildren():
            if child.tag == 'ref' and 'tip' in child.attrib and \
                    child.attrib['tip'] == 'dif':
                primary_definition.primary = get_reference_to_another(child)
            elif child.tag == 'refgrp':
                primary_definition.primary = get_reference_to_another(child)
            
    # note: may not have either <dif> or <ref> (e.g. sxilin.xml)

    # add transitivity notes if present, could be on <snc> or on <drv>
    transitivity = get_transitivity(snc_node)
    if not transitivity:
        transitivity = get_transitivity(snc_node.getparent())
    if primary_definition.primary and transitivity:
        primary_definition.primary = transitivity + ' ' + primary_definition.primary

    # if the primary definition is an empty string then we've done
    # something wrong or there's something wrong with the data (eg
    # bulgari.xml which is completely devoid of a definition)
    if primary_definition.primary == '':
        kap_node = snc_node.getparent().find('kap')
        print "Warning: '%s' has an example-only definition, skipping." % get_words_from_kap(kap_node)[0]
        return Definition(None, [])

    # get any subdefinitions
    subdefinitions = []
    for child in snc_node.getchildren():
        if child.tag == 'subsnc':
            # either a dif or a ref to another word
            dif_node = child.find('dif')
            if dif_node is not None:
                subdefinitions.append(get_definition_string(dif_node))
            else:
                for grandchild in child.getchildren():
                    if child.tag == 'ref' and 'tip' in child.attrib and \
                            child.attrib['tip'] == 'dif':
                        subdefinitions.append(get_reference_to_another(grandchild))

    primary_definition.subdefinitions = subdefinitions

    return primary_definition

def get_definition_string(dif_node):
    """Convert a definition node to a simple unicode string (this
    requires us to flatten it), and handle any references we
    encounter.

    """
    definition = ""

    if dif_node.text is not None:
        definition += dif_node.text
    for node in dif_node:
        if node.tag == 'ekz':
            # skip examples
            continue
        if node.tag == 'tld':
            definition += get_word_root(node)
        if node.tag == 'refgrp':
            definition += get_reference_to_another(node)
        if node.tag == 'ref' and 'tip' in node.attrib \
                and node.attrib['tip'] == 'dif':
            definition += get_reference_to_another(node)
        if node.text is not None:
            definition += node.text
        if node.tail is not None:
            definition += node.tail
    
    final_string = clean_string(definition)

    # if this definition has examples, it ends with a colon not a full stop
    # however we don't want those as we deal with examples separately
    if final_string.endswith(':'):
        final_string = final_string[:-1] + '.'

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

    reference = "Vidu " + reference.strip()
    if not reference.endswith('.'):
        reference += '.'

    return reference

def get_tree(xml_file):
    parser = lxml.etree.XMLParser(load_dtd=True)
    return lxml.etree.parse(xml_file, parser)

def get_entries(xml_file):
    """Get every entry from a given XML file: the words, their roots
    and their definitions.

    """

    tree = get_tree(xml_file)

    # each <drv> is one entry
    entries = []
    for drv_node in tree.iter('drv'):
        node_words = get_words_from_kap(drv_node.find('kap'))
        root = get_word_root(drv_node)
        definitions = get_all_definitions(drv_node)
        for word in node_words:
            entries.append(Entry(word, root, definitions))

    return entries

def get_all_entries():
    """Extract all dictionary data from every XML file in the ../xml
    directory.

    """

    # track which roots we've seen so far, so we can assign each root
    # a primary word when we first encounter it
    roots_seen = {}

    # fetch from xml files
    entries = {}
    path = '../xml/'
    for file in [(path + file) for file in os.listdir(path)]:
        # add every Entry to entries dict
        for entry in get_entries(file):
            if entry.word in entries:
                # we've already got an entry for this word, so add these definitions
                entries[entry.word].definitions += entry.definitions
            else:
                # new entry
                if not entry.root in roots_seen:
                    roots_seen[entry.root] = True
                    entry.is_primary = True

                entries[entry.word] = entry

    return entries

def export_entries(path, entries):
    """Write a list of Entries to a JSON file."""
    output_file = open(path, 'w')
    json.dump(dict((entry.word, entry.get_all()) for entry in entries.values()),
              output_file)
    output_file.close()

if __name__ == '__main__':
    whole_dictionary = get_all_entries()

    # write out as JSON
    export_entries('dictionary.json', whole_dictionary)
