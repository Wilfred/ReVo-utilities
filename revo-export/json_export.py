# -*- coding: utf-8 -*-
import os
import lxml.etree
import json

from esperanto_sort import compare_esperanto_strings

from definitions import get_all_definitions
from utilities import get_word_root, get_words_from_kap

class Entry:
    """Every entry consists of a word (a string which may contain
    spaces), a root (a string) and a list of definitions.

    """
    def __init__(self, word, root, definitions):
        self.word = word
        self.root = root
        self.definitions = definitions
        self.is_primary = False

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
        return {"root": self.root, "primary": self.is_primary,
                "definitions": [definition.get_all() for definition in self.definitions]}

def get_tree(xml_file):
    parser = lxml.etree.XMLParser(load_dtd=True, remove_comments=True)
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

def get_all_entries(files):
    """Extract all dictionary data from every XML file in the given
    list. The list can be either file names (normally used) or file
    objects (used in the unit tests).

    """
    # track which roots we've seen so far, so we can assign a primary
    # word to each root when we first encounter it
    roots_seen = {}

    entries = {}
    for file in files:
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

def write_out_json(target_file, entries):
    """Write a list of Entries to a JSON file."""

    output_file = open(target_file, 'w')
    json.dump(dict((entry.word, entry.get_all()) for entry in entries.values()),
              output_file)
    output_file.close()

if __name__ == '__main__':
    # fetch from xml files in order (so we do foo.xml before foo2.xml)
    # note this isn't proper alphabetical ordering but suffices here
    path = '../xml/'
    files = [(path + file) for file in os.listdir(path) 
             if file.endswith('.xml')]
    files.sort()

    whole_dictionary = get_all_entries(files)

    # write out as JSON
    write_out_json('dictionary.json', whole_dictionary)
