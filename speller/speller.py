import sys
import dictionary


def spell_correct_word(word, dictionary, language_model):
    """
    This function takes a word as input and returns
    the possible words list with descending probabilities.
    """
    pass


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
