# -*- coding: utf-8 -*-

"""A bunch of sanity tests for XML export, whilst still being faster
than running the tool itself.

Testing is a matter of
$ coverage run tests.py; coverage report

"""
import unittest
import StringIO

import json_export

class ExtractionTest(unittest.TestCase):
    """Generally, we're only interested in the <drv> part of the XML
    and generally call the get_all_entries function. This class
    collects the commonalities.

    Actual tests inherit from this class.

    """
    maxDiff = None

    def extract_words(self, drv_xml_string, root):
        """Given a string of the form "<drv>...</drv>", extract every
        word as if this were a whole XML file, and return a list of
        words.

        """
        xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">
<vortaro>
<art>
<kap>
  <rad>%s</rad>
</kap>
%s
</art>
</vortaro>""" % (root, drv_xml_string)

        return self.extract_from_xml(xml)

    def extract_from_xml(self, xml_text):
        """Convenience wrapper for json_export.get_all_entries

        """

        # get a file object since json_export can use that
        xml_file = StringIO.StringIO(xml_text)

        # get a dict mapping words to Entry objects
        entries = json_export.get_all_entries([xml_file])

        # this dict should always have its keys matching Entry.word
        for (key, value) in entries.items():
            self.assertEqual(key, value.word)

        return entries.values()

class SimpleStructureTest(ExtractionTest):

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

        entries = self.extract_from_xml(simple_xml)

        self.assertEqual(len(entries), 1)

        # check the word is correct inside the entry
        self.assertEqual(entries[0].word, 'saluto')

        # check the definitions of this entry
        definitions = entries[0].definitions
        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].primary, 'Saluto is a great word.')

class DefinitionTests(ExtractionTest):

    def test_definition_simple(self):
        """Test a real world example that has a simple
        definition. This example was taken from sekv.xml (though
        simplified).

        """
        xml = """<drv>
  <kap><ofc>*</ofc><tld/>i</kap>
  <snc mrk="sekv.0i.postiri">
    <dif>
      Iri post movi&gcirc;anta objekto a&ubreve; persono:
    </dif>
  </snc>
</drv>"""

        entries = self.extract_words(xml, root='sekv')

        # should only return one results
        self.assertEqual(len(entries), 1)

        # check definition, should end with a full stop despite XML
        definition = entries[0].definitions[0]
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
        xml = """<drv mrk="radik.0o">
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
</drv>"""

        entries = self.extract_words(xml, root='radik')

        # check the subdefinition is correct
        definition = entries[0].definitions[0].subdefinitions[0]
        self.assertEqual(definition.primary,
                         '(de polinomo) Nuliganto de la responda polinoma funkcio.')

class WordTests(ExtractionTest):
    """Check that we are exporting the word correctly, which is stored
    in <kap> (kapvorto = head word). This has several annoying corner
    cases.

    """
    def test_word_with_oficialness(self):
        xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">

<vortaro>
<art mrk="$Id: hom.xml,v 1.41 2009/09/16 16:30:34 revo Exp $">
<kap>
  <ofc>*</ofc>
  <rad>hom</rad>/o
</kap>

<drv mrk="hom.0o">
  <kap><ofc>*</ofc><tld/>o</kap>
</drv>
</art>
</vortaro>"""

        entries = self.extract_from_xml(xml)

        # check that the entry has the right word
        self.assertEqual(entries[0].word, 'homo')

    def test_word_with_reference(self):
        """Test that we ignore <ref>s in the <kap> and only return the
        word itself. This example was taken from hom.xml.

        """
        xml = """<drv mrk="hom.0ino">
  <kap><tld/>ino<fnt>Z</fnt></kap>
</drv>"""

        entries = self.extract_words(xml, root='hom')

        self.assertEqual(entries[0].word, 'homino')

    def test_word_with_capitals(self):
        """Words can have capitalisation specified as being different
        from the root. Check we handle this correctly, taking an
        example from skot.xml.

        """
        xml = """<drv mrk="skot.0lando">
  <kap>
    <tld lit="S"/>lando
    <fnt>
      <vrk>Oficiala Informo de AdE</vrk>,
      <lok>numero 12</lok>
    </fnt>
  </kap>
</drv>"""

        entries = self.extract_words(xml, root='skot')

        self.assertEqual(entries[0].word, 'Skotlando')

