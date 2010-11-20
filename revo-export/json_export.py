# -*- coding: utf-8 -*-
import os
import lxml.etree
import json

from esperanto_sort import compare_esperanto_strings

from words import get_word_root, get_words_from_kap
from definitions import get_all_definitions

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

    # fetch from xml files in order (so we do foo.xml before foo2.xml)
    # note this isn't proper alphabetical ordering but suffices here
    path = '../xml/'
    files = [(path + file) for file in os.listdir(path)]
    files.sort()

    entries = {}
    for file in files:
        print file
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
