# -*- coding: utf-8 -*-

"""A bunch of sanity tests for XML export, whilst still being faster
than running the tool itself.

Testing is a matter of
$ coverage run tests.py; coverage report

"""
import unittest
import StringIO

import json_export

class SimpleStructureTest(unittest.TestCase):

    def test_simple_structure(self):
        """A basic test that ensures all data is read out correctly
        when there are no complexities to deal with in the XML.

        """
        simple_xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">
<vortaro>
<art>
<kap>
  <rad>salut</rad>/o
</kap>
<drv>
  <kap><tld/>o</kap>
  <snc>
    <dif>
      Saluto is a great word.
    </dif>
  </snc>
</drv>

</art>
</vortaro>
"""

        # we need file objects for lxml
        simple_xml_file = StringIO.StringIO(simple_xml)

        entries = json_export.get_all_entries([simple_xml_file])

        # should be a dict with only one key, the word itself
        self.assertEqual(entries.keys(), ['saluto'])

        # check the word is correct inside the entry
        entry = entries['saluto']
        self.assertEqual(entry.word, 'saluto')

        # check the definitions of this entry
        definitions = entry.definitions
        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].primary, 'Saluto is a great word.')

class DefinitionTests(unittest.TestCase):

    def test_definition_simple(self):
        """Test a real world example that has a simple
        definition. This example was taken from sekv.xml (though
        simplified).

        """
        xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">
<vortaro>
<art mrk="$Id: sekv.xml,v 1.24 2009/01/12 17:30:22 revo Exp $">
<kap>
  <ofc>*</ofc>
  <rad>sekv</rad>/i <fnt><bib>PV</bib></fnt>
</kap>
<drv mrk="sekv.0i">
  <kap><ofc>*</ofc><tld/>i</kap>
  <snc mrk="sekv.0i.postiri">
    <dif>
      Iri post movi&gcirc;anta objekto a&ubreve; persono:
    </dif>
  </snc>
</drv>
</art>
</vortaro>"""

        xml_file = StringIO.StringIO(xml)

        entries = json_export.get_all_entries([xml_file])

        # this should be a dict whose only key is the word itself
        self.assertEqual(entries.keys(), ['sekvi'])

        # check definition, should end with a full stop despite XML
        entry = entries['sekvi']
        definition = entry.definitions[0]
        self.assertEqual(definition.primary,
                         u'Iri post moviĝanta objekto aŭ persono.')

    def test_definition_with_references(self):
        """Check that definitions are extracted correctly when there
        are clarifications (<klr>s) references (<ref>, sometimes
        without a type in this example). Note that here the definition
        (<dif>) is part of a subsense (<subsnc>) so is actually a
        subdefinition.

        This example is from radik.xml.

        """
        xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">
<vortaro>
<art mrk="$Id: radik.xml,v 1.42 2006/02/18 17:31:30 revo Exp $">
<kap>
  <ofc>*</ofc>
  <rad>radik</rad>/o
</kap>
<drv mrk="radik.0o">
  <kap><ofc>*</ofc><tld/>o</kap>
  <snc mrk="radik.0o.MAT">
    <uzo tip="fak">MAT</uzo>
    <subsnc mrk="radik.0o.polinomo">
      <fnt><bib>PIV2</bib></fnt>
      <dif>
        <klr>(de <ref cel="polino.0o">polinomo</ref>)</klr>
        <ref tip="super" cel="nul0.0iganto.de_funkcio">Nuliganto</ref>
        de la responda <ref cel="funkci.polinoma0o">polinoma funkcio</ref>.
      </dif>
    </subsnc>
  </snc>
</drv>
</art>
</vortaro>"""

        xml_file = StringIO.StringIO(xml)

        entries = json_export.get_all_entries([xml_file])

        # check the subdefinition is correct
        entry = entries['radiko']
        definition = entry.definitions[0].subdefinitions[0]
        self.assertEqual(definition.primary,
                         '(de polinomo) Nuliganto de la responda polinoma funkcio.')

class ExampleTests(unittest.TestCase):

    def test_simple_example(self):
        return

if __name__ == '__main__':
    unittest.main()