class DefinitionTests(ExtractionTest):

    def test_definition_inline_references(self):
        """Check that we don't label references when used inline. This
        sample was taken from virusologi.xml.

        """
        xml = """<drv mrk="virusologi.0o">
  <kap><tld/>o</kap>
  <snc mrk="virusologi.0o.SCI">
    <uzo tip="fak">BAK</uzo>
    <uzo tip="fak">SCI</uzo>
    <dif>
      Scienco pri la <ref tip="vid" cel="virus.0o.BAK">virusoj</ref>, 
      parto de <ref tip="malprt" 
      cel="mikrob1.0o.SCI">mikrobiologio</ref>:
</dif>
</snc>
</drv>"""

        entries = self.extract_words(xml, root='virusologi')

        definition = entries[0].definitions[0].primary
        self.assertEqual(definition, "Scienco pri la virusoj, parto de mikrobiologio.")

class ExampleTests(ExtractionTest):

    def test_example_with_reference(self):
        """Check that we don't label references inside of examples
        (for example we should just write 'foo' instead of 'See also:
        foo'). This example was taken from ent.xml.

        Note we remove clarifications (<klr>s) from examples. Ideally
        we'd include them and format them differently to the example
        itself.

        """

        xml = """<drv mrk="ent.0o">
      <kap><tld/>o</kap>
      <snc mrk="ent.0o.ioajn">
	<dif>
	  Io ajn individua, ekzistanta reale a&ubreve; koncepte,
          <ctl>la o</ctl>:
	  <ekz>
	    <tld/>o estas tio, kio estas, filozofia
            <ref tip="sin" cel="est.0ajxo.ento">est(ant)a&jcirc;o</ref>,
	    <klr>(dum)</klr> komunlingva <ctl>esta&jcirc;o</ctl>
	    ordinare estas vivanta <tld/>o
	    <fnt>
	      <aut>E. W&uuml;ster</aut>:
	      <vrk>La tri fundamentaj reguladoj</vrk>.
	      <lok>
		Esperanto Triumfonta, 2, 1921;
                cit. la&ubreve; la represo en:
		Esperantologiaj studoj, Stafeto 1978, p. 35.
	      </lok>
	    </fnt>.
	  </ekz>
	</dif>
      </snc>
    </drv>"""

        entries = self.extract_words(xml, root='ent')

        examples = entries[0].definitions[0].examples

        self.assertEqual(len(examples), 1)
        self.assertEqual(examples[0], u"ento estas tio, kio estas, filozofia est(ant)aĵo, komunlingva «estaĵo» ordinare estas vivanta ento")

        return

class RemarkTests(ExtractionTest):

    def test_remark_with_quotes(self):
        """Make sure that quotes are in the right place for a
        remark. This example was taken from tangx.xml and simplified.

        """
        xml = """<drv mrk="tangx.0a">
  <kap><tld/>a, <tld/>anta</kap>
  <snc>
    <dif>Blah blah.
    </dif>
    <rim>
      La difino estas intence naiva, &ccirc;ar la nocio ne povas esti
      rigore difinita kadre de elementa geometrio. Oni diras sendistinge,
      ke <ctl>la rekto estas <tld/>a al la kurbo</ctl> a&ubreve;
      <ctl>la kurbo estas <tld/>a al la rekto</ctl>.
    </rim>
  </snc>
</drv>"""

        entries = self.extract_words(xml, root=u"tanĝ")

        # remarks are associated with definitions
        remarks = entries[0].definitions[0].remarks

        self.assertEqual(remarks[0], u"Rimarko: La difino estas intence naiva, ĉar la nocio ne povas esti rigore difinita kadre de elementa geometrio. Oni diras sendistinge, ke «la rekto estas tanĝa al la kurbo» aŭ «la kurbo estas tanĝa al la rekto».")

if __name__ == '__main__':
    unittest.main()
