# -*- coding: utf-8 -*-

def compare_esperanto_strings(x_mixed_case, y_mixed_case):
    # alphabetical sort of esperanto strings
    # (not unicode strings, normal strings)
    # permitting whole latin alphabet (so including q, x etc)
    # falling back on unicode ordering for unknown characters

    # need utf8 strings or we cannot iterate over them
    # esperanto uses multibyte characters
    
    if type(x_mixed_case) == str:
        x = x_mixed_case.decode('utf8').strip()
    else:
        x = x_mixed_case.strip()
    if type(y_mixed_case) == str:
        y = y_mixed_case.decode('utf8').strip()
    else:
        y = y_mixed_case.strip()

    # we explicitly add ' ' and '-' to the alphabet
    # ' ' is first in the alphabet so 'a b' comes before 'ab'
    # '-' is second so that affixes come first

    alphabet = [' ', '-', 'a', 'A', 'b', 'B', 'c', 'C', 'ĉ', 'Ĉ', 'd', 
                'D', 'e', 'E', 'f', 'F', 'g', 'G', 'ĝ', 'Ĝ', 'h', 'H',
                'ĥ', 'Ĥ', 'i', 'I', 'j', 'J', 'ĵ', 'Ĵ', 'k', 'K','l',
                'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q',
                'r', 'R', 's', 'S', 'ŝ', 'Ŝ', 't', 'T', 'u', 'U', 'ŭ',
                'Ŭ', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y',  'z', 'Z']
    # used string literals above for readability, now convert
    alphabet = [letter.decode('utf8') for letter in alphabet]
    
    for i in range(min(len(x),len(y))):
        try:
            if alphabet.index(x[i]) < alphabet.index(y[i]):
                return -1
            elif alphabet.index(x[i]) > alphabet.index(y[i]):
                return 1
        except ValueError:
            # not in alphabet
            if x[i] in alphabet:
                return -1
            elif y[i] in alphabet:
                return 1
            else:
                # neither character in alphabet, use normal unicode ordering
                if x < y:
                    return -1
                elif x > y:
                    return 1

    # if one string is the prefix of the other we reach this point

    # longer strings come afterwards
    if len(x) < len(y):
        return -1
    elif len(x) > len(y):
        return 1
    else:
        # completely identical
        return 0