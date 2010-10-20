# -*- coding: utf-8 -*-

raw_alphabet = ['a', 'b', 'c', 'ĉ', 'd', 'e', 'f', 'g', 'ĝ', 'h', 'ĥ',
                'i', 'j', 'ĵ', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
                'ŝ', 't', 'u', 'ŭ', 'v', 'z']
alphabet = [letter.decode('utf8') for letter in raw_alphabet]

# every word in reta vortaro in a set
# name is counter-intuitive but seems to be the standard name
word_list = set()
word_list_file = open('word_list.txt', 'r')
for line in word_list_file:
    word_list.add(line.strip())
    
def transpose(word, position):
    # swap letter at position with letter at position+1
    letters = list(word)

    temp = letters[position]
    letters[position] = letters[position+1]
    letters[position+1] = temp

    return ''.join(letters)

def delete_letter(word, position):
    # remove letter at position in word
    letters = list(word)

    letters.pop(position)

    return ''.join(letters)

def insert_letter(word, position, letter):
    # insert letter at position in word
    letters = list(word)

    letters.insert(position, letter)

    return ''.join(letters)

def replace_letter(word, position, letter):
    # put letter at position at word, overwriting current
    letters = list(word)

    letters[position] = letter

    return ''.join(letters)

def get_variations(word):
    # return every possible spelling variation of this string
    # assumes lower case 
    # complexity O(57n+27), where n is the number of letters
    # somewhat inspired by http://norvig.com/spell-correct.html
    variations = []

    # transpositions
    # complexity O(n-1)
    for i in range(len(word)-1):
        variations.append(transpose(word, i))

    # deletions
    # complexity O(n)
    for i in range(len(word)):
        variations.append(delete_letter(word, i))

    # insertions
    # complexity O(28n+28)
    for letter in alphabet:
        for i in range(len(word)+1):
            variations.append(insert_letter(word, i, letter))

    # replacements, taking care not to recreate the original word
    # complexity O(27n)
    for i in range(len(word)):
        for letter in alphabet:
            if word[i] != letter:
                variations.append(replace_letter(word, i, letter))

    return variations

def spell_check(word):
    # lookup this word in word list, and every variation
    # returning all that are valid

    # assumes word list contains all tenses, cases, plurals etc

    # note this will fail on words put together
    # since they won't be in the word list (consider plifortigis)

    possible_words = []

    if word in word_list:
        possible_words.append(word)

    for variation in get_variations(word):
        if variation in word_list:
            possible_words.append(variation)

    return possible_words

# utf8 strings, esperanto uses multi-byte characters
test_word = 'episodo'.decode('utf8')

for word in spell_check(test_word):
    print word
