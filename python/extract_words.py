#!/usr/bin/python

import os
import lxml.etree
import re

from esperanto_sort import *

def get_words_from_kap(node):
    """Return a list of all the terms in a kap node. This is not
    necessarily single words, since ReVo includes entries such as
    'brazila nukso'.

    The heavy lifting is done in flatten_kap, all we do here is
    separate out terms and remove extraneous newlines.

    Possible formats encountered:
    'foo'
    'foo, bar'
    'foo,\n   bar'
    '(n,p)-matrico' (only term in ReVo with an internal comma)

    """
    flat_string = flatten_kap(node)

    # fix the '\n  ' problem
    # caused by newlines in awkward places in the xml
    flat_string = re.sub('\n\s+', ' ', flat_string)

    if flat_string == '(n,p)-matrico':
        words = ['(n,p)-matrico']
    else:
        words = flat_string.split(',')
    if len(words) > 1:
        for i in range(len(words)):
            # remove trailing/leading space
            words[i] = words[i].strip()

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
    assert kap != None
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
            if "lit" in child.attrib.keys():
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

    return flat_string.strip()

def get_word_root(arbitrary_node):
    # get the root without the ending
    assert arbitrary_node != None
    tree = arbitrary_node.getroottree()
    return list(tree.iter('rad'))[0].text

def get_tree(xml_file):
    parser = lxml.etree.XMLParser(load_dtd=True)
    return lxml.etree.parse(xml_file, parser)

def get_definitions(drv_node):
    # get all definitions for a word
    # this probably has bugs given the complexity of the input
    # some representative examples are:
    # sxilin.xml for subsenses
    # jakobi1.xml only <ref>, no <dif> node
    # frakci.xml only <ref> but huge and complex

    pass

def get_word_list():
    word_list = []

    # fetch from xml files
    path = '/home/wilfred/html/vortaro/xml'
    for file in os.listdir(path):
        tree = get_tree(path + '/' + file)

        # each word is a drv node
        for drv_node in tree.iter('drv'):
            words = get_words_from_kap(drv_node.find('kap'))
            for word in words:
                word_list.append(word.encode('utf8'))

    # sort them
    word_list.sort(cmp=compare_esperanto_strings)

    duplicates = []
    for i in range(1, len(word_list)):
        if word_list[i-1] != word_list[i] and word_list[i-1].lower() == word_list[i].lower():
            duplicates.append(word_list[i])

    return duplicates

    return word_list

if __name__ == '__main__':
    for word in get_word_list():
        print word
