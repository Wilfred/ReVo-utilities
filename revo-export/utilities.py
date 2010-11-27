# -*- coding: utf-8 -*-
import re

def clean_string(string):
    r"""Discard newlines, remove multiple spaces and remove leading or
    trailing whitespace. We also replace quotation mark characters
    since we've decided to use a different style (though usually
    quotes are marked with <ctl>).

    >>> clean_string(' \nfoo   bar  \n  ')
    'foo bar'

    """
    # collapse whitespace to single spaces
    string = re.sub('[\n\t ]+', ' ', string)

    # fix quotes
    string = string.replace(u'„', u'«').replace(u'“', u'»')

    # replace acronyms with their expanded versions
    string = string.replace('p.p.', 'parolante pri')
    string = string.replace('p. p.', 'parolante pri')

    # sometimes literal = is inserted for <ref>s
    string = string.replace('=', '')

    # fix ; having space before it (fixes remark in ankoraŭ)
    string = string.replace(' ;', ';')

    # get rid of leading/trailing space
    return string.strip()
