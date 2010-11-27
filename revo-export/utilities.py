# -*- coding: utf-8 -*-
import re

def clean_string(string):
    r"""Discard newlines, remove multiple spaces and remove leading or
    trailing whitespace. We also replace quotation mark characters
    since we've decided to use a different style (though usually
    quotes are marked with <ctl>).

    Note since this strips leading and trailing whitespace it should
    only be applied once we have finished concatenating a string
    (since e.g. 'the '.strip() + 'dog' gives 'thedog').

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
    string = string.replace('ktp', 'kaj tiel plu')
    string = string.replace('kp ', 'komparu ') # trailing space to avoid false positives
    string = string.replace('Kp ', 'Komparu ')
    string = string.replace('kp:', 'komparu:')
    string = string.replace('vd ', 'vidu ')
    string = string.replace('Vd ', 'Vidu ')

    # sometimes literal = is inserted for <ref>s
    string = string.replace('=', '')

    # fix ; having a space before it (fixes remark in 'ankoraŭ')
    string = string.replace(' ;', ';')

    # fix ? having a space before it (fixes example in 'surda')
    string = string.replace(' ?', '?')

    # fix ! having a space before it (fixes 'mufo')
    string = string.replace(' !', '!')

    # fix . having a space before it (fixes remark in 'unu')
    string = string.replace(' .', '.')

    # get rid of leading/trailing space
    return string.strip()
