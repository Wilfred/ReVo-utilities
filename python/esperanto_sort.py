#!/usr/bin/python
# -*- coding: utf-8 -*-

def compare_esperanto_strings(x_mixed_case, y_mixed_case):
    # alphabetical sort of esperanto strings
    # (not unicode strings, normal strings)
    # permitting whole latin alphabet (so including q, x etc)
    # falling back on unicode ordering for unknown characters

    # need utf8 strings or we cannot iterate over them
    # esperanto uses multibyte characters
    x = x_mixed_case.decode('utf8')
    y = y_mixed_case.decode('utf8')

    # case insensitive sort
    # TODO: it would be nice to be case sensitive
    x = x.lower().strip()
    y = y.lower().strip()

    # we explicitly add ' ' and '-' to the alphabet
    # ' ' is first in the alphabet so 'a b' comes before 'ab'
    # '-' is second so that affixes come first

    alphabet = [' ', '-', 'a', 'b', 'c', 'ĉ', 'd', 'e', 'f', 'g', 'ĝ',
                'h', 'ĥ', 'i', 'j', 'ĵ', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 'ŝ', 't', 'u', 'ŭ', 'v', 'w', 'x', 'y', 
                'z']
    # used string literals above for readability, now convert
    alphabet = [letter.decode('utf8') for letter in alphabet]
    
    for i in range(min(len(x),len(y))):
        try:
            if alphabet.index(x[i]) < alphabet.index(y[i]):
                return -1
            elif alphabet.index(x[i]) > alphabet.index(y[i]):
                return 1
        except:
            # not in alphabet
            if x[i] in alphabet:
                return -1
            elif y[i] in alphabet:
                return 1
            else:
                # neither character in alphabet, use normal unicode ordering
                if x < y:
                    return -1
                elif x == y:
                    return 0
                else:
                    return 1

    # if strings are not of the same length and on is the prefix of
    # the other we reach here:

    # longer strings come afterwards
    if len(x) < len(y):
        return -1
    elif len(x) > len(y):
        return 1
    else:
        return 0
