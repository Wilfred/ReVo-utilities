# -*- coding: utf-8 -*-

"""A bunch of sanity tests for XML export, whilst still being faster
than running the tool itself.

We use real data samples to test against, to ensure we test difficult
corner cases that actually occur without testing for scenarios that
don't occur.

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

    def test_all_definitions_with_transitivity(self):
        """Check that we assign transitivity to all definitions when
        transitivity is marked on the root <drv>. This example is from
        mangx.xml.

        """
        xml = """    <drv mrk="mangx.0i">
      <kap><ofc>*</ofc><tld/>i</kap>
      <gra><vspec>tr</vspec></gra>
      <snc mrk="mangx.0i.macxi">
        <dif>
          Ma&ccirc;i kaj gluti nutra&jcirc;on; sin nutri:
        </dif>
      </snc>
      <snc mrk="mangx.0i.konsumi">
        <uzo tip="klr">(io)</uzo>
        <dif>
          Konsumi:
        </dif>
      </snc>
      <snc mrk="mangx.0i.avide">
        <uzo tip="stl">FIG</uzo>
        <dif>
          Avide karesi:
        </dif>
      </snc>
    </drv>"""

        entries = self.extract_words(xml, root=u"manĝ")

        definitions = entries[0].definitions

        self.assertEqual(definitions[0].primary,
                         u"(transitiva) Maĉi kaj gluti nutraĵon; sin nutri.")
        self.assertEqual(definitions[1].primary,
                         u"(transitiva) Konsumi.")
        self.assertEqual(definitions[2].primary,
                         u"(transitiva) (figure) Avide karesi.")
        

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

    def test_remark_with_reference(self):
        """Make sure that references are not labelled with 'see also'
        inline in the remarks. This example was taken from firmam.xml.

        """
        xml = """<drv mrk="firmam.0o">
      <kap><tld/>o</kap>
      <snc>
        <ref tip="dif" cel="cxiel1.0osfero">&Ccirc;ielosfero</ref>
        <rim>
          La difinoj de la PIV-oj priskribas la biblian
          <ref tip="vid" cel="firm.0ajxo.BIB">firma&jcirc;on<sncref/></ref>,
          kio estus &ccirc;iela duonsfero.  Tamen la termino astronomia ja
          temas pri la tuta sfero, kiun tutan pli klare priskribas
          <ctl>&ccirc;ielosfero</ctl>.  Tio do lasas nenian pravigon por la
          malnecesa barbara&jcirc;o &leftquot;<tld/>o&rightquot;: en la senco mita-biblia la
          &gcirc;usta vorto estas <ctl>firma&jcirc;o</ctl> (cetere samstruktura
          kiel &leftquot;<tld/>o&rightquot;); por la senco astronomia,
          <ctl>&ccirc;ielosfero</ctl>; por la senco poezia pli klara kaj
          bonstila metaforo estas <ctl>&ccirc;ielvolbo</ctl>.
          <aut>Sergio Pokrovskij</aut>
        </rim>
      </snc>
    </drv>"""

        entries = self.extract_words(xml, root="firmament")

        remark = entries[0].definitions[0].remarks[0]

        self.assertEqual(remark, u"Rimarko: La difinoj de la PIV-oj priskribas la biblian firmaĵon, kio estus ĉiela duonsfero. Tamen la termino astronomia ja temas pri la tuta sfero, kiun tutan pli klare priskribas «ĉielosfero». Tio do lasas nenian pravigon por la malnecesa barbaraĵo «firmamento»: en la senco mita-biblia la ĝusta vorto estas «firmaĵo» (cetere samstruktura kiel «firmamento»); por la senco astronomia, «ĉielosfero»; por la senco poezia pli klara kaj bonstila metaforo estas «ĉielvolbo».")

class TranslationTests(ExtractionTest):
    def test_translations(self):
        """Check we extract translations for both <trd> and
        <trdgrp>s. This example was taken from salut.xml.

        """
        xml = """<drv mrk="salut.0i">
  <kap><ofc>*</ofc><tld/>i</kap>
  <snc>
    <dif>
      Montri al iu per ekstera &gcirc;entila signo sian respekton,
      estimon, &scirc;aton:
      <ekz>
        klini <tld/>e la kapon<fnt>Z</fnt>.
      </ekz>
    </dif>
    <trdgrp lng="be">
      <trd>&c_v;&c_ib;&c_t;&c_a;&c_c;&c_mol;</trd>,
      <trd>&c_p;&c_r;&c_y;&c_v;&c_ib;&c_t;&c_a;&c_c;&c_mol;</trd>,
      <trd>&c_p;&c_a;&c_v;&c_ib;&c_t;&c_a;&c_c;&c_mol;</trd>
    </trdgrp>
    <trd lng="cs">(po)zdravit</trd>
  </snc>
