from utilities import clean_string

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

def get_words_from_kap(node):
    r"""Return a list of all the terms in a <kap>. Every term in a
    <kap> is an alternative spelling of the same term. This is not
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
