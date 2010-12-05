from utilities import clean_string, tld_to_string
from flatten import flatten_node

def flatten_kap(kap):
    """Take everything between <kap> and </kap> and return a naked
    string. This will either be one term or multiple terms separated
    by commas.

    For the interested reader, an example:

    <kap><ofc>*</ofc><tld/>o</kap>
    <kap>brazil<tld/>arbo, <var><kap>brazila <tld/>arbo</kap></var></kap>
    (from nuks.xml)

    """
    assert kap != None and kap.tag == 'kap', "Cannot call flatten_kap without a <kap>"

    return flatten_node(kap, skip_tags=['ofc', 'fnt'])

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
