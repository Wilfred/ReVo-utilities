from flatten import flatten_node

def get_words_from_kap(node):
    r"""Return a list of all the terms in a <kap>. Every term in a
    <kap> is an alternative spelling of the same term. This is not
    necessarily single words, since ReVo includes entries such as
    'brazila nukso'.

    <kap><ofc>*</ofc><tld/>o</kap>
    <kap>brazil<tld/>arbo, <var><kap>brazila <tld/>arbo</kap></var></kap>
    (from nuks.xml)

    The heavy lifting is done in flatten_kap, all we do here is
    separate out terms and remove extraneous whitespace.

    Possible formats encountered:
    'foo'
    'foo, bar'
    'foo,\n   bar'
    '(n,p)-matrico' (the only term in ReVo with an internal comma)

    """
    flat_string = flatten_node(node, skip_tags=['ofc', 'fnt'])

    if flat_string == '(n,p)-matrico':
        words = ['(n,p)-matrico']
    else:
        words = flat_string.split(',')
    if len(words) > 1:
        for i in range(len(words)):
            # remove trailing/leading space and awkard newlines
            words[i] = clean_string(words[i])

    return words