</drv>"""

        entries = self.extract_words(xml, root='salut')

        translations = entries[0].definitions[0].translations
        self.assertEqual(translations['be'], [u'вітаць', u'прывітаць', u'павітаць'])
        self.assertEqual(translations['cs'], ['(po)zdravit'])

    def test_translation_flattening(self):
        """Check that translations are exported even when there's
        stuff inside the <trd> tag. This example was taken from
        abdik.xml.

        """
        xml = """<drv mrk="abdik.0i">
  <kap><tld/>i</kap>
  <gra><vspec>tr</vspec></gra>
  <snc mrk="abdik.0i.regxo">
    <dif>
      <refgrp tip="super">
        <ref cel="eks.0igxi">Eksi&gcirc;i</ref>,
        <ref cel="rezign.0i">rezigni</ref>
      </refgrp>
      pri plej supera potenco a&ubreve; rango.
    </dif>
    <trd lng="br"><ind>dilezel</ind> e garg a roue</trd>
  </snc>
</drv>"""

        entries = self.extract_words(xml, root='abdik')

        translations = entries[0].definitions[0].translations
        self.assertEqual(translations['br'], ['dilezel e garg a roue'])

    def test_translation_on_drv(self):
        """Check that translations are exported even when they're not
        assigned to any specific definition. We always put these loose
        translations on the first definition. This example was taken
        from unu.xml.

        """
        xml = """<?xml version="1.0"?>
<!DOCTYPE vortaro SYSTEM "../dtd/vokoxml.dtd">

<vortaro>
  <art mrk="$Id: unu.xml,v 1.68 2009/12/18 17:30:32 revo Exp $">
    <kap>
      <ofc>*</ofc>
      <rad>unu</rad>
    </kap>

    <drv mrk="unu.0">
      <kap><ofc>*</ofc><tld/></kap>
      <snc mrk="unu.0.num">
        <dif>
          Numeralo esprimanta la elementan nombron. Matematika simbolo 1:
        </dif>
      </snc>
      <snc mrk="unu.0.ununura">
        <ref tip="dif" cel="unik.0a">unika</ref>
      </snc>
      <trd lng="af">een</trd>
    </drv>
  </art>
</vortaro>"""

        entries = self.extract_from_xml(xml)

        translations = entries[0].definitions[0].translations
        self.assertEqual(translations['af'], ['een'])

    def test_translation_on_subdefinition(self):
        """Check that we export translations on subdefinitions. This
        example was taken from konsum.xml.

        """
        xml = """<drv>
  <kap><tld/>i</kap>
  <snc mrk="konsum.0i.KOMUNE">
    <dif>
      Iom post iom detrui, forprenante partetojn:
    </dif>
    <subsnc>
      <dif>
	Detrui iom post iom la substancon de io; malrapide kaj grade
	neniigi, perdigi:
      </dif>
      <trd lng="nl">verteren</trd>
    </subsnc>
  </snc>
</drv>"""

        entries = self.extract_words(xml, root='konsum')

        subdefinition = entries[0].definitions[0].subdefinitions[0]
        self.assertEqual(subdefinition.translations['nl'], ['verteren'])

if __name__ == '__main__':
    unittest.main()
