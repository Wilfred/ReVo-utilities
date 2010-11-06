import re

def clean_string(string):
    r"""Discard newlines, remove multiple spaces and remove leading or
    trailing whitespace.

    >>> clean_string(' \nfoo   bar  \n  ')
    'foo bar'

    """

    return re.sub('[\n\t ]+', ' ', string).strip()
