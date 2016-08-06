import sys
import dictionary
from collections import Counter

dictionary = dictionary.Dictionary()

WORDS = Counter(dictionary.words)

def prob(word):
    """Returns probability of occurence a word in the dictionary."""
    return WORDS[word] / sum(WORDS.values())

def edits1(word):
    """Returns a set of possible word combinations whose edit distance = 1"""
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    """Returns a set of possible word combinations whose edit distance = 2"""
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in WORDS)

def known(words):
    """Returns only those words from given words that exist in the dictionary"""
    return [w for w in words if w in WORDS]

def spell_correct_word(word):
    """
    This function takes a word as input and returns
    the probable corrected word.
    """
    probable = known([word]) or known(edits1(word)) or edits2(word) or [word]
    return max(probable, key=prob)


def spell_correct_sent(sent, dictionary, language_model):
    """
    It takes sentence as input, uses language model and
    list of possible spelling and finds out the most
    probable sentences and returns list of sentences
    with descending probabilities.
    """
    corrected_sent = []
    for w in sent:
        corrected_sent.append(
            spell_correct_word(w, dictionary, language_model))

    return corrected_sent


def main(sent):
    corrected_sent = spell_correct_word(sent)
    if corrected_sent == sent:
        print("spelling is correct")
    else:
        print("correct spelling sent :", corrected_sent)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python speller.py <english_sent_to_check_spelling>")
        sys.exit()
    sent = sys.argv[1:]
    main(sent)
